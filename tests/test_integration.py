"""
Integration Tests

End-to-end tests for the chatbot system.
"""

import pytest
import tempfile
import os

from chatbot import (
    SentimentAnalyzer,
    ConversationManager,
    Chatbot,
    EmotionDetector,
    StatisticsTracker,
)
from chatbot.session import SessionManager
from chatbot.persistence import ConversationStore
from chatbot.cache import SentimentCache
from chatbot.history import SentimentHistory


class TestChatbotIntegration:
    """Integration tests for full chatbot workflow."""

    def test_full_conversation_flow(self):
        """Test complete conversation with sentiment analysis."""
        chatbot = Chatbot()

        response1 = chatbot.process_message("Hello, how are you?")
        assert response1 is not None

        response2 = chatbot.process_message("I'm having a great day!")
        assert response2 is not None

        response3 = chatbot.process_message("Goodbye!")
        assert response3 is not None

    def test_sentiment_with_emotions(self):
        """Test sentiment analysis with emotion detection."""
        analyzer = SentimentAnalyzer()
        detector = EmotionDetector()

        text = "I am so happy and excited about this!"
        sentiment = analyzer.analyze(text)
        emotions = detector.detect(text)

        assert sentiment.label.value in ["positive", "negative", "neutral"]
        assert len(emotions.emotions) > 0

    def test_conversation_persistence(self):
        """Test saving and loading conversations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)

            # Create and save conversation
            conversation_data = {
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "bot", "content": "Hi there!"},
                ]
            }
            store.save("test-conv", conversation_data)

            # Load and verify
            loaded = store.load("test-conv")
            assert loaded == conversation_data

    def test_session_with_conversation(self):
        """Test session management with conversation."""
        session_manager = SessionManager()
        session = session_manager.create_session()

        # Store conversation in session
        session.data["conversation_id"] = "conv-123"
        session.data["message_count"] = 5

        # Retrieve session
        retrieved = session_manager.get_session(session.session_id)
        assert retrieved is not None
        assert retrieved.data["conversation_id"] == "conv-123"

    def test_sentiment_caching(self):
        """Test sentiment result caching."""
        cache = SentimentCache()
        analyzer = SentimentAnalyzer()

        text = "This is a test message"
        result = analyzer.analyze(text)

        # Cache the result
        cache.set(text, result)

        # Retrieve from cache
        cached = cache.get(text)
        assert cached is not None

    def test_sentiment_history_tracking(self):
        """Test tracking sentiment over time."""
        history = SentimentHistory()
        analyzer = SentimentAnalyzer()

        messages = [
            "I'm so happy!",
            "This is frustrating",
            "Everything is okay",
        ]

        for msg in messages:
            result = analyzer.analyze(msg)
            history.add(result.compound, result.label.value, msg)

        assert len(history) == 3
        assert history.trend() in ["improving", "declining", "stable"]

    def test_statistics_collection(self):
        """Test statistics tracking."""
        stats = StatisticsTracker()

        # Record some data
        stats.record_message("user", 10)
        stats.record_message("bot", 15)
        stats.record_sentiment(0.8)
        stats.record_sentiment(-0.2)

        summary = stats.get_summary()
        assert summary.total_messages >= 2
