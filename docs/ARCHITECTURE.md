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
