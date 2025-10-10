# Programmatic Access to MCP Tools via Bridge

This guide demonstrates how to programmatically access MCP tools through the HTTP/SSE bridge using Python and `uv`.

## Overview

While Claude Desktop provides a built-in MCP client, you can also access MCP servers programmatically through the bridge. This is useful for:

- Testing MCP tools in development
- Building custom integrations
- Automating workflows with MCP capabilities
- Creating standalone applications using MCP servers

## Requirements

- Python 3.8+
- `uv` package manager
- `httpx` library (for async HTTP)
- A configured MCP bridge (see [README.md](../README.md))

## Quick Start

We've provided a complete example in [tests/test_weather_tools.py](../tests/test_weather_tools.py) that demonstrates:

1. Connecting to an MCP server via the bridge
2. Listing available tools
3. Calling tools with arguments
4. Handling responses

### Running the Example

```bash
# From the project root
uv run tests/test_weather_tools.py
```

This will:
- Load your weather bridge config from `~/.config/mcp-bridge/weather.json`
- Connect to the server and initialize
- List available tools
- Test `get_hourly_weather()` for Tallahassee
- Test `geocode_location()` for Tokyo, Japan

## Example Output

```
📁 Loading config from: ~/.config/mcp-bridge/weather.json
🌐 Server URL: http://agentgateway.mixwarecs-home.net/weather-mcp

============================================================
STEP 1: Initialize Connection
============================================================
📤 Sending: initialize (id=1)
🔑 Session ID: 8678d478-5099-417d-936e-9749cb71befa
📥 Received: id=1
✅ Server: rmcp v0.7.0

============================================================
STEP 2: List Available Tools
============================================================
Found 2 tools:

  📦 get_hourly_weather
     Get hourly weather forecast for a location using Open-Meteo API

  📦 geocode_location
     Get coordinates and timezone information for a location.

============================================================
STEP 3: Test get_hourly_weather()
============================================================
🌤️  Getting weather for: Tallahassee

📍 Location: Tallahassee
🌍 Country: United States
🕐 Timezone: America/New_York

Current Conditions:
  🌡️  Temperature: 20.2°C (feels like 19.9°C)
  💧 Humidity: 78.0%
  🌧️  Precipitation: 0.0 mm
  💨 Wind: 16.8 km/h NE

Hourly Forecast (next 6 hours):
  00:00: 24.4°C - N/A (3.0% precip)
  01:00: 24.7°C - N/A (3.0% precip)
  02:00: 23.7°C - N/A (3.0% precip)
  ...

============================================================
STEP 4: Test geocode_location()
============================================================
📍 Geocoding: Tokyo, Japan

  Location: Tokyo
  Country: Japan
  Timezone: Asia/Tokyo

============================================================
✅ ALL TESTS COMPLETED SUCCESSFULLY!
============================================================
```

## Code Example: Simple MCP Client

Here's a minimal example of creating an MCP client:

```python
import json
import asyncio
import httpx
from pathlib import Path

class SimpleMCPClient:
    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers
        self.session_id = None
        self.client = httpx.AsyncClient(timeout=30.0)
        self.request_id = 0

    async def initialize(self):
        """Initialize the connection"""
        response = await self._request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "my-app", "version": "1.0"}
        })

        # Send initialized notification (required)
        await self._notify("notifications/initialized")

        return response

    async def call_tool(self, name: str, args: dict):
        """Call a tool"""
        return await self._request("tools/call", {
            "name": name,
            "arguments": args
        })

    async def _request(self, method: str, params: dict):
        """Send JSON-RPC request"""
        self.request_id += 1

        message = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }

        headers = {**self.headers, "Content-Type": "application/json"}
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        resp = await self.client.post(self.url, json=message, headers=headers)

        # Extract session ID from initialize
        if method == "initialize":
            self.session_id = resp.headers.get("mcp-session-id")

        # Parse SSE response
        for line in resp.text.split('\n'):
            if line.startswith("data: "):
                return json.loads(line[6:])

        return resp.json()

    async def _notify(self, method: str, params: dict = None):
        """Send notification (no response)"""
        message = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }

        headers = {**self.headers, "Content-Type": "application/json"}
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        await self.client.post(self.url, json=message, headers=headers)

    async def close(self):
        await self.client.aclose()


async def main():
    # Load config
    config_path = Path.home() / ".config/mcp-bridge/weather.json"
    with open(config_path) as f:
        config = json.load(f)

    # Create client
    client = SimpleMCPClient(config["url"], config.get("headers", {}))

    try:
        # Initialize
        await client.initialize()

        # Get weather
        result = await client.call_tool("get_hourly_weather", {
            "location": "Paris"
        })

        # Parse result
        weather_data = json.loads(result["result"]["content"][0]["text"])
        print(f"Weather in {weather_data['location']}: "
              f"{weather_data['current_conditions']['temperature']}°C")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

## MCP Protocol Basics

### 1. Initialize

Always start by sending an `initialize` request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "my-app", "version": "1.0"}
  }
}
```

### 2. Send Initialized Notification

After receiving the initialize response, send:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized",
  "params": {}
}
```

### 3. List Tools

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

### 4. Call a Tool

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_hourly_weather",
    "arguments": {
      "location": "Paris"
    }
  }
}
```

## Session Management

- The server returns a `mcp-session-id` header in the initialize response
- Include this header in all subsequent requests (except initialize)
- Session persists for the lifetime of your client connection
- Each client instance should have its own session

## Response Format

The bridge returns Server-Sent Events (SSE) format:

```
data: {"jsonrpc":"2.0","id":1,"result":{...}}

```

Parse lines starting with `data: ` and extract the JSON.

## Error Handling

Errors follow JSON-RPC format:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid request parameters",
    "data": "..."
  }
}
```

## Using Different Configs

To use a different MCP server config:

```python
# Use local-test server
config_path = Path.home() / ".config/mcp-bridge/local-test.json"

# Use database server
config_path = Path.home() / ".config/mcp-bridge/database.json"
```

## Integration with Other Languages

The HTTP/SSE protocol can be used from any language that supports HTTP:

### JavaScript/Node.js

```javascript
const response = await fetch('http://your-server/mcp', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'text/event-stream',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: { /* ... */ }
  })
});
```

### curl

```bash
curl -X POST http://your-server/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```

## Best Practices

1. **Always initialize first** - Send initialize + initialized notification
2. **Reuse sessions** - Don't initialize for every request
3. **Handle errors** - Check for both HTTP errors and JSON-RPC errors
4. **Close cleanly** - Always close the HTTP client when done
5. **Respect timeouts** - MCP servers may have request timeouts
6. **Cache tool schemas** - List tools once, reuse the schema

## Troubleshooting

### "Invalid request parameters" error

Make sure you send the `notifications/initialized` notification after initialize.

### Session ID not persisting

Ensure you're including the `mcp-session-id` header in requests after initialize.

### No response received

Check that you're parsing SSE format correctly (lines starting with `data: `).

### Connection timeout

Increase the HTTP client timeout (default in example: 30 seconds).

## Additional Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Full test example](../tests/test_weather_tools.py)
- [Bridge README](../README.md)
- [Claude Desktop Setup](./CLAUDE_DESKTOP_SETUP.md)
