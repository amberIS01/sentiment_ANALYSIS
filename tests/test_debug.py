"""
Tests for the Debug Module.
"""

import pytest
import time

from chatbot.debug import (
    Profiler,
    timed,
    timer,
    log_call,
    get_profiler,
    debug_repr,
    DebugContext,
)


class TestProfiler:
    """Test Profiler class."""

    def test_initialization(self):
        profiler = Profiler()
        assert profiler is not None

    def test_record(self):
        profiler = Profiler()
        profiler.record("test_func", 0.1)
        profiler.record("test_func", 0.2)
        stats = profiler.get_stats("test_func")
        assert stats["count"] == 2

    def test_get_stats_empty(self):
        profiler = Profiler()
        stats = profiler.get_stats("nonexistent")
        assert stats["count"] == 0

    def test_report(self):
        profiler = Profiler()
        profiler.record("func1", 0.1)
        profiler.record("func2", 0.2)
        report = profiler.report()
        assert "func1" in report
        assert "func2" in report

    def test_clear(self):
        profiler = Profiler()
        profiler.record("test", 0.1)
        profiler.clear()
        stats = profiler.get_stats("test")
        assert stats["count"] == 0


class TestTimedDecorator:
    """Test timed decorator."""

    def test_times_function(self):
        profiler = get_profiler()
        profiler.clear()

        @timed
        def slow_func():
            time.sleep(0.01)
            return "done"

        result = slow_func()
        assert result == "done"

    def test_preserves_return(self):
        @timed
        def returns_value():
            return 42

        assert returns_value() == 42


class TestTimerContext:
    """Test timer context manager."""

    def test_times_block(self):
        with timer("test_operation"):
            time.sleep(0.01)
        # No assertion needed, just verify it doesn't raise


class TestLogCall:
    """Test log_call decorator."""

    def test_logs_and_returns(self):
        @log_call
        def my_func(x):
            return x * 2

        result = my_func(5)
        assert result == 10


class TestDebugRepr:
    """Test debug_repr function."""

    def test_short_string(self):
        result = debug_repr("hello")
        assert result == "'hello'"

    def test_truncates_long(self):
        long_str = "x" * 200
        result = debug_repr(long_str, max_length=50)
        assert len(result) <= 53  # 50 + "..."


class TestDebugContext:
    """Test DebugContext class."""

    def test_enabled(self):
        with DebugContext("test", enabled=True) as ctx:
            assert ctx.name == "test"

    def test_disabled(self):
        with DebugContext("test", enabled=False) as ctx:
            assert ctx.start_time is None


class TestGetProfiler:
    """Test get_profiler function."""

    def test_returns_profiler(self):
        profiler = get_profiler()
        assert isinstance(profiler, Profiler)

    def test_same_instance(self):
        p1 = get_profiler()
        p2 = get_profiler()
        assert p1 is p2
