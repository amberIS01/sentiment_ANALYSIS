"""
Tests for the Trends Module.
"""

import pytest
from datetime import datetime, timedelta

from chatbot.trends import TrendAnalyzer, TrendDirection, TrendPoint, TrendAnalysis


class TestTrendPoint:
    """Test TrendPoint dataclass."""

    def test_creation(self):
        point = TrendPoint(
            timestamp=datetime.now(),
            value=0.5,
            label="positive",
        )
        assert point.value == 0.5
        assert point.label == "positive"


class TestTrendDirection:
    """Test TrendDirection enum."""

    def test_values(self):
        assert TrendDirection.RISING.value == "rising"
        assert TrendDirection.FALLING.value == "falling"
        assert TrendDirection.STABLE.value == "stable"
        assert TrendDirection.VOLATILE.value == "volatile"


class TestTrendAnalyzer:
    """Test TrendAnalyzer class."""

    def test_initialization(self):
        analyzer = TrendAnalyzer()
        assert analyzer.sensitivity == 0.1

    def test_custom_sensitivity(self):
        analyzer = TrendAnalyzer(sensitivity=0.2)
        assert analyzer.sensitivity == 0.2

    def test_add_point(self):
        analyzer = TrendAnalyzer()
        analyzer.add_point(0.5, "positive")
        assert len(analyzer._points) == 1

    def test_analyze_insufficient_data(self):
        analyzer = TrendAnalyzer()
        analyzer.add_point(0.5, "positive")
        result = analyzer.analyze()
        assert result is None

    def test_analyze_stable(self):
        analyzer = TrendAnalyzer()
        for _ in range(5):
            analyzer.add_point(0.5, "positive")
        result = analyzer.analyze()
        assert result.direction == TrendDirection.STABLE

    def test_analyze_rising(self):
        analyzer = TrendAnalyzer()
        values = [0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
        for v in values:
            analyzer.add_point(v, "positive")
        result = analyzer.analyze()
        assert result.direction == TrendDirection.RISING

    def test_analyze_falling(self):
        analyzer = TrendAnalyzer()
        values = [0.9, 0.7, 0.5, 0.3, 0.2, 0.1]
        for v in values:
            analyzer.add_point(v, "positive")
        result = analyzer.analyze()
        assert result.direction == TrendDirection.FALLING

    def test_get_recent(self):
        analyzer = TrendAnalyzer()
        for i in range(10):
            analyzer.add_point(i * 0.1, "neutral")
        recent = analyzer.get_recent(5)
        assert len(recent) == 5

    def test_moving_average(self):
        analyzer = TrendAnalyzer()
        for i in range(10):
            analyzer.add_point(float(i), "neutral")
        ma = analyzer.moving_average(window=3)
        assert len(ma) == 8

    def test_clear(self):
        analyzer = TrendAnalyzer()
        analyzer.add_point(0.5, "positive")
        analyzer.clear()
        assert len(analyzer._points) == 0

    def test_to_dict(self):
        analyzer = TrendAnalyzer()
        analyzer.add_point(0.5, "positive")
        analyzer.add_point(0.6, "positive")
        result = analyzer.to_dict()
        assert "points" in result
        assert "analysis" in result


class TestTrendAnalysis:
    """Test TrendAnalysis dataclass."""

    def test_creation(self):
        analysis = TrendAnalysis(
            direction=TrendDirection.STABLE,
            change=0.0,
            volatility=0.1,
            average=0.5,
            min_value=0.3,
            max_value=0.7,
            data_points=10,
        )
        assert analysis.direction == TrendDirection.STABLE
        assert analysis.data_points == 10
