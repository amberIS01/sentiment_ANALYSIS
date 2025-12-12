"""
Sentiment Analysis Module

This module provides sentiment analysis functionality using VADER
(Valence Aware Dictionary and sEntiment Reasoner) which is specifically
attuned to sentiments expressed in social media and conversational text.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


class SentimentLabel(Enum):
    """Enumeration of sentiment labels."""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


@dataclass
class SentimentResult:
    """Data class to hold sentiment analysis results."""
    label: SentimentLabel
    compound_score: float
    positive_score: float
    negative_score: float
    neutral_score: float

    def __str__(self) -> str:
        return f"{self.label.value} (score: {self.compound_score:.2f})"


@dataclass
class ConversationSentimentSummary:
    """Summary of sentiment analysis for an entire conversation."""
    overall_sentiment: SentimentLabel
    average_compound_score: float
    message_sentiments: List[Tuple[str, SentimentResult]]
    mood_trend: str
    positive_count: int
    negative_count: int
    neutral_count: int

    def __str__(self) -> str:
        trend_info = f" - {self.mood_trend}" if self.mood_trend else ""
        return f"Overall conversation sentiment: {self.overall_sentiment.value}{trend_info}"


class SentimentAnalyzer:
    """
    Sentiment analyzer using VADER for conversational text analysis.

    VADER is specifically designed for social media and conversational text,
    making it ideal for chatbot sentiment analysis. It handles:
    - Punctuation emphasis (e.g., "good!!!" vs "good")
    - Capitalization for emphasis (e.g., "GREAT" vs "great")
    - Degree modifiers (e.g., "very good" vs "good")
    - Contrastive conjunctions (e.g., "good, but not great")
    - Negations (e.g., "not good")
    - Slang and emoticons
    """

    # Thresholds for sentiment classification
    POSITIVE_THRESHOLD = 0.05
    NEGATIVE_THRESHOLD = -0.05

    def __init__(self):
        """Initialize the sentiment analyzer with VADER."""
        self._ensure_vader_lexicon()
        self._analyzer = SentimentIntensityAnalyzer()

    @staticmethod
    def _ensure_vader_lexicon():
        """Download VADER lexicon if not already available."""
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)

    def analyze_text(self, text: str) -> SentimentResult:
        """
        Analyze the sentiment of a single text message.

        Args:
            text: The text to analyze.

        Returns:
            SentimentResult containing the sentiment analysis.
        """
        scores = self._analyzer.polarity_scores(text)

        compound = scores['compound']

        if compound >= self.POSITIVE_THRESHOLD:
            label = SentimentLabel.POSITIVE
        elif compound <= self.NEGATIVE_THRESHOLD:
            label = SentimentLabel.NEGATIVE
        else:
            label = SentimentLabel.NEUTRAL

        return SentimentResult(
            label=label,
            compound_score=compound,
            positive_score=scores['pos'],
            negative_score=scores['neg'],
            neutral_score=scores['neu']
        )

    def analyze_conversation(
        self,
        messages: List[str]
    ) -> ConversationSentimentSummary:
        """
        Analyze sentiment for an entire conversation.

        Args:
            messages: List of user messages from the conversation.

        Returns:
            ConversationSentimentSummary with overall and per-message analysis.
        """
        if not messages:
            return ConversationSentimentSummary(
                overall_sentiment=SentimentLabel.NEUTRAL,
                average_compound_score=0.0,
                message_sentiments=[],
                mood_trend="No messages to analyze",
                positive_count=0,
                negative_count=0,
                neutral_count=0
            )

        # Analyze each message individually (Tier 2)
        message_sentiments: List[Tuple[str, SentimentResult]] = []
        compound_scores: List[float] = []

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for message in messages:
            result = self.analyze_text(message)
            message_sentiments.append((message, result))
            compound_scores.append(result.compound_score)

            if result.label == SentimentLabel.POSITIVE:
                positive_count += 1
            elif result.label == SentimentLabel.NEGATIVE:
                negative_count += 1
            else:
                neutral_count += 1

        # Calculate overall sentiment (Tier 1)
        avg_compound = sum(compound_scores) / len(compound_scores)

        if avg_compound >= self.POSITIVE_THRESHOLD:
            overall_sentiment = SentimentLabel.POSITIVE
        elif avg_compound <= self.NEGATIVE_THRESHOLD:
            overall_sentiment = SentimentLabel.NEGATIVE
        else:
            overall_sentiment = SentimentLabel.NEUTRAL

        # Determine mood trend (Tier 2 enhancement)
        mood_trend = self._analyze_mood_trend(compound_scores)

        return ConversationSentimentSummary(
            overall_sentiment=overall_sentiment,
            average_compound_score=avg_compound,
            message_sentiments=message_sentiments,
            mood_trend=mood_trend,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count
        )

    def _analyze_mood_trend(self, scores: List[float]) -> str:
        """
        Analyze the trend or shift in mood across the conversation.

        Args:
            scores: List of compound sentiment scores in chronological order.

        Returns:
            A string describing the mood trend.
        """
        if len(scores) < 2:
            return "Insufficient data for trend analysis"

        # Calculate the trend using first half vs second half comparison
        mid = len(scores) // 2
        first_half_avg = sum(scores[:mid]) / mid if mid > 0 else 0
        second_half_avg = sum(scores[mid:]) / (len(scores) - mid)

        diff = second_half_avg - first_half_avg

        # Also check start vs end
        start_score = scores[0]
        end_score = scores[-1]
        start_end_diff = end_score - start_score

        # Determine trend description
        if abs(diff) < 0.1 and abs(start_end_diff) < 0.1:
            return "Stable mood throughout the conversation"
        elif diff > 0.2 or start_end_diff > 0.3:
            return "Mood improved significantly during the conversation"
        elif diff > 0.1 or start_end_diff > 0.15:
            return "Slight improvement in mood over the conversation"
        elif diff < -0.2 or start_end_diff < -0.3:
            return "Mood declined significantly during the conversation"
        elif diff < -0.1 or start_end_diff < -0.15:
            return "Slight decline in mood over the conversation"
        else:
            # Check for fluctuation
            variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
            if variance > 0.2:
                return "Fluctuating mood throughout the conversation"
            return "Relatively stable mood with minor variations"
