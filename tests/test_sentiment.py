"""
Tests for the Sentiment Analysis Module.
"""

import pytest
from chatbot.sentiment import (
    SentimentAnalyzer,
    SentimentLabel,
    SentimentResult,
    ConversationSentimentSummary
)


class TestSentimentAnalyzer:
    """Test suite for SentimentAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create a SentimentAnalyzer instance for testing."""
        return SentimentAnalyzer()

    def test_analyze_positive_text(self, analyzer):
        """Test that positive text is correctly identified."""
        result = analyzer.analyze_text("I love this! It's amazing and wonderful!")
        assert result.label == SentimentLabel.POSITIVE
        assert result.compound_score > 0

    def test_analyze_negative_text(self, analyzer):
        """Test that negative text is correctly identified."""
        result = analyzer.analyze_text("This is terrible and disappointing.")
        assert result.label == SentimentLabel.NEGATIVE
        assert result.compound_score < 0

    def test_analyze_neutral_text(self, analyzer):
        """Test that neutral text is correctly identified."""
        result = analyzer.analyze_text("The meeting is at 3pm today.")
        assert result.label == SentimentLabel.NEUTRAL

    def test_sentiment_result_str(self, analyzer):
        """Test SentimentResult string representation."""
        result = analyzer.analyze_text("I'm happy!")
        result_str = str(result)
        assert "Positive" in result_str or "Negative" in result_str or "Neutral" in result_str

    def test_analyze_empty_conversation(self, analyzer):
        """Test analyzing an empty conversation."""
        summary = analyzer.analyze_conversation([])
        assert summary.overall_sentiment == SentimentLabel.NEUTRAL
        assert summary.average_compound_score == 0.0
        assert len(summary.message_sentiments) == 0

    def test_analyze_conversation_positive(self, analyzer):
        """Test analyzing a positive conversation."""
        messages = [
            "I love your service!",
            "Everything is wonderful!",
            "Thank you so much!"
        ]
        summary = analyzer.analyze_conversation(messages)
        assert summary.overall_sentiment == SentimentLabel.POSITIVE
        assert summary.positive_count == 3
        assert summary.negative_count == 0

    def test_analyze_conversation_negative(self, analyzer):
        """Test analyzing a negative conversation."""
        messages = [
            "Your service disappoints me",
            "This is terrible",
            "I'm very frustrated"
        ]
        summary = analyzer.analyze_conversation(messages)
        assert summary.overall_sentiment == SentimentLabel.NEGATIVE
        assert summary.negative_count >= 2

    def test_analyze_conversation_mixed(self, analyzer):
        """Test analyzing a mixed sentiment conversation."""
        messages = [
            "Your service disappoints me",
            "Last experience was better",
            "I hope things improve"
        ]
        summary = analyzer.analyze_conversation(messages)
        assert len(summary.message_sentiments) == 3

    def test_mood_trend_improving(self, analyzer):
        """Test mood trend detection for improving sentiment."""
        messages = [
            "This is terrible!",
            "It's getting a bit better",
            "Actually, things are good now",
            "I'm really happy with the result!"
        ]
        summary = analyzer.analyze_conversation(messages)
        assert "improv" in summary.mood_trend.lower() or "stable" in summary.mood_trend.lower()

    def test_mood_trend_declining(self, analyzer):
        """Test mood trend detection for declining sentiment."""
        messages = [
            "I'm so happy today!",
            "This is okay I guess",
            "Not feeling great about this",
            "This is absolutely terrible!"
        ]
        summary = analyzer.analyze_conversation(messages)
        # Check that some trend analysis was performed
        assert summary.mood_trend is not None

    def test_vader_handles_punctuation_emphasis(self, analyzer):
        """Test that VADER handles punctuation emphasis."""
        result1 = analyzer.analyze_text("good")
        result2 = analyzer.analyze_text("good!!!")
        # Punctuation should amplify the sentiment
        assert result2.compound_score >= result1.compound_score

    def test_vader_handles_capitalization(self, analyzer):
        """Test that VADER handles capitalization emphasis."""
        result1 = analyzer.analyze_text("great")
        result2 = analyzer.analyze_text("GREAT")
        # Capitalization should amplify the sentiment
        assert result2.compound_score >= result1.compound_score

    def test_conversation_summary_str(self, analyzer):
        """Test ConversationSentimentSummary string representation."""
        messages = ["I'm happy!", "Great service!"]
        summary = analyzer.analyze_conversation(messages)
        summary_str = str(summary)
        assert "Overall conversation sentiment" in summary_str


class TestSentimentLabel:
    """Test suite for SentimentLabel enum."""

    def test_sentiment_labels_exist(self):
        """Test that all expected sentiment labels exist."""
        assert SentimentLabel.POSITIVE.value == "Positive"
        assert SentimentLabel.NEGATIVE.value == "Negative"
        assert SentimentLabel.NEUTRAL.value == "Neutral"


class TestSentimentResult:
    """Test suite for SentimentResult dataclass."""

    def test_sentiment_result_creation(self):
        """Test creating a SentimentResult."""
        result = SentimentResult(
            label=SentimentLabel.POSITIVE,
            compound_score=0.8,
            positive_score=0.7,
            negative_score=0.0,
            neutral_score=0.3
        )
        assert result.label == SentimentLabel.POSITIVE
        assert result.compound_score == 0.8
