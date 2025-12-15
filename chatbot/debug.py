"""
Debug Utilities Module

Provides debugging and profiling utilities.
"""

import time
import functools
from typing import Callable, Any, Optional, Dict
from contextlib import contextmanager
import logging


logger = logging.getLogger(__name__)


class Profiler:
    """Simple function profiler."""

    def __init__(self):
        self._timings: Dict[str, list] = {}

    def record(self, name: str, duration: float) -> None:
        """Record a timing."""
        if name not in self._timings:
            self._timings[name] = []
        self._timings[name].append(duration)

    def get_stats(self, name: str) -> Dict[str, float]:
        """Get stats for a function."""
        timings = self._timings.get(name, [])
        if not timings:
            return {"count": 0, "total": 0, "avg": 0, "min": 0, "max": 0}
        return {
            "count": len(timings),
            "total": sum(timings),
            "avg": sum(timings) / len(timings),
            "min": min(timings),
            "max": max(timings),
        }

    def report(self) -> Dict[str, Dict[str, float]]:
        """Get full profiling report."""
        return {name: self.get_stats(name) for name in self._timings}

    def clear(self) -> None:
        """Clear all timings."""
        self._timings.clear()


_profiler = Profiler()


def timed(func: Callable) -> Callable:
    """Decorator to time function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            _profiler.record(func.__name__, duration)
    return wrapper


@contextmanager
def timer(name: str = "operation"):
    """Context manager for timing code blocks."""
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    logger.debug(f"{name} took {duration:.4f}s")


def log_call(func: Callable) -> Callable:
    """Decorator to log function calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} returned")
        return result
    return wrapper


def get_profiler() -> Profiler:
    """Get the global profiler instance."""
    return _profiler


def debug_repr(obj: Any, max_length: int = 100) -> str:
    """Create a debug representation of an object."""
    repr_str = repr(obj)
    if len(repr_str) > max_length:
        return repr_str[:max_length] + "..."
    return repr_str


class DebugContext:
    """Context manager for debug mode."""

    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled
        self.start_time: Optional[float] = None

    def __enter__(self):
        if self.enabled:
            self.start_time = time.perf_counter()
            logger.debug(f"[DEBUG] Entering {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.enabled and self.start_time:
            duration = time.perf_counter() - self.start_time
            logger.debug(f"[DEBUG] Exiting {self.name} ({duration:.4f}s)")
        return False
