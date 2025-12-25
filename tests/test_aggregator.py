"""
Tests for the Aggregator Module.
"""

import pytest

from chatbot.aggregator import (
    SentimentAggregator,
    AggregatedSentiment,
    AggregationType,
    SentimentSource,
)


class TestAggregationType:
    """Test AggregationType enum."""

    def test_values(self):
        assert AggregationType.AVERAGE.value == "average"
        assert AggregationType.WEIGHTED.value == "weighted"
        assert AggregationType.MEDIAN.value == "median"


class TestSentimentAggregator:
    """Test SentimentAggregator class."""

    def test_initialization(self):
        aggregator = SentimentAggregator()
        assert aggregator is not None

    def test_add_source(self):
        aggregator = SentimentAggregator()
        aggregator.add_source("twitter", weight=1.5)
        assert "twitter" in aggregator.get_source_names()

    def test_add_text(self):
        aggregator = SentimentAggregator()
        result = aggregator.add_text("reviews", "I love this product!")
        assert result is not None

    def test_aggregate_empty(self):
        aggregator = SentimentAggregator()
        result = aggregator.aggregate()
        assert result.count == 0

    def test_aggregate_average(self):
        aggregator = SentimentAggregator()
        aggregator.add_text("source1", "I love this!")
        aggregator.add_text("source1", "This is okay")
        result = aggregator.aggregate(AggregationType.AVERAGE)
        assert isinstance(result, AggregatedSentiment)
        assert result.count == 2

    def test_aggregate_weighted(self):
        aggregator = SentimentAggregator()
        aggregator.add_source("high", weight=2.0)
        aggregator.add_source("low", weight=0.5)
        aggregator.add_text("high", "Amazing!")
        aggregator.add_text("low", "Terrible!")
        result = aggregator.aggregate(AggregationType.WEIGHTED)
        assert result.count == 2

    def test_aggregate_by_source(self):
        aggregator = SentimentAggregator()
        aggregator.add_text("source1", "Great!")
        aggregator.add_text("source2", "Bad!")
        results = aggregator.aggregate_by_source()
        assert "source1" in results
        assert "source2" in results

    def test_clear(self):
        aggregator = SentimentAggregator()
        aggregator.add_text("test", "Hello")
        aggregator.clear()
        assert len(aggregator.get_source_names()) == 0


class TestAggregatedSentiment:
    """Test AggregatedSentiment dataclass."""

    def test_creation(self):
        result = AggregatedSentiment(
            score=0.5,
            label="positive",
            count=10,
            min_score=-0.2,
            max_score=0.9,
            std_dev=0.3,
            aggregation_type=AggregationType.AVERAGE,
        )
        assert result.score == 0.5
        assert result.label == "positive"
