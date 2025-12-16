"""
Conversation Analyzer Module

Deep analysis of conversations for insights.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from .sentiment import SentimentAnalyzer, SentimentLabel
from .emotions import EmotionDetector


@dataclass
class MessageAnalysis:
    """Analysis of a single message."""

    text: str
    sentiment_score: float
    sentiment_label: str
    emotions: List[str]
    word_count: int
    timestamp: Optional[datetime] = None


@dataclass
class ConversationInsights:
    """Insights from conversation analysis."""

    total_messages: int
    avg_sentiment: float
    sentiment_variance: float
    dominant_sentiment: str
    dominant_emotions: List[str]
    avg_message_length: float
    sentiment_shifts: int
    positive_ratio: float
    negative_ratio: float
    engagement_score: float


class ConversationAnalyzer:
    """Analyze conversations for insights."""

    def __init__(self):
        """Initialize analyzer."""
        self.sentiment_analyzer = SentimentAnalyzer()
        self.emotion_detector = EmotionDetector()

    def analyze_message(self, text: str) -> MessageAnalysis:
        """Analyze a single message."""
        sentiment = self.sentiment_analyzer.analyze(text)
        emotions = self.emotion_detector.detect(text)

        return MessageAnalysis(
            text=text,
            sentiment_score=sentiment.compound,
            sentiment_label=sentiment.label.value,
            emotions=[e.name for e in emotions.emotions],
            word_count=len(text.split()),
        )

    def analyze_conversation(
        self,
        messages: List[str],
    ) -> ConversationInsights:
        """Analyze a full conversation."""
        if not messages:
            return self._empty_insights()

        analyses = [self.analyze_message(msg) for msg in messages]

        # Calculate metrics
        scores = [a.sentiment_score for a in analyses]
        avg_sentiment = sum(scores) / len(scores)

        variance = sum((s - avg_sentiment) ** 2 for s in scores) / len(scores)

        # Count sentiments
        sentiment_counts: Dict[str, int] = {}
        for a in analyses:
            label = a.sentiment_label
            sentiment_counts[label] = sentiment_counts.get(label, 0) + 1

        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)

        # Count emotions
        emotion_counts: Dict[str, int] = {}
        for a in analyses:
            for emotion in a.emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        dominant_emotions = sorted(
            emotion_counts.keys(),
            key=lambda e: emotion_counts[e],
            reverse=True,
        )[:3]

        # Calculate ratios
        total = len(analyses)
        positive_count = sentiment_counts.get("positive", 0)
        negative_count = sentiment_counts.get("negative", 0)

        # Count sentiment shifts
        shifts = 0
        for i in range(1, len(analyses)):
            if analyses[i].sentiment_label != analyses[i-1].sentiment_label:
                shifts += 1

        # Calculate engagement score
        avg_length = sum(a.word_count for a in analyses) / total
        engagement = min(1.0, avg_length / 20)  # Normalize to 0-1

        return ConversationInsights(
            total_messages=total,
            avg_sentiment=avg_sentiment,
            sentiment_variance=variance,
            dominant_sentiment=dominant_sentiment,
            dominant_emotions=dominant_emotions,
            avg_message_length=avg_length,
            sentiment_shifts=shifts,
            positive_ratio=positive_count / total,
            negative_ratio=negative_count / total,
            engagement_score=engagement,
        )

    def _empty_insights(self) -> ConversationInsights:
        """Return empty insights for empty conversation."""
        return ConversationInsights(
            total_messages=0,
            avg_sentiment=0.0,
            sentiment_variance=0.0,
            dominant_sentiment="neutral",
            dominant_emotions=[],
            avg_message_length=0.0,
            sentiment_shifts=0,
            positive_ratio=0.0,
            negative_ratio=0.0,
            engagement_score=0.0,
        )

    def find_turning_points(
        self,
        messages: List[str],
        threshold: float = 0.3,
    ) -> List[Tuple[int, str, float]]:
        """Find significant sentiment changes in conversation."""
        if len(messages) < 2:
            return []

        analyses = [self.analyze_message(msg) for msg in messages]
        turning_points = []

        for i in range(1, len(analyses)):
            diff = abs(analyses[i].sentiment_score - analyses[i-1].sentiment_score)
            if diff >= threshold:
                turning_points.append((
                    i,
                    analyses[i].text[:50],
                    analyses[i].sentiment_score,
                ))

        return turning_points

    def summarize(self, messages: List[str]) -> str:
        """Generate a text summary of the conversation."""
        insights = self.analyze_conversation(messages)

        return (
            f"Conversation Summary:\n"
            f"- Messages: {insights.total_messages}\n"
            f"- Average Sentiment: {insights.avg_sentiment:.2f}\n"
            f"- Dominant Mood: {insights.dominant_sentiment}\n"
            f"- Top Emotions: {', '.join(insights.dominant_emotions)}\n"
            f"- Engagement: {insights.engagement_score:.1%}\n"
        )


def analyze_conversation(messages: List[str]) -> ConversationInsights:
    """Analyze a conversation and return insights."""
    analyzer = ConversationAnalyzer()
    return analyzer.analyze_conversation(messages)
