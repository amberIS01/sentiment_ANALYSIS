"""
Scheduler Module

Schedule sentiment analysis tasks.
"""

import time
import threading
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import heapq


class TaskStatus(Enum):
    """Status of a scheduled task."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(order=True)
class ScheduledTask:
    """A scheduled task."""

    run_at: float
    task_id: str = field(compare=False)
    func: Callable = field(compare=False)
    args: tuple = field(compare=False, default_factory=tuple)
    kwargs: Dict[str, Any] = field(compare=False, default_factory=dict)
    status: TaskStatus = field(compare=False, default=TaskStatus.PENDING)
    result: Any = field(compare=False, default=None)
    error: Optional[str] = field(compare=False, default=None)


class TaskScheduler:
    """Schedule and execute tasks."""

    def __init__(self):
        """Initialize scheduler."""
        self._tasks: Dict[str, ScheduledTask] = {}
        self._queue: List[ScheduledTask] = []
        self._task_counter = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()

    def schedule(
        self,
        func: Callable,
        delay: float = 0,
        args: tuple = (),
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Schedule a task to run after delay seconds."""
        self._task_counter += 1
        task_id = f"task_{self._task_counter}"

        task = ScheduledTask(
            run_at=time.time() + delay,
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs or {},
        )

        with self._lock:
            self._tasks[task_id] = task
            heapq.heappush(self._queue, task)

        return task_id

    def schedule_at(
        self,
        func: Callable,
        run_at: datetime,
        args: tuple = (),
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Schedule a task to run at specific time."""
        delay = (run_at - datetime.now()).total_seconds()
        return self.schedule(func, delay=max(0, delay), args=args, kwargs=kwargs)

    def cancel(self, task_id: str) -> bool:
        """Cancel a scheduled task."""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].status = TaskStatus.CANCELLED
                return True
        return False

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Get task by ID."""
        return self._tasks.get(task_id)

    def run_pending(self) -> int:
        """Run all pending tasks that are due."""
        executed = 0
        now = time.time()

        while self._queue:
            with self._lock:
                if not self._queue or self._queue[0].run_at > now:
                    break

                task = heapq.heappop(self._queue)

            if task.status == TaskStatus.CANCELLED:
                continue

            task.status = TaskStatus.RUNNING
            try:
                task.result = task.func(*task.args, **task.kwargs)
                task.status = TaskStatus.COMPLETED
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)

            executed += 1

        return executed

    def start(self, interval: float = 0.1) -> None:
        """Start background scheduler."""
        if self._running:
            return

        self._running = True

        def run():
            while self._running:
                self.run_pending()
                time.sleep(interval)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop background scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
            self._thread = None

    def clear(self) -> None:
        """Clear all tasks."""
        with self._lock:
            self._tasks.clear()
            self._queue.clear()

    @property
    def pending_count(self) -> int:
        """Get count of pending tasks."""
        return sum(
            1 for t in self._tasks.values()
            if t.status == TaskStatus.PENDING
        )


# Global scheduler instance
_scheduler = TaskScheduler()


def schedule(func: Callable, delay: float = 0) -> str:
    """Schedule a task with the global scheduler."""
    return _scheduler.schedule(func, delay=delay)


def run_pending() -> int:
    """Run pending tasks."""
    return _scheduler.run_pending()
