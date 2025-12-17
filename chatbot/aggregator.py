"""
Sentiment Aggregator Module

Aggregate sentiment data from multiple sources.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

from .sentiment import SentimentAnalyzer, SentimentResult


class AggregationType(Enum):
    """Type of aggregation."""

    AVERAGE = "average"
    WEIGHTED = "weighted"
    MEDIAN = "median"
    MODE = "mode"


@dataclass
class AggregatedSentiment:
    """Aggregated sentiment result."""

    score: float
    label: str
    count: int
    min_score: float
    max_score: float
    std_dev: float
    aggregation_type: AggregationType


@dataclass
class SentimentSource:
    """A source of sentiment data."""

    name: str
    weight: float = 1.0
    results: List[SentimentResult] = field(default_factory=list)


class SentimentAggregator:
    """Aggregate sentiment from multiple sources."""

    def __init__(self):
        """Initialize aggregator."""
        self._sources: Dict[str, SentimentSource] = {}
        self._analyzer = SentimentAnalyzer()

    def add_source(self, name: str, weight: float = 1.0) -> None:
        """Add a sentiment source."""
        self._sources[name] = SentimentSource(name=name, weight=weight)

    def add_result(self, source_name: str, result: SentimentResult) -> None:
        """Add a result to a source."""
        if source_name not in self._sources:
            self.add_source(source_name)
        self._sources[source_name].results.append(result)

    def add_text(self, source_name: str, text: str) -> SentimentResult:
        """Analyze text and add to source."""
        result = self._analyzer.analyze(text)
        self.add_result(source_name, result)
        return result

    def aggregate(
        self,
        aggregation_type: AggregationType = AggregationType.AVERAGE,
    ) -> AggregatedSentiment:
        """Aggregate all sentiment data."""
        all_scores: List[float] = []
        weights: List[float] = []

        for source in self._sources.values():
            for result in source.results:
                all_scores.append(result.compound)
                weights.append(source.weight)

        if not all_scores:
            return AggregatedSentiment(
                score=0.0,
                label="neutral",
                count=0,
                min_score=0.0,
                max_score=0.0,
                std_dev=0.0,
                aggregation_type=aggregation_type,
            )

        if aggregation_type == AggregationType.WEIGHTED:
            total_weight = sum(weights)
            score = sum(s * w for s, w in zip(all_scores, weights)) / total_weight
        elif aggregation_type == AggregationType.MEDIAN:
            sorted_scores = sorted(all_scores)
            mid = len(sorted_scores) // 2
            score = sorted_scores[mid]
        else:  # AVERAGE
            score = sum(all_scores) / len(all_scores)

        # Determine label
        if score > 0.05:
            label = "positive"
        elif score < -0.05:
            label = "negative"
        else:
            label = "neutral"

        # Calculate std dev
        mean = sum(all_scores) / len(all_scores)
        variance = sum((s - mean) ** 2 for s in all_scores) / len(all_scores)
        std_dev = variance ** 0.5

        return AggregatedSentiment(
            score=score,
            label=label,
            count=len(all_scores),
            min_score=min(all_scores),
            max_score=max(all_scores),
            std_dev=std_dev,
            aggregation_type=aggregation_type,
        )

    def aggregate_by_source(self) -> Dict[str, AggregatedSentiment]:
        """Get aggregation for each source separately."""
        results: Dict[str, AggregatedSentiment] = {}

        for name, source in self._sources.items():
            scores = [r.compound for r in source.results]
            if not scores:
                continue

            avg = sum(scores) / len(scores)
            mean = avg
            variance = sum((s - mean) ** 2 for s in scores) / len(scores)

            if avg > 0.05:
                label = "positive"
            elif avg < -0.05:
                label = "negative"
            else:
                label = "neutral"

            results[name] = AggregatedSentiment(
                score=avg,
                label=label,
                count=len(scores),
                min_score=min(scores),
                max_score=max(scores),
                std_dev=variance ** 0.5,
                aggregation_type=AggregationType.AVERAGE,
            )

        return results

    def clear(self) -> None:
        """Clear all sources and results."""
        self._sources.clear()

    def get_source_names(self) -> List[str]:
        """Get names of all sources."""
        return list(self._sources.keys())
