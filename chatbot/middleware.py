"""
Middleware Module

Provides middleware chain for message processing.
"""

from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Any
from dataclasses import dataclass


@dataclass
class Context:
    """Request context passed through middleware."""

    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[dict] = None

    def with_message(self, message: str) -> "Context":
        """Create new context with updated message."""
        return Context(
            message=message,
            user_id=self.user_id,
            session_id=self.session_id,
            metadata=self.metadata,
        )


NextFunction = Callable[[Context], str]


class Middleware(ABC):
    """Base middleware class."""

    @abstractmethod
    def __call__(self, context: Context, next_fn: NextFunction) -> str:
        """Process the context and call next middleware."""
        pass


class MiddlewareChain:
    """Chain of middleware processors."""

    def __init__(self):
        """Initialize chain."""
        self._middlewares: List[Middleware] = []
        self._handler: Optional[Callable[[Context], str]] = None

    def use(self, middleware: Middleware) -> "MiddlewareChain":
        """Add middleware to chain."""
        self._middlewares.append(middleware)
        return self

    def set_handler(
        self,
        handler: Callable[[Context], str],
    ) -> "MiddlewareChain":
        """Set the final handler."""
        self._handler = handler
        return self

    def process(self, context: Context) -> str:
        """Process context through middleware chain."""
        if not self._handler:
            raise ValueError("No handler set")

        def create_next(index: int) -> NextFunction:
            if index >= len(self._middlewares):
                return self._handler

            def next_fn(ctx: Context) -> str:
                middleware = self._middlewares[index]
                return middleware(ctx, create_next(index + 1))

            return next_fn

        return create_next(0)(context)


class LoggingMiddleware(Middleware):
    """Log messages passing through."""

    def __init__(self, logger: Optional[Any] = None):
        self.logger = logger

    def __call__(self, context: Context, next_fn: NextFunction) -> str:
        if self.logger:
            self.logger.debug(f"Processing: {context.message[:50]}")
        response = next_fn(context)
        if self.logger:
            self.logger.debug(f"Response: {response[:50]}")
        return response


class TrimMiddleware(Middleware):
    """Trim whitespace from messages."""

    def __call__(self, context: Context, next_fn: NextFunction) -> str:
        trimmed = context.message.strip()
        return next_fn(context.with_message(trimmed))


class LengthLimitMiddleware(Middleware):
    """Limit message length."""

    def __init__(self, max_length: int = 5000):
        self.max_length = max_length

    def __call__(self, context: Context, next_fn: NextFunction) -> str:
        message = context.message
        if len(message) > self.max_length:
            message = message[:self.max_length]
        return next_fn(context.with_message(message))
