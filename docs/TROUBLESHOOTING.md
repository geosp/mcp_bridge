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
