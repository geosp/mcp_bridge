# Claude Desktop Setup Guide

This guide shows you how to configure Claude Desktop to use MCP Bridge with your remote servers.

## Prerequisites

### Install uv (Recommended)

`uv` is a fast Python package installer and runner. It's the recommended way to run MCP Bridge.

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation:**
```bash
uv --version
uvx --version
```

### Alternative: Install with pip

If you prefer pip:
```bash
pip install mcp-bridge
```

## Configuration Location

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

## Setup Steps

### 1. Create Your Bridge Configuration

Create a configuration file for your remote MCP server with your connection details and credentials.

**Example config file** (`weather.json`):
```json
{
  "url": "http://your-server.example.com/mcp-endpoint",
  "headers": {
    "Authorization": "Bearer YOUR_API_TOKEN_HERE"
  }
}
```

Save this file in a secure location (e.g., `~/mcp-configs/weather.json`).

### 2. Configure Claude Desktop

#### Option A: Using uvx with GitHub (Recommended)

This approach automatically installs MCP Bridge from GitHub - no manual installation needed!

**macOS:**
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/geosp/mcp-bridge",
        "mcp-bridge",
        "--config", "/Users/yourusername/mcp-configs/weather.json"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/geosp/mcp-bridge",
        "mcp-bridge",
        "--config", "C:\\Users\\yourusername\\mcp-configs\\weather.json"
      ]
    }
  }
}
```

**Benefits:**
- No manual installation required
- Always uses the latest version from GitHub
- Isolated environment per run
- Easy to update (just restart Claude Desktop)

#### Option B: Using uv with Local Development

For local development or modifications:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/mcp-bridge",
        "run",
        "mcp-bridge",
        "--config", "/Users/yourusername/mcp-configs/weather.json"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "uv",
      "args": [
        "--directory", "C:\\path\\to\\mcp-bridge",
        "run",
        "mcp-bridge",
        "--config", "C:\\Users\\yourusername\\mcp-configs\\weather.json"
      ]
    }
  }
}
```

#### Option C: Using Installed Package (pip)

If you installed with pip:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "mcp-bridge",
      "args": ["--config", "/path/to/weather.json"]
    }
  }
}
```

### 3. Multiple Servers Setup

You can configure multiple remote servers:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/geosp/mcp-bridge",
        "mcp-bridge",
        "--config", "/Users/yourusername/mcp-configs/weather.json"
      ]
    },
    "database-server": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/geosp/mcp-bridge",
        "mcp-bridge",
        "--config", "/Users/yourusername/mcp-configs/database.json"
      ]
    },
    "analytics-server": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/geosp/mcp-bridge",
        "mcp-bridge",
        "--config", "/Users/yourusername/mcp-configs/analytics.json"
      ]
    }
  }
}
```

## Finding the uvx Path

On some systems, you may need to specify the full path to `uvx`:

**macOS/Linux:**
```bash
which uvx
# Usually: /Users/yourusername/.local/bin/uvx or ~/.cargo/bin/uvx
```

**Windows:**
```powershell
where.exe uvx
# Usually: C:\Users\yourusername\.local\bin\uvx.exe
```

