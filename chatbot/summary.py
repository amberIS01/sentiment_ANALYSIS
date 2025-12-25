"""
Summary Generator Module

Generate summaries from conversations and analysis.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class SummaryStats:
    """Statistics for summary."""

    total_messages: int
    avg_sentiment: float
    positive_ratio: float
    negative_ratio: float
    neutral_ratio: float
    top_emotions: List[str]
    top_topics: List[str]


@dataclass
class ConversationSummary:
    """Summary of a conversation."""

    title: str
    duration: Optional[float]
    stats: SummaryStats
    highlights: List[str]
    conclusion: str
    generated_at: datetime


class SummaryGenerator:
    """Generate conversation summaries."""

    def __init__(self):
        self._templates = {
            "positive": "The conversation was predominantly positive with an average sentiment of {avg:.2f}.",
            "negative": "The conversation had a negative tone with an average sentiment of {avg:.2f}.",
            "neutral": "The conversation was mostly neutral with an average sentiment of {avg:.2f}.",
            "mixed": "The conversation showed mixed sentiments with an average of {avg:.2f}.",
        }

    def generate(
        self,
        messages: List[str],
        sentiments: List[float],
        emotions: Optional[List[List[str]]] = None,
        topics: Optional[List[str]] = None,
    ) -> ConversationSummary:
        """Generate a conversation summary."""
        stats = self._calculate_stats(messages, sentiments, emotions, topics)
        highlights = self._extract_highlights(messages, sentiments)
        conclusion = self._generate_conclusion(stats)

        return ConversationSummary(
            title=self._generate_title(stats),
            duration=None,
            stats=stats,
            highlights=highlights,
            conclusion=conclusion,
            generated_at=datetime.now(),
        )

    def _calculate_stats(
        self,
        messages: List[str],
        sentiments: List[float],
        emotions: Optional[List[List[str]]],
        topics: Optional[List[str]],
    ) -> SummaryStats:
        """Calculate summary statistics."""
        total = len(messages)
        avg = sum(sentiments) / total if total > 0 else 0

        positive = sum(1 for s in sentiments if s > 0.05) / total if total else 0
        negative = sum(1 for s in sentiments if s < -0.05) / total if total else 0
        neutral = 1 - positive - negative

        # Get top emotions
        top_emotions = []
        if emotions:
            emotion_counts: Dict[str, int] = {}
            for emo_list in emotions:
                for emo in emo_list:
                    emotion_counts[emo] = emotion_counts.get(emo, 0) + 1
            top_emotions = sorted(emotion_counts, key=emotion_counts.get, reverse=True)[:3]

        return SummaryStats(
            total_messages=total,
            avg_sentiment=avg,
            positive_ratio=positive,
            negative_ratio=negative,
            neutral_ratio=neutral,
            top_emotions=top_emotions,
            top_topics=topics[:5] if topics else [],
        )

    def _extract_highlights(
        self,
        messages: List[str],
        sentiments: List[float],
    ) -> List[str]:
        """Extract conversation highlights."""
        if not messages:
            return []

        highlights = []

        # Find most positive message
        max_idx = sentiments.index(max(sentiments))
        highlights.append(f"Most positive: \"{messages[max_idx][:50]}...\"")

        # Find most negative message
        min_idx = sentiments.index(min(sentiments))
        if sentiments[min_idx] < 0:
            highlights.append(f"Most negative: \"{messages[min_idx][:50]}...\"")

        return highlights

    def _generate_conclusion(self, stats: SummaryStats) -> str:
        """Generate conclusion text."""
        if stats.avg_sentiment > 0.2:
            template = self._templates["positive"]
        elif stats.avg_sentiment < -0.2:
            template = self._templates["negative"]
        elif abs(stats.avg_sentiment) < 0.05:
            template = self._templates["neutral"]
        else:
            template = self._templates["mixed"]

        return template.format(avg=stats.avg_sentiment)

    def _generate_title(self, stats: SummaryStats) -> str:
        """Generate summary title."""
        if stats.avg_sentiment > 0.2:
            tone = "Positive"
        elif stats.avg_sentiment < -0.2:
            tone = "Negative"
        else:
            tone = "Neutral"

        return f"{tone} Conversation Summary ({stats.total_messages} messages)"


def summarize_conversation(
    messages: List[str],
    sentiments: List[float],
) -> str:
    """Generate a simple text summary."""
    generator = SummaryGenerator()
    summary = generator.generate(messages, sentiments)
    return summary.conclusion
