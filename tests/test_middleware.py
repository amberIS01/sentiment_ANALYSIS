"""
Tests for the Middleware Module.
"""

import pytest

from chatbot.middleware import (
    Context,
    Middleware,
    MiddlewareChain,
    LoggingMiddleware,
    TrimMiddleware,
    LengthLimitMiddleware,
)


class TestContext:
    """Test Context dataclass."""

    def test_creation(self):
        ctx = Context(message="hello")
        assert ctx.message == "hello"

    def test_with_metadata(self):
        ctx = Context(
            message="hello",
            user_id="user1",
            session_id="sess1",
            metadata={"key": "value"},
        )
        assert ctx.user_id == "user1"
        assert ctx.metadata["key"] == "value"

    def test_with_message(self):
        ctx = Context(message="hello", user_id="user1")
        new_ctx = ctx.with_message("world")
        assert new_ctx.message == "world"
        assert new_ctx.user_id == "user1"


class TestTrimMiddleware:
    """Test TrimMiddleware class."""

    def test_trims_whitespace(self):
        middleware = TrimMiddleware()
        ctx = Context(message="  hello world  ")
        result = middleware(ctx, lambda c: c.message)
        assert result == "hello world"


class TestLengthLimitMiddleware:
    """Test LengthLimitMiddleware class."""

    def test_truncates_long_message(self):
        middleware = LengthLimitMiddleware(max_length=5)
        ctx = Context(message="hello world")
        result = middleware(ctx, lambda c: c.message)
        assert len(result) == 5

    def test_keeps_short_message(self):
        middleware = LengthLimitMiddleware(max_length=100)
        ctx = Context(message="hello")
        result = middleware(ctx, lambda c: c.message)
        assert result == "hello"


class TestMiddlewareChain:
    """Test MiddlewareChain class."""

    def test_initialization(self):
        chain = MiddlewareChain()
        assert chain is not None

    def test_no_handler_raises(self):
        chain = MiddlewareChain()
        ctx = Context(message="hello")
        with pytest.raises(ValueError):
            chain.process(ctx)

    def test_handler_only(self):
        chain = MiddlewareChain()
        chain.set_handler(lambda c: c.message.upper())
        ctx = Context(message="hello")
        result = chain.process(ctx)
        assert result == "HELLO"

    def test_single_middleware(self):
        chain = MiddlewareChain()
        chain.use(TrimMiddleware())
        chain.set_handler(lambda c: c.message)
        ctx = Context(message="  hello  ")
        result = chain.process(ctx)
        assert result == "hello"

    def test_multiple_middleware(self):
        chain = MiddlewareChain()
        chain.use(TrimMiddleware())
        chain.use(LengthLimitMiddleware(max_length=5))
        chain.set_handler(lambda c: c.message)
        ctx = Context(message="  hello world  ")
        result = chain.process(ctx)
        assert result == "hello"

    def test_chaining_syntax(self):
        chain = (
            MiddlewareChain()
            .use(TrimMiddleware())
            .set_handler(lambda c: c.message)
        )
        ctx = Context(message="  test  ")
        result = chain.process(ctx)
        assert result == "test"


class TestLoggingMiddleware:
    """Test LoggingMiddleware class."""

    def test_passes_through(self):
        middleware = LoggingMiddleware()
        ctx = Context(message="hello")
        result = middleware(ctx, lambda c: c.message)
        assert result == "hello"
