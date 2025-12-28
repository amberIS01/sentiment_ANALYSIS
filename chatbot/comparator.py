"""
Comparator Module

Compare sentiment analysis results.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum


class ComparisonResult(Enum):
    """Comparison outcomes."""

    EQUAL = "equal"
    GREATER = "greater"
    LESS = "less"
    SIMILAR = "similar"
    DIFFERENT = "different"


@dataclass
class SentimentComparison:
    """Result of comparing two sentiments."""

    score_a: float
    score_b: float
    difference: float
    result: ComparisonResult
    percent_change: float


@dataclass
class BatchComparison:
    """Result of batch comparison."""

    comparisons: List[SentimentComparison]
    avg_difference: float
    max_difference: float
    agreement_rate: float


class SentimentComparator:
    """Compare sentiment scores."""

    def __init__(self, tolerance: float = 0.1):
        """Initialize comparator."""
        self.tolerance = tolerance

    def compare(self, score_a: float, score_b: float) -> SentimentComparison:
        """Compare two sentiment scores."""
        diff = score_b - score_a
        abs_diff = abs(diff)

        if abs_diff < self.tolerance:
            result = ComparisonResult.SIMILAR
        elif diff > 0:
            result = ComparisonResult.GREATER
        else:
            result = ComparisonResult.LESS

        pct_change = (diff / abs(score_a) * 100) if score_a != 0 else 0.0

        return SentimentComparison(
            score_a=score_a,
            score_b=score_b,
            difference=diff,
            result=result,
            percent_change=pct_change,
        )

    def compare_many(
        self,
        scores_a: List[float],
        scores_b: List[float],
    ) -> BatchComparison:
        """Compare multiple sentiment pairs."""
        if len(scores_a) != len(scores_b):
            raise ValueError("Score lists must have same length")

        comparisons = [
            self.compare(a, b)
            for a, b in zip(scores_a, scores_b)
        ]

        diffs = [abs(c.difference) for c in comparisons]
        similar = sum(1 for c in comparisons if c.result == ComparisonResult.SIMILAR)

        return BatchComparison(
            comparisons=comparisons,
            avg_difference=sum(diffs) / len(diffs) if diffs else 0.0,
            max_difference=max(diffs) if diffs else 0.0,
            agreement_rate=similar / len(comparisons) if comparisons else 0.0,
        )

    def is_similar(self, score_a: float, score_b: float) -> bool:
        """Check if two scores are similar."""
        return abs(score_a - score_b) < self.tolerance

    def is_opposite(self, score_a: float, score_b: float) -> bool:
        """Check if scores have opposite polarity."""
        return (score_a > 0 and score_b < 0) or (score_a < 0 and score_b > 0)


def compare_sentiments(
    score_a: float,
    score_b: float,
    tolerance: float = 0.1,
) -> SentimentComparison:
    """Compare two sentiment scores."""
    comparator = SentimentComparator(tolerance)
    return comparator.compare(score_a, score_b)


def agreement_score(
    scores_a: List[float],
    scores_b: List[float],
    tolerance: float = 0.1,
) -> float:
    """Calculate agreement between two score lists."""
    comparator = SentimentComparator(tolerance)
    result = comparator.compare_many(scores_a, scores_b)
    return result.agreement_rate
