"""
Tests for the Retry Module.
"""

import pytest

from chatbot.retry import retry, retry_on_exception, RetryError, RetryContext


class TestRetryDecorator:
    """Test retry decorator."""

    def test_success_no_retry(self):
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 1

    def test_retry_on_failure(self):
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("fail")
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 3

    def test_max_attempts_exceeded(self):
        @retry(max_attempts=2, delay=0.01)
        def test_func():
            raise ValueError("always fails")

        with pytest.raises(RetryError):
            test_func()

    def test_specific_exception(self):
        @retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
        def test_func():
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            test_func()


class TestRetryOnException:
    """Test retry_on_exception decorator."""

    def test_retries_specific_exception(self):
        call_count = 0

        @retry_on_exception(ValueError, max_attempts=3)
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("fail")
            return "ok"

        result = test_func()
        assert result == "ok"


class TestRetryContext:
    """Test RetryContext class."""

    def test_iteration(self):
        context = RetryContext(max_attempts=3, delay=0.01)
        attempts = list(context)
        assert attempts == [1, 2, 3]

    def test_limited_attempts(self):
        context = RetryContext(max_attempts=2, delay=0.01)
        attempts = list(context)
        assert len(attempts) == 2


class TestRetryError:
    """Test RetryError exception."""

    def test_message(self):
        error = RetryError("Test error")
        assert str(error) == "Test error"

    def test_last_exception(self):
        original = ValueError("original")
        error = RetryError("Retry failed", last_exception=original)
        assert error.last_exception == original
