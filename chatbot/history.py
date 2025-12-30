"""
History Module

Track sentiment history over time.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from collections import deque


@dataclass
class HistoryEntry:
    """A single history entry."""

    text: str
    score: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HistoryStats:
    """Statistics from history."""

    count: int
    avg_score: float
    min_score: float
    max_score: float
    std_dev: float
    trend: str


class SentimentHistory:
    """Track sentiment over time."""

    def __init__(self, max_size: int = 1000):
        """Initialize history."""
        self._entries: deque = deque(maxlen=max_size)
        self._max_size = max_size

    def add(
        self,
        text: str,
        score: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> HistoryEntry:
        """Add entry to history."""
        entry = HistoryEntry(
            text=text,
            score=score,
            timestamp=datetime.now(),
            metadata=metadata or {},
        )
        self._entries.append(entry)
        return entry

    def get_recent(self, n: int = 10) -> List[HistoryEntry]:
        """Get recent entries."""
        entries = list(self._entries)
        return entries[-n:]

    def get_by_range(
        self,
        start: datetime,
        end: datetime,
    ) -> List[HistoryEntry]:
        """Get entries in time range."""
        return [
            e for e in self._entries
            if start <= e.timestamp <= end
        ]

    def get_stats(self) -> HistoryStats:
        """Get history statistics."""
        if not self._entries:
            return HistoryStats(
                count=0,
                avg_score=0.0,
                min_score=0.0,
                max_score=0.0,
                std_dev=0.0,
                trend="stable",
            )

        scores = [e.score for e in self._entries]
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)

        # Calculate trend
        if len(scores) >= 2:
            first_half = scores[:len(scores) // 2]
            second_half = scores[len(scores) // 2:]
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            if second_avg - first_avg > 0.1:
                trend = "improving"
            elif first_avg - second_avg > 0.1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"

        return HistoryStats(
            count=len(scores),
            avg_score=avg,
            min_score=min(scores),
            max_score=max(scores),
            std_dev=variance ** 0.5,
            trend=trend,
        )

    def clear(self) -> None:
        """Clear history."""
        self._entries.clear()

    def export(self) -> List[Dict[str, Any]]:
        """Export history as list of dicts."""
        return [
            {
                "text": e.text,
                "score": e.score,
                "timestamp": e.timestamp.isoformat(),
                "metadata": e.metadata,
            }
            for e in self._entries
        ]

    def __len__(self) -> int:
        return len(self._entries)


def track_sentiment(
    history: SentimentHistory,
    text: str,
    score: float,
) -> HistoryEntry:
    """Track a sentiment score."""
    return history.add(text, score)


def get_trend(history: SentimentHistory) -> str:
    """Get sentiment trend from history."""
    stats = history.get_stats()
    return stats.trend
