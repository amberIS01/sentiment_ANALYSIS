"""
Tests for the Utils Module.
"""

import pytest
from datetime import datetime, timedelta

from chatbot.utils import (
    truncate_text,
    format_timestamp,
    format_duration,
    format_percentage,
    safe_divide,
    clamp,
    flatten_dict,
    word_count,
    sentence_count,
    average,
    generate_id,
)


class TestTruncateText:
    """Test truncate_text function."""

    def test_short_text_unchanged(self):
        assert truncate_text("Hello", 10) == "Hello"

    def test_long_text_truncated(self):
        result = truncate_text("Hello World", 8)
        assert len(result) == 8
        assert result.endswith("...")

    def test_empty_text(self):
        assert truncate_text("", 10) == ""

    def test_custom_suffix(self):
        result = truncate_text("Hello World", 9, suffix="..")
        assert result.endswith("..")


class TestFormatDuration:
    """Test format_duration function."""

    def test_seconds_only(self):
        assert format_duration(timedelta(seconds=30)) == "30s"

    def test_minutes_and_seconds(self):
        assert format_duration(timedelta(minutes=5, seconds=30)) == "5m 30s"

    def test_hours_minutes_seconds(self):
        result = format_duration(timedelta(hours=1, minutes=30, seconds=45))
        assert "1h" in result
        assert "30m" in result

    def test_zero_duration(self):
        assert format_duration(timedelta(0)) == "0s"


class TestFormatPercentage:
    """Test format_percentage function."""

    def test_basic_percentage(self):
        assert format_percentage(0.5) == "50.0%"

    def test_custom_decimal(self):
        assert format_percentage(0.333, decimal_places=2) == "33.30%"

    def test_zero(self):
        assert format_percentage(0) == "0.0%"


class TestSafeDivide:
    """Test safe_divide function."""

    def test_normal_division(self):
        assert safe_divide(10, 2) == 5.0

    def test_division_by_zero(self):
        assert safe_divide(10, 0) == 0.0

    def test_custom_default(self):
        assert safe_divide(10, 0, default=-1) == -1


class TestClamp:
    """Test clamp function."""

    def test_value_in_range(self):
        assert clamp(5, 0, 10) == 5

    def test_value_below_min(self):
        assert clamp(-5, 0, 10) == 0

    def test_value_above_max(self):
        assert clamp(15, 0, 10) == 10


class TestFlattenDict:
    """Test flatten_dict function."""

    def test_flat_dict(self):
        d = {"a": 1, "b": 2}
        assert flatten_dict(d) == {"a": 1, "b": 2}

    def test_nested_dict(self):
        d = {"a": {"b": 1}}
        assert flatten_dict(d) == {"a.b": 1}

    def test_custom_separator(self):
        d = {"a": {"b": 1}}
        assert flatten_dict(d, sep="_") == {"a_b": 1}


class TestWordCount:
    """Test word_count function."""

    def test_basic_count(self):
        assert word_count("Hello world") == 2

    def test_empty_string(self):
        assert word_count("") == 0

    def test_multiple_spaces(self):
        assert word_count("Hello   world") == 2


class TestSentenceCount:
    """Test sentence_count function."""

    def test_single_sentence(self):
        assert sentence_count("Hello world.") == 1

    def test_multiple_sentences(self):
        assert sentence_count("Hello! How are you? Fine.") == 3

    def test_empty_string(self):
        assert sentence_count("") == 0


class TestAverage:
    """Test average function."""

    def test_basic_average(self):
        assert average([1, 2, 3]) == 2.0

    def test_empty_list(self):
        assert average([]) == 0.0

    def test_single_value(self):
        assert average([5]) == 5.0


class TestGenerateId:
    """Test generate_id function."""

    def test_basic_id(self):
        id1 = generate_id()
        assert len(id1) > 0

    def test_with_prefix(self):
        id1 = generate_id("test")
        assert id1.startswith("test_")

    def test_unique_ids(self):
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2
