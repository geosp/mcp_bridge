#!/usr/bin/env python3
"""
Test script to call MCP weather tools via the bridge.

This demonstrates how to programmatically interact with MCP servers
through the HTTP/SSE bridge.
"""

import json
import asyncio
import httpx
from typing import Dict, Any


class MCPClient:
    """Simple MCP client that communicates via HTTP/SSE"""

    def __init__(self, url: str, headers: Dict[str, str]):
        self.url = url
        self.headers = headers
        self.session_id = None
        self.client = httpx.AsyncClient(timeout=30.0)
        self.request_id = 0

    def _next_id(self) -> int:
        """Get next request ID"""
        self.request_id += 1
        return self.request_id

    async def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request and get response"""
        request_id = self._next_id()

        message = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params or {}
        }

        headers = {
            **self.headers,
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json"
        }

        if self.session_id and method != "initialize":
            headers["mcp-session-id"] = self.session_id

        print(f"📤 Sending: {method} (id={request_id})")

        response = await self.client.post(
            self.url,
            json=message,
            headers=headers
        )
        response.raise_for_status()

        # Extract session ID from initialize response
        if method == "initialize":
            self.session_id = response.headers.get("mcp-session-id")
            if self.session_id:
                print(f"🔑 Session ID: {self.session_id}")

        # Parse SSE or JSON response
        content_type = response.headers.get("content-type", "")

        if "text/event-stream" in content_type:
            # Parse SSE format
            lines = response.text.split('\n')
            for line in lines:
                if line.startswith("data: "):
                    data = line[6:].strip()
                    if data:
                        result = json.loads(data)
                        print(f"📥 Received: id={result.get('id')}")
                        return result
        else:
            # Direct JSON response
            return response.json()

        raise ValueError("No valid response received")

    async def initialize(self):
        """Initialize the MCP connection"""
        result = await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        })

        # Send initialized notification (required by protocol)
        await self._send_notification("notifications/initialized")

        return result

    async def _send_notification(self, method: str, params: Dict[str, Any] = None):
        """Send a notification (no response expected)"""
        message = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }

        headers = {
            **self.headers,
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json"
        }

        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        print(f"📤 Sending notification: {method}")

        await self.client.post(
            self.url,
            json=message,
            headers=headers
        )

    async def list_tools(self):
        """List available tools"""
        return await self._send_request("tools/list")

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Call a tool with arguments"""
        return await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })

    async def close(self):
        """Close the client connection"""
        await self.client.aclose()


async def main():
    """Test the weather MCP tools"""

    # Load config
    import os
    from pathlib import Path

    config_path = Path.home() / ".config" / "mcp-bridge" / "weather.json"

    print(f"📁 Loading config from: {config_path}")

    with open(config_path) as f:
        config = json.load(f)

    print(f"🌐 Server URL: {config['url']}\n")

    # Create client
    client = MCPClient(
        url=config["url"],
        headers=config.get("headers", {})
    )

    try:
        # Initialize
        print("=" * 60)
        print("STEP 1: Initialize Connection")
        print("=" * 60)
        init_response = await client.initialize()
        print(f"✅ Server: {init_response['result']['serverInfo']['name']} "
              f"v{init_response['result']['serverInfo']['version']}")
        print()

        # List tools
        print("=" * 60)
        print("STEP 2: List Available Tools")
        print("=" * 60)
        tools_response = await client.list_tools()

        if 'error' in tools_response:
            print(f"❌ Error from server: {tools_response['error']}")
            tools = []
        else:
            tools = tools_response.get('result', {}).get('tools', [])

        print(f"Found {len(tools)} tools:\n")
        for tool in tools:
            print(f"  📦 {tool['name']}")
            desc = tool['description'].split('\n')[0]  # First line only
            print(f"     {desc}")
            print()

        # Test get_hourly_weather
        print("=" * 60)
        print("STEP 3: Test get_hourly_weather()")
        print("=" * 60)

        location = "Tallahassee"
        print(f"🌤️  Getting weather for: {location}\n")

        weather_response = await client.call_tool("get_hourly_weather", {
            "location": location
        })

        if "result" in weather_response:
            weather_data = weather_response["result"]["content"][0]["text"]
            weather_json = json.loads(weather_data)

            print(f"📍 Location: {weather_json['location']}")
            print(f"🌍 Country: {weather_json['country']}")
            print(f"🕐 Timezone: {weather_json['timezone']}\n")

            current = weather_json['current_conditions']
            print("Current Conditions:")

            # Handle units in values
            def get_val(field):
                if isinstance(field, dict) and 'value' in field:
                    return field['value']
                return field

            temp = get_val(current['temperature'])
            feels = get_val(current['feels_like'])
            humidity = get_val(current['humidity'])
            precip = get_val(current['precipitation'])

            print(f"  🌡️  Temperature: {temp}°C (feels like {feels}°C)")
            print(f"  💧 Humidity: {humidity}%")
            print(f"  🌧️  Precipitation: {precip} mm")
            print(f"  💨 Wind: {current['wind']['speed']} km/h {current['wind']['direction']}")
            if 'weather_description' in current:
                print(f"  ☁️  Conditions: {current['weather_description']}")
            print()

            print("Hourly Forecast (next 6 hours):")
            for hour in weather_json['hourly_forecast'][:6]:
                time_str = hour['time']
                if 'T' in time_str:
                    time = time_str.split('T')[1][:5]  # Extract HH:MM
                else:
                    time = time_str[:5]

                temp = get_val(hour['temperature'])
                precip_prob = get_val(hour.get('precipitation_probability', 0))

                desc = hour.get('weather_description', 'N/A')
                print(f"  {time}: {temp}°C - {desc} ({precip_prob}% precip)")

        print()

        # Test geocode_location
        print("=" * 60)
        print("STEP 4: Test geocode_location()")
        print("=" * 60)

        location = "Tokyo, Japan"
        print(f"📍 Geocoding: {location}\n")

        geocode_response = await client.call_tool("geocode_location", {
            "location": location
        })

        if "result" in geocode_response:
            geocode_data = geocode_response["result"]["content"][0]["text"]
            geocode_json = json.loads(geocode_data)

            print(f"  Location: {geocode_json.get('location', 'N/A')}")
            print(f"  Name: {geocode_json.get('name', 'N/A')}")
            print(f"  Country: {geocode_json.get('country', 'N/A')}")
            print(f"  Latitude: {geocode_json.get('latitude', 'N/A')}")
            print(f"  Longitude: {geocode_json.get('longitude', 'N/A')}")
            print(f"  Timezone: {geocode_json.get('timezone', 'N/A')}")

        print()
        print("=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
