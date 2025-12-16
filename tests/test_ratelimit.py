"""
Tests for the Rate Limit Module.
"""

import pytest
import time

from chatbot.ratelimit import RateLimiter, RateLimitConfig, rate_limited


class TestRateLimiter:
    """Test RateLimiter class."""

    def test_initialization(self):
        limiter = RateLimiter(requests=10, period=1.0)
        assert limiter.requests == 10
        assert limiter.period == 1.0

    def test_acquire_allowed(self):
        limiter = RateLimiter(requests=10, period=1.0)
        assert limiter.acquire() is True

    def test_acquire_rate_limited(self):
        limiter = RateLimiter(requests=2, period=10.0)
        assert limiter.acquire() is True
        assert limiter.acquire() is True
        assert limiter.acquire() is False

    def test_remaining(self):
        limiter = RateLimiter(requests=5, period=10.0)
        assert limiter.remaining() == 5
        limiter.acquire()
        assert limiter.remaining() == 4

    def test_reset_time(self):
        limiter = RateLimiter(requests=5, period=10.0)
        assert limiter.reset_time() is None
        limiter.acquire()
        reset = limiter.reset_time()
        assert reset is not None
        assert reset <= 10.0


class TestRateLimitConfig:
    """Test RateLimitConfig dataclass."""

    def test_creation(self):
        config = RateLimitConfig(requests=100, period_seconds=60.0)
        assert config.requests == 100
        assert config.period_seconds == 60.0


class TestRateLimitedDecorator:
    """Test rate_limited decorator."""

    def test_allows_requests(self):
        @rate_limited(requests=10, period=1.0)
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"

    def test_multiple_calls(self):
        call_count = 0

        @rate_limited(requests=100, period=1.0)
        def test_func():
            nonlocal call_count
            call_count += 1
            return call_count

        for _ in range(5):
            test_func()
        assert call_count == 5
