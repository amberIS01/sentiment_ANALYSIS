"""Tests for history module."""

import pytest
from datetime import datetime, timedelta
from chatbot.history import (
    HistoryEntry,
    HistoryStats,
    SentimentHistory,
    track_sentiment,
    get_trend,
)


class TestSentimentHistory:
    """Tests for SentimentHistory."""

    def test_add_entry(self):
        """Test adding entry."""
        history = SentimentHistory()
        entry = history.add("Hello", 0.5)
        
        assert entry.text == "Hello"
        assert entry.score == 0.5
        assert len(history) == 1

    def test_max_size(self):
        """Test max size limit."""
        history = SentimentHistory(max_size=3)
        for i in range(5):
            history.add(f"text{i}", 0.5)
        
        assert len(history) == 3

    def test_get_recent(self):
        """Test getting recent entries."""
        history = SentimentHistory()
        for i in range(10):
            history.add(f"text{i}", float(i) / 10)
        
        recent = history.get_recent(3)
        
        assert len(recent) == 3

    def test_get_stats(self):
        """Test getting statistics."""
        history = SentimentHistory()
        history.add("a", 0.3)
        history.add("b", 0.5)
        history.add("c", 0.7)
        
        stats = history.get_stats()
        
        assert stats.count == 3
        assert stats.avg_score == pytest.approx(0.5)
        assert stats.min_score == 0.3
        assert stats.max_score == 0.7

    def test_empty_stats(self):
        """Test stats on empty history."""
        history = SentimentHistory()
        stats = history.get_stats()
        
        assert stats.count == 0
        assert stats.avg_score == 0.0

    def test_trend_improving(self):
        """Test improving trend."""
        history = SentimentHistory()
        for score in [0.1, 0.2, 0.3, 0.7, 0.8, 0.9]:
            history.add("t", score)
        
        stats = history.get_stats()
        assert stats.trend == "improving"

    def test_trend_declining(self):
        """Test declining trend."""
        history = SentimentHistory()
        for score in [0.9, 0.8, 0.7, 0.3, 0.2, 0.1]:
            history.add("t", score)
        
        stats = history.get_stats()
        assert stats.trend == "declining"

    def test_clear(self):
        """Test clearing history."""
        history = SentimentHistory()
        history.add("test", 0.5)
        history.clear()
        
        assert len(history) == 0

    def test_export(self):
        """Test exporting history."""
        history = SentimentHistory()
        history.add("test", 0.5)
        
        exported = history.export()
        
        assert len(exported) == 1
        assert exported[0]["text"] == "test"


class TestTrackSentiment:
    """Tests for track_sentiment function."""

    def test_track(self):
        """Test tracking sentiment."""
        history = SentimentHistory()
        entry = track_sentiment(history, "Hello", 0.8)
        
        assert entry.score == 0.8


class TestGetTrend:
    """Tests for get_trend function."""

    def test_get_trend(self):
        """Test getting trend."""
        history = SentimentHistory()
        for score in [0.5, 0.5, 0.5, 0.5]:
            history.add("t", score)
        
        trend = get_trend(history)
        assert trend == "stable"
