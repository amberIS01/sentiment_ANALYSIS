"""
Tests for the Chatbot Module.
"""

import pytest
from chatbot.bot import Chatbot
from chatbot.conversation import ConversationManager
from chatbot.sentiment import SentimentLabel


class TestChatbot:
    """Test suite for Chatbot."""

    @pytest.fixture
    def bot(self):
        """Create a Chatbot instance for testing."""
        return Chatbot()

    def test_chatbot_initialization(self, bot):
        """Test that chatbot initializes with empty conversation."""
        assert bot.conversation.is_empty

    def test_chatbot_with_custom_conversation_manager(self):
        """Test chatbot with custom conversation manager."""
        manager = ConversationManager()
        bot = Chatbot(conversation_manager=manager)
        assert bot.conversation is manager

    def test_process_message_returns_tuple(self, bot):
        """Test that process_message returns response and sentiment."""
        response, sentiment = bot.process_message("Hello!")
        assert isinstance(response, str)
        assert sentiment is not None

    def test_process_message_adds_to_conversation(self, bot):
        """Test that process_message adds messages to conversation."""
        bot.process_message("Hello!")
        assert bot.conversation.message_count == 2  # User + Bot

    def test_chat_returns_string(self, bot):
        """Test that chat method returns just the response string."""
        response = bot.chat("Hello!")
        assert isinstance(response, str)
        assert len(response) > 0

    def test_positive_message_response(self, bot):
        """Test response to positive message."""
        response, sentiment = bot.process_message("I love this service!")
        assert sentiment.label == SentimentLabel.POSITIVE
        assert len(response) > 0

    def test_negative_message_response(self, bot):
        """Test response to negative message."""
        response, sentiment = bot.process_message("This is terrible!")
        assert sentiment.label == SentimentLabel.NEGATIVE
        assert len(response) > 0

    def test_neutral_message_response(self, bot):
        """Test response to neutral message."""
        response, sentiment = bot.process_message("The time is 3pm.")
        assert sentiment.label == SentimentLabel.NEUTRAL
        assert len(response) > 0

    def test_keyword_response_hello(self, bot):
        """Test keyword-based response for 'hello'."""
        response = bot.chat("Hello there!")
        assert "Hello" in response or "Hi" in response

    def test_keyword_response_bye(self, bot):
        """Test keyword-based response for 'bye'."""
        response = bot.chat("Goodbye!")
        assert any(word in response.lower() for word in ["bye", "goodbye", "take care"])

    def test_keyword_response_thanks(self, bot):
        """Test keyword-based response for 'thanks'."""
        response = bot.chat("Thank you so much!")
        assert "welcome" in response.lower() or "help" in response.lower()

    def test_get_conversation_summary(self, bot):
        """Test getting conversation summary."""
        bot.chat("I love this!")
        bot.chat("Everything is great!")

        summary = bot.get_conversation_summary()
        assert summary.overall_sentiment == SentimentLabel.POSITIVE
        assert len(summary.message_sentiments) == 2

    def test_get_formatted_summary(self, bot):
        """Test getting formatted summary string."""
        bot.chat("Hello!")
        bot.chat("I'm happy today!")

        formatted = bot.get_formatted_summary()
        assert "CONVERSATION SUMMARY" in formatted
        assert "Sentiment Statistics" in formatted
        assert "FINAL OUTPUT" in formatted

    def test_reset(self, bot):
        """Test resetting the chatbot."""
        bot.chat("Hello!")
        bot.chat("How are you?")
        assert not bot.conversation.is_empty

        bot.reset()
        assert bot.conversation.is_empty

    def test_conversation_history_maintained(self, bot):
        """Test that conversation history is maintained across messages."""
        bot.chat("First message")
        bot.chat("Second message")
        bot.chat("Third message")

        assert bot.conversation.message_count == 6  # 3 user + 3 bot

    def test_sentiment_tracking_tier2(self, bot):
        """Test Tier 2 per-message sentiment tracking."""
        messages = [
            "Your service disappoints me",
            "Last experience was better",
            "I hope things improve"
        ]

        for msg in messages:
            bot.process_message(msg)

        summary = bot.get_conversation_summary()

        # Verify each message has sentiment
        assert len(summary.message_sentiments) == 3

        # Check that sentiments were tracked
        for msg, sentiment in summary.message_sentiments:
            assert sentiment is not None
            assert sentiment.label in [SentimentLabel.POSITIVE, SentimentLabel.NEGATIVE, SentimentLabel.NEUTRAL]

    def test_mood_trend_analysis_tier2(self, bot):
        """Test Tier 2 mood trend analysis."""
        # Simulate improving mood
        bot.chat("This is terrible!")
        bot.chat("It's getting a bit better")
        bot.chat("Actually this is quite good!")
        bot.chat("I'm really happy now!")

        summary = bot.get_conversation_summary()
        assert summary.mood_trend is not None
        assert len(summary.mood_trend) > 0


class TestChatbotEdgeCases:
    """Test edge cases for Chatbot."""

    @pytest.fixture
    def bot(self):
        """Create a Chatbot instance for testing."""
        return Chatbot()

    def test_empty_message(self, bot):
        """Test handling of empty message."""
        response, sentiment = bot.process_message("")
        assert isinstance(response, str)

    def test_very_long_message(self, bot):
        """Test handling of very long message."""
        long_message = "I am happy! " * 100
        response, sentiment = bot.process_message(long_message)
        assert sentiment.label == SentimentLabel.POSITIVE

    def test_special_characters(self, bot):
        """Test handling of special characters."""
        response, sentiment = bot.process_message("Hello!!! @#$%^&*()")
        assert isinstance(response, str)

    def test_unicode_characters(self, bot):
        """Test handling of unicode characters."""
        response, sentiment = bot.process_message("Hello! 你好!")
        assert isinstance(response, str)

    def test_emoticons(self, bot):
        """Test handling of emoticons."""
        response, sentiment = bot.process_message("I'm so happy :) :D")
        # VADER should recognize emoticons as positive
        assert sentiment.label == SentimentLabel.POSITIVE

    def test_multiple_resets(self, bot):
        """Test multiple reset calls."""
        bot.chat("Hello")
        bot.reset()
        bot.reset()  # Should not fail
        assert bot.conversation.is_empty
