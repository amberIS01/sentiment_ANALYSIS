"""
Tests for the Queue Module.
"""

import pytest

from chatbot.queue import (
    SentimentQueue,
    QueueProcessor,
    QueueItem,
    ProcessedItem,
    Priority,
)


class TestPriority:
    """Test Priority enum."""

    def test_values(self):
        assert Priority.LOW.value == 0
        assert Priority.NORMAL.value == 1
        assert Priority.HIGH.value == 2
        assert Priority.URGENT.value == 3


class TestQueueItem:
    """Test QueueItem dataclass."""

    def test_creation(self):
        item = QueueItem(id="test-1", data="Hello")
        assert item.id == "test-1"
        assert item.data == "Hello"
        assert item.priority == Priority.NORMAL


class TestSentimentQueue:
    """Test SentimentQueue class."""

    def test_initialization(self):
        queue = SentimentQueue()
        assert queue.is_empty() is True

    def test_put(self):
        queue = SentimentQueue()
        item_id = queue.put("Test data")
        assert item_id is not None
        assert queue.size() == 1

    def test_put_with_priority(self):
        queue = SentimentQueue()
        queue.put("Low priority", priority=Priority.LOW)
        queue.put("High priority", priority=Priority.HIGH)
        item = queue.get()
        assert item.data == "High priority"

    def test_get_empty(self):
        queue = SentimentQueue()
        item = queue.get()
        assert item is None

    def test_peek(self):
        queue = SentimentQueue()
        queue.put("Test")
        item = queue.peek()
        assert item is not None
        assert queue.size() == 1  # Still in queue

    def test_size(self):
        queue = SentimentQueue()
        queue.put("Item 1")
        queue.put("Item 2")
        queue.put("Item 3")
        assert queue.size() == 3

    def test_is_empty(self):
        queue = SentimentQueue()
        assert queue.is_empty() is True
        queue.put("Item")
        assert queue.is_empty() is False

    def test_clear(self):
        queue = SentimentQueue()
        queue.put("Item 1")
        queue.put("Item 2")
        queue.clear()
        assert queue.is_empty() is True

    def test_maxsize(self):
        queue = SentimentQueue(maxsize=2)
        queue.put("Item 1")
        queue.put("Item 2")
        with pytest.raises(ValueError):
            queue.put("Item 3")

    def test_priority_order(self):
        queue = SentimentQueue()
        queue.put("Normal", priority=Priority.NORMAL)
        queue.put("Urgent", priority=Priority.URGENT)
        queue.put("Low", priority=Priority.LOW)

        assert queue.get().data == "Urgent"
        assert queue.get().data == "Normal"
        assert queue.get().data == "Low"


class TestQueueProcessor:
    """Test QueueProcessor class."""

    def test_initialization(self):
        queue = SentimentQueue()
        processor = QueueProcessor(queue, lambda x: x.upper())
        assert processor is not None

    def test_process_one(self):
        queue = SentimentQueue()
        queue.put("hello")
        processor = QueueProcessor(queue, lambda x: x.upper())
        result = processor.process_one()
        assert result.result == "HELLO"
        assert result.success is True

    def test_process_all(self):
        queue = SentimentQueue()
        queue.put("a")
        queue.put("b")
        processor = QueueProcessor(queue, lambda x: x.upper())
        results = processor.process_all()
        assert len(results) == 2
