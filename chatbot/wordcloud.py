"""
Word Cloud Generator Module

Generate word frequency data for visualization.
"""

import re
from collections import Counter
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


# Common stop words to exclude
STOP_WORDS: Set[str] = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "as", "is", "was", "are",
    "were", "been", "be", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "must",
    "shall", "can", "need", "dare", "ought", "used", "i", "you",
    "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "this",
    "that", "these", "those", "what", "which", "who", "whom",
    "whose", "where", "when", "why", "how", "all", "each", "every",
    "both", "few", "more", "most", "other", "some", "such", "no",
    "not", "only", "same", "so", "than", "too", "very", "just",
    "also", "now", "here", "there", "then", "once", "if", "because",
    "while", "although", "though", "after", "before", "since", "until",
}


@dataclass
class WordFrequency:
    """Word frequency data."""

    word: str
    count: int
    percentage: float


class WordCloudGenerator:
    """Generate word frequency data for word clouds."""

    def __init__(
        self,
        min_length: int = 3,
        max_words: int = 100,
        exclude_stop_words: bool = True,
    ):
        """Initialize generator.

        Args:
            min_length: Minimum word length to include
            max_words: Maximum number of words to return
            exclude_stop_words: Whether to exclude common stop words
        """
        self.min_length = min_length
        self.max_words = max_words
        self.exclude_stop_words = exclude_stop_words
        self._custom_stop_words: Set[str] = set()

    def add_stop_word(self, word: str) -> None:
        """Add a custom stop word."""
        self._custom_stop_words.add(word.lower())

    def add_stop_words(self, words: List[str]) -> None:
        """Add multiple custom stop words."""
        for word in words:
            self._custom_stop_words.add(word.lower())

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return words

    def _filter_words(self, words: List[str]) -> List[str]:
        """Filter words based on criteria."""
        filtered = []
        for word in words:
            if len(word) < self.min_length:
                continue
            if self.exclude_stop_words and word in STOP_WORDS:
                continue
            if word in self._custom_stop_words:
                continue
            filtered.append(word)
        return filtered

    def generate(self, text: str) -> List[WordFrequency]:
        """Generate word frequency data from text."""
        words = self._tokenize(text)
        words = self._filter_words(words)

        if not words:
            return []

        counter = Counter(words)
        total = sum(counter.values())

        result = []
        for word, count in counter.most_common(self.max_words):
            result.append(WordFrequency(
                word=word,
                count=count,
                percentage=(count / total) * 100,
            ))

        return result

    def generate_from_messages(
        self,
        messages: List[str],
    ) -> List[WordFrequency]:
        """Generate word cloud from list of messages."""
        combined = " ".join(messages)
        return self.generate(combined)

    def to_dict(self, frequencies: List[WordFrequency]) -> Dict[str, int]:
        """Convert to simple word-count dictionary."""
        return {f.word: f.count for f in frequencies}


def generate_word_cloud(text: str, max_words: int = 50) -> List[WordFrequency]:
    """Generate word cloud data from text."""
    generator = WordCloudGenerator(max_words=max_words)
    return generator.generate(text)
