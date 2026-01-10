"""Tests for events module."""

import pytest
from chatbot.events import (
    EventType,
    Event,
    EventEmitter,
    EventLog,
    get_emitter,
    emit,
    on,
)


class TestEventEmitter:
    """Tests for EventEmitter."""

    def test_on_and_emit(self):
        """Test registering and emitting."""
        emitter = EventEmitter()
        received = []
        
        emitter.on(EventType.ANALYSIS_START, lambda e: received.append(e))
        emitter.emit(EventType.ANALYSIS_START, {"text": "test"})
        
        assert len(received) == 1
        assert received[0].data["text"] == "test"

    def test_off(self):
        """Test unregistering handler."""
        emitter = EventEmitter()
        received = []
        handler = lambda e: received.append(e)
        
        emitter.on(EventType.ANALYSIS_START, handler)
        emitter.off(EventType.ANALYSIS_START, handler)
        emitter.emit(EventType.ANALYSIS_START)
        
        assert len(received) == 0

    def test_on_any(self):
        """Test global handler."""
        emitter = EventEmitter()
        received = []
        
        emitter.on_any(lambda e: received.append(e))
        emitter.emit(EventType.ANALYSIS_START)
        emitter.emit(EventType.ANALYSIS_COMPLETE)
        
        assert len(received) == 2

    def test_emit_returns_event(self):
        """Test emit returns event."""
        emitter = EventEmitter()
        event = emitter.emit(EventType.SCORE_CALCULATED, {"score": 0.5})
        
        assert isinstance(event, Event)
        assert event.type == EventType.SCORE_CALCULATED

    def test_clear(self):
        """Test clearing handlers."""
        emitter = EventEmitter()
        emitter.on(EventType.ANALYSIS_START, lambda e: None)
        emitter.clear(EventType.ANALYSIS_START)
        
        assert EventType.ANALYSIS_START not in emitter._handlers or \
               len(emitter._handlers[EventType.ANALYSIS_START]) == 0

    def test_clear_all(self):
        """Test clearing all handlers."""
        emitter = EventEmitter()
        emitter.on(EventType.ANALYSIS_START, lambda e: None)
        emitter.on_any(lambda e: None)
        emitter.clear()
        
        assert len(emitter._handlers) == 0


class TestEventLog:
    """Tests for EventLog."""

    def test_add(self):
        """Test adding event."""
        log = EventLog()
        event = Event(EventType.ANALYSIS_START, {})
        log.add(event)
        
        assert len(log.get_all()) == 1

    def test_max_size(self):
        """Test max size limit."""
        log = EventLog(max_size=3)
        for i in range(5):
            log.add(Event(EventType.ANALYSIS_START, {"i": i}))
        
        assert len(log.get_all()) == 3

    def test_get_by_type(self):
        """Test getting by type."""
        log = EventLog()
        log.add(Event(EventType.ANALYSIS_START, {}))
        log.add(Event(EventType.ANALYSIS_COMPLETE, {}))
        log.add(Event(EventType.ANALYSIS_START, {}))
        
        starts = log.get_by_type(EventType.ANALYSIS_START)
        
        assert len(starts) == 2

    def test_clear(self):
        """Test clearing log."""
        log = EventLog()
        log.add(Event(EventType.ANALYSIS_START, {}))
        log.clear()
        
        assert len(log.get_all()) == 0


class TestEvent:
    """Tests for Event dataclass."""

    def test_create(self):
        """Test creating event."""
        event = Event(
            type=EventType.SCORE_CALCULATED,
            data={"score": 0.5},
            source="test",
        )
        
        assert event.type == EventType.SCORE_CALCULATED
        assert event.data["score"] == 0.5

    def test_timestamp(self):
        """Test timestamp is set."""
        event = Event(EventType.ANALYSIS_START, {})
        
        assert event.timestamp is not None


class TestGlobalEmitter:
    """Tests for global emitter functions."""

    def test_get_emitter(self):
        """Test getting global emitter."""
        emitter = get_emitter()
        
        assert isinstance(emitter, EventEmitter)
