"""
Normalizer Module

Normalize sentiment scores to standard ranges.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from abc import ABC, abstractmethod


@dataclass
class NormalizationResult:
    """Result of normalization."""

    original: float
    normalized: float
    range_min: float
    range_max: float


class ScoreNormalizer(ABC):
    """Base normalizer class."""

    @abstractmethod
    def normalize(self, score: float) -> float:
        """Normalize a score."""
        pass

    @abstractmethod
    def denormalize(self, score: float) -> float:
        """Denormalize a score."""
        pass


class RangeNormalizer(ScoreNormalizer):
    """Normalize to a specific range."""

    def __init__(
        self,
        input_range: Tuple[float, float] = (-1.0, 1.0),
        output_range: Tuple[float, float] = (0.0, 1.0),
    ):
        """Initialize normalizer."""
        self.input_min, self.input_max = input_range
        self.output_min, self.output_max = output_range

    def normalize(self, score: float) -> float:
        """Normalize score to output range."""
        score = max(self.input_min, min(self.input_max, score))
        normalized = (score - self.input_min) / (self.input_max - self.input_min)
        return self.output_min + normalized * (self.output_max - self.output_min)

    def denormalize(self, score: float) -> float:
        """Denormalize score to input range."""
        score = max(self.output_min, min(self.output_max, score))
        denormalized = (score - self.output_min) / (self.output_max - self.output_min)
        return self.input_min + denormalized * (self.input_max - self.input_min)


class ZScoreNormalizer(ScoreNormalizer):
    """Z-score normalization."""

    def __init__(self, mean: float = 0.0, std: float = 1.0):
        """Initialize normalizer."""
        self.mean = mean
        self.std = std

    def normalize(self, score: float) -> float:
        """Normalize using z-score."""
        if self.std == 0:
            return 0.0
        return (score - self.mean) / self.std

    def denormalize(self, score: float) -> float:
        """Denormalize from z-score."""
        return score * self.std + self.mean

    def fit(self, scores: List[float]) -> None:
        """Fit normalizer to data."""
        if not scores:
            return
        self.mean = sum(scores) / len(scores)
        variance = sum((s - self.mean) ** 2 for s in scores) / len(scores)
        self.std = variance ** 0.5


class MinMaxNormalizer(ScoreNormalizer):
    """Min-max normalization."""

    def __init__(self, min_val: float = 0.0, max_val: float = 1.0):
        """Initialize normalizer."""
        self.min_val = min_val
        self.max_val = max_val
        self.data_min = 0.0
        self.data_max = 1.0

    def fit(self, scores: List[float]) -> None:
        """Fit to data range."""
        if scores:
            self.data_min = min(scores)
            self.data_max = max(scores)

    def normalize(self, score: float) -> float:
        """Normalize to [min_val, max_val]."""
        if self.data_max == self.data_min:
            return self.min_val
        normalized = (score - self.data_min) / (self.data_max - self.data_min)
        return self.min_val + normalized * (self.max_val - self.min_val)

    def denormalize(self, score: float) -> float:
        """Denormalize from [min_val, max_val]."""
        if self.max_val == self.min_val:
            return self.data_min
        denormalized = (score - self.min_val) / (self.max_val - self.min_val)
        return self.data_min + denormalized * (self.data_max - self.data_min)


def normalize_score(
    score: float,
    from_range: Tuple[float, float] = (-1.0, 1.0),
    to_range: Tuple[float, float] = (0.0, 1.0),
) -> float:
    """Normalize a score between ranges."""
    normalizer = RangeNormalizer(from_range, to_range)
    return normalizer.normalize(score)


def normalize_scores(
    scores: List[float],
    to_range: Tuple[float, float] = (0.0, 1.0),
) -> List[float]:
    """Normalize a list of scores."""
    if not scores:
        return []
    normalizer = MinMaxNormalizer(to_range[0], to_range[1])
    normalizer.fit(scores)
    return [normalizer.normalize(s) for s in scores]
