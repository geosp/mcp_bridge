"""
Command-line interface for MCP Bridge
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Optional
import click

from .bridge import MCPHTTPBridge, log

def find_config_path(config_name: Optional[str] = None) -> Path:
    """
    Find configuration file in order of precedence:
    1. Explicit path (if provided and exists)
    2. ~/.config/mcp-bridge/<config_name or config.json>
    3. Current directory config.json (for backward compat)
    4. Old location: mcp_http_bridge/config.json (deprecated)
    """
    
    # 1. Explicit path provided
    if config_name:
        explicit_path = Path(config_name)
        if explicit_path.is_absolute() and explicit_path.exists():
            return explicit_path
    
    # 2. Check user config directory
    config_dir = Path.home() / ".config" / "mcp-bridge"
    if config_name:
        # Look for named config in config directory
        config_path = config_dir / config_name
        if config_path.exists():
            return config_path
        # Also try with .json extension if not provided
        if not config_name.endswith('.json'):
            config_path = config_dir / f"{config_name}.json"
            if config_path.exists():
                return config_path
    else:
        # Look for default config.json
        default_config = config_dir / "config.json"
        if default_config.exists():
            return default_config
    
    # 3. Check current directory (backward compat)
    local_config = Path("config.json")
    if local_config.exists():
        log("Warning: Using config.json from current directory (deprecated)")
        log(f"         Please move to {config_dir}/config.json")
        return local_config
    
    # 4. Check old location (deprecated)
    old_location = Path("mcp_http_bridge") / "config.json"
    if old_location.exists():
        log("Warning: Using config from mcp_http_bridge/config.json (deprecated)")
        log(f"         Please move to {config_dir}/config.json")
        return old_location
    
    # Not found - show helpful error
    search_locations = [
        str(config_dir),
        str(local_config.absolute()),
        str(old_location.absolute())
    ]
    raise FileNotFoundError(
        f"Config file not found. Searched:\n" + 
        "\n".join(f"  - {loc}" for loc in search_locations) +
        f"\n\nCreate a config file with:\n  mcp-bridge init"
    )

def load_config(config_path: Path) -> dict:
    """Load and validate configuration file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'url' not in config:
            log("Error: 'url' is required in config file")
            sys.exit(1)
        
        log(f"Loaded config from {config_path}")
        return config
    
    except json.JSONDecodeError as e:
        log(f"Error: Invalid JSON in config file: {e}")
        sys.exit(1)
    except Exception as e:
        log(f"Error loading config: {e}")
        sys.exit(1)

@click.group(invoke_without_command=True)
@click.option('--config', '-c', default=None, help='Path to config file')
@click.option('--version', is_flag=True, help='Show version')
@click.pass_context
def cli(ctx, config, version):
    """MCP Bridge - Connect stdio MCP clients to HTTP/SSE servers"""
    
    if version:
        from . import __version__
        click.echo(f"mcp-bridge version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        # Run the bridge
        asyncio.run(run_bridge(config))

@cli.command()
@click.option('--name', '-n', default=None, help='Config file name')
def init(name):
    """Initialize config directory and create example config"""
    
    config_dir = Path.home() / ".config" / "mcp-bridge"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_name = name if name else "config.json"
    if not config_name.endswith('.json'):
        config_name = f"{config_name}.json"
    
    config_path = config_dir / config_name
    
    if config_path.exists():
        click.echo(f"❌ Config already exists: {config_path}")
        click.echo(f"   Use --name to create a different config")
        sys.exit(1)
    
    # Create example config
    example_config = {
        "url": "http://your-server.example.com/mcp",
        "headers": {
            "Authorization": "Bearer YOUR_TOKEN_HERE"
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(example_config, f, indent=2)
    
    click.echo(f"✓ Created config directory: {config_dir}")
    click.echo(f"✓ Created config file: {config_path}")
    click.echo(f"\nNext steps:")
    click.echo(f"1. Edit the config file:")
    click.echo(f"   vi {config_path}")
    click.echo(f"2. Update the 'url' and 'headers' with your server details")
    click.echo(f"3. Run the bridge:")
    if name:
        click.echo(f"   mcp-bridge --config {config_name}")
    else:
        click.echo(f"   mcp-bridge")

@cli.command()
def list_configs():
    """List available config files"""
    
    config_dir = Path.home() / ".config" / "mcp-bridge"
    
    if not config_dir.exists():
        click.echo(f"Config directory not found: {config_dir}")
        click.echo(f"Create configs with: mcp-bridge init")
        return
    
    configs = sorted(config_dir.glob("*.json"))
    
    if not configs:
        click.echo(f"No config files found in {config_dir}")
        click.echo(f"Create a config with: mcp-bridge init")
        return
    
    click.echo(f"Available configs in {config_dir}:\n")
    for config in configs:
        is_default = config.name == "config.json"
        marker = "  (default)" if is_default else ""
        click.echo(f"  • {config.name}{marker}")
    
    click.echo(f"\nUse with: mcp-bridge --config <name>")

async def run_bridge(config_name: Optional[str]):
    """Run the bridge with specified config"""
    
    try:
        config_path = find_config_path(config_name)
        config = load_config(config_path)
        
        bridge = MCPHTTPBridge(
            url=config['url'],
            headers=config.get('headers', {})
        )
        
        try:
            await bridge.run()
        finally:
            await bridge.close()
            log("Bridge shut down")
    
    except FileNotFoundError as e:
        log(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        log("Interrupted by user")

def main():
    """Entry point for console script"""
    cli()

if __name__ == "__main__":
    main()
