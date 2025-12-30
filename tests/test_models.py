"""Tests for models module."""

import pytest
from datetime import datetime
from chatbot.models import (
    TextDocument,
    AnalysisRequest,
    AnalysisResult,
    Conversation,
    UserProfile,
)


class TestTextDocument:
    """Tests for TextDocument."""

    def test_create(self):
        """Test creating document."""
        doc = TextDocument(
            id="doc1",
            content="Hello world",
            source="user",
        )
        
        assert doc.id == "doc1"
        assert doc.content == "Hello world"

    def test_metadata(self):
        """Test document metadata."""
        doc = TextDocument(
            id="doc1",
            content="Test",
            metadata={"key": "value"},
        )
        
        assert doc.metadata["key"] == "value"


class TestAnalysisRequest:
    """Tests for AnalysisRequest."""

    def test_create(self):
        """Test creating request."""
        request = AnalysisRequest(
            text="Analyze this",
            options={"detailed": True},
        )
        
        assert request.text == "Analyze this"

    def test_default_options(self):
        """Test default options."""
        request = AnalysisRequest(text="Test")
        
        assert request.options == {}


class TestAnalysisResult:
    """Tests for AnalysisResult."""

    def test_create(self):
        """Test creating result."""
        result = AnalysisResult(
            score=0.75,
            label="positive",
            confidence=0.9,
        )
        
        assert result.score == 0.75
        assert result.label == "positive"

    def test_extras(self):
        """Test extra fields."""
        result = AnalysisResult(
            score=0.5,
            label="neutral",
            extras={"emotion": "calm"},
        )
        
        assert result.extras["emotion"] == "calm"


class TestConversation:
    """Tests for Conversation."""

    def test_create(self):
        """Test creating conversation."""
        conv = Conversation(id="conv1")
        
        assert conv.id == "conv1"
        assert len(conv.messages) == 0

    def test_add_message(self):
        """Test adding message."""
        conv = Conversation(id="conv1")
        conv.add_message("user", "Hello")
        
        assert len(conv.messages) == 1

    def test_get_messages(self):
        """Test getting messages."""
        conv = Conversation(id="conv1")
        conv.add_message("user", "Hi")
        conv.add_message("bot", "Hello")
        
        messages = conv.get_messages()
        assert len(messages) == 2


class TestUserProfile:
    """Tests for UserProfile."""

    def test_create(self):
        """Test creating profile."""
        profile = UserProfile(
            user_id="user1",
            name="Test User",
        )
        
        assert profile.user_id == "user1"

    def test_preferences(self):
        """Test user preferences."""
        profile = UserProfile(
            user_id="user1",
            preferences={"theme": "dark"},
        )
        
        assert profile.preferences["theme"] == "dark"

    def test_sentiment_history(self):
        """Test sentiment history."""
        profile = UserProfile(user_id="user1")
        profile.add_sentiment(0.5)
        profile.add_sentiment(0.7)
        
        assert len(profile.sentiment_history) == 2
        assert profile.avg_sentiment == pytest.approx(0.6)
