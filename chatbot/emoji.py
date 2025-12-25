"""
Emoji Analyzer Module

Analyze emoji sentiment in text.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import re


# Emoji sentiment mappings
POSITIVE_EMOJIS: Dict[str, float] = {
    "😀": 0.8, "😃": 0.8, "😄": 0.9, "😁": 0.8, "😆": 0.7,
    "😊": 0.8, "🙂": 0.5, "😍": 0.9, "🥰": 0.9, "😘": 0.8,
    "❤️": 0.9, "💕": 0.8, "💖": 0.9, "👍": 0.7, "👏": 0.7,
    "🎉": 0.8, "✨": 0.6, "🌟": 0.7, "💯": 0.8, "🔥": 0.6,
    "😎": 0.6, "🤗": 0.8, "😇": 0.7, "🥳": 0.9, "💪": 0.6,
}

NEGATIVE_EMOJIS: Dict[str, float] = {
    "😢": -0.7, "😭": -0.9, "😞": -0.6, "😔": -0.5, "😟": -0.5,
    "😠": -0.8, "😡": -0.9, "🤬": -1.0, "😤": -0.6, "😒": -0.5,
    "👎": -0.7, "💔": -0.8, "😱": -0.6, "😰": -0.5, "😥": -0.6,
    "🙁": -0.5, "☹️": -0.6, "😿": -0.7, "💀": -0.4, "🤮": -0.8,
}

NEUTRAL_EMOJIS: Dict[str, float] = {
    "😐": 0.0, "😑": 0.0, "🤔": 0.1, "🤷": 0.0, "😶": 0.0,
    "👀": 0.0, "🙄": -0.2, "😏": 0.1, "🤨": -0.1, "😬": -0.1,
}


@dataclass
class EmojiMatch:
    """A matched emoji."""

    emoji: str
    score: float
    position: int


@dataclass
class EmojiAnalysis:
    """Emoji analysis result."""

    emojis_found: List[EmojiMatch]
    total_count: int
    positive_count: int
    negative_count: int
    neutral_count: int
    avg_score: float
    sentiment_impact: float


class EmojiAnalyzer:
    """Analyze emoji sentiment."""

    def __init__(self):
        """Initialize analyzer."""
        self._positive = POSITIVE_EMOJIS.copy()
        self._negative = NEGATIVE_EMOJIS.copy()
        self._neutral = NEUTRAL_EMOJIS.copy()
        self._all_emojis = {
            **self._positive,
            **self._negative,
            **self._neutral,
        }

    def add_emoji(self, emoji: str, score: float) -> None:
        """Add custom emoji mapping."""
        if score > 0:
            self._positive[emoji] = score
        elif score < 0:
            self._negative[emoji] = score
        else:
            self._neutral[emoji] = score
        self._all_emojis[emoji] = score

    def find_emojis(self, text: str) -> List[EmojiMatch]:
        """Find all emojis in text."""
        matches = []
        for i, char in enumerate(text):
            if char in self._all_emojis:
                matches.append(EmojiMatch(
                    emoji=char,
                    score=self._all_emojis[char],
                    position=i,
                ))
        return matches

    def analyze(self, text: str) -> EmojiAnalysis:
        """Analyze emoji sentiment."""
        matches = self.find_emojis(text)

        if not matches:
            return EmojiAnalysis(
                emojis_found=[],
                total_count=0,
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                avg_score=0.0,
                sentiment_impact=0.0,
            )

        positive = sum(1 for m in matches if m.score > 0)
        negative = sum(1 for m in matches if m.score < 0)
        neutral = len(matches) - positive - negative
        total_score = sum(m.score for m in matches)

        return EmojiAnalysis(
            emojis_found=matches,
            total_count=len(matches),
            positive_count=positive,
            negative_count=negative,
            neutral_count=neutral,
            avg_score=total_score / len(matches),
            sentiment_impact=total_score * 0.1,
        )

    def get_score(self, text: str) -> float:
        """Get emoji sentiment score."""
        analysis = self.analyze(text)
        return analysis.avg_score

    def strip_emojis(self, text: str) -> str:
        """Remove emojis from text."""
        return "".join(c for c in text if c not in self._all_emojis)


def analyze_emojis(text: str) -> EmojiAnalysis:
    """Analyze emojis in text."""
    analyzer = EmojiAnalyzer()
    return analyzer.analyze(text)


def get_emoji_score(text: str) -> float:
    """Get emoji sentiment score."""
    analyzer = EmojiAnalyzer()
    return analyzer.get_score(text)
