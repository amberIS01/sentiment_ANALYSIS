"""Tests for feedback module."""

import pytest
from chatbot.feedback import (
    FeedbackType,
    FeedbackCategory,
    FeedbackEntry,
    FeedbackCollector,
    collect_feedback,
)


class TestFeedbackCollector:
    """Tests for FeedbackCollector."""

    def test_add_feedback(self):
        """Test adding feedback."""
        collector = FeedbackCollector()
        entry = collector.add_feedback(
            text="Great product",
            predicted_value=0.8,
            feedback_type=FeedbackType.CORRECT,
            category=FeedbackCategory.SENTIMENT,
        )
        assert entry.id == "fb_1"
        assert entry.text == "Great product"

    def test_mark_correct(self):
        """Test marking as correct."""
        collector = FeedbackCollector()
        entry = collector.mark_correct("Good", 0.5)
        assert entry.feedback_type == FeedbackType.CORRECT

    def test_mark_incorrect(self):
        """Test marking as incorrect."""
        collector = FeedbackCollector()
        entry = collector.mark_incorrect("Bad", -0.5, 0.5)
        assert entry.feedback_type == FeedbackType.INCORRECT
        assert entry.correct_value == 0.5

    def test_get_entries(self):
        """Test getting entries."""
        collector = FeedbackCollector()
        collector.mark_correct("A", 0.5)
        collector.mark_incorrect("B", -0.5, 0.5)
        
        entries = collector.get_entries()
        assert len(entries) == 2

    def test_filter_by_type(self):
        """Test filtering by type."""
        collector = FeedbackCollector()
        collector.mark_correct("A", 0.5)
        collector.mark_incorrect("B", -0.5, 0.5)
        
        correct = collector.get_entries(feedback_type=FeedbackType.CORRECT)
        assert len(correct) == 1

    def test_get_stats(self):
        """Test getting statistics."""
        collector = FeedbackCollector()
        collector.mark_correct("A", 0.5)
        collector.mark_correct("B", 0.6)
        collector.mark_incorrect("C", -0.5, 0.5)
        
        stats = collector.get_stats()
        assert stats.total_entries == 3
        assert stats.correct_count == 2
        assert stats.accuracy_rate == pytest.approx(0.666, rel=0.01)

    def test_callback(self):
        """Test feedback callback."""
        collector = FeedbackCollector()
        results = []
        collector.on_feedback(lambda e: results.append(e))
        
        collector.mark_correct("Test", 0.5)
        assert len(results) == 1

    def test_export(self):
        """Test export."""
        collector = FeedbackCollector()
        collector.mark_correct("Test", 0.5)
        
        exported = collector.export()
        assert len(exported) == 1
        assert exported[0]["text"] == "Test"

    def test_clear(self):
        """Test clear."""
        collector = FeedbackCollector()
        collector.mark_correct("Test", 0.5)
        collector.clear()
        
        assert len(collector.get_entries()) == 0
