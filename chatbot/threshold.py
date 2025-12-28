"""
Threshold Module

Manage sentiment thresholds for classification.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class SentimentCategory(Enum):
    """Sentiment categories."""

    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"


@dataclass
class ThresholdConfig:
    """Threshold configuration."""

    very_negative: float = -0.6
    negative: float = -0.2
    neutral_low: float = -0.2
    neutral_high: float = 0.2
    positive: float = 0.2
    very_positive: float = 0.6


@dataclass
class ThresholdResult:
    """Result of threshold classification."""

    score: float
    category: SentimentCategory
    confidence: float
    distance_to_boundary: float


class ThresholdClassifier:
    """Classify sentiment using thresholds."""

    def __init__(self, config: Optional[ThresholdConfig] = None):
        """Initialize classifier."""
        self.config = config or ThresholdConfig()

    def classify(self, score: float) -> ThresholdResult:
        """Classify a sentiment score."""
        config = self.config

        if score <= config.very_negative:
            category = SentimentCategory.VERY_NEGATIVE
            boundary_dist = abs(score - config.very_negative)
        elif score <= config.negative:
            category = SentimentCategory.NEGATIVE
            boundary_dist = min(
                abs(score - config.very_negative),
                abs(score - config.neutral_low),
            )
        elif score <= config.neutral_high:
            category = SentimentCategory.NEUTRAL
            boundary_dist = min(
                abs(score - config.neutral_low),
                abs(score - config.neutral_high),
            )
        elif score <= config.very_positive:
            category = SentimentCategory.POSITIVE
            boundary_dist = min(
                abs(score - config.neutral_high),
                abs(score - config.very_positive),
            )
        else:
            category = SentimentCategory.VERY_POSITIVE
            boundary_dist = abs(score - config.very_positive)

        confidence = min(1.0, boundary_dist / 0.4)

        return ThresholdResult(
            score=score,
            category=category,
            confidence=confidence,
            distance_to_boundary=boundary_dist,
        )

    def classify_many(self, scores: List[float]) -> List[ThresholdResult]:
        """Classify multiple scores."""
        return [self.classify(s) for s in scores]

    def is_positive(self, score: float) -> bool:
        """Check if score is positive."""
        return score > self.config.neutral_high

    def is_negative(self, score: float) -> bool:
        """Check if score is negative."""
        return score < self.config.neutral_low

    def is_neutral(self, score: float) -> bool:
        """Check if score is neutral."""
        return self.config.neutral_low <= score <= self.config.neutral_high

    def get_boundaries(self) -> Dict[str, float]:
        """Get all threshold boundaries."""
        return {
            "very_negative": self.config.very_negative,
            "negative": self.config.negative,
            "neutral_low": self.config.neutral_low,
            "neutral_high": self.config.neutral_high,
            "positive": self.config.positive,
            "very_positive": self.config.very_positive,
        }


def classify_sentiment(
    score: float,
    thresholds: Optional[ThresholdConfig] = None,
) -> SentimentCategory:
    """Classify a sentiment score."""
    classifier = ThresholdClassifier(thresholds)
    result = classifier.classify(score)
    return result.category


def get_category_label(category: SentimentCategory) -> str:
    """Get human-readable label for category."""
    labels = {
        SentimentCategory.VERY_NEGATIVE: "Very Negative",
        SentimentCategory.NEGATIVE: "Negative",
        SentimentCategory.NEUTRAL: "Neutral",
        SentimentCategory.POSITIVE: "Positive",
        SentimentCategory.VERY_POSITIVE: "Very Positive",
    }
    return labels.get(category, "Unknown")
