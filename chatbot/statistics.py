"""
Conversation Statistics Module

This module provides comprehensive statistics tracking and analysis
for chatbot conversations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, TYPE_CHECKING
import statistics as stats

if TYPE_CHECKING:
    from .conversation import ConversationManager, Message
    from .sentiment import SentimentResult


@dataclass
class MessageStatistics:
    """Statistics for a single message."""

    word_count: int
    character_count: int
    sentence_count: int
    average_word_length: float


@dataclass
class ConversationStatistics:
    """Comprehensive statistics for a conversation."""

    # Message counts
    total_messages: int
    user_messages: int
    bot_messages: int

    # Timing
    duration: timedelta
    average_response_time: Optional[timedelta]

    # Content statistics
    total_words: int
    total_characters: int
    average_message_length: float
    longest_message_length: int
    shortest_message_length: int

    # Sentiment statistics
    sentiment_distribution: Dict[str, int]
    average_sentiment_score: float
    sentiment_variance: float
    most_positive_message: Optional[str]
    most_negative_message: Optional[str]

    # Engagement metrics
    messages_per_minute: float
    user_engagement_ratio: float

    def __str__(self) -> str:
        lines = [
            "Conversation Statistics",
            "=" * 40,
            f"Total Messages: {self.total_messages}",
            f"  User: {self.user_messages}",
            f"  Bot: {self.bot_messages}",
            f"Duration: {self._format_duration(self.duration)}",
            f"Total Words: {self.total_words}",
            f"Avg Message Length: {self.average_message_length:.1f} chars",
            f"Avg Sentiment: {self.average_sentiment_score:.2f}",
            f"Messages/Min: {self.messages_per_minute:.2f}",
        ]
        return "\n".join(lines)

    @staticmethod
    def _format_duration(duration: timedelta) -> str:
        """Format duration for display."""
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"


class StatisticsTracker:
    """
    Track and calculate conversation statistics.

    Provides real-time and post-conversation statistics
    for monitoring and analysis.
    """

    def __init__(self):
        """Initialize the statistics tracker."""
        self._message_timestamps: List[datetime] = []
        self._response_times: List[timedelta] = []
        self._last_user_message_time: Optional[datetime] = None

    def record_message(self, timestamp: datetime, is_user: bool) -> None:
        """
        Record a message timestamp.

        Args:
            timestamp: When the message was sent.
            is_user: Whether this is a user message.
        """
        self._message_timestamps.append(timestamp)

        if is_user:
            self._last_user_message_time = timestamp
        elif self._last_user_message_time:
            response_time = timestamp - self._last_user_message_time
            self._response_times.append(response_time)
            self._last_user_message_time = None

    def get_average_response_time(self) -> Optional[timedelta]:
        """Get average bot response time."""
        if not self._response_times:
            return None

        total_seconds = sum(rt.total_seconds() for rt in self._response_times)
        avg_seconds = total_seconds / len(self._response_times)
        return timedelta(seconds=avg_seconds)

    def calculate_statistics(
        self,
        conversation: "ConversationManager",
    ) -> ConversationStatistics:
        """
        Calculate comprehensive statistics for a conversation.

        Args:
            conversation: The conversation manager.

        Returns:
            ConversationStatistics with all metrics.
        """
        messages = conversation.messages
        user_messages = conversation.user_messages
        bot_messages = conversation.bot_messages

        # Basic counts
        total_messages = len(messages)
        user_count = len(user_messages)
        bot_count = len(bot_messages)

        # Handle empty conversation
        if total_messages == 0:
            return ConversationStatistics(
                total_messages=0,
                user_messages=0,
                bot_messages=0,
                duration=timedelta(0),
                average_response_time=None,
                total_words=0,
                total_characters=0,
                average_message_length=0.0,
                longest_message_length=0,
                shortest_message_length=0,
                sentiment_distribution={},
                average_sentiment_score=0.0,
                sentiment_variance=0.0,
                most_positive_message=None,
                most_negative_message=None,
                messages_per_minute=0.0,
                user_engagement_ratio=0.0,
            )

        # Duration
        first_msg = messages[0].timestamp
        last_msg = messages[-1].timestamp
        duration = last_msg - first_msg

        # Content statistics
        all_contents = [m.content for m in messages]
        word_counts = [len(c.split()) for c in all_contents]
        char_counts = [len(c) for c in all_contents]

        total_words = sum(word_counts)
        total_chars = sum(char_counts)
        avg_length = total_chars / total_messages if total_messages > 0 else 0.0

        # Sentiment statistics
        sentiment_dist: Dict[str, int] = {"Positive": 0, "Negative": 0, "Neutral": 0}
        sentiment_scores: List[float] = []
        most_positive: Optional[tuple] = None
        most_negative: Optional[tuple] = None

        for msg in user_messages:
            if msg.sentiment:
                label = msg.sentiment.label.value
                sentiment_dist[label] = sentiment_dist.get(label, 0) + 1
                score = msg.sentiment.compound_score
                sentiment_scores.append(score)

                if most_positive is None or score > most_positive[0]:
                    most_positive = (score, msg.content)
                if most_negative is None or score < most_negative[0]:
                    most_negative = (score, msg.content)

        avg_sentiment = (
            sum(sentiment_scores) / len(sentiment_scores)
            if sentiment_scores
            else 0.0
        )

        sentiment_var = (
            stats.variance(sentiment_scores)
            if len(sentiment_scores) > 1
            else 0.0
        )

        # Engagement metrics
        duration_minutes = duration.total_seconds() / 60
        messages_per_min = (
            total_messages / duration_minutes
            if duration_minutes > 0
            else total_messages
        )

        engagement_ratio = user_count / total_messages if total_messages > 0 else 0.0

        return ConversationStatistics(
            total_messages=total_messages,
            user_messages=user_count,
            bot_messages=bot_count,
            duration=duration,
            average_response_time=self.get_average_response_time(),
            total_words=total_words,
            total_characters=total_chars,
            average_message_length=avg_length,
            longest_message_length=max(char_counts) if char_counts else 0,
            shortest_message_length=min(char_counts) if char_counts else 0,
            sentiment_distribution=sentiment_dist,
            average_sentiment_score=avg_sentiment,
            sentiment_variance=sentiment_var,
            most_positive_message=most_positive[1] if most_positive else None,
            most_negative_message=most_negative[1] if most_negative else None,
            messages_per_minute=messages_per_min,
            user_engagement_ratio=engagement_ratio,
        )

    def get_sentiment_trend(
        self,
        messages: List["Message"],
        window_size: int = 3,
    ) -> List[float]:
        """
        Calculate rolling average sentiment trend.

        Args:
            messages: List of messages with sentiment.
            window_size: Size of rolling window.

        Returns:
            List of rolling average sentiment scores.
        """
        scores = [
            m.sentiment.compound_score
            for m in messages
            if m.sentiment is not None
        ]

        if len(scores) < window_size:
            return scores

        trend = []
        for i in range(len(scores) - window_size + 1):
            window = scores[i : i + window_size]
            trend.append(sum(window) / len(window))

        return trend

    def reset(self) -> None:
        """Reset all tracked statistics."""
        self._message_timestamps.clear()
        self._response_times.clear()
        self._last_user_message_time = None


def analyze_message(content: str) -> MessageStatistics:
    """
    Analyze a single message.

    Args:
        content: The message content.

    Returns:
        MessageStatistics for the message.
    """
    words = content.split()
    word_count = len(words)
    char_count = len(content)

    # Simple sentence detection
    sentence_count = content.count(".") + content.count("!") + content.count("?")
    sentence_count = max(1, sentence_count)

    avg_word_length = (
        sum(len(w) for w in words) / word_count
        if word_count > 0
        else 0.0
    )

    return MessageStatistics(
        word_count=word_count,
        character_count=char_count,
        sentence_count=sentence_count,
        average_word_length=avg_word_length,
    )
