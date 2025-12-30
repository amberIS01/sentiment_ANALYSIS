"""Tests for threshold module."""

import pytest
from chatbot.threshold import (
    SentimentCategory,
    ThresholdConfig,
    ThresholdResult,
    ThresholdClassifier,
    classify_sentiment,
    get_category_label,
)


class TestThresholdClassifier:
    """Tests for ThresholdClassifier."""

    def test_classify_very_negative(self):
        """Test classifying very negative."""
        classifier = ThresholdClassifier()
        result = classifier.classify(-0.8)
        
        assert result.category == SentimentCategory.VERY_NEGATIVE

    def test_classify_negative(self):
        """Test classifying negative."""
        classifier = ThresholdClassifier()
        result = classifier.classify(-0.4)
        
        assert result.category == SentimentCategory.NEGATIVE

    def test_classify_neutral(self):
        """Test classifying neutral."""
        classifier = ThresholdClassifier()
        result = classifier.classify(0.0)
        
        assert result.category == SentimentCategory.NEUTRAL

    def test_classify_positive(self):
        """Test classifying positive."""
        classifier = ThresholdClassifier()
        result = classifier.classify(0.4)
        
        assert result.category == SentimentCategory.POSITIVE

    def test_classify_very_positive(self):
        """Test classifying very positive."""
        classifier = ThresholdClassifier()
        result = classifier.classify(0.8)
        
        assert result.category == SentimentCategory.VERY_POSITIVE

    def test_classify_many(self):
        """Test classifying multiple scores."""
        classifier = ThresholdClassifier()
        results = classifier.classify_many([-0.8, 0.0, 0.8])
        
        assert len(results) == 3

    def test_is_positive(self):
        """Test is_positive check."""
        classifier = ThresholdClassifier()
        
        assert classifier.is_positive(0.5) is True
        assert classifier.is_positive(-0.5) is False

    def test_is_negative(self):
        """Test is_negative check."""
        classifier = ThresholdClassifier()
        
        assert classifier.is_negative(-0.5) is True
        assert classifier.is_negative(0.5) is False

    def test_is_neutral(self):
        """Test is_neutral check."""
        classifier = ThresholdClassifier()
        
        assert classifier.is_neutral(0.0) is True
        assert classifier.is_neutral(0.5) is False

    def test_get_boundaries(self):
        """Test getting boundaries."""
        classifier = ThresholdClassifier()
        boundaries = classifier.get_boundaries()
        
        assert "very_negative" in boundaries
        assert "very_positive" in boundaries

    def test_custom_config(self):
        """Test with custom config."""
        config = ThresholdConfig(neutral_low=-0.1, neutral_high=0.1)
        classifier = ThresholdClassifier(config)
        
        result = classifier.classify(0.15)
        assert result.category == SentimentCategory.POSITIVE


class TestClassifySentiment:
    """Tests for classify_sentiment function."""

    def test_classify(self):
        """Test classify function."""
        category = classify_sentiment(0.5)
        
        assert category == SentimentCategory.POSITIVE


class TestGetCategoryLabel:
    """Tests for get_category_label function."""

    def test_labels(self):
        """Test getting labels."""
        assert get_category_label(SentimentCategory.POSITIVE) == "Positive"
        assert get_category_label(SentimentCategory.NEGATIVE) == "Negative"
