"""
Tests for the Statistics Module.
"""

import pytest
from datetime import datetime, timedelta

from chatbot.statistics import (
    StatisticsTracker,
    ConversationStatistics,
    MessageStatistics,
    analyze_message,
)
from chatbot.conversation import ConversationManager


class TestMessageStatistics:
    """Test cases for MessageStatistics dataclass."""

    def test_message_statistics_creation(self):
        """Test creating MessageStatistics."""
        stats = MessageStatistics(
            word_count=10,
            character_count=50,
            sentence_count=2,
            average_word_length=4.5
        )
        assert stats.word_count == 10
        assert stats.character_count == 50
        assert stats.sentence_count == 2
        assert stats.average_word_length == 4.5


class TestConversationStatistics:
    """Test cases for ConversationStatistics."""

    def test_conversation_statistics_str(self):
        """Test string representation."""
        stats = ConversationStatistics(
            total_messages=10,
            user_messages=5,
            bot_messages=5,
            duration=timedelta(minutes=5),
            average_response_time=None,
            total_words=100,
            total_characters=500,
            average_message_length=50.0,
            longest_message_length=100,
            shortest_message_length=10,
            sentiment_distribution={"Positive": 3, "Negative": 1, "Neutral": 1},
            average_sentiment_score=0.5,
            sentiment_variance=0.1,
            most_positive_message="Great!",
            most_negative_message="Bad",
            messages_per_minute=2.0,
            user_engagement_ratio=0.5
        )
        str_repr = str(stats)
        assert "Total Messages: 10" in str_repr
        assert "User: 5" in str_repr


class TestStatisticsTracker:
    """Test cases for StatisticsTracker."""

    @pytest.fixture
    def tracker(self):
        """Create a StatisticsTracker instance."""
        return StatisticsTracker()

    @pytest.fixture
    def conversation(self):
        """Create a conversation with messages."""
        conv = ConversationManager()
        conv.add_user_message("Hello, how are you?")
        conv.add_bot_message("I'm doing well!")
        conv.add_user_message("That's great!")
        conv.add_bot_message("How can I help?")
        return conv

    @pytest.fixture
    def empty_conversation(self):
        """Create an empty conversation."""
        return ConversationManager()

    def test_record_message(self, tracker):
        """Test recording messages."""
        now = datetime.now()
        tracker.record_message(now, is_user=True)
        assert len(tracker._message_timestamps) == 1

    def test_record_response_time(self, tracker):
        """Test response time calculation."""
        now = datetime.now()
        tracker.record_message(now, is_user=True)
        tracker.record_message(now + timedelta(seconds=2), is_user=False)

        avg_response = tracker.get_average_response_time()
        assert avg_response is not None
        assert avg_response.total_seconds() == 2.0

    def test_no_response_time_without_messages(self, tracker):
        """Test no response time with no messages."""
        assert tracker.get_average_response_time() is None

    def test_calculate_statistics(self, tracker, conversation):
        """Test calculating statistics."""
        stats = tracker.calculate_statistics(conversation)

        assert stats.total_messages == 4
        assert stats.user_messages == 2
        assert stats.bot_messages == 2
        assert stats.total_words > 0

    def test_calculate_statistics_empty(self, tracker, empty_conversation):
        """Test statistics for empty conversation."""
        stats = tracker.calculate_statistics(empty_conversation)

        assert stats.total_messages == 0
        assert stats.user_messages == 0
        assert stats.bot_messages == 0
        assert stats.total_words == 0

    def test_sentiment_distribution(self, tracker, conversation):
        """Test sentiment distribution calculation."""
        stats = tracker.calculate_statistics(conversation)

        assert 'Positive' in stats.sentiment_distribution or \
               'Negative' in stats.sentiment_distribution or \
               'Neutral' in stats.sentiment_distribution

    def test_get_sentiment_trend(self, tracker, conversation):
        """Test sentiment trend calculation."""
        messages = conversation.user_messages
        trend = tracker.get_sentiment_trend(messages, window_size=2)

        # Should return list of rolling averages
        assert isinstance(trend, list)

    def test_reset(self, tracker):
        """Test resetting tracker."""
        now = datetime.now()
        tracker.record_message(now, is_user=True)
        tracker.reset()

        assert len(tracker._message_timestamps) == 0
        assert len(tracker._response_times) == 0


class TestAnalyzeMessage:
    """Test the analyze_message function."""

    def test_analyze_simple_message(self):
        """Test analyzing a simple message."""
        stats = analyze_message("Hello, how are you?")

        assert stats.word_count == 4
        assert stats.character_count == 19
        assert stats.sentence_count >= 1

    def test_analyze_empty_message(self):
        """Test analyzing empty message."""
        stats = analyze_message("")

        assert stats.word_count == 0
        assert stats.character_count == 0

    def test_analyze_multiple_sentences(self):
        """Test analyzing multiple sentences."""
        stats = analyze_message("Hello! How are you? I am fine.")

        assert stats.sentence_count == 3

    def test_average_word_length(self):
        """Test average word length calculation."""
        stats = analyze_message("Hi there")

        # "Hi" = 2, "there" = 5, avg = 3.5
        assert stats.average_word_length == 3.5
