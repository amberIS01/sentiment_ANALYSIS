"""Tests for summary module."""

import pytest
from datetime import datetime
from chatbot.summary import (
    SummaryStats,
    ConversationSummary,
    SummaryGenerator,
    summarize_conversation,
)


class TestSummaryStats:
    """Tests for SummaryStats."""

    def test_create_stats(self):
        """Test creating summary stats."""
        stats = SummaryStats(
            total_messages=10,
            avg_sentiment=0.5,
            positive_ratio=0.6,
            negative_ratio=0.2,
            neutral_ratio=0.2,
            top_emotions=["happy", "excited"],
            top_topics=["weather", "sports"],
        )
        assert stats.total_messages == 10
        assert stats.avg_sentiment == 0.5
        assert stats.positive_ratio == 0.6

    def test_empty_emotions(self):
        """Test stats with empty emotions."""
        stats = SummaryStats(
            total_messages=5,
            avg_sentiment=0.0,
            positive_ratio=0.0,
            negative_ratio=0.0,
            neutral_ratio=1.0,
            top_emotions=[],
            top_topics=[],
        )
        assert len(stats.top_emotions) == 0


class TestConversationSummary:
    """Tests for ConversationSummary."""

    def test_create_summary(self):
        """Test creating conversation summary."""
        stats = SummaryStats(
            total_messages=5,
            avg_sentiment=0.3,
            positive_ratio=0.6,
            negative_ratio=0.2,
            neutral_ratio=0.2,
            top_emotions=["happy"],
            top_topics=["greetings"],
        )
        summary = ConversationSummary(
            title="Test Summary",
            duration=120.0,
            stats=stats,
            highlights=["Good message"],
            conclusion="Positive conversation",
            generated_at=datetime.now(),
        )
        assert summary.title == "Test Summary"
        assert summary.duration == 120.0


class TestSummaryGenerator:
    """Tests for SummaryGenerator."""

    def test_generate_positive(self):
        """Test generating positive summary."""
        generator = SummaryGenerator()
        messages = ["I love this!", "Great product!", "Amazing!"]
        sentiments = [0.8, 0.7, 0.9]
        
        summary = generator.generate(messages, sentiments)
        
        assert "Positive" in summary.title
        assert summary.stats.avg_sentiment > 0.5

    def test_generate_negative(self):
        """Test generating negative summary."""
        generator = SummaryGenerator()
        messages = ["This is bad", "Terrible experience", "Awful"]
        sentiments = [-0.7, -0.8, -0.9]
        
        summary = generator.generate(messages, sentiments)
        
        assert "Negative" in summary.title
        assert summary.stats.avg_sentiment < -0.5

    def test_generate_neutral(self):
        """Test generating neutral summary."""
        generator = SummaryGenerator()
        messages = ["Okay product", "It works", "Normal"]
        sentiments = [0.0, 0.02, -0.01]
        
        summary = generator.generate(messages, sentiments)
        
        assert "Neutral" in summary.title

    def test_with_emotions(self):
        """Test with emotions provided."""
        generator = SummaryGenerator()
        messages = ["Happy day!", "Excited!"]
        sentiments = [0.8, 0.9]
        emotions = [["happy", "joy"], ["excited"]]
        
        summary = generator.generate(messages, sentiments, emotions)
        
        assert len(summary.stats.top_emotions) > 0

    def test_with_topics(self):
        """Test with topics provided."""
        generator = SummaryGenerator()
        messages = ["Weather is great", "Sports update"]
        sentiments = [0.5, 0.3]
        topics = ["weather", "sports", "news"]
        
        summary = generator.generate(messages, sentiments, topics=topics)
        
        assert len(summary.stats.top_topics) > 0

    def test_empty_messages(self):
        """Test with empty messages."""
        generator = SummaryGenerator()
        summary = generator.generate([], [])
        
        assert summary.stats.total_messages == 0

    def test_highlights_extraction(self):
        """Test highlights are extracted."""
        generator = SummaryGenerator()
        messages = ["Bad day", "Great news!", "Okay"]
        sentiments = [-0.5, 0.8, 0.0]
        
        summary = generator.generate(messages, sentiments)
        
        assert len(summary.highlights) > 0


class TestSummarizeConversation:
    """Tests for summarize_conversation function."""

    def test_simple_summary(self):
        """Test simple text summary."""
        messages = ["Hello!", "Great to meet you!"]
        sentiments = [0.5, 0.7]
        
        result = summarize_conversation(messages, sentiments)
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_negative_summary(self):
        """Test negative summary text."""
        messages = ["Bad experience", "Disappointed"]
        sentiments = [-0.6, -0.8]
        
        result = summarize_conversation(messages, sentiments)
        
        assert "negative" in result.lower()
