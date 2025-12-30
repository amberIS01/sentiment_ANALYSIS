"""
Middleware Module

Middleware system for sentiment analysis.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Callable
from abc import ABC, abstractmethod


@dataclass
class MiddlewareContext:
    """Context passed through middleware."""

    text: str
    score: Optional[float] = None
    metadata: Dict[str, Any] = None
    should_continue: bool = True

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


NextFunction = Callable[[MiddlewareContext], MiddlewareContext]


class Middleware(ABC):
    """Base middleware class."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Middleware name."""
        pass

    @abstractmethod
    def process(
        self,
        context: MiddlewareContext,
        next_fn: NextFunction,
    ) -> MiddlewareContext:
        """Process context."""
        pass


class LoggingMiddleware(Middleware):
    """Log requests."""

    def __init__(self, logger: Optional[Callable[[str], None]] = None):
        self._logger = logger or print

    @property
    def name(self) -> str:
        return "logging"

    def process(
        self,
        context: MiddlewareContext,
        next_fn: NextFunction,
    ) -> MiddlewareContext:
        self._logger(f"Processing: {context.text[:50]}...")
        result = next_fn(context)
        self._logger(f"Result: score={result.score}")
        return result


class ValidationMiddleware(Middleware):
    """Validate input."""

    def __init__(self, min_length: int = 1, max_length: int = 10000):
        self.min_length = min_length
        self.max_length = max_length

    @property
    def name(self) -> str:
        return "validation"

    def process(
        self,
        context: MiddlewareContext,
        next_fn: NextFunction,
    ) -> MiddlewareContext:
        if len(context.text) < self.min_length:
            context.should_continue = False
            context.metadata["error"] = "Text too short"
            return context
        if len(context.text) > self.max_length:
            context.text = context.text[:self.max_length]
        return next_fn(context)


class CacheMiddleware(Middleware):
    """Cache results."""

    def __init__(self):
        self._cache: Dict[str, float] = {}

    @property
    def name(self) -> str:
        return "cache"

    def process(
        self,
        context: MiddlewareContext,
        next_fn: NextFunction,
    ) -> MiddlewareContext:
        cache_key = context.text
        if cache_key in self._cache:
            context.score = self._cache[cache_key]
            context.metadata["cached"] = True
            return context

        result = next_fn(context)
        if result.score is not None:
            self._cache[cache_key] = result.score
        return result


class MiddlewareChain:
    """Chain of middleware."""

    def __init__(self):
        """Initialize chain."""
        self._middleware: List[Middleware] = []

    def use(self, middleware: Middleware) -> "MiddlewareChain":
        """Add middleware."""
        self._middleware.append(middleware)
        return self

    def remove(self, name: str) -> bool:
        """Remove middleware by name."""
        for i, m in enumerate(self._middleware):
            if m.name == name:
                self._middleware.pop(i)
                return True
        return False

    def execute(
        self,
        text: str,
        analyzer: Callable[[str], float],
    ) -> MiddlewareContext:
        """Execute chain."""
        context = MiddlewareContext(text=text)

        def final_handler(ctx: MiddlewareContext) -> MiddlewareContext:
            if ctx.should_continue:
                ctx.score = analyzer(ctx.text)
            return ctx

        def build_chain(index: int) -> NextFunction:
            if index >= len(self._middleware):
                return final_handler

            middleware = self._middleware[index]

            def next_fn(ctx: MiddlewareContext) -> MiddlewareContext:
                if not ctx.should_continue:
                    return ctx
                return middleware.process(ctx, build_chain(index + 1))

            return next_fn

        return build_chain(0)(context)


def create_chain(*middleware: Middleware) -> MiddlewareChain:
    """Create middleware chain."""
    chain = MiddlewareChain()
    for m in middleware:
        chain.use(m)
    return chain
