"""
Tests for the Conversation Manager Module.
"""

import pytest
from chatbot.conversation import (
    ConversationManager,
    Message,
    MessageRole
)
from chatbot.sentiment import SentimentLabel


class TestMessage:
    """Test suite for Message dataclass."""

    def test_message_creation_user(self):
        """Test creating a user message."""
        msg = Message(role=MessageRole.USER, content="Hello")
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello"
        assert msg.timestamp is not None

    def test_message_creation_bot(self):
        """Test creating a bot message."""
        msg = Message(role=MessageRole.BOT, content="Hi there!")
        assert msg.role == MessageRole.BOT
        assert msg.content == "Hi there!"

    def test_message_str_user(self):
        """Test user message string representation."""
        msg = Message(role=MessageRole.USER, content="Test message")
        assert 'User' in str(msg)
        assert 'Test message' in str(msg)

    def test_message_str_bot(self):
        """Test bot message string representation."""
        msg = Message(role=MessageRole.BOT, content="Bot response")
        assert 'Chatbot' in str(msg)
        assert 'Bot response' in str(msg)


class TestConversationManager:
    """Test suite for ConversationManager."""

    @pytest.fixture
    def manager(self):
        """Create a ConversationManager instance for testing."""
        return ConversationManager()

    def test_initial_state(self, manager):
        """Test that a new conversation manager is empty."""
        assert manager.is_empty
        assert manager.message_count == 0
        assert len(manager.messages) == 0

    def test_add_user_message(self, manager):
        """Test adding a user message."""
        msg = manager.add_user_message("Hello!")
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello!"
        assert manager.message_count == 1
        assert not manager.is_empty

    def test_add_user_message_with_sentiment(self, manager):
        """Test that user messages get sentiment analysis."""
        msg = manager.add_user_message("I love this!")
        assert msg.sentiment is not None
        assert msg.sentiment.label == SentimentLabel.POSITIVE

    def test_add_user_message_without_sentiment(self, manager):
        """Test adding user message without sentiment analysis."""
        msg = manager.add_user_message("Hello!", analyze=False)
        assert msg.sentiment is None

    def test_add_bot_message(self, manager):
        """Test adding a bot message."""
        msg = manager.add_bot_message("How can I help?")
        assert msg.role == MessageRole.BOT
        assert msg.content == "How can I help?"
        assert msg.sentiment is None  # Bot messages shouldn't be analyzed

    def test_user_messages_property(self, manager):
        """Test getting only user messages."""
        manager.add_user_message("User message 1")
        manager.add_bot_message("Bot response")
        manager.add_user_message("User message 2")

        user_msgs = manager.user_messages
        assert len(user_msgs) == 2
        assert all(m.role == MessageRole.USER for m in user_msgs)

    def test_bot_messages_property(self, manager):
        """Test getting only bot messages."""
        manager.add_user_message("User message")
        manager.add_bot_message("Bot response 1")
        manager.add_bot_message("Bot response 2")

        bot_msgs = manager.bot_messages
        assert len(bot_msgs) == 2
        assert all(m.role == MessageRole.BOT for m in bot_msgs)

    def test_get_conversation_history(self, manager):
        """Test getting conversation history as list of dicts."""
        manager.add_user_message("Hello")
        manager.add_bot_message("Hi there!")

        history = manager.get_conversation_history()
        assert len(history) == 2
        assert history[0] == {"role": "user", "content": "Hello"}
        assert history[1] == {"role": "bot", "content": "Hi there!"}

    def test_analyze_conversation(self, manager):
        """Test analyzing the entire conversation."""
        manager.add_user_message("I love this service!")
        manager.add_user_message("Everything is great!")

        summary = manager.analyze_conversation()
        assert summary.overall_sentiment == SentimentLabel.POSITIVE
        assert len(summary.message_sentiments) == 2

    def test_get_formatted_history(self, manager):
        """Test getting formatted conversation history."""
        manager.add_user_message("Hello")
        manager.add_bot_message("Hi there!")

        formatted = manager.get_formatted_history()
        assert "User:" in formatted
        assert "Chatbot:" in formatted
        assert "Hello" in formatted
        assert "Hi there!" in formatted

    def test_clear(self, manager):
        """Test clearing the conversation."""
        manager.add_user_message("Hello")
        manager.add_bot_message("Hi")
        assert manager.message_count == 2

        manager.clear()
        assert manager.is_empty
        assert manager.message_count == 0

    def test_get_last_user_message(self, manager):
        """Test getting the last user message."""
        manager.add_user_message("First")
        manager.add_bot_message("Response")
        manager.add_user_message("Last user message")

        last = manager.get_last_user_message()
        assert last is not None
        assert last.content == "Last user message"

    def test_get_last_user_message_empty(self, manager):
        """Test getting last user message when none exist."""
        assert manager.get_last_user_message() is None

    def test_get_last_bot_message(self, manager):
        """Test getting the last bot message."""
        manager.add_user_message("User")
        manager.add_bot_message("First bot")
        manager.add_bot_message("Last bot message")

        last = manager.get_last_bot_message()
        assert last is not None
        assert last.content == "Last bot message"

    def test_get_last_bot_message_empty(self, manager):
        """Test getting last bot message when none exist."""
        assert manager.get_last_bot_message() is None

    def test_messages_returns_copy(self, manager):
        """Test that messages property returns a copy."""
        manager.add_user_message("Test")
        messages = manager.messages
        messages.clear()  # Modify the returned list
        assert manager.message_count == 1  # Original should be unchanged


class TestMessageRole:
    """Test suite for MessageRole enum."""

    def test_message_roles_exist(self):
        """Test that all expected message roles exist."""
        assert MessageRole.USER.value == "user"
        assert MessageRole.BOT.value == "bot"
