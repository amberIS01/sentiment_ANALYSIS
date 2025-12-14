"""
CLI Formatters Module

This module provides formatting utilities for CLI output including
colors, tables, and styled text output.
"""

from enum import Enum
from typing import List, Optional, Dict, Any


class Color(Enum):
    """ANSI color codes."""
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


class CLIFormatter:
    """Format output for CLI display."""

    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors

    def colorize(self, text: str, color: Color) -> str:
        """Apply color to text."""
        if not self.use_colors:
            return text
        return f"{color.value}{text}{Color.RESET.value}"

    def success(self, text: str) -> str:
        """Format success message."""
        return self.colorize(f"✓ {text}", Color.GREEN)

    def error(self, text: str) -> str:
        """Format error message."""
        return self.colorize(f"✗ {text}", Color.RED)

    def warning(self, text: str) -> str:
        """Format warning message."""
        return self.colorize(f"⚠ {text}", Color.YELLOW)

    def info(self, text: str) -> str:
        """Format info message."""
        return self.colorize(f"ℹ {text}", Color.BLUE)

    def bold(self, text: str) -> str:
        """Make text bold."""
        return self.colorize(text, Color.BOLD)

    def dim(self, text: str) -> str:
        """Make text dim."""
        return self.colorize(text, Color.DIM)

    def header(self, text: str, width: int = 60) -> str:
        """Format a header."""
        line = "=" * width
        return f"{line}\n  {self.bold(text)}\n{line}"

    def subheader(self, text: str, width: int = 40) -> str:
        """Format a subheader."""
        line = "-" * width
        return f"{line}\n{text}\n{line}"

    def sentiment_label(self, label: str) -> str:
        """Color-code sentiment label."""
        colors = {
            "Positive": Color.GREEN,
            "Negative": Color.RED,
            "Neutral": Color.YELLOW,
        }
        color = colors.get(label, Color.WHITE)
        return self.colorize(label, color)

    def progress_bar(self, value: float, width: int = 30) -> str:
        """Create a progress bar."""
        filled = int(value * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        percent = f"{value * 100:.1f}%"
        return f"[{bar}] {percent}"

    def table(self, headers: List[str], rows: List[List[str]]) -> str:
        """Format data as a simple table."""
        if not headers or not rows:
            return ""

        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        lines = []
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        lines.append(header_line)
        lines.append("-" * len(header_line))

        for row in rows:
            row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            lines.append(row_line)

        return "\n".join(lines)


def format_sentiment_output(label: str, score: float, use_colors: bool = True) -> str:
    """Format sentiment output with optional colors."""
    formatter = CLIFormatter(use_colors)
    colored_label = formatter.sentiment_label(label)
    return f"Sentiment: {colored_label} (score: {score:.2f})"


def format_summary_stats(stats: Dict[str, Any], use_colors: bool = True) -> str:
    """Format summary statistics."""
    formatter = CLIFormatter(use_colors)
    lines = [
        formatter.subheader("Statistics"),
        f"  Positive: {stats.get('positive', 0)}",
        f"  Negative: {stats.get('negative', 0)}",
        f"  Neutral: {stats.get('neutral', 0)}",
        f"  Average Score: {stats.get('average', 0.0):.2f}",
    ]
    return "\n".join(lines)
