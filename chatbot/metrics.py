"""
Metrics Collection Module

This module provides metrics collection and monitoring capabilities.
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import time


@dataclass
class MetricPoint:
    """A single metric data point."""
    name: str
    value: float
    timestamp: datetime = field(default_factory=datetime.now)
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Collect and track metrics."""

    def __init__(self):
        self._metrics: Dict[str, List[MetricPoint]] = {}
        self._counters: Dict[str, int] = {}
        self._start_time = datetime.now()

    def increment(self, name: str, value: int = 1) -> None:
        """Increment a counter."""
        self._counters[name] = self._counters.get(name, 0) + value

    def record(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a metric value."""
        if name not in self._metrics:
            self._metrics[name] = []

        point = MetricPoint(name=name, value=value, tags=tags or {})
        self._metrics[name].append(point)

    def get_counter(self, name: str) -> int:
        """Get counter value."""
        return self._counters.get(name, 0)

    def get_average(self, name: str) -> float:
        """Get average of recorded values."""
        points = self._metrics.get(name, [])
        if not points:
            return 0.0
        return sum(p.value for p in points) / len(points)

    def get_summary(self) -> Dict[str, any]:
        """Get metrics summary."""
        uptime = datetime.now() - self._start_time
        return {
            "uptime_seconds": uptime.total_seconds(),
            "counters": dict(self._counters),
            "averages": {name: self.get_average(name) for name in self._metrics},
        }

    def reset(self) -> None:
        """Reset all metrics."""
        self._metrics.clear()
        self._counters.clear()
        self._start_time = datetime.now()


class Timer:
    """Context manager for timing operations."""

    def __init__(self, collector: MetricsCollector, name: str):
        self.collector = collector
        self.name = name
        self._start: Optional[float] = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        elapsed = time.perf_counter() - self._start
        self.collector.record(f"{self.name}_duration_ms", elapsed * 1000)


# Global metrics instance
_metrics: Optional[MetricsCollector] = None


def get_metrics() -> MetricsCollector:
    """Get global metrics collector."""
    global _metrics
    if _metrics is None:
        _metrics = MetricsCollector()
    return _metrics
