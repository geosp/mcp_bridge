#!/usr/bin/env python3
"""
Unit tests for the stringified parameter deserialization workaround.

Tests the fix for Claude Desktop's parameter serialization bug where
object/array parameters are stringified instead of preserved as objects.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mcp_bridge.bridge import deserialize_stringified_params


class TestDeserializeStringifiedParams:
    """Test cases for parameter deserialization"""

    def test_stringified_object(self):
        """Test that stringified objects are deserialized"""
        arguments = {
            "filter": '{"lastName": "Fajardo", "status": "active"}'
        }
        result = deserialize_stringified_params(arguments)

        assert result["filter"] == {"lastName": "Fajardo", "status": "active"}
        assert isinstance(result["filter"], dict)

    def test_stringified_array(self):
        """Test that stringified arrays are deserialized"""
        arguments = {
            "items": '[1, 2, 3, 4]',
            "tags": '["python", "testing", "mcp"]'
        }
        result = deserialize_stringified_params(arguments)

        assert result["items"] == [1, 2, 3, 4]
        assert result["tags"] == ["python", "testing", "mcp"]
        assert isinstance(result["items"], list)
        assert isinstance(result["tags"], list)

    def test_nested_object(self):
        """Test stringified objects with nested structures"""
        arguments = {
            "config": '{"database": {"host": "localhost", "port": 5432}, "cache": true}'
        }
        result = deserialize_stringified_params(arguments)

        expected = {
            "database": {"host": "localhost", "port": 5432},
            "cache": True
        }
        assert result["config"] == expected

    def test_mixed_types(self):
        """Test arguments with both stringified and normal values"""
        arguments = {
            "filter": '{"status": "active"}',  # Stringified object
            "limit": 10,  # Normal integer
            "offset": 20,  # Normal integer
            "sort": "desc",  # Normal string
            "tags": '["tag1", "tag2"]'  # Stringified array
        }
        result = deserialize_stringified_params(arguments)

        assert result["filter"] == {"status": "active"}
        assert result["limit"] == 10
        assert result["offset"] == 20
        assert result["sort"] == "desc"
        assert result["tags"] == ["tag1", "tag2"]

    def test_invalid_json_preserved(self):
        """Test that invalid JSON strings are preserved as-is"""
        arguments = {
            "malformed": '{"incomplete":',
            "notjson": '{this is not valid json}'
        }
        result = deserialize_stringified_params(arguments)

        # Should keep original invalid strings
        assert result["malformed"] == '{"incomplete":'
        assert result["notjson"] == '{this is not valid json}'

    def test_normal_string_preserved(self):
        """Test that normal strings are not affected"""
        arguments = {
            "message": "This is a normal string",
            "url": "https://example.com",
            "path": "/home/user/file.txt"
        }
        result = deserialize_stringified_params(arguments)

        assert result["message"] == "This is a normal string"
        assert result["url"] == "https://example.com"
        assert result["path"] == "/home/user/file.txt"

    def test_empty_arguments(self):
        """Test that empty arguments dict works"""
        arguments = {}
        result = deserialize_stringified_params(arguments)

        assert result == {}

    def test_null_and_special_values(self):
        """Test handling of null, boolean, and numeric values"""
        arguments = {
            "enabled": True,
            "count": 42,
            "ratio": 3.14,
            "data": None
        }
        result = deserialize_stringified_params(arguments)

        assert result["enabled"] is True
        assert result["count"] == 42
        assert result["ratio"] == 3.14
        assert result["data"] is None

    def test_stringified_boolean_not_converted(self):
        """Test that stringified booleans/numbers are NOT converted (only objects/arrays)"""
        arguments = {
            "value": "true",  # String, not JSON object/array
            "number": "42"    # String, not JSON object/array
        }
        result = deserialize_stringified_params(arguments)

        # These should remain as strings since they're not objects or arrays
        assert result["value"] == "true"
        assert result["number"] == "42"

    def test_whitespace_handling(self):
        """Test that whitespace around JSON is handled correctly"""
        arguments = {
            "filter": '  {"key": "value"}  ',
            "items": '  [1, 2, 3]  '
        }
        result = deserialize_stringified_params(arguments)

        assert result["filter"] == {"key": "value"}
        assert result["items"] == [1, 2, 3]

    def test_empty_object_and_array(self):
        """Test that empty objects and arrays are deserialized"""
        arguments = {
            "empty_obj": '{}',
            "empty_arr": '[]'
        }
        result = deserialize_stringified_params(arguments)

        assert result["empty_obj"] == {}
        assert result["empty_arr"] == []

    def test_complex_real_world_example(self):
        """Test a complex real-world scenario with multiple stringified params"""
        arguments = {
            "filter": '{"lastName": "Fajardo", "department": "Engineering", "active": true}',
            "sort": '{"field": "lastName", "order": "asc"}',
            "pagination": '{"page": 1, "pageSize": 50}',
            "include": '["profile", "permissions", "groups"]',
            "query": "search term",  # Normal string
            "limit": 100  # Normal number
        }
        result = deserialize_stringified_params(arguments)

        assert result["filter"] == {
            "lastName": "Fajardo",
            "department": "Engineering",
            "active": True
        }
        assert result["sort"] == {"field": "lastName", "order": "asc"}
        assert result["pagination"] == {"page": 1, "pageSize": 50}
        assert result["include"] == ["profile", "permissions", "groups"]
        assert result["query"] == "search term"
        assert result["limit"] == 100

    def test_string_starting_with_brace_but_not_json(self):
        """Test strings that start with { or [ but aren't valid JSON"""
        arguments = {
            "regex": "{2,5}",  # Regex pattern, not JSON
            "text": "[Note] This is a note"  # Text starting with [
        }
        result = deserialize_stringified_params(arguments)

        # Should preserve these as strings since they're not valid JSON
        assert result["regex"] == "{2,5}"
        assert result["text"] == "[Note] This is a note"

    def test_unicode_in_stringified_json(self):
        """Test that Unicode characters in stringified JSON are handled"""
        arguments = {
            "user": '{"name": "José García", "city": "São Paulo"}'
        }
        result = deserialize_stringified_params(arguments)

        assert result["user"] == {"name": "José García", "city": "São Paulo"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
