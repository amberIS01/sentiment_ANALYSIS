"""
Sampler Module

Sample and select text for analysis.
"""

from dataclasses import dataclass
from typing import List, Optional, Callable
import random


@dataclass
class Sample:
    """A text sample."""

    text: str
    index: int
    weight: float = 1.0


@dataclass
class SampleResult:
    """Result of sampling."""

    samples: List[Sample]
    total_count: int
    sample_count: int


class TextSampler:
    """Sample text for analysis."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize sampler."""
        self._random = random.Random(seed)

    def random_sample(
        self,
        texts: List[str],
        n: int,
    ) -> SampleResult:
        """Random sampling."""
        n = min(n, len(texts))
        indices = self._random.sample(range(len(texts)), n)
        
        samples = [
            Sample(text=texts[i], index=i)
            for i in indices
        ]
        
        return SampleResult(
            samples=samples,
            total_count=len(texts),
            sample_count=n,
        )

    def stratified_sample(
        self,
        texts: List[str],
        n: int,
        strata_fn: Callable[[str], str],
    ) -> SampleResult:
        """Stratified sampling."""
        strata: dict = {}
        for i, text in enumerate(texts):
            key = strata_fn(text)
            if key not in strata:
                strata[key] = []
            strata[key].append(i)

        per_stratum = max(1, n // len(strata))
        indices = []
        
        for indices_list in strata.values():
            k = min(per_stratum, len(indices_list))
            indices.extend(self._random.sample(indices_list, k))

        samples = [
            Sample(text=texts[i], index=i)
            for i in indices[:n]
        ]

        return SampleResult(
            samples=samples,
            total_count=len(texts),
            sample_count=len(samples),
        )

    def weighted_sample(
        self,
        texts: List[str],
        weights: List[float],
        n: int,
    ) -> SampleResult:
        """Weighted sampling."""
        indices = self._random.choices(
            range(len(texts)),
            weights=weights,
            k=min(n, len(texts)),
        )
        
        samples = [
            Sample(text=texts[i], index=i, weight=weights[i])
            for i in indices
        ]

        return SampleResult(
            samples=samples,
            total_count=len(texts),
            sample_count=len(samples),
        )

    def systematic_sample(
        self,
        texts: List[str],
        n: int,
    ) -> SampleResult:
        """Systematic sampling."""
        if n >= len(texts):
            indices = list(range(len(texts)))
        else:
            step = len(texts) // n
            start = self._random.randint(0, step - 1)
            indices = list(range(start, len(texts), step))[:n]

        samples = [
            Sample(text=texts[i], index=i)
            for i in indices
        ]

        return SampleResult(
            samples=samples,
            total_count=len(texts),
            sample_count=len(samples),
        )


def sample_texts(
    texts: List[str],
    n: int,
    method: str = "random",
) -> List[str]:
    """Sample texts using specified method."""
    sampler = TextSampler()
    
    if method == "random":
        result = sampler.random_sample(texts, n)
    elif method == "systematic":
        result = sampler.systematic_sample(texts, n)
    else:
        result = sampler.random_sample(texts, n)

    return [s.text for s in result.samples]
