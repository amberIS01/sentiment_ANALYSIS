"""Tests for comparator module."""

import pytest
from chatbot.comparator import (
    ComparisonResult,
    SentimentComparison,
    BatchComparison,
    SentimentComparator,
    compare_sentiments,
    agreement_score,
)


class TestSentimentComparator:
    """Tests for SentimentComparator."""

    def test_compare_equal(self):
        """Test comparing similar scores."""
        comparator = SentimentComparator(tolerance=0.1)
        result = comparator.compare(0.5, 0.52)
        
        assert result.result == ComparisonResult.SIMILAR

    def test_compare_greater(self):
        """Test comparing when b is greater."""
        comparator = SentimentComparator(tolerance=0.1)
        result = comparator.compare(0.3, 0.7)
        
        assert result.result == ComparisonResult.GREATER
        assert result.difference == pytest.approx(0.4)

    def test_compare_less(self):
        """Test comparing when b is less."""
        comparator = SentimentComparator(tolerance=0.1)
        result = comparator.compare(0.8, 0.3)
        
        assert result.result == ComparisonResult.LESS

    def test_compare_many(self):
        """Test batch comparison."""
        comparator = SentimentComparator()
        scores_a = [0.5, 0.6, 0.7]
        scores_b = [0.52, 0.58, 0.72]
        
        result = comparator.compare_many(scores_a, scores_b)
        
        assert len(result.comparisons) == 3
        assert result.agreement_rate > 0

    def test_is_similar(self):
        """Test similarity check."""
        comparator = SentimentComparator(tolerance=0.1)
        
        assert comparator.is_similar(0.5, 0.55) is True
        assert comparator.is_similar(0.5, 0.8) is False

    def test_is_opposite(self):
        """Test opposite polarity check."""
        comparator = SentimentComparator()
        
        assert comparator.is_opposite(0.5, -0.5) is True
        assert comparator.is_opposite(0.5, 0.3) is False


class TestCompareSentiments:
    """Tests for compare_sentiments function."""

    def test_compare(self):
        """Test compare function."""
        result = compare_sentiments(0.3, 0.8)
        
        assert isinstance(result, SentimentComparison)
        assert result.difference == pytest.approx(0.5)


class TestAgreementScore:
    """Tests for agreement_score function."""

    def test_perfect_agreement(self):
        """Test perfect agreement."""
        scores_a = [0.5, 0.6, 0.7]
        scores_b = [0.5, 0.6, 0.7]
        
        score = agreement_score(scores_a, scores_b)
        assert score == 1.0

    def test_no_agreement(self):
        """Test no agreement."""
        scores_a = [0.1, 0.2, 0.3]
        scores_b = [0.9, 0.8, 0.7]
        
        score = agreement_score(scores_a, scores_b)
        assert score == 0.0
