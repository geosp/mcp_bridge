#!/bin/bash
# Setup script for mcp-bridge repository structure

set -e

echo "Setting up mcp-bridge repository structure..."
echo ""

# Create main directories
mkdir -p docs
mkdir -p examples

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Config files with secrets
config.json
*.local.json

# Logs
*.log
EOF
echo "✓ Created .gitignore"

# Create LICENSE (MIT)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 MCP Bridge Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
echo "✓ Created LICENSE"

# Create README.md
cat > README.md << 'EOF'
# MCP Bridge

Universal transport bridge for Model Context Protocol (MCP) - connect stdio-based MCP clients to remote servers over HTTP/SSE.

## What is MCP Bridge?

MCP Bridge solves a common integration challenge: **MCP clients like Claude Desktop expect stdio connections, but many MCP servers run remotely over HTTP/SSE**. This bridge sits in the middle, translating between these protocols seamlessly.

```
[Claude Desktop/MCP Client] <--stdio--> [MCP Bridge] <--HTTP/SSE--> [Remote MCP Server]
```

### Use Cases

- Connect Claude Desktop to remote/containerized MCP servers
- Access cloud-hosted MCP services from local clients
- Bridge to MCP servers behind authentication
- Enable any stdio-based MCP client to use HTTP/SSE servers

## Installation

### Using uv (recommended)

```bash
pip install uv
uv pip install mcp-sse-bridge
```

### Using pip

```bash
pip install mcp-sse-bridge
```

### From source

```bash
git clone https://github.com/yourusername/mcp-bridge.git
cd mcp-bridge
uv pip install -e .
```

## Configuration

Create a `config.json` file in the `mcp_http_bridge` directory:

```json
{
  "url": "http://your-mcp-server.example.com/mcp-endpoint",
  "headers": {
    "Authorization": "Bearer your-token-here"
  }
}
```

### Configuration Options

- `url` (required): The HTTP/SSE endpoint of your remote MCP server
- `headers` (optional): HTTP headers to include with requests (e.g., authentication tokens)

## Usage with Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "remote-server": {
      "command": "mcp-http-bridge",
      "args": []
    }
  }
}
```

Make sure the bridge's `config.json` is properly configured before starting Claude Desktop.

## How It Works

1. **Stdio Interface**: Listens for JSON-RPC messages from Claude Desktop on stdin
2. **HTTP Translation**: Forwards requests to the remote MCP server via HTTP POST
3. **SSE Streaming**: Reads Server-Sent Events responses from the HTTP connection
4. **Session Management**: Maintains session IDs across requests
5. **Response Forwarding**: Writes responses back to stdout for the client

## Architecture

```
┌─────────────────┐
│ Claude Desktop  │
│  (MCP Client)   │
└────────┬────────┘
         │ stdio (JSON-RPC)
         │
┌────────▼────────┐
│   MCP Bridge    │
│  - Read stdin   │
│  - HTTP client  │
│  - SSE parser   │
│  - Write stdout │
└────────┬────────┘
         │ HTTP/SSE
         │
