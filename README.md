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
