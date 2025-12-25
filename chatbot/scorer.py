"""
Sentiment Scorer Module

Custom scoring algorithms for sentiment analysis.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum


class ScoringMethod(Enum):
    """Scoring method types."""

    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    CUSTOM = "custom"


@dataclass
class ScoreResult:
    """Result from scoring."""

    raw_score: float
    normalized_score: float
    confidence: float
    method: ScoringMethod


class Scorer(ABC):
    """Base scorer class."""

    @abstractmethod
    def score(self, value: float) -> float:
        """Calculate score from value."""
        pass


class LinearScorer(Scorer):
    """Linear scoring."""

    def __init__(self, min_val: float = -1.0, max_val: float = 1.0):
        self.min_val = min_val
        self.max_val = max_val

    def score(self, value: float) -> float:
        # Normalize to 0-1 range
        range_val = self.max_val - self.min_val
        return (value - self.min_val) / range_val if range_val != 0 else 0.5


class ExponentialScorer(Scorer):
    """Exponential scoring for emphasizing extremes."""

    def __init__(self, base: float = 2.0):
        self.base = base

    def score(self, value: float) -> float:
        # Value should be -1 to 1
        if value >= 0:
            return (self.base ** value - 1) / (self.base - 1)
        else:
            return -((self.base ** abs(value) - 1) / (self.base - 1))


class WeightedScorer:
    """Weighted scoring with multiple factors."""

    def __init__(self):
        self._weights: Dict[str, float] = {}
        self._values: Dict[str, float] = {}

    def add_factor(self, name: str, weight: float = 1.0) -> None:
        """Add a scoring factor."""
        self._weights[name] = weight

    def set_value(self, name: str, value: float) -> None:
        """Set value for a factor."""
        self._values[name] = value

    def calculate(self) -> float:
        """Calculate weighted score."""
        if not self._weights:
            return 0.0

        total_weight = sum(self._weights.values())
        weighted_sum = sum(
            self._values.get(name, 0) * weight
            for name, weight in self._weights.items()
        )

        return weighted_sum / total_weight if total_weight != 0 else 0.0


class SentimentScorer:
    """Advanced sentiment scoring."""

    def __init__(self, method: ScoringMethod = ScoringMethod.LINEAR):
        self.method = method
        self._scorer = self._create_scorer(method)

    def _create_scorer(self, method: ScoringMethod) -> Scorer:
        if method == ScoringMethod.LINEAR:
            return LinearScorer()
        elif method == ScoringMethod.EXPONENTIAL:
            return ExponentialScorer()
        else:
            return LinearScorer()

    def score(
        self,
        positive: float,
        negative: float,
        neutral: float,
    ) -> ScoreResult:
        """Calculate sentiment score."""
        # Calculate raw compound score
        raw_score = positive - negative

        # Normalize using selected method
        normalized = self._scorer.score(raw_score)

        # Calculate confidence based on neutrality
        confidence = 1.0 - (neutral * 0.5)

        return ScoreResult(
            raw_score=raw_score,
            normalized_score=normalized,
            confidence=confidence,
            method=self.method,
        )

    def combine_scores(self, scores: List[float]) -> float:
        """Combine multiple scores."""
        if not scores:
            return 0.0
        return sum(scores) / len(scores)


def calculate_sentiment_score(
    positive: float,
    negative: float,
    neutral: float = 0.0,
) -> float:
    """Calculate simple sentiment score."""
    scorer = SentimentScorer()
    result = scorer.score(positive, negative, neutral)
    return result.normalized_score