┌────────▼────────┐
│  Remote MCP     │
│     Server      │
└─────────────────┘
```

## Example Configurations

See the `examples/` directory for sample configurations:

- `examples/local-server.json` - Connect to a local MCP server
- `examples/authenticated-server.json` - Server with bearer token auth
- `examples/claude-desktop-config.json` - Claude Desktop configuration

## Troubleshooting

### Bridge not connecting

- Check that `config.json` exists and has valid JSON
- Verify the `url` is accessible from your machine
- Check logs in stderr for error messages

### Authentication failures

- Ensure your `Authorization` header token is valid
- Check if the token has expired
- Verify the token format matches server expectations

### Claude Desktop not finding the bridge

- Verify `mcp-http-bridge` is in your PATH: `which mcp-http-bridge`
- Try using the full path to the script in Claude Desktop config
- Check Claude Desktop logs for error messages

### Enable debug logging

The bridge logs to stderr. To capture logs:

```bash
mcp-http-bridge 2> bridge.log
```

## Future Enhancements

- [ ] WebSocket transport support
- [ ] Multiple endpoint configurations
- [ ] Request/response logging options
- [ ] Retry logic and connection pooling
- [ ] Health check endpoints
- [ ] TLS/SSL certificate configuration

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Related Projects

- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP documentation
- [Claude Desktop](https://claude.ai/download) - Anthropic's desktop client

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mcp-bridge/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mcp-bridge/discussions)
- **Documentation**: [docs.claude.com](https://docs.claude.com)
EOF
echo "✓ Created README.md"

# Create CONTRIBUTING.md
cat > CONTRIBUTING.md << 'EOF'
# Contributing to MCP Bridge

Thank you for your interest in contributing to MCP Bridge!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/mcp-bridge.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Description of changes"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-bridge.git
cd mcp-bridge

# Install dependencies
uv pip install -e ".[dev]"

# Run tests (when available)
pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

## Testing

- Add tests for new features
- Ensure existing tests pass
- Test with actual MCP servers when possible

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Update documentation as needed
- Add examples if introducing new features
- Reference any related issues

## Questions?

Open an issue or start a discussion on GitHub!
EOF
echo "✓ Created CONTRIBUTING.md"

# Create example config files
cat > examples/config.example.json << 'EOF'
{
  "url": "http://localhost:8000/mcp",
  "headers": {
    "Authorization": "Bearer your-token-here",
    "X-Custom-Header": "optional-value"
  }
}
EOF
echo "✓ Created examples/config.example.json"

cat > examples/local-server.json << 'EOF'
{
  "url": "http://localhost:8000/mcp"
}
EOF
echo "✓ Created examples/local-server.json"

cat > examples/authenticated-server.json << 'EOF'
{
  "url": "https://api.example.com/mcp",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN_HERE"
  }
}
EOF
echo "✓ Created examples/authenticated-server.json"

cat > examples/claude-desktop-config.json << 'EOF'
{
  "mcpServers": {
    "my-remote-server": {
      "command": "mcp-http-bridge",
      "args": []
    }
  }
}
EOF
echo "✓ Created examples/claude-desktop-config.json"

# Create docs/ARCHITECTURE.md
cat > docs/ARCHITECTURE.md << 'EOF'
# MCP Bridge Architecture

## Overview

MCP Bridge is a protocol translator that bridges the gap between stdio-based MCP clients and HTTP/SSE-based MCP servers.

## Components

### 1. Stdin Reader
- Reads JSON-RPC messages from stdin
- Parses and validates message format
- Queues messages for processing

### 2. HTTP Client
- Sends requests to remote MCP server
- Manages connection pooling
- Handles timeouts and retries

### 3. SSE Parser
- Reads Server-Sent Events from HTTP response
- Extracts JSON data from SSE messages
- Handles connection errors gracefully

### 4. Session Manager
- Tracks session IDs from initialize requests
- Adds session headers to subsequent requests
- Maintains session state

### 5. Stdout Writer
- Formats responses as JSON-RPC
- Writes to stdout for client consumption
- Handles broken pipe errors

## Message Flow

1. Client sends JSON-RPC request to stdin
2. Bridge reads and parses the message
3. Bridge forwards request to remote server via HTTP POST
4. Remote server responds with SSE stream
5. Bridge parses SSE events and extracts JSON
6. Bridge writes JSON-RPC response to stdout
7. Client receives response

## Session Handling

The `initialize` method establishes a session:
- Server returns `mcp-session-id` header
- Bridge stores session ID
- Subsequent requests include session ID header

## Error Handling

- Network errors: Logged to stderr, error response to stdout
- Parse errors: Logged and sent as JSON-RPC error
- Broken pipe: Gracefully terminates connection
- Timeouts: Configurable, defaults to 60s

## Future Architecture

### Multi-Transport Support

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │ stdio
┌──────▼───────┐
│ MCP Bridge   │
│ ┌──────────┐ │
│ │Transport │ │
│ │ Manager  │ │
│ └────┬─────┘ │
│      │       │
│ ┌────▼────┐  │
│ │  HTTP   │  │
│ │  SSE    │  │
│ └─────────┘  │
│ ┌─────────┐  │
│ │WebSocket│  │
│ └─────────┘  │
│ ┌─────────┐  │
│ │  gRPC   │  │
│ └─────────┘  │
└──────────────┘
```
EOF
echo "✓ Created docs/ARCHITECTURE.md"

