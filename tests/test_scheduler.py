"""
Tests for the Scheduler Module.
"""

import pytest
import time
from datetime import datetime, timedelta

from chatbot.scheduler import (
    TaskScheduler,
    ScheduledTask,
    TaskStatus,
    schedule,
    run_pending,
)


class TestTaskStatus:
    """Test TaskStatus enum."""

    def test_values(self):
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.RUNNING.value == "running"
        assert TaskStatus.COMPLETED.value == "completed"


class TestTaskScheduler:
    """Test TaskScheduler class."""

    def test_initialization(self):
        scheduler = TaskScheduler()
        assert scheduler is not None

    def test_schedule(self):
        scheduler = TaskScheduler()
        task_id = scheduler.schedule(lambda: "done", delay=0)
        assert task_id is not None
        assert task_id.startswith("task_")

    def test_schedule_with_delay(self):
        scheduler = TaskScheduler()
        task_id = scheduler.schedule(lambda: "done", delay=1)
        task = scheduler.get_task(task_id)
        assert task.status == TaskStatus.PENDING

    def test_cancel(self):
        scheduler = TaskScheduler()
        task_id = scheduler.schedule(lambda: "done", delay=10)
        result = scheduler.cancel(task_id)
        assert result is True
        task = scheduler.get_task(task_id)
        assert task.status == TaskStatus.CANCELLED

    def test_run_pending(self):
        scheduler = TaskScheduler()
        results = []
        scheduler.schedule(lambda: results.append(1), delay=0)
        scheduler.schedule(lambda: results.append(2), delay=0)
        scheduler.run_pending()
        assert results == [1, 2]

    def test_run_pending_respects_delay(self):
        scheduler = TaskScheduler()
        results = []
        scheduler.schedule(lambda: results.append(1), delay=10)
        scheduler.run_pending()
        assert results == []

    def test_get_task(self):
        scheduler = TaskScheduler()
        task_id = scheduler.schedule(lambda: "done")
        task = scheduler.get_task(task_id)
        assert task is not None
        assert task.task_id == task_id

    def test_pending_count(self):
        scheduler = TaskScheduler()
        scheduler.schedule(lambda: None, delay=10)
        scheduler.schedule(lambda: None, delay=10)
        assert scheduler.pending_count == 2

    def test_clear(self):
        scheduler = TaskScheduler()
        scheduler.schedule(lambda: None)
        scheduler.clear()
        assert scheduler.pending_count == 0


class TestScheduledTask:
    """Test ScheduledTask dataclass."""

    def test_creation(self):
        task = ScheduledTask(
            run_at=time.time(),
            task_id="test",
            func=lambda: None,
        )
        assert task.task_id == "test"
        assert task.status == TaskStatus.PENDING


class TestScheduleFunction:
    """Test schedule function."""

    def test_basic(self):
        task_id = schedule(lambda: "done", delay=100)
        assert task_id is not None
