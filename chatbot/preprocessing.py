"""
Preprocessing Module

Text preprocessing pipeline for sentiment analysis.
"""

from dataclasses import dataclass
from typing import List, Optional, Callable
from abc import ABC, abstractmethod
import re


@dataclass
class PreprocessResult:
    """Preprocessing result."""

    original: str
    processed: str
    steps_applied: List[str]


class PreprocessStep(ABC):
    """Base preprocessing step."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Step name."""
        pass

    @abstractmethod
    def process(self, text: str) -> str:
        """Process text."""
        pass


class LowercaseStep(PreprocessStep):
    """Convert to lowercase."""

    @property
    def name(self) -> str:
        return "lowercase"

    def process(self, text: str) -> str:
        return text.lower()


class StripWhitespaceStep(PreprocessStep):
    """Strip extra whitespace."""

    @property
    def name(self) -> str:
        return "strip_whitespace"

    def process(self, text: str) -> str:
        return " ".join(text.split())


class RemovePunctuationStep(PreprocessStep):
    """Remove punctuation."""

    def __init__(self, keep: str = ""):
        self.keep = keep

    @property
    def name(self) -> str:
        return "remove_punctuation"

    def process(self, text: str) -> str:
        pattern = f"[^\\w\\s{re.escape(self.keep)}]"
        return re.sub(pattern, "", text)


class RemoveNumbersStep(PreprocessStep):
    """Remove numbers."""

    @property
    def name(self) -> str:
        return "remove_numbers"

    def process(self, text: str) -> str:
        return re.sub(r"\d+", "", text)


class RemoveUrlsStep(PreprocessStep):
    """Remove URLs."""

    @property
    def name(self) -> str:
        return "remove_urls"

    def process(self, text: str) -> str:
        return re.sub(r"https?://\S+|www\.\S+", "", text)


class RemoveEmailsStep(PreprocessStep):
    """Remove email addresses."""

    @property
    def name(self) -> str:
        return "remove_emails"

    def process(self, text: str) -> str:
        return re.sub(r"\S+@\S+", "", text)


class RemoveHtmlStep(PreprocessStep):
    """Remove HTML tags."""

    @property
    def name(self) -> str:
        return "remove_html"

    def process(self, text: str) -> str:
        return re.sub(r"<[^>]+>", "", text)


class PreprocessPipeline:
    """Pipeline of preprocessing steps."""

    def __init__(self):
        """Initialize pipeline."""
        self._steps: List[PreprocessStep] = []

    def add_step(self, step: PreprocessStep) -> "PreprocessPipeline":
        """Add a step."""
        self._steps.append(step)
        return self

    def remove_step(self, name: str) -> bool:
        """Remove a step by name."""
        for i, step in enumerate(self._steps):
            if step.name == name:
                self._steps.pop(i)
                return True
        return False

    def process(self, text: str) -> PreprocessResult:
        """Process text through pipeline."""
        original = text
        current = text
        steps_applied = []

        for step in self._steps:
            current = step.process(current)
            steps_applied.append(step.name)

        return PreprocessResult(
            original=original,
            processed=current,
            steps_applied=steps_applied,
        )

    def process_many(self, texts: List[str]) -> List[PreprocessResult]:
        """Process multiple texts."""
        return [self.process(t) for t in texts]


def create_default_pipeline() -> PreprocessPipeline:
    """Create default preprocessing pipeline."""
    return (
        PreprocessPipeline()
        .add_step(RemoveHtmlStep())
        .add_step(RemoveUrlsStep())
        .add_step(RemoveEmailsStep())
        .add_step(StripWhitespaceStep())
    )


def preprocess_text(text: str) -> str:
    """Preprocess text with default pipeline."""
    pipeline = create_default_pipeline()
    result = pipeline.process(text)
    return result.processed
