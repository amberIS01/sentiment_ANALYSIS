"""
Context Analyzer Module

Analyze sentiment in context.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class ContextType(Enum):
    """Types of context."""

    GENERAL = "general"
    BUSINESS = "business"
    CASUAL = "casual"
    TECHNICAL = "technical"
    EMOTIONAL = "emotional"


@dataclass
class ContextWindow:
    """A window of context."""

    texts: List[str]
    sentiments: List[float]
    window_size: int = 5


@dataclass
class ContextualSentiment:
    """Sentiment with context."""

    text: str
    raw_score: float
    contextual_score: float
    context_type: ContextType
    context_weight: float
    adjustment: float


class ContextAnalyzer:
    """Analyze sentiment with context."""

    def __init__(self, window_size: int = 5):
        """Initialize analyzer."""
        self._window_size = window_size
        self._history: List[float] = []
        self._context_type = ContextType.GENERAL
        self._modifiers: Dict[ContextType, float] = {
            ContextType.GENERAL: 1.0,
            ContextType.BUSINESS: 0.8,
            ContextType.CASUAL: 1.2,
            ContextType.TECHNICAL: 0.7,
            ContextType.EMOTIONAL: 1.5,
        }

    def set_context(self, context_type: ContextType) -> None:
        """Set context type."""
        self._context_type = context_type

    def add_to_history(self, score: float) -> None:
        """Add score to history."""
        self._history.append(score)
        if len(self._history) > self._window_size:
            self._history.pop(0)

    def get_context_average(self) -> float:
        """Get average sentiment from context."""
        if not self._history:
            return 0.0
        return sum(self._history) / len(self._history)

    def analyze(
        self,
        text: str,
        raw_score: float,
    ) -> ContextualSentiment:
        """Analyze sentiment with context."""
        context_avg = self.get_context_average()
        modifier = self._modifiers[self._context_type]

        # Blend with context
        if self._history:
            context_weight = min(len(self._history) / self._window_size, 1.0)
            blended = raw_score * (1 - context_weight * 0.3) + context_avg * context_weight * 0.3
        else:
            blended = raw_score
            context_weight = 0.0

        # Apply context modifier
        adjusted = blended * modifier
        adjusted = max(-1.0, min(1.0, adjusted))

        self.add_to_history(raw_score)

        return ContextualSentiment(
            text=text,
            raw_score=raw_score,
            contextual_score=adjusted,
            context_type=self._context_type,
            context_weight=context_weight,
            adjustment=adjusted - raw_score,
        )

    def reset(self) -> None:
        """Reset context history."""
        self._history.clear()

    def get_trend(self) -> str:
        """Get sentiment trend."""
        if len(self._history) < 2:
            return "stable"

        first_half = self._history[:len(self._history) // 2]
        second_half = self._history[len(self._history) // 2:]

        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)

        diff = second_avg - first_avg
        if diff > 0.1:
            return "improving"
        elif diff < -0.1:
            return "declining"
        return "stable"


@dataclass
class ConversationContext:
    """Track conversation context."""

    messages: List[str] = field(default_factory=list)
    sentiments: List[float] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    context_type: ContextType = ContextType.GENERAL

    def add_message(
        self,
        message: str,
        sentiment: float,
        topic: Optional[str] = None,
    ) -> None:
        """Add message to context."""
        self.messages.append(message)
        self.sentiments.append(sentiment)
        if topic:
            self.topics.append(topic)

    def get_summary(self) -> Dict[str, Any]:
        """Get context summary."""
        return {
            "message_count": len(self.messages),
            "avg_sentiment": sum(self.sentiments) / len(self.sentiments) if self.sentiments else 0,
            "topics": list(set(self.topics)),
            "context_type": self.context_type.value,
        }


def analyze_with_context(
    text: str,
    score: float,
    history: List[float],
) -> float:
    """Analyze sentiment with historical context."""
    analyzer = ContextAnalyzer()
    for h in history:
        analyzer.add_to_history(h)
    result = analyzer.analyze(text, score)
    return result.contextual_score
