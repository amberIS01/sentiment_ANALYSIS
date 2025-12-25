"""
Tests for the Filters Module.
"""

import pytest

from chatbot.filters import (
    Filter,
    ScoreFilter,
    LabelFilter,
    CompositeFilter,
    FilterChain,
    FilterOperator,
    FilterResult,
    filter_positive,
    filter_negative,
    filter_by_score,
)
from chatbot.sentiment import SentimentResult, SentimentLabel


class TestFilterOperator:
    """Test FilterOperator enum."""

    def test_values(self):
        assert FilterOperator.GREATER_THAN.value == "greater_than"
        assert FilterOperator.LESS_THAN.value == "less_than"


class TestFilterResult:
    """Test FilterResult dataclass."""

    def test_creation(self):
        result = FilterResult(passed=True, reason="Test passed")
        assert result.passed is True


class TestScoreFilter:
    """Test ScoreFilter class."""

    def test_greater_than(self):
        filter_ = ScoreFilter(0.5, FilterOperator.GREATER_THAN)
        result = SentimentResult(0.3, 0.1, 0.6, 0.7, SentimentLabel.POSITIVE)
        assert filter_.apply(result).passed is True

    def test_less_than(self):
        filter_ = ScoreFilter(0.0, FilterOperator.LESS_THAN)
        result = SentimentResult(0.3, 0.5, 0.2, -0.5, SentimentLabel.NEGATIVE)
        assert filter_.apply(result).passed is True


class TestLabelFilter:
    """Test LabelFilter class."""

    def test_include(self):
        filter_ = LabelFilter([SentimentLabel.POSITIVE])
        result = SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE)
        assert filter_.apply(result).passed is True

    def test_exclude(self):
        filter_ = LabelFilter([SentimentLabel.NEGATIVE], exclude=True)
        result = SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE)
        assert filter_.apply(result).passed is True


class TestCompositeFilter:
    """Test CompositeFilter class."""

    def test_require_all(self):
        f1 = ScoreFilter(0.0, FilterOperator.GREATER_THAN)
        f2 = LabelFilter([SentimentLabel.POSITIVE])
        composite = CompositeFilter([f1, f2], require_all=True)
        result = SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE)
        assert composite.apply(result).passed is True

    def test_require_any(self):
        f1 = ScoreFilter(0.9, FilterOperator.GREATER_THAN)
        f2 = LabelFilter([SentimentLabel.POSITIVE])
        composite = CompositeFilter([f1, f2], require_all=False)
        result = SentimentResult(0.5, 0.1, 0.4, 0.5, SentimentLabel.POSITIVE)
        assert composite.apply(result).passed is True


class TestFilterChain:
    """Test FilterChain class."""

    def test_initialization(self):
        chain = FilterChain()
        assert chain is not None

    def test_add_filter(self):
        chain = FilterChain()
        chain.add(ScoreFilter(0.0))
        result = SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE)
        filtered = chain.filter([result])
        assert len(filtered) == 1

    def test_filter_multiple(self):
        chain = FilterChain()
        chain.add(LabelFilter([SentimentLabel.POSITIVE]))
        results = [
            SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE),
            SentimentResult(0.1, 0.8, 0.1, -0.8, SentimentLabel.NEGATIVE),
        ]
        filtered = chain.filter(results)
        assert len(filtered) == 1


class TestFilterFunctions:
    """Test filter convenience functions."""

    def test_filter_positive(self):
        results = [
            SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE),
            SentimentResult(0.1, 0.8, 0.1, -0.8, SentimentLabel.NEGATIVE),
        ]
        filtered = filter_positive(results)
        assert len(filtered) == 1

    def test_filter_negative(self):
        results = [
            SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE),
            SentimentResult(0.1, 0.8, 0.1, -0.8, SentimentLabel.NEGATIVE),
        ]
        filtered = filter_negative(results)
        assert len(filtered) == 1

    def test_filter_by_score(self):
        results = [
            SentimentResult(0.8, 0.1, 0.1, 0.8, SentimentLabel.POSITIVE),
            SentimentResult(0.1, 0.8, 0.1, -0.8, SentimentLabel.NEGATIVE),
        ]
        filtered = filter_by_score(results, min_score=0.0)
        assert len(filtered) == 1
