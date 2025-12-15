"""
Sentiment History Tracker Module

Tracks sentiment changes over time for trend analysis.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from collections import deque


@dataclass
class SentimentPoint:
    """A single sentiment measurement point."""

    timestamp: datetime
    score: float
    label: str
    text: Optional[str] = None


class SentimentHistory:
    """Track sentiment over time."""

    def __init__(self, max_size: int = 1000):
        """Initialize history tracker.

        Args:
            max_size: Maximum number of points to keep
        """
        self._points: deque = deque(maxlen=max_size)
        self._max_size = max_size

    def add(
        self,
        score: float,
        label: str,
        text: Optional[str] = None,
    ) -> SentimentPoint:
        """Add a sentiment point."""
        point = SentimentPoint(
            timestamp=datetime.now(),
            score=score,
            label=label,
            text=text,
        )
        self._points.append(point)
        return point

    def get_recent(self, n: int = 10) -> List[SentimentPoint]:
        """Get n most recent points."""
        return list(self._points)[-n:]

    def get_all(self) -> List[SentimentPoint]:
        """Get all points."""
        return list(self._points)

    def average_score(self) -> float:
        """Get average sentiment score."""
        if not self._points:
            return 0.0
        return sum(p.score for p in self._points) / len(self._points)

    def trend(self) -> str:
        """Determine sentiment trend."""
        if len(self._points) < 2:
            return "stable"

        recent = list(self._points)[-5:]
        if len(recent) < 2:
            return "stable"

        first_half = recent[:len(recent) // 2]
        second_half = recent[len(recent) // 2:]

        avg_first = sum(p.score for p in first_half) / len(first_half)
        avg_second = sum(p.score for p in second_half) / len(second_half)

        diff = avg_second - avg_first
        if diff > 0.1:
            return "improving"
        elif diff < -0.1:
            return "declining"
        return "stable"

    def label_counts(self) -> Dict[str, int]:
        """Count occurrences of each label."""
        counts: Dict[str, int] = {}
        for point in self._points:
            counts[point.label] = counts.get(point.label, 0) + 1
        return counts

    def clear(self) -> None:
        """Clear all history."""
        self._points.clear()

    def __len__(self) -> int:
        return len(self._points)

    def to_dict(self) -> Dict[str, Any]:
        """Export history as dictionary."""
        return {
            "points": [
                {
                    "timestamp": p.timestamp.isoformat(),
                    "score": p.score,
                    "label": p.label,
                }
                for p in self._points
            ],
            "average": self.average_score(),
            "trend": self.trend(),
            "counts": self.label_counts(),
        }
