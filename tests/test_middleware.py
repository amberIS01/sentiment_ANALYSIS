"""Tests for middleware module."""

import pytest
from chatbot.middleware import (
    MiddlewareContext,
    LoggingMiddleware,
    ValidationMiddleware,
    CacheMiddleware,
    MiddlewareChain,
    create_chain,
)


class TestMiddlewareContext:
    """Tests for MiddlewareContext."""

    def test_create(self):
        """Test creating context."""
        ctx = MiddlewareContext(text="Hello")
        
        assert ctx.text == "Hello"
        assert ctx.score is None
        assert ctx.should_continue is True

    def test_metadata(self):
        """Test metadata."""
        ctx = MiddlewareContext(text="Hi", metadata={"key": "val"})
        
        assert ctx.metadata["key"] == "val"


class TestValidationMiddleware:
    """Tests for ValidationMiddleware."""

    def test_valid_text(self):
        """Test valid text passes."""
        middleware = ValidationMiddleware(min_length=1)
        ctx = MiddlewareContext(text="Hello")
        
        result = middleware.process(ctx, lambda c: c)
        
        assert result.should_continue is True

    def test_short_text(self):
        """Test short text blocked."""
        middleware = ValidationMiddleware(min_length=10)
        ctx = MiddlewareContext(text="Hi")
        
        result = middleware.process(ctx, lambda c: c)
        
        assert result.should_continue is False
        assert "error" in result.metadata

    def test_truncate_long(self):
        """Test long text truncated."""
        middleware = ValidationMiddleware(max_length=5)
        ctx = MiddlewareContext(text="Hello World")
        
        result = middleware.process(ctx, lambda c: c)
        
        assert len(result.text) == 5


class TestCacheMiddleware:
    """Tests for CacheMiddleware."""

    def test_cache_hit(self):
        """Test cache hit."""
        middleware = CacheMiddleware()
        ctx = MiddlewareContext(text="test")
        
        # First call
        call_count = [0]
        def next_fn(c):
            call_count[0] += 1
            c.score = 0.5
            return c
        
        middleware.process(ctx, next_fn)
        
        # Second call - should hit cache
        ctx2 = MiddlewareContext(text="test")
        result = middleware.process(ctx2, next_fn)
        
        assert call_count[0] == 1  # Only called once
        assert result.metadata.get("cached") is True


class TestMiddlewareChain:
    """Tests for MiddlewareChain."""

    def test_execute(self):
        """Test executing chain."""
        chain = MiddlewareChain()
        chain.use(ValidationMiddleware())
        
        result = chain.execute("Hello", lambda x: 0.5)
        
        assert result.score == 0.5

    def test_chain_order(self):
        """Test middleware order."""
        order = []
        
        class OrderMiddleware:
            def __init__(self, name):
                self._name = name
            
            @property
            def name(self):
                return self._name
            
            def process(self, ctx, next_fn):
                order.append(self._name)
                return next_fn(ctx)
        
        chain = MiddlewareChain()
        chain.use(OrderMiddleware("first"))
        chain.use(OrderMiddleware("second"))
        
        chain.execute("test", lambda x: 0.5)
        
        assert order == ["first", "second"]

    def test_remove_middleware(self):
        """Test removing middleware."""
        chain = MiddlewareChain()
        chain.use(ValidationMiddleware())
        chain.remove("validation")
        
        # Should not fail with empty text now
        ctx = MiddlewareContext(text="")
        result = chain.execute("", lambda x: 0.5)
        
        assert result.score == 0.5

    def test_stop_chain(self):
        """Test stopping chain."""
        chain = MiddlewareChain()
        chain.use(ValidationMiddleware(min_length=100))
        
        result = chain.execute("short", lambda x: 0.5)
        
        assert result.score is None


class TestCreateChain:
    """Tests for create_chain function."""

    def test_create(self):
        """Test creating chain."""
        chain = create_chain(
            ValidationMiddleware(),
            CacheMiddleware(),
        )
        
        result = chain.execute("Hello", lambda x: 0.5)
        
        assert result.score == 0.5