# Create docs/TROUBLESHOOTING.md
cat > docs/TROUBLESHOOTING.md << 'EOF'
# Troubleshooting Guide

## Common Issues

### Bridge Won't Start

**Symptom**: Bridge exits immediately or shows configuration error

**Solutions**:
- Verify `config.json` exists in `mcp_http_bridge/` directory
- Check JSON syntax is valid: `python -m json.tool config.json`
- Ensure `url` field is present and valid
- Check file permissions

### Connection Refused

**Symptom**: `Connection refused` or `Connection timeout` errors

**Solutions**:
- Verify the remote server is running and accessible
- Check firewall rules
- Test connectivity: `curl -v http://your-server/mcp`
- Verify URL in config.json is correct

### Authentication Failures

**Symptom**: 401 or 403 HTTP errors

**Solutions**:
- Check token format in `Authorization` header
- Verify token hasn't expired
- Test with curl: `curl -H "Authorization: Bearer TOKEN" http://server/mcp`
- Check server logs for auth errors

### Claude Desktop Not Connecting

**Symptom**: Claude Desktop doesn't show the MCP server

**Solutions**:
- Verify bridge is in PATH: `which mcp-http-bridge`
- Check Claude Desktop config file location
- Try full path to bridge in config
- Restart Claude Desktop after config changes
- Check Claude Desktop logs

### SSE Parsing Errors

**Symptom**: Invalid JSON or SSE format errors

**Solutions**:
- Verify server is sending proper SSE format
- Check for `data:` prefix in SSE messages
- Ensure JSON is valid in SSE data field
- Enable debug logging to see raw SSE

### Session Issues

**Symptom**: Requests fail after initialize

**Solutions**:
- Check server returns `mcp-session-id` header
- Verify session ID is being stored
- Check logs for session ID in requests
- Some servers may not require sessions

## Debugging

### Enable Verbose Logging

Redirect stderr to a file:
```bash
mcp-http-bridge 2> debug.log
```

### Test Bridge Manually

Send a test message:
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | mcp-http-bridge
```

### Check Server Response

Test the server directly:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  http://your-server/mcp
```

## Getting Help

If you're still stuck:
1. Check existing GitHub issues
2. Enable debug logging and capture the output
3. Open a new issue with:
   - Error messages
   - Configuration (remove sensitive tokens)
   - Steps to reproduce
   - Environment details (OS, Python version)
EOF
echo "✓ Created docs/TROUBLESHOOTING.md"

echo ""
echo "✅ Repository structure created successfully!"
echo ""
echo "Next steps:"
echo "1. Review and customize the files as needed"
echo "2. Update README.md with your GitHub username"
echo "3. Add your actual code to the repository"
echo "4. Initialize git: git init"
echo "5. Make first commit: git add . && git commit -m 'Initial commit'"
echo "6. Create GitHub repo and push"
echo ""
echo "Files created:"
echo "  - .gitignore"
echo "  - LICENSE"
echo "  - README.md"
echo "  - CONTRIBUTING.md"
echo "  - examples/config.example.json"
echo "  - examples/local-server.json"
echo "  - examples/authenticated-server.json"
echo "  - examples/claude-desktop-config.json"
echo "  - docs/ARCHITECTURE.md"
echo "  - docs/TROUBLESHOOTING.md"
