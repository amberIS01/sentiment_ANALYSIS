"""
Tests for the History Module.
"""

import pytest

from chatbot.history import SentimentHistory, SentimentPoint


class TestSentimentPoint:
    """Test SentimentPoint dataclass."""

    def test_creation(self):
        from datetime import datetime
        point = SentimentPoint(
            timestamp=datetime.now(),
            score=0.5,
            label="positive",
        )
        assert point.score == 0.5
        assert point.label == "positive"

    def test_with_text(self):
        from datetime import datetime
        point = SentimentPoint(
            timestamp=datetime.now(),
            score=0.5,
            label="positive",
            text="Hello world",
        )
        assert point.text == "Hello world"


class TestSentimentHistory:
    """Test SentimentHistory class."""

    def test_initialization(self):
        history = SentimentHistory()
        assert len(history) == 0

    def test_add_point(self):
        history = SentimentHistory()
        point = history.add(0.5, "positive", "test")
        assert len(history) == 1
        assert point.score == 0.5

    def test_get_recent(self):
        history = SentimentHistory()
        for i in range(10):
            history.add(i * 0.1, "neutral")
        recent = history.get_recent(5)
        assert len(recent) == 5

    def test_get_all(self):
        history = SentimentHistory()
        history.add(0.5, "positive")
        history.add(-0.5, "negative")
        all_points = history.get_all()
        assert len(all_points) == 2

    def test_average_score(self):
        history = SentimentHistory()
        history.add(0.5, "positive")
        history.add(0.3, "positive")
        avg = history.average_score()
        assert avg == 0.4

    def test_average_score_empty(self):
        history = SentimentHistory()
        assert history.average_score() == 0.0

    def test_trend_stable(self):
        history = SentimentHistory()
        for _ in range(5):
            history.add(0.5, "positive")
        assert history.trend() == "stable"

    def test_trend_improving(self):
        history = SentimentHistory()
        history.add(-0.5, "negative")
        history.add(-0.3, "negative")
        history.add(0.0, "neutral")
        history.add(0.3, "positive")
        history.add(0.5, "positive")
        assert history.trend() == "improving"

    def test_label_counts(self):
        history = SentimentHistory()
        history.add(0.5, "positive")
        history.add(0.6, "positive")
        history.add(-0.5, "negative")
        counts = history.label_counts()
        assert counts["positive"] == 2
        assert counts["negative"] == 1

    def test_clear(self):
        history = SentimentHistory()
        history.add(0.5, "positive")
        history.clear()
        assert len(history) == 0

    def test_max_size(self):
        history = SentimentHistory(max_size=5)
        for i in range(10):
            history.add(i * 0.1, "neutral")
        assert len(history) == 5

    def test_to_dict(self):
        history = SentimentHistory()
        history.add(0.5, "positive")
        data = history.to_dict()
        assert "points" in data
        assert "average" in data
        assert "trend" in data
