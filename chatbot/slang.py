"""
Slang Detector Module

Detect and normalize slang in text.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import re


# Common slang mappings
SLANG_MAPPINGS: Dict[str, str] = {
    "lol": "laughing out loud",
    "lmao": "laughing",
    "rofl": "laughing",
    "omg": "oh my god",
    "wtf": "what the",
    "btw": "by the way",
    "imo": "in my opinion",
    "imho": "in my humble opinion",
    "idk": "i do not know",
    "tbh": "to be honest",
    "ngl": "not going to lie",
    "smh": "shaking my head",
    "fomo": "fear of missing out",
    "yolo": "you only live once",
    "goat": "greatest of all time",
    "lit": "exciting",
    "salty": "upset",
    "slay": "doing great",
    "lowkey": "kind of",
    "highkey": "very much",
    "sus": "suspicious",
    "vibe": "feeling",
    "mood": "relatable",
    "fire": "amazing",
    "cap": "lie",
    "bet": "okay",
    "flex": "show off",
    "ghosted": "ignored",
    "tea": "gossip",
    "stan": "big fan",
}

# Slang sentiment scores
SLANG_SENTIMENTS: Dict[str, float] = {
    "lol": 0.3,
    "lmao": 0.4,
    "rofl": 0.5,
    "omg": 0.2,
    "lit": 0.7,
    "fire": 0.8,
    "slay": 0.8,
    "goat": 0.9,
    "salty": -0.5,
    "sus": -0.3,
    "cap": -0.2,
    "ghosted": -0.6,
}


@dataclass
class SlangMatch:
    """A detected slang term."""

    term: str
    normalized: str
    sentiment: Optional[float]
    position: int


@dataclass
class SlangAnalysis:
    """Slang analysis result."""

    matches: List[SlangMatch]
    total_count: int
    normalized_text: str
    sentiment_adjustment: float


class SlangDetector:
    """Detect and normalize slang."""

    def __init__(self):
        """Initialize detector."""
        self._mappings = SLANG_MAPPINGS.copy()
        self._sentiments = SLANG_SENTIMENTS.copy()

    def add_slang(
        self,
        term: str,
        normalized: str,
        sentiment: Optional[float] = None,
    ) -> None:
        """Add custom slang mapping."""
        term = term.lower()
        self._mappings[term] = normalized
        if sentiment is not None:
            self._sentiments[term] = sentiment

    def detect(self, text: str) -> List[SlangMatch]:
        """Detect slang in text."""
        words = re.findall(r'\b\w+\b', text.lower())
        matches = []

        for i, word in enumerate(words):
            if word in self._mappings:
                matches.append(SlangMatch(
                    term=word,
                    normalized=self._mappings[word],
                    sentiment=self._sentiments.get(word),
                    position=i,
                ))

        return matches

    def normalize(self, text: str) -> str:
        """Normalize slang in text."""
        result = text
        for term, normalized in self._mappings.items():
            pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
            result = pattern.sub(normalized, result)
        return result

    def analyze(self, text: str) -> SlangAnalysis:
        """Analyze slang in text."""
        matches = self.detect(text)
        normalized = self.normalize(text)

        sentiment_adj = sum(
            m.sentiment for m in matches
            if m.sentiment is not None
        ) * 0.1

        return SlangAnalysis(
            matches=matches,
            total_count=len(matches),
            normalized_text=normalized,
            sentiment_adjustment=sentiment_adj,
        )

    def get_known_slang(self) -> Set[str]:
        """Get all known slang terms."""
        return set(self._mappings.keys())


def detect_slang(text: str) -> List[SlangMatch]:
    """Detect slang in text."""
    detector = SlangDetector()
    return detector.detect(text)


def normalize_slang(text: str) -> str:
    """Normalize slang in text."""
    detector = SlangDetector()
    return detector.normalize(text)
