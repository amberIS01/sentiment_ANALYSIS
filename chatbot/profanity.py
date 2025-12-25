"""
Profanity Filter Module

Detect and filter profanity in text.
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Optional
import re


# Note: Using mild/example words for demonstration
PROFANITY_WORDS: Set[str] = {
    "damn", "crap", "hell", "darn", "heck",
}

# Severity levels (1-5)
PROFANITY_SEVERITY: Dict[str, int] = {
    "damn": 2,
    "crap": 2,
    "hell": 1,
    "darn": 1,
    "heck": 1,
}


@dataclass
class ProfanityMatch:
    """A detected profanity."""

    word: str
    severity: int
    position: int
    masked: str


@dataclass
class ProfanityAnalysis:
    """Profanity analysis result."""

    matches: List[ProfanityMatch]
    total_count: int
    max_severity: int
    filtered_text: str
    is_clean: bool


class ProfanityFilter:
    """Filter profanity from text."""

    def __init__(self, mask_char: str = "*"):
        """Initialize filter."""
        self._words = PROFANITY_WORDS.copy()
        self._severity = PROFANITY_SEVERITY.copy()
        self._mask_char = mask_char
        self._whitelist: Set[str] = set()

    def add_word(self, word: str, severity: int = 3) -> None:
        """Add word to filter."""
        word = word.lower()
        self._words.add(word)
        self._severity[word] = severity

    def remove_word(self, word: str) -> None:
        """Remove word from filter."""
        word = word.lower()
        self._words.discard(word)
        self._severity.pop(word, None)

    def add_whitelist(self, word: str) -> None:
        """Add word to whitelist."""
        self._whitelist.add(word.lower())

    def _mask_word(self, word: str) -> str:
        """Mask a word."""
        if len(word) <= 2:
            return self._mask_char * len(word)
        return word[0] + self._mask_char * (len(word) - 2) + word[-1]

    def detect(self, text: str) -> List[ProfanityMatch]:
        """Detect profanity in text."""
        words = re.findall(r'\b\w+\b', text.lower())
        matches = []

        for i, word in enumerate(words):
            if word in self._words and word not in self._whitelist:
                matches.append(ProfanityMatch(
                    word=word,
                    severity=self._severity.get(word, 3),
                    position=i,
                    masked=self._mask_word(word),
                ))

        return matches

    def filter(self, text: str) -> str:
        """Filter profanity from text."""
        result = text
        for word in self._words:
            if word in self._whitelist:
                continue
            pattern = re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)
            result = pattern.sub(self._mask_word(word), result)
        return result

    def analyze(self, text: str) -> ProfanityAnalysis:
        """Analyze text for profanity."""
        matches = self.detect(text)
        filtered = self.filter(text)

        return ProfanityAnalysis(
            matches=matches,
            total_count=len(matches),
            max_severity=max((m.severity for m in matches), default=0),
            filtered_text=filtered,
            is_clean=len(matches) == 0,
        )

    def is_clean(self, text: str) -> bool:
        """Check if text is clean."""
        return len(self.detect(text)) == 0

    def get_severity(self, text: str) -> int:
        """Get max severity in text."""
        matches = self.detect(text)
        return max((m.severity for m in matches), default=0)


def filter_profanity(text: str) -> str:
    """Filter profanity from text."""
    pf = ProfanityFilter()
    return pf.filter(text)


def check_profanity(text: str) -> bool:
    """Check if text contains profanity."""
    pf = ProfanityFilter()
    return not pf.is_clean(text)
