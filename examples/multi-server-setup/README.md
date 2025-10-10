# Multi-Server Setup Example

This example demonstrates how to configure mcp-bridge for multiple MCP servers.

## Setup

1. Create the config directory:
   ```bash
   mkdir -p ~/.config/mcp-bridge
   ```

2. Copy example configs:
   ```bash
   cp weather.json ~/.config/mcp-bridge/
   cp database.json ~/.config/mcp-bridge/
   ```

3. Edit each config with your actual server details:
   ```bash
   vi ~/.config/mcp-bridge/weather.json
   vi ~/.config/mcp-bridge/database.json
   ```

4. Configure Claude Desktop:
   - Copy the contents of `claude-desktop-config.json`
   - Add to your Claude Desktop config file:
     - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
     - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

5. Restart Claude Desktop

## Files

- `weather.json` - Example weather service configuration
- `database.json` - Example database service configuration
- `claude-desktop-config.json` - Example Claude Desktop configuration

## Usage

Each config file can be used independently:

```bash
# Use weather service
mcp-bridge --config weather.json

# Use database service  
mcp-bridge --config database.json

# Or use full name
mcp-bridge --config weather
```

## Directory Organization

You can organize configs in subdirectories:

```
~/.config/mcp-bridge/
├── config.json          # Default
├── weather.json
├── database.json
├── prod/
│   ├── api.json
│   └── db.json
└── dev/
    ├── api.json
    └── db.json
```

Then use: `mcp-bridge --config prod/api.json`
