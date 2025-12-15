"""
Event Emitter Module

Provides event-driven architecture support.
"""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """Represents an event."""

    name: str
    data: Any = None
    timestamp: datetime = field(default_factory=datetime.now)


EventHandler = Callable[[Event], None]


class EventEmitter:
    """Simple event emitter implementation."""

    def __init__(self):
        """Initialize event emitter."""
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._once_handlers: Dict[str, List[EventHandler]] = {}

    def on(self, event_name: str, handler: EventHandler) -> None:
        """Register an event handler."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    def once(self, event_name: str, handler: EventHandler) -> None:
        """Register a one-time event handler."""
        if event_name not in self._once_handlers:
            self._once_handlers[event_name] = []
        self._once_handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Optional[EventHandler] = None) -> None:
        """Remove an event handler."""
        if handler is None:
            self._handlers.pop(event_name, None)
            self._once_handlers.pop(event_name, None)
        else:
            if event_name in self._handlers:
                self._handlers[event_name] = [
                    h for h in self._handlers[event_name] if h != handler
                ]
            if event_name in self._once_handlers:
                self._once_handlers[event_name] = [
                    h for h in self._once_handlers[event_name] if h != handler
                ]

    def emit(self, event_name: str, data: Any = None) -> None:
        """Emit an event."""
        event = Event(name=event_name, data=data)

        # Call regular handlers
        for handler in self._handlers.get(event_name, []):
            handler(event)

        # Call and remove once handlers
        once_handlers = self._once_handlers.pop(event_name, [])
        for handler in once_handlers:
            handler(event)

    def listeners(self, event_name: str) -> List[EventHandler]:
        """Get all listeners for an event."""
        return (
            self._handlers.get(event_name, [])
            + self._once_handlers.get(event_name, [])
        )

    def clear(self) -> None:
        """Remove all handlers."""
        self._handlers.clear()
        self._once_handlers.clear()


# Predefined events
class ChatEvents:
    """Standard chat event names."""

    MESSAGE_RECEIVED = "message_received"
    MESSAGE_SENT = "message_sent"
    SENTIMENT_ANALYZED = "sentiment_analyzed"
    SESSION_STARTED = "session_started"
    SESSION_ENDED = "session_ended"
    ERROR = "error"


# Global emitter instance
_emitter = EventEmitter()


def get_emitter() -> EventEmitter:
    """Get the global event emitter."""
    return _emitter


def emit(event_name: str, data: Any = None) -> None:
    """Emit an event on the global emitter."""
    _emitter.emit(event_name, data)


def on(event_name: str, handler: EventHandler) -> None:
    """Register handler on global emitter."""
    _emitter.on(event_name, handler)
