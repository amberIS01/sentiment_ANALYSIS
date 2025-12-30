"""
Events Module

Event system for sentiment analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """Event types."""

    ANALYSIS_START = "analysis_start"
    ANALYSIS_COMPLETE = "analysis_complete"
    ANALYSIS_ERROR = "analysis_error"
    SCORE_CALCULATED = "score_calculated"
    THRESHOLD_CROSSED = "threshold_crossed"
    BATCH_START = "batch_start"
    BATCH_COMPLETE = "batch_complete"


@dataclass
class Event:
    """An event."""

    type: EventType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""


EventHandler = Callable[[Event], None]


class EventEmitter:
    """Emit and handle events."""

    def __init__(self):
        """Initialize emitter."""
        self._handlers: Dict[EventType, List[EventHandler]] = {}
        self._global_handlers: List[EventHandler] = []

    def on(self, event_type: EventType, handler: EventHandler) -> None:
        """Register event handler."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def off(self, event_type: EventType, handler: EventHandler) -> bool:
        """Unregister event handler."""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
                return True
            except ValueError:
                pass
        return False

    def on_any(self, handler: EventHandler) -> None:
        """Register global handler."""
        self._global_handlers.append(handler)

    def emit(
        self,
        event_type: EventType,
        data: Optional[Dict[str, Any]] = None,
        source: str = "",
    ) -> Event:
        """Emit an event."""
        event = Event(
            type=event_type,
            data=data or {},
            source=source,
        )

        # Call specific handlers
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(event)

        # Call global handlers
        for handler in self._global_handlers:
            handler(event)

        return event

    def clear(self, event_type: Optional[EventType] = None) -> None:
        """Clear handlers."""
        if event_type:
            self._handlers[event_type] = []
        else:
            self._handlers.clear()
            self._global_handlers.clear()


class EventLog:
    """Log events."""

    def __init__(self, max_size: int = 1000):
        """Initialize log."""
        self._events: List[Event] = []
        self._max_size = max_size

    def add(self, event: Event) -> None:
        """Add event to log."""
        self._events.append(event)
        if len(self._events) > self._max_size:
            self._events.pop(0)

    def get_all(self) -> List[Event]:
        """Get all events."""
        return self._events.copy()

    def get_by_type(self, event_type: EventType) -> List[Event]:
        """Get events by type."""
        return [e for e in self._events if e.type == event_type]

    def clear(self) -> None:
        """Clear log."""
        self._events.clear()


# Global emitter instance
_emitter = EventEmitter()


def get_emitter() -> EventEmitter:
    """Get global event emitter."""
    return _emitter


def emit(
    event_type: EventType,
    data: Optional[Dict[str, Any]] = None,
) -> Event:
    """Emit event using global emitter."""
    return _emitter.emit(event_type, data)


def on(event_type: EventType, handler: EventHandler) -> None:
    """Register handler with global emitter."""
    _emitter.on(event_type, handler)
