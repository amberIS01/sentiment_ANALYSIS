"""
Pytest configuration and shared fixtures.
"""

import pytest
from chatbot import Chatbot, ConversationManager, SentimentAnalyzer


@pytest.fixture
def analyzer():
    """Create a SentimentAnalyzer instance."""
    return SentimentAnalyzer()


@pytest.fixture
def conversation():
    """Create a ConversationManager instance."""
    return ConversationManager()


@pytest.fixture
def chatbot():
    """Create a Chatbot instance."""
    return Chatbot()


@pytest.fixture
def conversation_with_messages():
    """Create a ConversationManager with sample messages."""
    conv = ConversationManager()
    conv.add_user_message("Hello, how are you?")
    conv.add_bot_message("I'm doing well, thank you!")
    conv.add_user_message("That's great to hear!")
    conv.add_bot_message("How can I help you today?")
    return conv


@pytest.fixture
def sample_messages():
    """Sample messages for testing."""
    return [
        "I am very happy today!",
        "This is frustrating.",
        "The weather is nice.",
        "I love this product!",
        "I'm disappointed with the service.",
    ]
