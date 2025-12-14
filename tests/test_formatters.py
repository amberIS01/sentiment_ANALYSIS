"""
Tests for the Formatters Module.
"""

import pytest
from chatbot.formatters import CLIFormatter, Color, format_sentiment_output


class TestCLIFormatter:
    """Test CLIFormatter class."""

    @pytest.fixture
    def formatter(self):
        return CLIFormatter(use_colors=True)

    @pytest.fixture
    def no_color_formatter(self):
        return CLIFormatter(use_colors=False)

    def test_colorize(self, formatter):
        result = formatter.colorize("test", Color.RED)
        assert Color.RED.value in result

    def test_no_colors(self, no_color_formatter):
        result = no_color_formatter.colorize("test", Color.RED)
        assert result == "test"

    def test_success(self, formatter):
        result = formatter.success("Done")
        assert "✓" in result

    def test_error(self, formatter):
        result = formatter.error("Failed")
        assert "✗" in result

    def test_warning(self, formatter):
        result = formatter.warning("Caution")
        assert "⚠" in result

    def test_info(self, formatter):
        result = formatter.info("Note")
        assert "ℹ" in result

    def test_header(self, formatter):
        result = formatter.header("Title")
        assert "Title" in result
        assert "=" in result

    def test_sentiment_label_positive(self, formatter):
        result = formatter.sentiment_label("Positive")
        assert "Positive" in result

    def test_sentiment_label_negative(self, formatter):
        result = formatter.sentiment_label("Negative")
        assert "Negative" in result

    def test_progress_bar(self, formatter):
        result = formatter.progress_bar(0.5)
        assert "50.0%" in result
        assert "█" in result

    def test_table(self, formatter):
        headers = ["Name", "Value"]
        rows = [["A", "1"], ["B", "2"]]
        result = formatter.table(headers, rows)
        assert "Name" in result
        assert "Value" in result


class TestFormatSentimentOutput:
    """Test format_sentiment_output function."""

    def test_with_colors(self):
        result = format_sentiment_output("Positive", 0.75, use_colors=True)
        assert "Positive" in result
        assert "0.75" in result

    def test_without_colors(self):
        result = format_sentiment_output("Negative", -0.5, use_colors=False)
        assert "Negative" in result
