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
