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

### 1. Install MCP Bridge from GitHub using uv

Use `uv` to install mcp-bridge directly from GitHub:

```bash
# Install from GitHub repository
uv pip install git+https://github.com/geosp/mcp_bridge.git

# Verify installation
mcp-bridge --version
which mcp-bridge
```

This installs mcp-bridge into your local Python environment managed by `uv`.

**Optional: Install in a specific environment**
```bash
# Create a dedicated virtual environment
uv venv ~/.venvs/mcp-bridge

# Install into that environment
uv pip install --python ~/.venvs/mcp-bridge/bin/python git+https://github.com/geosp/mcp_bridge.git

# The binary will be at:
# ~/.venvs/mcp-bridge/bin/mcp-bridge
```

### 2. Create Your Bridge Configuration

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

### 3. Configure Claude Desktop

Now configure Claude Desktop to use the installed mcp-bridge.

#### Option A: Using the installed command directly (Recommended)

If you installed globally or can access `mcp-bridge` from your PATH:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "mcp-bridge",
      "args": [
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
      "command": "mcp-bridge",
      "args": [
        "--config", "C:\\Users\\yourusername\\mcp-configs\\weather.json"
      ]
    }
  }
}
```

#### Option B: Using full path to installed binary

If Claude Desktop can't find `mcp-bridge`, use the full path:

**Find the path:**
```bash
which mcp-bridge
# macOS/Linux: Usually ~/.local/bin/mcp-bridge or ~/.venvs/mcp-bridge/bin/mcp-bridge
```

```powershell
where.exe mcp-bridge
# Windows: Usually C:\Users\yourusername\.local\bin\mcp-bridge.exe
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "/Users/yourusername/.local/bin/mcp-bridge",
      "args": [
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
      "command": "C:\\Users\\yourusername\\.local\\bin\\mcp-bridge.exe",
      "args": [
        "--config", "C:\\Users\\yourusername\\mcp-configs\\weather.json"
      ]
    }
  }
}
```

#### Option C: Using uv run (if not in PATH)

Use `uv run` to execute the installed package:

**macOS/Linux:**
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "uv",
      "args": [
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
        "run",
        "mcp-bridge",
        "--config", "C:\\Users\\yourusername\\mcp-configs\\weather.json"
      ]
    }
  }
}
```

### 4. Multiple Servers Setup

You can configure multiple remote servers by creating separate config files:

```json
{
  "mcpServers": {
    "weather-server": {
      "command": "mcp-bridge",
      "args": [
        "--config", "/Users/yourusername/mcp-configs/weather.json"
      ]
    },
    "database-server": {
      "command": "mcp-bridge",
      "args": [
        "--config", "/Users/yourusername/mcp-configs/database.json"
      ]
    },
    "analytics-server": {
      "command": "mcp-bridge",
      "args": [
        "--config", "/Users/yourusername/mcp-configs/analytics.json"
      ]
    }
  }
}
```

## Updating MCP Bridge

To update to the latest version from GitHub:

```bash
# Update the installation
uv pip install --upgrade git+https://github.com/geosp/mcp_bridge.git

# Verify new version
mcp-bridge --version

# Restart Claude Desktop to use the updated version
```

### Installing Specific Versions

To install a specific version, branch, or commit:

**Specific tag/version:**
```bash
uv pip install git+https://github.com/geosp/mcp_bridge.git@v0.2.0
```

**Specific branch:**
```bash
uv pip install git+https://github.com/geosp/mcp_bridge.git@main
```

**Specific commit:**
```bash
uv pip install git+https://github.com/geosp/mcp_bridge.git@abc1234
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

### Git authentication error

If you get "could not read Username" or "terminal prompts disabled":

**Most common cause: Wrong repository URL**

Make sure you're using the correct repository name with underscore:
```bash
# Correct (with underscore):
uv pip install git+https://github.com/geosp/mcp_bridge.git

# Incorrect (with dash):
uv pip install git+https://github.com/geosp/mcp-bridge.git  # This will fail!
```

**For private repositories:**

**Solution 1: Use HTTPS with token**
```bash
# Create a GitHub personal access token at https://github.com/settings/tokens
# Then use:
uv pip install git+https://YOUR_TOKEN@github.com/geosp/mcp_bridge.git
```

**Solution 2: Use SSH instead**
```bash
# Ensure you have SSH keys set up with GitHub
uv pip install git+ssh://git@github.com/geosp/mcp_bridge.git
```

**Solution 3: Clone and install locally**
```bash
# Clone the repository first
git clone https://github.com/geosp/mcp_bridge.git
cd mcp_bridge

# Install from local directory
uv pip install .
```

### mcp-bridge command not found

If you get "command not found" for `mcp-bridge`:

1. **Verify it's installed:**
   ```bash
   uv pip list | grep mcp-bridge
   ```

2. **Find where it's installed:**
   ```bash
   which mcp-bridge  # macOS/Linux
   where.exe mcp-bridge  # Windows
   ```

3. **Use the full path in your Claude Desktop config:**
   ```json
   "command": "/Users/yourusername/.local/bin/mcp-bridge"
   ```

4. **Reinstall if needed:**
   ```bash
   uv pip install git+https://github.com/geosp/mcp_bridge.git
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

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | mcp-bridge --config /path/to/weather.json
```

You should see a response with the server's capabilities and a session ID.

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
      "command": "mcp-bridge",
      "args": [
        "--config", "/Users/yourusername/mcp-configs/weather.json"
      ]
    }
  }
}
```

Or with full path if needed:
```json
{
  "mcpServers": {
    "weather-server": {
      "command": "/Users/yourusername/.local/bin/mcp-bridge",
      "args": [
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
