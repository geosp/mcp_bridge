# Claude Desktop Setup Guide

This guide shows you how to configure Claude Desktop to use MCP Bridge with your remote servers.

## Prerequisites

1. Install MCP Bridge:
   ```bash
   pip install mcp-bridge
   ```

2. Create your bridge configuration:
   ```bash
   mcp-bridge init --name weather
   # Edit ~/.config/mcp-bridge/weather.json with your server details
   ```

## Configuration Location

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

## Example: Single Server

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "mcp-bridge",
      "args": ["--config", "weather.json"]
    }
  }
}
```

## Example: Multiple Servers

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "mcp-bridge",
      "args": ["--config", "weather.json"]
    },
    "database-server": {
      "command": "mcp-bridge",
      "args": ["--config", "database.json"]
    },
    "analytics-server": {
      "command": "mcp-bridge",
      "args": ["--config", "analytics.json"]
    }
  }
}
```

## Using Virtual Environment

If you installed mcp-bridge in a virtual environment, use the full path:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "/Users/yourusername/path/to/.venv/bin/mcp-bridge",
      "args": ["--config", "weather.json"]
    }
  }
}
```

To find the full path:
```bash
which mcp-bridge
```

## Tested Configuration

This configuration has been tested and verified working:

### Bridge Config: `~/.config/mcp-bridge/weather.json`

```json
{
  "url": "http://agentgateway.mixwarecs-home.net/weather-mcp",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN_HERE"
  }
}
```

### Claude Desktop Config

```json
{
  "mcpServers": {
    "weather-gateway": {
      "command": "mcp-bridge",
      "args": ["--config", "weather.json"]
    }
  }
}
```

## Troubleshooting

### Bridge not starting

1. Check Claude Desktop logs (varies by OS)
2. Test the bridge manually:
   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | mcp-bridge --config weather.json
   ```

### Server not responding

1. Verify your server URL is accessible:
   ```bash
   curl -X POST http://your-server.example.com/mcp \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

2. Check bridge logs (stderr output)

### Config file not found

```bash
# List available configs
mcp-bridge list-configs

# Create missing config
mcp-bridge init --name weather
```

## Verification

After configuring Claude Desktop:

1. Restart Claude Desktop completely
2. Open Claude Desktop
3. Look for your server in the MCP servers list
4. Try using tools/capabilities from your remote server

The bridge logs will appear in Claude Desktop's developer console/logs.

## Advanced: Custom Headers

If your server requires custom headers:

```json
{
  "url": "http://your-server.example.com/mcp",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN",
    "X-Custom-Header": "custom-value",
    "X-Request-ID": "client-123"
  }
}
```

## Session Management

The bridge automatically manages session IDs:

1. First request (`initialize`) receives a session ID from the server
2. Subsequent requests include the session ID in `mcp-session-id` header
3. Session persists for the lifetime of the bridge process
4. Each Claude Desktop restart creates a new session
