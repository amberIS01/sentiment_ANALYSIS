"""
Queue Module

Queue-based sentiment analysis processing.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
from collections import deque
from enum import Enum
import threading
import time


class Priority(Enum):
    """Task priority levels."""

    LOW = 0
    NORMAL = 1
    HIGH = 2
    URGENT = 3


@dataclass
class QueueItem:
    """An item in the queue."""

    id: str
    data: Any
    priority: Priority = Priority.NORMAL
    created_at: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessedItem:
    """A processed queue item."""

    item: QueueItem
    result: Any
    processed_at: float
    processing_time: float
    success: bool
    error: Optional[str] = None


class SentimentQueue:
    """Priority queue for sentiment analysis."""

    def __init__(self, maxsize: int = 0):
        """Initialize queue.

        Args:
            maxsize: Maximum queue size (0 = unlimited)
        """
        self.maxsize = maxsize
        self._queues: Dict[Priority, deque] = {
            Priority.URGENT: deque(),
            Priority.HIGH: deque(),
            Priority.NORMAL: deque(),
            Priority.LOW: deque(),
        }
        self._lock = threading.Lock()
        self._item_counter = 0

    def put(
        self,
        data: Any,
        priority: Priority = Priority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Add item to queue."""
        with self._lock:
            if self.maxsize > 0 and self.size() >= self.maxsize:
                raise ValueError("Queue is full")

            self._item_counter += 1
            item_id = f"item_{self._item_counter}"

            item = QueueItem(
                id=item_id,
                data=data,
                priority=priority,
                metadata=metadata or {},
            )

            self._queues[priority].append(item)
            return item_id

    def get(self) -> Optional[QueueItem]:
        """Get next item from queue (highest priority first)."""
        with self._lock:
            for priority in [Priority.URGENT, Priority.HIGH, Priority.NORMAL, Priority.LOW]:
                if self._queues[priority]:
                    return self._queues[priority].popleft()
        return None

    def peek(self) -> Optional[QueueItem]:
        """Peek at next item without removing."""
        with self._lock:
            for priority in [Priority.URGENT, Priority.HIGH, Priority.NORMAL, Priority.LOW]:
                if self._queues[priority]:
                    return self._queues[priority][0]
        return None

    def size(self) -> int:
        """Get total queue size."""
        return sum(len(q) for q in self._queues.values())

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.size() == 0

    def clear(self) -> None:
        """Clear all items."""
        with self._lock:
            for q in self._queues.values():
                q.clear()


class QueueProcessor:
    """Process items from a queue."""

    def __init__(
        self,
        queue: SentimentQueue,
        processor: Callable[[Any], Any],
    ):
        """Initialize processor."""
        self.queue = queue
        self.processor = processor
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._processed: List[ProcessedItem] = []

    def process_one(self) -> Optional[ProcessedItem]:
        """Process a single item."""
        item = self.queue.get()
        if not item:
            return None

        start = time.time()
        try:
            result = self.processor(item.data)
            return ProcessedItem(
                item=item,
                result=result,
                processed_at=time.time(),
                processing_time=time.time() - start,
                success=True,
            )
        except Exception as e:
            return ProcessedItem(
                item=item,
                result=None,
                processed_at=time.time(),
                processing_time=time.time() - start,
                success=False,
                error=str(e),
            )

    def process_all(self) -> List[ProcessedItem]:
        """Process all items in queue."""
        results = []
        while not self.queue.is_empty():
            result = self.process_one()
            if result:
                results.append(result)
        return results

    def start(self, interval: float = 0.01) -> None:
        """Start background processing."""
        if self._running:
            return

        self._running = True

        def run():
            while self._running:
                result = self.process_one()
                if result:
                    self._processed.append(result)
                else:
                    time.sleep(interval)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop background processing."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None

    @property
    def processed_count(self) -> int:
        """Get count of processed items."""
        return len(self._processed)
