"""
Output Formatters Module

Format sentiment analysis output for various uses.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import json


@dataclass
class FormattedOutput:
    """Formatted output container."""

    content: str
    format_type: str
    metadata: Optional[Dict[str, Any]] = None


class OutputFormatter(ABC):
    """Base output formatter."""

    @abstractmethod
    def format(self, data: Dict[str, Any]) -> str:
        """Format data to string."""
        pass


class JSONFormatter(OutputFormatter):
    """Format output as JSON."""

    def __init__(self, indent: int = 2, sort_keys: bool = False):
        self.indent = indent
        self.sort_keys = sort_keys

    def format(self, data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=self.indent, sort_keys=self.sort_keys)


class TextFormatter(OutputFormatter):
    """Format output as plain text."""

    def __init__(self, separator: str = ": ", line_sep: str = "\n"):
        self.separator = separator
        self.line_sep = line_sep

    def format(self, data: Dict[str, Any]) -> str:
        lines = []
        for key, value in data.items():
            lines.append(f"{key}{self.separator}{value}")
        return self.line_sep.join(lines)


class TableFormatter(OutputFormatter):
    """Format output as ASCII table."""

    def __init__(self, headers: Optional[List[str]] = None):
        self.headers = headers

    def format(self, data: Dict[str, Any]) -> str:
        if not data:
            return ""

        # Calculate column widths
        key_width = max(len(str(k)) for k in data.keys())
        val_width = max(len(str(v)) for v in data.values())

        lines = []
        border = "+" + "-" * (key_width + 2) + "+" + "-" * (val_width + 2) + "+"
        lines.append(border)

        for key, value in data.items():
            lines.append(
                f"| {str(key):<{key_width}} | {str(value):<{val_width}} |"
            )

        lines.append(border)
        return "\n".join(lines)


class MarkdownFormatter(OutputFormatter):
    """Format output as Markdown."""

    def format(self, data: Dict[str, Any]) -> str:
        lines = []
        for key, value in data.items():
            lines.append(f"**{key}**: {value}")
        return "\n\n".join(lines)


class HTMLFormatter(OutputFormatter):
    """Format output as HTML."""

    def format(self, data: Dict[str, Any]) -> str:
        lines = ["<div class='sentiment-output'>"]
        for key, value in data.items():
            lines.append(f"  <p><strong>{key}:</strong> {value}</p>")
        lines.append("</div>")
        return "\n".join(lines)


class CSVFormatter(OutputFormatter):
    """Format output as CSV."""

    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    def format(self, data: Dict[str, Any]) -> str:
        keys = self.delimiter.join(str(k) for k in data.keys())
        values = self.delimiter.join(str(v) for v in data.values())
        return f"{keys}\n{values}"


class OutputManager:
    """Manage multiple output formatters."""

    def __init__(self):
        self._formatters: Dict[str, OutputFormatter] = {
            "json": JSONFormatter(),
            "text": TextFormatter(),
            "table": TableFormatter(),
            "markdown": MarkdownFormatter(),
            "html": HTMLFormatter(),
            "csv": CSVFormatter(),
        }

    def register(self, name: str, formatter: OutputFormatter) -> None:
        """Register a custom formatter."""
        self._formatters[name] = formatter

    def format(self, data: Dict[str, Any], format_type: str = "json") -> str:
        """Format data using specified formatter."""
        formatter = self._formatters.get(format_type)
        if not formatter:
            raise ValueError(f"Unknown format type: {format_type}")
        return formatter.format(data)

    def get_available_formats(self) -> List[str]:
        """Get list of available formats."""
        return list(self._formatters.keys())


def format_output(data: Dict[str, Any], format_type: str = "json") -> str:
    """Format sentiment output."""
    manager = OutputManager()
    return manager.format(data, format_type)
