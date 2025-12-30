"""
Postprocessing Module

Postprocess sentiment analysis results.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Callable
from abc import ABC, abstractmethod


@dataclass
class PostprocessResult:
    """Postprocessing result."""

    original_score: float
    final_score: float
    adjustments: List[str]
    metadata: Dict[str, Any]


class PostprocessStep(ABC):
    """Base postprocessing step."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Step name."""
        pass

    @abstractmethod
    def process(
        self,
        score: float,
        text: str,
        context: Dict[str, Any],
    ) -> float:
        """Process score."""
        pass


class ClampScoreStep(PostprocessStep):
    """Clamp score to range."""

    def __init__(self, min_val: float = -1.0, max_val: float = 1.0):
        self.min_val = min_val
        self.max_val = max_val

    @property
    def name(self) -> str:
        return "clamp_score"

    def process(
        self,
        score: float,
        text: str,
        context: Dict[str, Any],
    ) -> float:
        return max(self.min_val, min(self.max_val, score))


class RoundScoreStep(PostprocessStep):
    """Round score to decimal places."""

    def __init__(self, decimals: int = 3):
        self.decimals = decimals

    @property
    def name(self) -> str:
        return "round_score"

    def process(
        self,
        score: float,
        text: str,
        context: Dict[str, Any],
    ) -> float:
        return round(score, self.decimals)


class NeutralizeSmallStep(PostprocessStep):
    """Set very small scores to neutral."""

    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold

    @property
    def name(self) -> str:
        return "neutralize_small"

    def process(
        self,
        score: float,
        text: str,
        context: Dict[str, Any],
    ) -> float:
        if abs(score) < self.threshold:
            return 0.0
        return score


class ScaleScoreStep(PostprocessStep):
    """Scale score by factor."""

    def __init__(self, factor: float = 1.0):
        self.factor = factor

    @property
    def name(self) -> str:
        return "scale_score"

    def process(
        self,
        score: float,
        text: str,
        context: Dict[str, Any],
    ) -> float:
        return score * self.factor


class ContextAdjustStep(PostprocessStep):
    """Adjust based on context."""

    def __init__(self, adjustments: Dict[str, float]):
        self.adjustments = adjustments

    @property
    def name(self) -> str:
        return "context_adjust"

    def process(
        self,
        score: float,
        text: str,
        context: Dict[str, Any],
    ) -> float:
        for key, adj in self.adjustments.items():
            if context.get(key):
                score += adj
        return score


class PostprocessPipeline:
    """Pipeline of postprocessing steps."""

    def __init__(self):
        """Initialize pipeline."""
        self._steps: List[PostprocessStep] = []

    def add_step(self, step: PostprocessStep) -> "PostprocessPipeline":
        """Add a step."""
        self._steps.append(step)
        return self

    def process(
        self,
        score: float,
        text: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> PostprocessResult:
        """Process score through pipeline."""
        ctx = context or {}
        original = score
        current = score
        adjustments = []

        for step in self._steps:
            prev = current
            current = step.process(current, text, ctx)
            if current != prev:
                adjustments.append(f"{step.name}: {prev:.3f} -> {current:.3f}")

        return PostprocessResult(
            original_score=original,
            final_score=current,
            adjustments=adjustments,
            metadata=ctx,
        )


def create_default_pipeline() -> PostprocessPipeline:
    """Create default postprocessing pipeline."""
    return (
        PostprocessPipeline()
        .add_step(ClampScoreStep())
        .add_step(NeutralizeSmallStep())
        .add_step(RoundScoreStep())
    )


def postprocess_score(score: float) -> float:
    """Postprocess score with default pipeline."""
    pipeline = create_default_pipeline()
    result = pipeline.process(score)
    return result.final_score
