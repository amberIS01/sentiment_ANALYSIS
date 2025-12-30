"""Tests for output module."""

import pytest
import json
from chatbot.output import (
    OutputFormat,
    OutputFormatter,
    JsonFormatter,
    TextFormatter,
    TableFormatter,
    MarkdownFormatter,
    format_output,
)


class TestJsonFormatter:
    """Tests for JsonFormatter."""

    def test_format(self):
        """Test JSON formatting."""
        formatter = JsonFormatter()
        data = {"score": 0.5, "label": "positive"}
        
        result = formatter.format(data)
        
        parsed = json.loads(result)
        assert parsed["score"] == 0.5

    def test_format_pretty(self):
        """Test pretty JSON."""
        formatter = JsonFormatter(indent=2)
        data = {"key": "value"}
        
        result = formatter.format(data)
        
        assert "\n" in result


class TestTextFormatter:
    """Tests for TextFormatter."""

    def test_format_dict(self):
        """Test dict formatting."""
        formatter = TextFormatter()
        data = {"score": 0.5, "label": "positive"}
        
        result = formatter.format(data)
        
        assert "score" in result
        assert "0.5" in result

    def test_format_list(self):
        """Test list formatting."""
        formatter = TextFormatter()
        data = [0.5, 0.6, 0.7]
        
        result = formatter.format(data)
        
        assert "0.5" in result


class TestTableFormatter:
    """Tests for TableFormatter."""

    def test_format(self):
        """Test table formatting."""
        formatter = TableFormatter()
        data = [
            {"name": "A", "score": 0.5},
            {"name": "B", "score": 0.8},
        ]
        
        result = formatter.format(data)
        
        assert "name" in result
        assert "score" in result

    def test_empty_data(self):
        """Test with empty data."""
        formatter = TableFormatter()
        result = formatter.format([])
        
        assert result == ""


class TestMarkdownFormatter:
    """Tests for MarkdownFormatter."""

    def test_format_dict(self):
        """Test dict as markdown."""
        formatter = MarkdownFormatter()
        data = {"score": 0.5}
        
        result = formatter.format(data)
        
        assert "**score**" in result

    def test_format_list(self):
        """Test list as markdown."""
        formatter = MarkdownFormatter()
        data = ["item1", "item2"]
        
        result = formatter.format(data)
        
        assert "- " in result


class TestOutputFormatter:
    """Tests for OutputFormatter."""

    def test_format_json(self):
        """Test JSON output."""
        formatter = OutputFormatter(OutputFormat.JSON)
        result = formatter.format({"key": "value"})
        
        assert json.loads(result)["key"] == "value"

    def test_format_text(self):
        """Test text output."""
        formatter = OutputFormatter(OutputFormat.TEXT)
        result = formatter.format({"key": "value"})
        
        assert "key" in result


class TestFormatOutput:
    """Tests for format_output function."""

    def test_format(self):
        """Test format function."""
        result = format_output({"score": 0.5}, OutputFormat.JSON)
        
        assert "score" in result
