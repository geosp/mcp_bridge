"""
Core bridge logic for MCP HTTP/SSE Bridge
"""

import sys
import json
import asyncio
import httpx
from typing import Optional

def log(message: str):
    """Log to stderr"""
    sys.stderr.write(f"[Bridge] {message}\n")
    sys.stderr.flush()

def deserialize_stringified_params(arguments: dict) -> dict:
    """
    Detect and fix stringified parameters that should be objects or arrays.

    This is a workaround for Claude Desktop's parameter serialization bug
    where object/array parameters are converted to JSON strings instead of
    being preserved as objects in the JSON-RPC payload.

    Bug behavior:
    - Expected: {"filter": {"lastName": "Fajardo"}}
    - Actual:   {"filter": "{\"lastName\": \"Fajardo\"}"}

    This function detects stringified JSON and deserializes it back to
    the correct type, allowing MCP servers to receive properly formatted
    parameters.

    Args:
        arguments: The tool arguments dict to process

    Returns:
        Corrected arguments dict with deserialized objects/arrays
    """
    corrected = {}
    fixed_params = []

    for key, value in arguments.items():
        # Only process string values that look like JSON objects or arrays
        if isinstance(value, str) and value.strip() and value.strip()[0] in ('{', '['):
            try:
                parsed = json.loads(value)
                # Accept both dicts and lists
                if isinstance(parsed, (dict, list)):
                    corrected[key] = parsed
                    fixed_params.append(f"{key}:{type(parsed).__name__}")
                else:
                    # Successfully parsed but not an object/array, keep original
                    corrected[key] = value
            except json.JSONDecodeError:
                # If it fails to parse, keep the original string
                corrected[key] = value
        else:
            # Pass through non-string values unchanged
            corrected[key] = value

    if fixed_params:
        log(f"Fixed stringified params: {', '.join(fixed_params)}")

    return corrected

class MCPHTTPBridge:
    def __init__(self, url: str, headers: Optional[dict] = None):
        self.url = url
        self.headers = headers or {}
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0))
        self.session_id = None
        
    async def send_message(self, message: dict):
        """Send a message and read SSE response"""
        try:
            method = message.get('method', 'unknown')
            msg_id = message.get('id')

            # Fix stringified parameters (workaround for Claude Desktop bug)
            # For tools/call, the arguments are nested in params.arguments
            if method == 'tools/call' and 'params' in message and 'arguments' in message['params']:
                original_args = message['params']['arguments']
                fixed_args = deserialize_stringified_params(original_args)
                if fixed_args != original_args:
                    message['params']['arguments'] = fixed_args

            log(f"Sending: {method} (id={msg_id})")
            
            # Build headers
            headers = {
                **self.headers,
                "Content-Type": "application/json",
                "Accept": "text/event-stream, application/json"
            }
            
            # Add session ID header for non-initialize requests
            if self.session_id and method != "initialize":
                headers["mcp-session-id"] = self.session_id
            
            # Send request with streaming
            request = self.client.build_request(
                "POST",
                self.url,
                json=message,
                headers=headers
            )
            
            response = await self.client.send(request, stream=True)
            response.raise_for_status()
            
            # For initialize, extract session ID
            if method == "initialize":
                self.session_id = response.headers.get("mcp-session-id")
                if self.session_id:
                    log(f"Session ID: {self.session_id}")
            
            # Read SSE response from this request
            content_type = response.headers.get("content-type", "")
            if "text/event-stream" in content_type:
                log(f"Reading SSE response...")
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:].strip()
                        if data:
                            try:
                                sse_message = json.loads(data)
                                log(f"Received SSE: id={sse_message.get('id')}")
                                
                                # Write to stdout
                                try:
                                    sys.stdout.write(json.dumps(sse_message) + '\n')
                                    sys.stdout.flush()
                                except BrokenPipeError:
                                    log("Stdout broken")
                                    return
                                    
                            except json.JSONDecodeError as e:
                                log(f"Invalid JSON in SSE: {e}")
            else:
                log(f"Unexpected content type: {content_type}")
                
        except Exception as e:
            log(f"Error: {e}")
            import traceback
            log(f"Traceback: {traceback.format_exc()}")
            
            # Send error response
            error_response = {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {"code": -32603, "message": str(e)}
            }
            try:
                sys.stdout.write(json.dumps(error_response) + '\n')
                sys.stdout.flush()
            except:
                pass
    
    async def read_stdin(self):
        """Read messages from stdin"""
        loop = asyncio.get_event_loop()
        
        while True:
            try:
                # Read line from stdin
                line = await loop.run_in_executor(None, sys.stdin.readline)
                
                if not line:
                    log("stdin closed")
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse and send message
                message = json.loads(line)
                await self.send_message(message)
                
            except json.JSONDecodeError as e:
                log(f"Invalid JSON from stdin: {e}")
            except Exception as e:
                log(f"Error reading stdin: {e}")
                import traceback
                log(f"Traceback: {traceback.format_exc()}")
                break
    
    async def run(self):
        """Run the bridge"""
        log(f"Bridge ready. Target URL: {self.url}")
        await self.read_stdin()
    
    async def close(self):
        """Close connections"""
        await self.client.aclose()
