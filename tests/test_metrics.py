"""
Tests for the Metrics Module.
"""

import pytest
import time

from chatbot.metrics import MetricsCollector, Timer


class TestTimer:
    """Test Timer class."""

    def test_context_manager(self):
        with Timer() as t:
            time.sleep(0.01)
        assert t.elapsed > 0

    def test_elapsed_property(self):
        timer = Timer()
        timer.start()
        time.sleep(0.01)
        timer.stop()
        assert timer.elapsed >= 0.01


class TestMetricsCollector:
    """Test MetricsCollector class."""

    def test_initialization(self):
        collector = MetricsCollector()
        assert collector is not None

    def test_increment(self):
        collector = MetricsCollector()
        collector.increment("requests")
        collector.increment("requests")
        assert collector.get("requests") == 2

    def test_record_value(self):
        collector = MetricsCollector()
        collector.record("response_time", 0.5)
        collector.record("response_time", 1.0)
        stats = collector.get_stats("response_time")
        assert stats["count"] == 2

    def test_get_all(self):
        collector = MetricsCollector()
        collector.increment("a")
        collector.increment("b")
        all_metrics = collector.get_all()
        assert "a" in all_metrics
        assert "b" in all_metrics

    def test_reset(self):
        collector = MetricsCollector()
        collector.increment("test")
        collector.reset()
        assert collector.get("test") == 0

    def test_average(self):
        collector = MetricsCollector()
        collector.record("time", 1.0)
        collector.record("time", 2.0)
        collector.record("time", 3.0)
        stats = collector.get_stats("time")
        assert stats["average"] == 2.0
