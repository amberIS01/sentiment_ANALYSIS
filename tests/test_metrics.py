"""Tests for metrics module."""

import pytest
from chatbot.metrics import (
    MetricPoint,
    MetricSummary,
    Counter,
    Gauge,
    Histogram,
    Timer,
    MetricsCollector,
    get_metrics,
)


class TestCounter:
    """Tests for Counter."""

    def test_increment(self):
        """Test incrementing."""
        counter = Counter("test")
        counter.increment()
        
        assert counter.value == 1

    def test_decrement(self):
        """Test decrementing."""
        counter = Counter("test")
        counter.increment(5)
        counter.decrement(2)
        
        assert counter.value == 3

    def test_reset(self):
        """Test resetting."""
        counter = Counter("test")
        counter.increment(10)
        counter.reset()
        
        assert counter.value == 0


class TestGauge:
    """Tests for Gauge."""

    def test_set(self):
        """Test setting value."""
        gauge = Gauge("test")
        gauge.set(42.5)
        
        assert gauge.value == 42.5

    def test_increment(self):
        """Test incrementing."""
        gauge = Gauge("test")
        gauge.set(10.0)
        gauge.increment(5.0)
        
        assert gauge.value == 15.0


class TestHistogram:
    """Tests for Histogram."""

    def test_observe(self):
        """Test observing values."""
        hist = Histogram("test")
        hist.observe(1.0)
        hist.observe(2.0)
        hist.observe(3.0)
        
        summary = hist.get_summary()
        
        assert summary.count == 3
        assert summary.total == 6.0
        assert summary.average == 2.0

    def test_min_max(self):
        """Test min/max values."""
        hist = Histogram("test")
        hist.observe(5.0)
        hist.observe(10.0)
        hist.observe(2.0)
        
        summary = hist.get_summary()
        
        assert summary.min_value == 2.0
        assert summary.max_value == 10.0

    def test_empty_histogram(self):
        """Test empty histogram."""
        hist = Histogram("test")
        summary = hist.get_summary()
        
        assert summary.count == 0


class TestMetricsCollector:
    """Tests for MetricsCollector."""

    def test_counter(self):
        """Test getting counter."""
        collector = MetricsCollector()
        counter = collector.counter("requests")
        counter.increment()
        
        assert counter.value == 1

    def test_gauge(self):
        """Test getting gauge."""
        collector = MetricsCollector()
        gauge = collector.gauge("temperature")
        gauge.set(25.5)
        
        assert gauge.value == 25.5

    def test_histogram(self):
        """Test getting histogram."""
        collector = MetricsCollector()
        hist = collector.histogram("latency")
        hist.observe(0.1)
        
        assert hist.get_summary().count == 1

    def test_record(self):
        """Test recording metric."""
        collector = MetricsCollector()
        collector.record("custom", 42.0, {"env": "test"})
        
        assert len(collector._points) == 1

    def test_get_all(self):
        """Test getting all metrics."""
        collector = MetricsCollector()
        collector.counter("c").increment()
        collector.gauge("g").set(1.0)
        
        all_metrics = collector.get_all()
        
        assert "counters" in all_metrics
        assert "gauges" in all_metrics


class TestTimer:
    """Tests for Timer."""

    def test_timer_context(self):
        """Test timer as context manager."""
        hist = Histogram("duration")
        
        with Timer(hist):
            pass  # Do something
        
        assert hist.get_summary().count == 1
