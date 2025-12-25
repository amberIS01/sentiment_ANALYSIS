"""
Metrics Module

Track and report sentiment analysis metrics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import threading
import time


@dataclass
class MetricPoint:
    """A single metric point."""

    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSummary:
    """Summary of a metric."""

    name: str
    count: int
    total: float
    average: float
    min_value: float
    max_value: float


class Counter:
    """Thread-safe counter."""

    def __init__(self, name: str):
        self.name = name
        self._value = 0
        self._lock = threading.Lock()

    def increment(self, amount: int = 1) -> None:
        """Increment counter."""
        with self._lock:
            self._value += amount

    def decrement(self, amount: int = 1) -> None:
        """Decrement counter."""
        with self._lock:
            self._value -= amount

    @property
    def value(self) -> int:
        return self._value

    def reset(self) -> None:
        """Reset counter."""
        with self._lock:
            self._value = 0


class Gauge:
    """Thread-safe gauge."""

    def __init__(self, name: str):
        self.name = name
        self._value = 0.0
        self._lock = threading.Lock()

    def set(self, value: float) -> None:
        """Set gauge value."""
        with self._lock:
            self._value = value

    def increment(self, amount: float = 1.0) -> None:
        """Increment gauge."""
        with self._lock:
            self._value += amount

    @property
    def value(self) -> float:
        return self._value


class Histogram:
    """Histogram for tracking distributions."""

    def __init__(self, name: str, buckets: Optional[List[float]] = None):
        self.name = name
        self._values: List[float] = []
        self._buckets = buckets or [0.1, 0.5, 1.0, 2.0, 5.0]
        self._lock = threading.Lock()

    def observe(self, value: float) -> None:
        """Record a value."""
        with self._lock:
            self._values.append(value)

    def get_summary(self) -> MetricSummary:
        """Get histogram summary."""
        with self._lock:
            if not self._values:
                return MetricSummary(
                    name=self.name,
                    count=0,
                    total=0,
                    average=0,
                    min_value=0,
                    max_value=0,
                )
            return MetricSummary(
                name=self.name,
                count=len(self._values),
                total=sum(self._values),
                average=sum(self._values) / len(self._values),
                min_value=min(self._values),
                max_value=max(self._values),
            )


class Timer:
    """Context manager for timing."""

    def __init__(self, histogram: Histogram):
        self._histogram = histogram
        self._start: float = 0

    def __enter__(self) -> "Timer":
        self._start = time.time()
        return self

    def __exit__(self, *args) -> None:
        elapsed = time.time() - self._start
        self._histogram.observe(elapsed)


class MetricsCollector:
    """Collect and manage metrics."""

    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._points: List[MetricPoint] = []

    def counter(self, name: str) -> Counter:
        """Get or create counter."""
        if name not in self._counters:
            self._counters[name] = Counter(name)
        return self._counters[name]

    def gauge(self, name: str) -> Gauge:
        """Get or create gauge."""
        if name not in self._gauges:
            self._gauges[name] = Gauge(name)
        return self._gauges[name]

    def histogram(self, name: str) -> Histogram:
        """Get or create histogram."""
        if name not in self._histograms:
            self._histograms[name] = Histogram(name)
        return self._histograms[name]

    def timer(self, name: str) -> Timer:
        """Get timer for histogram."""
        return Timer(self.histogram(name))

    def record(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        """Record a metric point."""
        self._points.append(MetricPoint(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {},
        ))

    def get_all(self) -> Dict[str, Any]:
        """Get all metrics."""
        return {
            "counters": {n: c.value for n, c in self._counters.items()},
            "gauges": {n: g.value for n, g in self._gauges.items()},
            "histograms": {
                n: h.get_summary().__dict__
                for n, h in self._histograms.items()
            },
        }


# Global metrics instance
_metrics = MetricsCollector()


def get_metrics() -> MetricsCollector:
    """Get global metrics collector."""
    return _metrics
