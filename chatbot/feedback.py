"""
Feedback Collector Module

Collect and analyze user feedback on sentiment analysis.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from enum import Enum


class FeedbackType(Enum):
    """Types of feedback."""

    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIALLY_CORRECT = "partially_correct"
    UNSURE = "unsure"


class FeedbackCategory(Enum):
    """Feedback categories."""

    SENTIMENT = "sentiment"
    EMOTION = "emotion"
    TOPIC = "topic"
    INTENT = "intent"
    OVERALL = "overall"


@dataclass
class FeedbackEntry:
    """A single feedback entry."""

    id: str
    text: str
    predicted_value: Any
    feedback_type: FeedbackType
    category: FeedbackCategory
    correct_value: Optional[Any] = None
    comment: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FeedbackStats:
    """Feedback statistics."""

    total_entries: int
    correct_count: int
    incorrect_count: int
    accuracy_rate: float
    by_category: Dict[str, Dict[str, int]]


class FeedbackCollector:
    """Collect and manage feedback."""

    def __init__(self):
        """Initialize collector."""
        self._entries: List[FeedbackEntry] = []
        self._counter = 0
        self._callbacks: List[Callable[[FeedbackEntry], None]] = []

    def add_feedback(
        self,
        text: str,
        predicted_value: Any,
        feedback_type: FeedbackType,
        category: FeedbackCategory = FeedbackCategory.SENTIMENT,
        correct_value: Optional[Any] = None,
        comment: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> FeedbackEntry:
        """Add a feedback entry."""
        self._counter += 1
        entry = FeedbackEntry(
            id=f"fb_{self._counter}",
            text=text,
            predicted_value=predicted_value,
            feedback_type=feedback_type,
            category=category,
            correct_value=correct_value,
            comment=comment,
            metadata=metadata or {},
        )
        self._entries.append(entry)

        for callback in self._callbacks:
            callback(entry)

        return entry

    def mark_correct(
        self,
        text: str,
        predicted_value: Any,
        category: FeedbackCategory = FeedbackCategory.SENTIMENT,
    ) -> FeedbackEntry:
        """Mark a prediction as correct."""
        return self.add_feedback(
            text=text,
            predicted_value=predicted_value,
            feedback_type=FeedbackType.CORRECT,
            category=category,
        )

    def mark_incorrect(
        self,
        text: str,
        predicted_value: Any,
        correct_value: Any,
        category: FeedbackCategory = FeedbackCategory.SENTIMENT,
        comment: Optional[str] = None,
    ) -> FeedbackEntry:
        """Mark a prediction as incorrect."""
        return self.add_feedback(
            text=text,
            predicted_value=predicted_value,
            feedback_type=FeedbackType.INCORRECT,
            category=category,
            correct_value=correct_value,
            comment=comment,
        )

    def on_feedback(self, callback: Callable[[FeedbackEntry], None]) -> None:
        """Register feedback callback."""
        self._callbacks.append(callback)

    def get_entries(
        self,
        category: Optional[FeedbackCategory] = None,
        feedback_type: Optional[FeedbackType] = None,
    ) -> List[FeedbackEntry]:
        """Get filtered feedback entries."""
        entries = self._entries
        if category:
            entries = [e for e in entries if e.category == category]
        if feedback_type:
            entries = [e for e in entries if e.feedback_type == feedback_type]
        return entries

    def get_stats(self) -> FeedbackStats:
        """Get feedback statistics."""
        total = len(self._entries)
        correct = sum(1 for e in self._entries if e.feedback_type == FeedbackType.CORRECT)
        incorrect = sum(1 for e in self._entries if e.feedback_type == FeedbackType.INCORRECT)

        by_category: Dict[str, Dict[str, int]] = {}
        for entry in self._entries:
            cat = entry.category.value
            if cat not in by_category:
                by_category[cat] = {"correct": 0, "incorrect": 0, "other": 0}
            if entry.feedback_type == FeedbackType.CORRECT:
                by_category[cat]["correct"] += 1
            elif entry.feedback_type == FeedbackType.INCORRECT:
                by_category[cat]["incorrect"] += 1
            else:
                by_category[cat]["other"] += 1

        return FeedbackStats(
            total_entries=total,
            correct_count=correct,
            incorrect_count=incorrect,
            accuracy_rate=correct / total if total > 0 else 0.0,
            by_category=by_category,
        )

    def export(self) -> List[Dict[str, Any]]:
        """Export feedback as list of dicts."""
        return [
            {
                "id": e.id,
                "text": e.text,
                "predicted": e.predicted_value,
                "feedback": e.feedback_type.value,
                "category": e.category.value,
                "correct": e.correct_value,
                "comment": e.comment,
                "created_at": e.created_at.isoformat(),
            }
            for e in self._entries
        ]

    def clear(self) -> None:
        """Clear all entries."""
        self._entries.clear()


def collect_feedback(
    text: str,
    predicted: Any,
    is_correct: bool,
) -> FeedbackEntry:
    """Simple feedback collection function."""
    collector = FeedbackCollector()
    if is_correct:
        return collector.mark_correct(text, predicted)
    return collector.mark_incorrect(text, predicted, None)
