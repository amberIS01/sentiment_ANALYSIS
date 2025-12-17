"""
Sentiment Keywords Module

Manage and analyze sentiment keywords.
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import re


class KeywordCategory(Enum):
    """Keyword sentiment categories."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    INTENSIFIER = "intensifier"
    NEGATION = "negation"


@dataclass
class KeywordMatch:
    """A matched keyword."""

    word: str
    category: KeywordCategory
    score: float
    position: int


# Default keyword dictionaries
POSITIVE_KEYWORDS: Dict[str, float] = {
    "love": 0.8, "excellent": 0.9, "amazing": 0.85, "wonderful": 0.8,
    "great": 0.7, "good": 0.5, "happy": 0.7, "fantastic": 0.85,
    "awesome": 0.8, "perfect": 0.9, "beautiful": 0.7, "best": 0.8,
    "brilliant": 0.85, "superb": 0.9, "outstanding": 0.9,
    "pleased": 0.6, "delighted": 0.8, "enjoy": 0.6, "like": 0.4,
}

NEGATIVE_KEYWORDS: Dict[str, float] = {
    "hate": -0.8, "terrible": -0.9, "awful": -0.85, "horrible": -0.85,
    "bad": -0.5, "poor": -0.6, "sad": -0.6, "angry": -0.7,
    "disappointed": -0.7, "worst": -0.9, "disgusting": -0.85,
    "annoying": -0.6, "frustrating": -0.7, "boring": -0.5,
    "useless": -0.7, "waste": -0.6, "ugly": -0.6, "stupid": -0.7,
}

INTENSIFIERS: Dict[str, float] = {
    "very": 1.3, "really": 1.3, "extremely": 1.5, "absolutely": 1.5,
    "totally": 1.4, "completely": 1.4, "incredibly": 1.5, "highly": 1.3,
    "super": 1.3, "so": 1.2, "quite": 1.1, "pretty": 1.1,
}

NEGATIONS: Set[str] = {
    "not", "no", "never", "neither", "nobody", "nothing",
    "nowhere", "none", "without", "hardly", "barely", "rarely",
    "don't", "doesn't", "didn't", "won't", "wouldn't", "couldn't",
    "shouldn't", "isn't", "aren't", "wasn't", "weren't",
}


class KeywordAnalyzer:
    """Analyze text for sentiment keywords."""

    def __init__(self):
        """Initialize analyzer."""
        self._positive = POSITIVE_KEYWORDS.copy()
        self._negative = NEGATIVE_KEYWORDS.copy()
        self._intensifiers = INTENSIFIERS.copy()
        self._negations = NEGATIONS.copy()

    def add_keyword(
        self,
        word: str,
        category: KeywordCategory,
        score: float = 0.5,
    ) -> None:
        """Add a custom keyword."""
        word = word.lower()
        if category == KeywordCategory.POSITIVE:
            self._positive[word] = abs(score)
        elif category == KeywordCategory.NEGATIVE:
            self._negative[word] = -abs(score)
        elif category == KeywordCategory.INTENSIFIER:
            self._intensifiers[word] = score
        elif category == KeywordCategory.NEGATION:
            self._negations.add(word)

    def find_keywords(self, text: str) -> List[KeywordMatch]:
        """Find all sentiment keywords in text."""
        words = re.findall(r'\b\w+\b', text.lower())
        matches = []

        for i, word in enumerate(words):
            if word in self._positive:
                matches.append(KeywordMatch(
                    word=word,
                    category=KeywordCategory.POSITIVE,
                    score=self._positive[word],
                    position=i,
                ))
            elif word in self._negative:
                matches.append(KeywordMatch(
                    word=word,
                    category=KeywordCategory.NEGATIVE,
                    score=self._negative[word],
                    position=i,
                ))
            elif word in self._intensifiers:
                matches.append(KeywordMatch(
                    word=word,
                    category=KeywordCategory.INTENSIFIER,
                    score=self._intensifiers[word],
                    position=i,
                ))
            elif word in self._negations:
                matches.append(KeywordMatch(
                    word=word,
                    category=KeywordCategory.NEGATION,
                    score=-1.0,
                    position=i,
                ))

        return matches

    def calculate_score(self, text: str) -> float:
        """Calculate sentiment score from keywords."""
        matches = self.find_keywords(text)
        if not matches:
            return 0.0

        score = 0.0
        negation_active = False
        intensifier = 1.0

        for match in matches:
            if match.category == KeywordCategory.NEGATION:
                negation_active = True
            elif match.category == KeywordCategory.INTENSIFIER:
                intensifier = match.score
            else:
                keyword_score = match.score * intensifier
                if negation_active:
                    keyword_score *= -0.5
                    negation_active = False
                score += keyword_score
                intensifier = 1.0

        return max(-1.0, min(1.0, score))

    def get_summary(self, text: str) -> Dict[str, any]:
        """Get keyword analysis summary."""
        matches = self.find_keywords(text)
        return {
            "total_keywords": len(matches),
            "positive_count": sum(1 for m in matches if m.category == KeywordCategory.POSITIVE),
            "negative_count": sum(1 for m in matches if m.category == KeywordCategory.NEGATIVE),
            "score": self.calculate_score(text),
            "keywords": [m.word for m in matches],
        }


def extract_keywords(text: str) -> List[str]:
    """Extract sentiment keywords from text."""
    analyzer = KeywordAnalyzer()
    matches = analyzer.find_keywords(text)
    return [m.word for m in matches]
