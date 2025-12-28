"""Tests for retry module."""

import pytest
from chatbot.retry import (
    BackoffStrategy,
    RetryConfig,
    RetryResult,
    RetryError,
    Retrier,
    retry,
    with_retry,
)


class TestRetrier:
    """Tests for Retrier."""

    def test_success_first_try(self):
        """Test success on first try."""
        retrier = Retrier()
        result = retrier.execute(lambda: "success")
        
        assert result.success is True
        assert result.value == "success"
        assert result.attempts == 1

    def test_retry_on_failure(self):
        """Test retrying on failure."""
        attempts = [0]
        
        def fail_twice():
            attempts[0] += 1
            if attempts[0] < 3:
                raise ValueError("fail")
            return "success"
        
        config = RetryConfig(max_attempts=5, initial_delay=0.01)
        retrier = Retrier(config)
        result = retrier.execute(fail_twice)
        
        assert result.success is True
        assert result.attempts == 3

    def test_max_attempts_exceeded(self):
        """Test max attempts exceeded."""
        config = RetryConfig(max_attempts=2, initial_delay=0.01)
        retrier = Retrier(config)
        
        result = retrier.execute(lambda: 1/0)
        
        assert result.success is False
        assert result.attempts == 2

    def test_retry_on_specific_exception(self):
        """Test retry on specific exception."""
        config = RetryConfig(max_attempts=3, initial_delay=0.01)
        retrier = Retrier(config).retry_on(ValueError)
        
        result = retrier.execute(lambda: (_ for _ in ()).throw(ValueError("test")))
        
        assert result.success is False

    def test_callable(self):
        """Test callable interface."""
        config = RetryConfig(max_attempts=2, initial_delay=0.01)
        retrier = Retrier(config)
        
        result = retrier(lambda: "ok")
        assert result == "ok"

    def test_callable_raises(self):
        """Test callable raises on failure."""
        config = RetryConfig(max_attempts=2, initial_delay=0.01)
        retrier = Retrier(config)
        
        with pytest.raises(RetryError):
            retrier(lambda: 1/0)


class TestRetryFunction:
    """Tests for retry function."""

    def test_retry_success(self):
        """Test retry success."""
        result = retry(lambda: "ok", max_attempts=3, delay=0.01)
        assert result == "ok"


class TestWithRetryDecorator:
    """Tests for with_retry decorator."""

    def test_decorator(self):
        """Test decorator."""
        @with_retry(max_attempts=3, delay=0.01)
        def always_works():
            return "success"
        
        result = always_works()
        assert result == "success"

    def test_decorator_with_args(self):
        """Test decorator with function args."""
        @with_retry(max_attempts=3, delay=0.01)
        def add(a, b):
            return a + b
        
        result = add(1, 2)
        assert result == 3
