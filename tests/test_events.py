"""
Tests for the Events Module.
"""

import pytest

from chatbot.events import Event, EventEmitter, ChatEvents, get_emitter, emit, on


class TestEvent:
    """Test Event dataclass."""

    def test_creation(self):
        event = Event(name="test", data={"key": "value"})
        assert event.name == "test"
        assert event.data == {"key": "value"}

    def test_timestamp(self):
        event = Event(name="test")
        assert event.timestamp is not None


class TestEventEmitter:
    """Test EventEmitter class."""

    def test_initialization(self):
        emitter = EventEmitter()
        assert emitter is not None

    def test_on_and_emit(self):
        emitter = EventEmitter()
        received = []

        def handler(event):
            received.append(event.data)

        emitter.on("test", handler)
        emitter.emit("test", "hello")

        assert len(received) == 1
        assert received[0] == "hello"

    def test_multiple_handlers(self):
        emitter = EventEmitter()
        results = []

        emitter.on("test", lambda e: results.append(1))
        emitter.on("test", lambda e: results.append(2))
        emitter.emit("test")

        assert results == [1, 2]

    def test_once(self):
        emitter = EventEmitter()
        count = [0]

        def handler(event):
            count[0] += 1

        emitter.once("test", handler)
        emitter.emit("test")
        emitter.emit("test")

        assert count[0] == 1

    def test_off_specific(self):
        emitter = EventEmitter()
        results = []

        def handler(event):
            results.append(1)

        emitter.on("test", handler)
        emitter.off("test", handler)
        emitter.emit("test")

        assert len(results) == 0

    def test_off_all(self):
        emitter = EventEmitter()
        results = []

        emitter.on("test", lambda e: results.append(1))
        emitter.on("test", lambda e: results.append(2))
        emitter.off("test")
        emitter.emit("test")

        assert len(results) == 0

    def test_listeners(self):
        emitter = EventEmitter()
        handler = lambda e: None
        emitter.on("test", handler)
        listeners = emitter.listeners("test")
        assert handler in listeners

    def test_clear(self):
        emitter = EventEmitter()
        emitter.on("test1", lambda e: None)
        emitter.on("test2", lambda e: None)
        emitter.clear()
        assert len(emitter.listeners("test1")) == 0
        assert len(emitter.listeners("test2")) == 0


class TestChatEvents:
    """Test ChatEvents constants."""

    def test_event_names(self):
        assert ChatEvents.MESSAGE_RECEIVED == "message_received"
        assert ChatEvents.SENTIMENT_ANALYZED == "sentiment_analyzed"
        assert ChatEvents.ERROR == "error"


class TestGlobalEmitter:
    """Test global emitter functions."""

    def test_get_emitter(self):
        emitter = get_emitter()
        assert isinstance(emitter, EventEmitter)

    def test_emit_and_on(self):
        received = []
        on("global_test", lambda e: received.append(e.data))
        emit("global_test", "value")
        assert "value" in received
