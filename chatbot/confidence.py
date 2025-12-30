"""
Confidence Module

Calculate confidence scores for sentiment predictions.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from abc import ABC, abstractmethod


@dataclass
class ConfidenceResult:
    """Confidence calculation result."""

    score: float
    level: str
    factors: Dict[str, float]


class ConfidenceCalculator(ABC):
    """Base confidence calculator."""

    @abstractmethod
    def calculate(self, sentiment_score: float, **kwargs) -> float:
        """Calculate confidence score."""
        pass


class DistanceConfidence(ConfidenceCalculator):
    """Confidence based on distance from neutral."""

    def __init__(self, max_distance: float = 1.0):
        """Initialize calculator."""
        self.max_distance = max_distance

    def calculate(self, sentiment_score: float, **kwargs) -> float:
        """Calculate based on distance from 0."""
        distance = abs(sentiment_score)
        return min(1.0, distance / self.max_distance)


class ConsistencyConfidence(ConfidenceCalculator):
    """Confidence based on prediction consistency."""

    def calculate(
        self,
        sentiment_score: float,
        scores: Optional[List[float]] = None,
        **kwargs,
    ) -> float:
        """Calculate based on score consistency."""
        if not scores or len(scores) < 2:
            return 0.5

        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5

        return max(0.0, 1.0 - std_dev)


class TextLengthConfidence(ConfidenceCalculator):
    """Confidence based on text length."""

    def __init__(self, optimal_length: int = 50):
        """Initialize calculator."""
        self.optimal_length = optimal_length

    def calculate(
        self,
        sentiment_score: float,
        text: str = "",
        **kwargs,
    ) -> float:
        """Calculate based on text length."""
        length = len(text.split())
        if length == 0:
            return 0.0
        
        ratio = min(length, self.optimal_length) / self.optimal_length
        return ratio


class CompositeConfidence:
    """Combine multiple confidence calculators."""

    def __init__(self):
        """Initialize composite calculator."""
        self._calculators: List[Tuple[ConfidenceCalculator, float]] = []

    def add(
        self,
        calculator: ConfidenceCalculator,
        weight: float = 1.0,
    ) -> "CompositeConfidence":
        """Add a calculator with weight."""
        self._calculators.append((calculator, weight))
        return self

    def calculate(
        self,
        sentiment_score: float,
        **kwargs,
    ) -> ConfidenceResult:
        """Calculate combined confidence."""
        if not self._calculators:
            return ConfidenceResult(
                score=0.5,
                level="medium",
                factors={},
            )

        total_weight = sum(w for _, w in self._calculators)
        weighted_sum = 0.0
        factors = {}

        for calc, weight in self._calculators:
            score = calc.calculate(sentiment_score, **kwargs)
            weighted_sum += score * weight
            factors[calc.__class__.__name__] = score

        final_score = weighted_sum / total_weight

        if final_score >= 0.8:
            level = "high"
        elif final_score >= 0.5:
            level = "medium"
        else:
            level = "low"

        return ConfidenceResult(
            score=final_score,
            level=level,
            factors=factors,
        )


def calculate_confidence(
    sentiment_score: float,
    text: str = "",
) -> float:
    """Calculate confidence score."""
    composite = CompositeConfidence()
    composite.add(DistanceConfidence(), 0.5)
    composite.add(TextLengthConfidence(), 0.5)

    result = composite.calculate(sentiment_score, text=text)
    return result.score


def get_confidence_level(score: float) -> str:
    """Get confidence level label."""
    if score >= 0.8:
        return "high"
    elif score >= 0.5:
        return "medium"
    return "low"
