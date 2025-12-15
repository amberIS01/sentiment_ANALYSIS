"""
Context Management Module

Provides context managers for chatbot operations.
"""

from contextlib import contextmanager
from typing import Optional, Generator, Any, Dict
from dataclasses import dataclass, field
from datetime import datetime
import threading


@dataclass
class ChatContext:
    """Context for a chat session."""

    session_id: str
    user_id: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    message_count: int = 0

    def increment_messages(self) -> None:
        """Increment message count."""
        self.message_count += 1


class ContextVar:
    """Thread-local context variable."""

    def __init__(self, name: str, default: Any = None):
        """Initialize context variable."""
        self.name = name
        self.default = default
        self._local = threading.local()

    def get(self) -> Any:
        """Get current value."""
        return getattr(self._local, "value", self.default)

    def set(self, value: Any) -> Any:
        """Set value and return previous."""
        previous = self.get()
        self._local.value = value
        return previous

    def reset(self) -> None:
        """Reset to default."""
        if hasattr(self._local, "value"):
            delattr(self._local, "value")


# Global context variable
_current_context: ContextVar = ContextVar("current_context")


def get_current_context() -> Optional[ChatContext]:
    """Get the current chat context."""
    return _current_context.get()


def set_current_context(context: Optional[ChatContext]) -> None:
    """Set the current chat context."""
    _current_context.set(context)


@contextmanager
def chat_context(
    session_id: str,
    user_id: Optional[str] = None,
) -> Generator[ChatContext, None, None]:
    """Context manager for chat sessions."""
    context = ChatContext(
        session_id=session_id,
        user_id=user_id,
    )
    previous = _current_context.set(context)
    try:
        yield context
    finally:
        _current_context.set(previous)


@contextmanager
def temporary_context(
    **kwargs: Any,
) -> Generator[ChatContext, None, None]:
    """Create a temporary context with custom metadata."""
    current = get_current_context()
    if current:
        # Clone current context with updates
        new_context = ChatContext(
            session_id=current.session_id,
            user_id=current.user_id,
            started_at=current.started_at,
            metadata={**current.metadata, **kwargs},
            message_count=current.message_count,
        )
    else:
        new_context = ChatContext(
            session_id="temp",
            metadata=kwargs,
        )

    previous = _current_context.set(new_context)
    try:
        yield new_context
    finally:
        _current_context.set(previous)


class ContextManager:
    """Manage multiple chat contexts."""

    def __init__(self):
        """Initialize context manager."""
        self._contexts: Dict[str, ChatContext] = {}

    def create(
        self,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> ChatContext:
        """Create a new context."""
        context = ChatContext(session_id=session_id, user_id=user_id)
        self._contexts[session_id] = context
        return context

    def get(self, session_id: str) -> Optional[ChatContext]:
        """Get context by session ID."""
        return self._contexts.get(session_id)

    def remove(self, session_id: str) -> bool:
        """Remove a context."""
        if session_id in self._contexts:
            del self._contexts[session_id]
            return True
        return False

    def list_all(self) -> Dict[str, ChatContext]:
        """Get all contexts."""
        return self._contexts.copy()
