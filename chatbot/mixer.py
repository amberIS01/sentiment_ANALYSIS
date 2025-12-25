"""
Sentiment Mixer Module

Combine multiple sentiment scores.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from abc import ABC, abstractmethod
from enum import Enum


class MixStrategy(Enum):
    """Mixing strategies."""

    AVERAGE = "average"
    WEIGHTED = "weighted"
    MAX = "max"
    MIN = "min"
    FIRST = "first"
    LAST = "last"


@dataclass
class SentimentSource:
    """A sentiment score from a source."""

    name: str
    score: float
    confidence: float = 1.0
    weight: float = 1.0


@dataclass
class MixedSentiment:
    """Combined sentiment result."""

    final_score: float
    strategy: MixStrategy
    sources: List[SentimentSource]
    details: Dict[str, float]


class SentimentMixer(ABC):
    """Base mixer class."""

    @abstractmethod
    def mix(self, sources: List[SentimentSource]) -> float:
        """Mix sentiment scores."""
        pass


class AverageMixer(SentimentMixer):
    """Average sentiment scores."""

    def mix(self, sources: List[SentimentSource]) -> float:
        if not sources:
            return 0.0
        return sum(s.score for s in sources) / len(sources)


class WeightedMixer(SentimentMixer):
    """Weight-based mixing."""

    def mix(self, sources: List[SentimentSource]) -> float:
        if not sources:
            return 0.0
        total_weight = sum(s.weight for s in sources)
        if total_weight == 0:
            return 0.0
        return sum(s.score * s.weight for s in sources) / total_weight


class ConfidenceMixer(SentimentMixer):
    """Confidence-weighted mixing."""

    def mix(self, sources: List[SentimentSource]) -> float:
        if not sources:
            return 0.0
        total_conf = sum(s.confidence for s in sources)
        if total_conf == 0:
            return 0.0
        return sum(s.score * s.confidence for s in sources) / total_conf


class MaxMixer(SentimentMixer):
    """Take maximum sentiment."""

    def mix(self, sources: List[SentimentSource]) -> float:
        if not sources:
            return 0.0
        return max(s.score for s in sources)


class MinMixer(SentimentMixer):
    """Take minimum sentiment."""

    def mix(self, sources: List[SentimentSource]) -> float:
        if not sources:
            return 0.0
        return min(s.score for s in sources)


class SentimentCombiner:
    """Combine multiple sentiment analyses."""

    def __init__(self, strategy: MixStrategy = MixStrategy.WEIGHTED):
        """Initialize combiner."""
        self._strategy = strategy
        self._mixers: Dict[MixStrategy, SentimentMixer] = {
            MixStrategy.AVERAGE: AverageMixer(),
            MixStrategy.WEIGHTED: WeightedMixer(),
            MixStrategy.MAX: MaxMixer(),
            MixStrategy.MIN: MinMixer(),
        }

    def set_strategy(self, strategy: MixStrategy) -> None:
        """Set mixing strategy."""
        self._strategy = strategy

    def combine(
        self,
        sources: List[SentimentSource],
        strategy: Optional[MixStrategy] = None,
    ) -> MixedSentiment:
        """Combine sentiment sources."""
        strat = strategy or self._strategy

        if strat == MixStrategy.FIRST:
            final = sources[0].score if sources else 0.0
        elif strat == MixStrategy.LAST:
            final = sources[-1].score if sources else 0.0
        else:
            mixer = self._mixers.get(strat, AverageMixer())
            final = mixer.mix(sources)

        details = {s.name: s.score for s in sources}

        return MixedSentiment(
            final_score=final,
            strategy=strat,
            sources=sources,
            details=details,
        )

    def add_mixer(
        self,
        strategy: MixStrategy,
        mixer: SentimentMixer,
    ) -> None:
        """Add custom mixer."""
        self._mixers[strategy] = mixer


def mix_sentiments(
    scores: Dict[str, float],
    strategy: MixStrategy = MixStrategy.AVERAGE,
) -> float:
    """Mix sentiment scores from dict."""
    sources = [
        SentimentSource(name=name, score=score)
        for name, score in scores.items()
    ]
    combiner = SentimentCombiner(strategy)
    result = combiner.combine(sources)
    return result.final_score