Use the full path in your configuration if needed:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "/Users/yourusername/.local/bin/uvx",
      "args": [
        "--from", "git+https://github.com/geosp/mcp-bridge",
        "mcp-bridge",
        "--config", "/Users/yourusername/mcp-configs/weather.json"
      ]
    }
  }
}
```

## Using Specific Versions

To use a specific version, branch, or tag from GitHub:

**Specific tag/version:**
```json
"args": [
  "--from", "git+https://github.com/geosp/mcp-bridge@v0.2.0",
  "mcp-bridge",
  "--config", "/path/to/weather.json"
]
```

**Specific branch:**
```json
"args": [
  "--from", "git+https://github.com/geosp/mcp-bridge@main",
  "mcp-bridge",
  "--config", "/path/to/weather.json"
]
```

**Specific commit:**
```json
"args": [
  "--from", "git+https://github.com/geosp/mcp-bridge@abc1234",
  "mcp-bridge",
  "--config", "/path/to/weather.json"
]
```

## Troubleshooting

### Checking Claude Desktop Logs

**macOS:**
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

**Windows:**
```powershell
Get-Content -Path "$env:APPDATA\Claude\logs\mcp*.log" -Wait
```

**Linux:**
```bash
tail -f ~/.config/Claude/logs/mcp*.log
```

### uvx command not found

If you get "command not found" for `uvx`:

1. **Verify uv is installed:**
   ```bash
   uv --version
   ```

2. **Find the full path:**
   ```bash
   which uvx  # macOS/Linux
   where.exe uvx  # Windows
   ```

3. **Use the full path in your config:**
   ```json
   "command": "/Users/yourusername/.local/bin/uvx"
   ```

4. **Reinstall uv if needed:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Git operation failed

If you see "Git operation failed" in the logs:

1. **Check your network connection** - ensure you can access GitHub
2. **Verify the repository URL:**
   ```bash
   git ls-remote https://github.com/geosp/mcp-bridge
   ```
3. **Try using a specific version:**
   ```json
   "--from", "git+https://github.com/geosp/mcp-bridge@v0.2.0"
   ```

### Config file not found

If the bridge can't find your config file:

1. **Use absolute paths** - avoid relative paths like `weather.json`
2. **Verify the file exists:**
   ```bash
   cat /path/to/weather.json
   ```
3. **Check file permissions:**
   ```bash
   ls -l /path/to/weather.json
   ```

### Connection errors

If you see connection errors like "nodename nor servname provided":

1. **Verify your server URL in the config file:**
   ```bash
   cat /path/to/weather.json
   ```

2. **Test the server is accessible:**
   ```bash
   curl -X POST http://your-server.example.com/mcp \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -d '{"jsonrpc":"2.0","method":"initialize","id":1}'
   ```

3. **Check for typos** in the URL (http vs https, correct domain, etc.)

### Testing the bridge manually

Test the bridge outside of Claude Desktop:

**Using uvx:**
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | uvx --from git+https://github.com/geosp/mcp-bridge mcp-bridge --config /path/to/weather.json
```

**Using installed package:**
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | mcp-bridge --config /path/to/weather.json
```

## Verification

After configuring Claude Desktop:

1. **Restart Claude Desktop completely** (Quit and reopen)
2. **Check the logs** to see if the server started successfully:
   ```bash
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```
3. **Look for success messages** like:
   - "Server started and connected successfully"
   - "Initialized session" with a session ID
4. **Try using the server** in Claude Desktop - your remote server's tools should be available

## Complete Working Example

Here's a complete, tested configuration:

**Config file** (`~/mcp-configs/weather.json`):
```json
{
  "url": "http://agentgateway.mixwarecs-home.net/weather-mcp",
  "headers": {
    "Authorization": "Bearer YOUR_API_TOKEN_HERE"
  }
}
```

**Claude Desktop config** (macOS):
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "/Users/yourusername/.local/bin/uvx",
      "args": [
        "--from", "git+https://github.com/geosp/mcp-bridge",
        "mcp-bridge",
        "--config", "/Users/yourusername/mcp-configs/weather.json"
      ]
    }
  }
}
```

## Advanced Configuration

### Custom Headers

If your server requires additional custom headers:

```json
{
  "url": "http://your-server.example.com/mcp",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN",
    "X-Custom-Header": "custom-value",
    "X-Request-ID": "client-123",
    "X-API-Version": "v2"
  }
}
```

### Timeout Configuration

Configure custom timeouts (in seconds):

```json
{
  "url": "http://your-server.example.com/mcp",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  },
  "timeout": 30
}
```

### Environment-Specific Configs

Use different configs for different environments:

```bash
# Development
~/mcp-configs/weather-dev.json

# Staging
~/mcp-configs/weather-staging.json

# Production
~/mcp-configs/weather-prod.json
```

Switch by changing the `--config` argument in Claude Desktop config.

## Session Management

The bridge automatically manages session IDs:

1. First request (`initialize`) receives a session ID from the server
2. Subsequent requests include the session ID in `mcp-session-id` header
3. Session persists for the lifetime of the bridge process
4. Each Claude Desktop restart creates a new session

## Updating MCP Bridge

### When using uvx with GitHub

Simply restart Claude Desktop - `uvx` will pull the latest version automatically!

To force a specific version:
```json
"--from", "git+https://github.com/geosp/mcp-bridge@v0.2.0"
```

### When using local installation

```bash
pip install --upgrade mcp-bridge
# or
uv pip install --upgrade mcp-bridge
```

## Security Best Practices

1. **Never commit config files with credentials** to version control
2. **Use environment variables** for sensitive data when possible
3. **Store config files** in secure locations with appropriate permissions:
   ```bash
   chmod 600 ~/mcp-configs/weather.json
   ```
4. **Use HTTPS** for production servers
5. **Rotate API tokens** regularly

## Getting Help

- **Documentation**: https://github.com/geosp/mcp-bridge
- **Issues**: https://github.com/geosp/mcp-bridge/issues
- **MCP Protocol**: https://modelcontextprotocol.io
