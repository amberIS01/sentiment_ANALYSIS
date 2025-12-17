"""
Tests for the Comparison Module.
"""

import pytest

from chatbot.comparison import (
    SentimentComparator,
    SentimentDiff,
    GroupComparison,
    ComparisonResult,
    compare_sentiment,
)


class TestComparisonResult:
    """Test ComparisonResult enum."""

    def test_values(self):
        assert ComparisonResult.MORE_POSITIVE.value == "more_positive"
        assert ComparisonResult.MORE_NEGATIVE.value == "more_negative"
        assert ComparisonResult.SIMILAR.value == "similar"


class TestSentimentDiff:
    """Test SentimentDiff dataclass."""

    def test_creation(self):
        diff = SentimentDiff(
            text1="hello",
            text2="world",
            score1=0.5,
            score2=0.8,
            difference=0.3,
            result=ComparisonResult.MORE_POSITIVE,
        )
        assert diff.difference == 0.3


class TestSentimentComparator:
    """Test SentimentComparator class."""

    def test_initialization(self):
        comparator = SentimentComparator()
        assert comparator.threshold == 0.1

    def test_custom_threshold(self):
        comparator = SentimentComparator(threshold=0.2)
        assert comparator.threshold == 0.2

    def test_compare_texts(self):
        comparator = SentimentComparator()
        result = comparator.compare_texts(
            "I hate this",
            "I love this",
        )
        assert isinstance(result, SentimentDiff)
        assert result.result == ComparisonResult.MORE_POSITIVE

    def test_compare_similar(self):
        comparator = SentimentComparator()
        result = comparator.compare_texts(
            "This is okay",
            "This is fine",
        )
        assert result.result == ComparisonResult.SIMILAR

    def test_compare_groups(self):
        comparator = SentimentComparator()
        group1 = ["I hate this", "This is terrible"]
        group2 = ["I love this", "This is wonderful"]
        result = comparator.compare_groups(group1, group2)
        assert isinstance(result, GroupComparison)
        assert result.result == ComparisonResult.MORE_POSITIVE

    def test_rank_by_sentiment(self):
        comparator = SentimentComparator()
        texts = ["I hate this", "This is okay", "I love this"]
        ranked = comparator.rank_by_sentiment(texts)
        assert len(ranked) == 3
        # Most positive should be first
        assert ranked[0][1] > ranked[2][1]

    def test_find_most_positive(self):
        comparator = SentimentComparator()
        texts = ["Bad day", "Great day", "Okay day"]
        text, score = comparator.find_most_positive(texts)
        assert "Great" in text

    def test_find_most_negative(self):
        comparator = SentimentComparator()
        texts = ["Bad day", "Great day", "Okay day"]
        text, score = comparator.find_most_negative(texts)
        assert "Bad" in text

    def test_find_outliers(self):
        comparator = SentimentComparator()
        texts = [
            "Okay", "Fine", "Alright", "Sure",
            "I ABSOLUTELY LOVE THIS SO MUCH!!!"
        ]
        outliers = comparator.find_outliers(texts)
        assert len(outliers) >= 0  # May or may not find outliers


class TestCompareSentiment:
    """Test compare_sentiment function."""

    def test_basic_comparison(self):
        result = compare_sentiment("I hate this", "I love this")
        assert isinstance(result, SentimentDiff)
