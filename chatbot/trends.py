"""
Sentiment Trends Module

Analyze and track sentiment trends over time.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple
from enum import Enum


class TrendDirection(Enum):
    """Trend direction."""

    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"
    VOLATILE = "volatile"


@dataclass
class TrendPoint:
    """Single point in trend data."""

    timestamp: datetime
    value: float
    label: str


@dataclass
class TrendAnalysis:
    """Result of trend analysis."""

    direction: TrendDirection
    change: float
    volatility: float
    average: float
    min_value: float
    max_value: float
    data_points: int


class TrendAnalyzer:
    """Analyze sentiment trends."""

    def __init__(self, sensitivity: float = 0.1):
        """Initialize analyzer.

        Args:
            sensitivity: Threshold for detecting trend changes
        """
        self.sensitivity = sensitivity
        self._points: List[TrendPoint] = []

    def add_point(
        self,
        value: float,
        label: str,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Add a data point."""
        self._points.append(TrendPoint(
            timestamp=timestamp or datetime.now(),
            value=value,
            label=label,
        ))

    def analyze(self) -> Optional[TrendAnalysis]:
        """Analyze the current trend."""
        if len(self._points) < 2:
            return None

        values = [p.value for p in self._points]
        avg = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)

        # Calculate volatility
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        volatility = variance ** 0.5

        # Calculate trend direction
        first_half = values[:len(values) // 2]
        second_half = values[len(values) // 2:]

        avg_first = sum(first_half) / len(first_half) if first_half else 0
        avg_second = sum(second_half) / len(second_half) if second_half else 0
        change = avg_second - avg_first

        if volatility > 0.3:
            direction = TrendDirection.VOLATILE
        elif change > self.sensitivity:
            direction = TrendDirection.RISING
        elif change < -self.sensitivity:
            direction = TrendDirection.FALLING
        else:
            direction = TrendDirection.STABLE

        return TrendAnalysis(
            direction=direction,
            change=change,
            volatility=volatility,
            average=avg,
            min_value=min_val,
            max_value=max_val,
            data_points=len(self._points),
        )

    def get_recent(self, n: int = 10) -> List[TrendPoint]:
        """Get n most recent points."""
        return self._points[-n:]

    def get_by_timeframe(
        self,
        start: datetime,
        end: Optional[datetime] = None,
    ) -> List[TrendPoint]:
        """Get points within timeframe."""
        end = end or datetime.now()
        return [
            p for p in self._points
            if start <= p.timestamp <= end
        ]

    def moving_average(self, window: int = 5) -> List[float]:
        """Calculate moving average."""
        values = [p.value for p in self._points]
        if len(values) < window:
            return values

        result = []
        for i in range(len(values) - window + 1):
            avg = sum(values[i:i + window]) / window
            result.append(avg)
        return result

    def clear(self) -> None:
        """Clear all data points."""
        self._points.clear()

    def to_dict(self) -> Dict:
        """Export as dictionary."""
        analysis = self.analyze()
        return {
            "points": [
                {
                    "timestamp": p.timestamp.isoformat(),
                    "value": p.value,
                    "label": p.label,
                }
                for p in self._points
            ],
            "analysis": {
                "direction": analysis.direction.value if analysis else None,
                "change": analysis.change if analysis else None,
                "average": analysis.average if analysis else None,
            } if analysis else None,
        }
