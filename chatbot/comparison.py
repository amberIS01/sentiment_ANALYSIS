"""
Sentiment Comparison Module

Compare sentiment across multiple texts or time periods.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

from .sentiment import SentimentAnalyzer, SentimentResult


class ComparisonResult(Enum):
    """Result of sentiment comparison."""

    MORE_POSITIVE = "more_positive"
    MORE_NEGATIVE = "more_negative"
    SIMILAR = "similar"


@dataclass
class SentimentDiff:
    """Difference between two sentiment analyses."""

    text1: str
    text2: str
    score1: float
    score2: float
    difference: float
    result: ComparisonResult


@dataclass
class GroupComparison:
    """Comparison of two groups of texts."""

    group1_avg: float
    group2_avg: float
    difference: float
    result: ComparisonResult
    group1_count: int
    group2_count: int


class SentimentComparator:
    """Compare sentiment between texts."""

    def __init__(self, threshold: float = 0.1):
        """Initialize comparator.

        Args:
            threshold: Minimum difference to consider significant
        """
        self.threshold = threshold
        self.analyzer = SentimentAnalyzer()

    def compare_texts(self, text1: str, text2: str) -> SentimentDiff:
        """Compare sentiment of two texts."""
        result1 = self.analyzer.analyze(text1)
        result2 = self.analyzer.analyze(text2)

        diff = result2.compound - result1.compound

        if diff > self.threshold:
            comparison = ComparisonResult.MORE_POSITIVE
        elif diff < -self.threshold:
            comparison = ComparisonResult.MORE_NEGATIVE
        else:
            comparison = ComparisonResult.SIMILAR

        return SentimentDiff(
            text1=text1,
            text2=text2,
            score1=result1.compound,
            score2=result2.compound,
            difference=diff,
            result=comparison,
        )

    def compare_groups(
        self,
        group1: List[str],
        group2: List[str],
    ) -> GroupComparison:
        """Compare average sentiment of two groups."""
        scores1 = [self.analyzer.analyze(t).compound for t in group1]
        scores2 = [self.analyzer.analyze(t).compound for t in group2]

        avg1 = sum(scores1) / len(scores1) if scores1 else 0
        avg2 = sum(scores2) / len(scores2) if scores2 else 0

        diff = avg2 - avg1

        if diff > self.threshold:
            comparison = ComparisonResult.MORE_POSITIVE
        elif diff < -self.threshold:
            comparison = ComparisonResult.MORE_NEGATIVE
        else:
            comparison = ComparisonResult.SIMILAR

        return GroupComparison(
            group1_avg=avg1,
            group2_avg=avg2,
            difference=diff,
            result=comparison,
            group1_count=len(group1),
            group2_count=len(group2),
        )

    def rank_by_sentiment(
        self,
        texts: List[str],
        ascending: bool = False,
    ) -> List[Tuple[str, float]]:
        """Rank texts by sentiment score."""
        scored = [
            (text, self.analyzer.analyze(text).compound)
            for text in texts
        ]
        return sorted(scored, key=lambda x: x[1], reverse=not ascending)

    def find_most_positive(self, texts: List[str]) -> Tuple[str, float]:
        """Find the most positive text."""
        ranked = self.rank_by_sentiment(texts, ascending=False)
        return ranked[0] if ranked else ("", 0.0)

    def find_most_negative(self, texts: List[str]) -> Tuple[str, float]:
        """Find the most negative text."""
        ranked = self.rank_by_sentiment(texts, ascending=True)
        return ranked[0] if ranked else ("", 0.0)

    def find_outliers(
        self,
        texts: List[str],
        std_threshold: float = 2.0,
    ) -> List[Tuple[str, float]]:
        """Find sentiment outliers."""
        scores = [
            (text, self.analyzer.analyze(text).compound)
            for text in texts
        ]

        if len(scores) < 3:
            return []

        values = [s[1] for s in scores]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = variance ** 0.5

        outliers = [
            (text, score)
            for text, score in scores
            if abs(score - mean) > std_threshold * std
        ]

        return outliers


def compare_sentiment(text1: str, text2: str) -> SentimentDiff:
    """Compare sentiment of two texts."""
    comparator = SentimentComparator()
    return comparator.compare_texts(text1, text2)
