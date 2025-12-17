"""
Tests for the Analyzer Module.
"""

import pytest

from chatbot.analyzer import (
    ConversationAnalyzer,
    MessageAnalysis,
    ConversationInsights,
    analyze_conversation,
)


class TestMessageAnalysis:
    """Test MessageAnalysis dataclass."""

    def test_creation(self):
        analysis = MessageAnalysis(
            text="Hello world",
            sentiment_score=0.5,
            sentiment_label="positive",
            emotions=["joy"],
            word_count=2,
        )
        assert analysis.word_count == 2
        assert analysis.sentiment_label == "positive"


class TestConversationInsights:
    """Test ConversationInsights dataclass."""

    def test_creation(self):
        insights = ConversationInsights(
            total_messages=10,
            avg_sentiment=0.5,
            sentiment_variance=0.1,
            dominant_sentiment="positive",
            dominant_emotions=["joy", "trust"],
            avg_message_length=15.0,
            sentiment_shifts=3,
            positive_ratio=0.6,
            negative_ratio=0.2,
            engagement_score=0.75,
        )
        assert insights.total_messages == 10
        assert insights.dominant_sentiment == "positive"


class TestConversationAnalyzer:
    """Test ConversationAnalyzer class."""

    def test_initialization(self):
        analyzer = ConversationAnalyzer()
        assert analyzer.sentiment_analyzer is not None
        assert analyzer.emotion_detector is not None

    def test_analyze_message(self):
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze_message("I am so happy today!")
        assert isinstance(result, MessageAnalysis)
        assert result.word_count == 5

    def test_analyze_conversation_empty(self):
        analyzer = ConversationAnalyzer()
        result = analyzer.analyze_conversation([])
        assert result.total_messages == 0

    def test_analyze_conversation(self):
        analyzer = ConversationAnalyzer()
        messages = [
            "I love this product!",
            "It works great",
            "Very satisfied",
        ]
        result = analyzer.analyze_conversation(messages)
        assert isinstance(result, ConversationInsights)
        assert result.total_messages == 3

    def test_analyze_mixed_sentiment(self):
        analyzer = ConversationAnalyzer()
        messages = [
            "This is amazing!",
            "I hate waiting",
            "It's okay I guess",
        ]
        result = analyzer.analyze_conversation(messages)
        assert result.sentiment_shifts >= 0

    def test_find_turning_points(self):
        analyzer = ConversationAnalyzer()
        messages = [
            "Everything is terrible",
            "Actually, this is great!",
            "I changed my mind",
        ]
        points = analyzer.find_turning_points(messages, threshold=0.3)
        assert isinstance(points, list)

    def test_summarize(self):
        analyzer = ConversationAnalyzer()
        messages = ["Good day", "Great work", "Nice job"]
        summary = analyzer.summarize(messages)
        assert isinstance(summary, str)
        assert "Summary" in summary


class TestAnalyzeConversation:
    """Test analyze_conversation function."""

    def test_basic_analysis(self):
        messages = ["Hello", "How are you?", "I'm fine"]
        result = analyze_conversation(messages)
        assert isinstance(result, ConversationInsights)
        assert result.total_messages == 3
