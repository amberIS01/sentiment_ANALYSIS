"""Tests for context module."""

import pytest
from chatbot.context import (
    ContextType,
    ContextWindow,
    ContextualSentiment,
    ContextAnalyzer,
    ConversationContext,
    analyze_with_context,
)


class TestContextAnalyzer:
    """Tests for ContextAnalyzer."""

    def test_set_context(self):
        """Test setting context."""
        analyzer = ContextAnalyzer()
        analyzer.set_context(ContextType.BUSINESS)
        
        assert analyzer._context_type == ContextType.BUSINESS

    def test_add_to_history(self):
        """Test adding to history."""
        analyzer = ContextAnalyzer(window_size=3)
        analyzer.add_to_history(0.5)
        analyzer.add_to_history(0.6)
        
        assert len(analyzer._history) == 2

    def test_history_limit(self):
        """Test history size limit."""
        analyzer = ContextAnalyzer(window_size=3)
        for i in range(5):
            analyzer.add_to_history(float(i) / 10)
        
        assert len(analyzer._history) == 3

    def test_get_context_average(self):
        """Test getting context average."""
        analyzer = ContextAnalyzer()
        analyzer.add_to_history(0.4)
        analyzer.add_to_history(0.6)
        
        avg = analyzer.get_context_average()
        assert avg == pytest.approx(0.5)

    def test_analyze(self):
        """Test analyzing with context."""
        analyzer = ContextAnalyzer()
        analyzer.add_to_history(0.5)
        
        result = analyzer.analyze("Test", 0.7)
        
        assert isinstance(result, ContextualSentiment)
        assert result.raw_score == 0.7

    def test_reset(self):
        """Test resetting context."""
        analyzer = ContextAnalyzer()
        analyzer.add_to_history(0.5)
        analyzer.reset()
        
        assert len(analyzer._history) == 0

    def test_get_trend_improving(self):
        """Test improving trend."""
        analyzer = ContextAnalyzer()
        for score in [0.1, 0.2, 0.3, 0.7, 0.8, 0.9]:
            analyzer.add_to_history(score)
        
        trend = analyzer.get_trend()
        assert trend == "improving"

    def test_get_trend_declining(self):
        """Test declining trend."""
        analyzer = ContextAnalyzer()
        for score in [0.9, 0.8, 0.7, 0.3, 0.2, 0.1]:
            analyzer.add_to_history(score)
        
        trend = analyzer.get_trend()
        assert trend == "declining"


class TestConversationContext:
    """Tests for ConversationContext."""

    def test_add_message(self):
        """Test adding message."""
        ctx = ConversationContext()
        ctx.add_message("Hello", 0.5, "greeting")
        
        assert len(ctx.messages) == 1
        assert len(ctx.sentiments) == 1

    def test_get_summary(self):
        """Test getting summary."""
        ctx = ConversationContext()
        ctx.add_message("Hi", 0.5, "greeting")
        ctx.add_message("Bye", 0.3, "farewell")
        
        summary = ctx.get_summary()
        
        assert summary["message_count"] == 2
        assert summary["avg_sentiment"] == pytest.approx(0.4)


class TestAnalyzeWithContext:
    """Tests for analyze_with_context function."""

    def test_analyze(self):
        """Test analyzing with history."""
        history = [0.5, 0.6, 0.7]
        result = analyze_with_context("Test", 0.8, history)
        
        assert isinstance(result, float)
