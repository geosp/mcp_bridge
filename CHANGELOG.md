# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Automatic workaround for Claude Desktop parameter serialization bug
  - Detects and deserializes stringified object/array parameters in `tools/call` requests
  - Logs parameter corrections to stderr for debugging
  - Comprehensive test suite with 14 unit tests
  - Documentation in README explaining the bug and workaround
  - ✅ Tested and confirmed working with Claude Desktop
- CHANGELOG.md to track project changes

### Fixed
- MCP tool calls with object/array parameters now work correctly with Claude Desktop
  - Previously failed with "Input validation error" due to stringified parameters
  - Bridge now automatically converts `{"filter": "{\"key\":\"value\"}"}` to `{"filter": {"key":"value"}}`
  - Affects tools like database filters, complex configurations, and nested data structures
  - Fix applied specifically to `tools/call` method where parameters are nested in `params.arguments`

## [0.2.0] - 2025

### Added
- Multiple server configuration support
- Named configuration files (e.g., `weather.json`, `database.json`)
- `mcp-bridge init --name` command for creating named configs
- `mcp-bridge list-configs` command to list all available configurations
- `--config` flag to specify which configuration to use

### Changed
- Configuration system now supports multiple named configs
- Improved CLI with better configuration management

## [0.1.0] - 2025

### Added
- Initial release of MCP Bridge
- Stdio to HTTP/SSE protocol translation
- Session management with session ID tracking
- Support for JSON-RPC 2.0 protocol
- Basic error handling and logging
- Configuration file support (`~/.config/mcp-bridge/config.json`)
- `mcp-bridge init` command for configuration setup
- Authentication header support
- Claude Desktop integration support

### Technical Details
- Built with Python 3.8+ support
- Uses httpx for HTTP/SSE communication
- Async/await architecture with asyncio
- Comprehensive error handling and logging to stderr

[Unreleased]: https://github.com/geosp/mcp_bridge/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/geosp/mcp_bridge/releases/tag/v0.2.0
[0.1.0]: https://github.com/geosp/mcp_bridge/releases/tag/v0.1.0
