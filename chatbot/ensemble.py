"""
Ensemble Module

Ensemble methods for sentiment analysis.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable, Any
from abc import ABC, abstractmethod


@dataclass
class EnsemblePrediction:
    """Ensemble prediction result."""

    final_score: float
    individual_scores: Dict[str, float]
    confidence: float
    method: str


class BaseAnalyzer(ABC):
    """Base analyzer interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Analyzer name."""
        pass

    @abstractmethod
    def analyze(self, text: str) -> float:
        """Analyze text and return score."""
        pass


class EnsembleMethod(ABC):
    """Base ensemble method."""

    @abstractmethod
    def combine(self, scores: List[float], weights: List[float]) -> float:
        """Combine scores."""
        pass


class AverageEnsemble(EnsembleMethod):
    """Simple average ensemble."""

    def combine(self, scores: List[float], weights: List[float]) -> float:
        if not scores:
            return 0.0
        return sum(scores) / len(scores)


class WeightedEnsemble(EnsembleMethod):
    """Weighted average ensemble."""

    def combine(self, scores: List[float], weights: List[float]) -> float:
        if not scores:
            return 0.0
        total_weight = sum(weights)
        if total_weight == 0:
            return sum(scores) / len(scores)
        return sum(s * w for s, w in zip(scores, weights)) / total_weight


class VotingEnsemble(EnsembleMethod):
    """Voting-based ensemble."""

    def combine(self, scores: List[float], weights: List[float]) -> float:
        if not scores:
            return 0.0
        
        positive = sum(1 for s in scores if s > 0)
        negative = sum(1 for s in scores if s < 0)
        
        if positive > negative:
            return sum(s for s in scores if s > 0) / max(1, positive)
        elif negative > positive:
            return sum(s for s in scores if s < 0) / max(1, negative)
        return 0.0


class MaxConfidenceEnsemble(EnsembleMethod):
    """Use prediction with highest confidence."""

    def combine(self, scores: List[float], weights: List[float]) -> float:
        if not scores:
            return 0.0
        
        max_conf_idx = 0
        max_conf = abs(scores[0])
        
        for i, score in enumerate(scores):
            if abs(score) > max_conf:
                max_conf = abs(score)
                max_conf_idx = i
        
        return scores[max_conf_idx]


class SentimentEnsemble:
    """Ensemble of sentiment analyzers."""

    def __init__(self, method: Optional[EnsembleMethod] = None):
        """Initialize ensemble."""
        self._analyzers: List[tuple] = []
        self._method = method or WeightedEnsemble()

    def add_analyzer(
        self,
        analyzer: Callable[[str], float],
        name: str,
        weight: float = 1.0,
    ) -> "SentimentEnsemble":
        """Add an analyzer."""
        self._analyzers.append((analyzer, name, weight))
        return self

    def set_method(self, method: EnsembleMethod) -> None:
        """Set ensemble method."""
        self._method = method

    def predict(self, text: str) -> EnsemblePrediction:
        """Make ensemble prediction."""
        scores = []
        weights = []
        individual = {}

        for analyzer, name, weight in self._analyzers:
            score = analyzer(text)
            scores.append(score)
            weights.append(weight)
            individual[name] = score

        final = self._method.combine(scores, weights)
        
        # Calculate confidence from agreement
        if scores:
            variance = sum((s - final) ** 2 for s in scores) / len(scores)
            confidence = max(0.0, 1.0 - (variance ** 0.5))
        else:
            confidence = 0.0

        return EnsemblePrediction(
            final_score=final,
            individual_scores=individual,
            confidence=confidence,
            method=self._method.__class__.__name__,
        )


def create_ensemble(
    analyzers: List[Callable[[str], float]],
    method: str = "weighted",
) -> SentimentEnsemble:
    """Create an ensemble from analyzers."""
    methods = {
        "average": AverageEnsemble(),
        "weighted": WeightedEnsemble(),
        "voting": VotingEnsemble(),
        "max_confidence": MaxConfidenceEnsemble(),
    }
    
    ensemble = SentimentEnsemble(methods.get(method, WeightedEnsemble()))
    
    for i, analyzer in enumerate(analyzers):
        ensemble.add_analyzer(analyzer, f"analyzer_{i}")
    
    return ensemble
