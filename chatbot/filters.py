"""
Filters Module

Filter sentiment results based on various criteria.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Callable, Any
from enum import Enum

from .sentiment import SentimentResult, SentimentLabel


class FilterOperator(Enum):
    """Filter comparison operators."""

    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_OR_EQUAL = "greater_or_equal"
    LESS_OR_EQUAL = "less_or_equal"
    IN = "in"
    NOT_IN = "not_in"


@dataclass
class FilterResult:
    """Result of filtering operation."""

    passed: bool
    reason: Optional[str] = None


class Filter(ABC):
    """Base filter class."""

    @abstractmethod
    def apply(self, result: SentimentResult) -> FilterResult:
        """Apply filter to sentiment result."""
        pass


class ScoreFilter(Filter):
    """Filter by sentiment score."""

    def __init__(
        self,
        threshold: float,
        operator: FilterOperator = FilterOperator.GREATER_THAN,
    ):
        self.threshold = threshold
        self.operator = operator

    def apply(self, result: SentimentResult) -> FilterResult:
        score = result.compound

        if self.operator == FilterOperator.GREATER_THAN:
            passed = score > self.threshold
        elif self.operator == FilterOperator.LESS_THAN:
            passed = score < self.threshold
        elif self.operator == FilterOperator.GREATER_OR_EQUAL:
            passed = score >= self.threshold
        elif self.operator == FilterOperator.LESS_OR_EQUAL:
            passed = score <= self.threshold
        elif self.operator == FilterOperator.EQUALS:
            passed = abs(score - self.threshold) < 0.001
        else:
            passed = True

        return FilterResult(
            passed=passed,
            reason=f"Score {score} {self.operator.value} {self.threshold}",
        )


class LabelFilter(Filter):
    """Filter by sentiment label."""

    def __init__(
        self,
        labels: List[SentimentLabel],
        exclude: bool = False,
    ):
        self.labels = labels
        self.exclude = exclude

    def apply(self, result: SentimentResult) -> FilterResult:
        in_labels = result.label in self.labels

        if self.exclude:
            passed = not in_labels
            reason = f"Label {result.label.value} excluded"
        else:
            passed = in_labels
            reason = f"Label {result.label.value} included"

        return FilterResult(passed=passed, reason=reason)


class CompositeFilter(Filter):
    """Combine multiple filters."""

    def __init__(self, filters: List[Filter], require_all: bool = True):
        self.filters = filters
        self.require_all = require_all

    def apply(self, result: SentimentResult) -> FilterResult:
        results = [f.apply(result) for f in self.filters]

        if self.require_all:
            passed = all(r.passed for r in results)
        else:
            passed = any(r.passed for r in results)

        return FilterResult(
            passed=passed,
            reason="Composite filter result",
        )


class FilterChain:
    """Chain of filters to apply."""

    def __init__(self):
        self._filters: List[Filter] = []

    def add(self, filter_: Filter) -> "FilterChain":
        """Add a filter to the chain."""
        self._filters.append(filter_)
        return self

    def filter(self, results: List[SentimentResult]) -> List[SentimentResult]:
        """Filter a list of results."""
        filtered = []
        for result in results:
            if all(f.apply(result).passed for f in self._filters):
                filtered.append(result)
        return filtered

    def clear(self) -> "FilterChain":
        """Clear all filters."""
        self._filters.clear()
        return self


def filter_positive(results: List[SentimentResult]) -> List[SentimentResult]:
    """Filter to only positive results."""
    return [r for r in results if r.label == SentimentLabel.POSITIVE]


def filter_negative(results: List[SentimentResult]) -> List[SentimentResult]:
    """Filter to only negative results."""
    return [r for r in results if r.label == SentimentLabel.NEGATIVE]


def filter_by_score(
    results: List[SentimentResult],
    min_score: float = -1.0,
    max_score: float = 1.0,
) -> List[SentimentResult]:
    """Filter results by score range."""
    return [r for r in results if min_score <= r.compound <= max_score]
