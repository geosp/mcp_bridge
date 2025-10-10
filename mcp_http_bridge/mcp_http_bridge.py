#!/usr/bin/env python3
"""
MCP HTTP/SSE Bridge
Bridges between stdio (for Claude Desktop) and HTTP/SSE (for remote MCP servers)
This server sends SSE responses directly in POST responses, not via persistent stream.
"""

import sys
import json
import asyncio
import httpx
from pathlib import Path
from typing import Optional

def log(message: str):
    """Log to stderr"""
    sys.stderr.write(f"[Bridge] {message}\n")
    sys.stderr.flush()

def load_config():
    """Load configuration from config.json"""
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.json'
    
    if not config_path.exists():
        log(f"Error: config.json not found at {config_path}")
        sys.exit(1)
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'url' not in config:
            log("Error: 'url' is required in config.json")
            sys.exit(1)
        
        log(f"Loaded config from {config_path}")
        return config
    
    except Exception as e:
        log(f"Error loading config: {e}")
        sys.exit(1)

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

async def async_main():
    log("Starting MCP HTTP/SSE Bridge")
    
    config = load_config()
    
    bridge = MCPHTTPBridge(
        url=config['url'],
        headers=config.get('headers', {})
    )
    
    try:
        await bridge.run()
    finally:
        await bridge.close()
        log("Bridge shut down")

def main():
    """Entry point for console script"""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        log("Interrupted by user")

if __name__ == "__main__":
    main()
