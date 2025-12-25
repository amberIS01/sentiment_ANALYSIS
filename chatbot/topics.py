"""
Topic Extractor Module

Extract topics from text.
"""

from dataclasses import dataclass
from typing import List, Dict, Set, Optional
from collections import Counter
import re


@dataclass
class Topic:
    """An extracted topic."""

    name: str
    frequency: int
    relevance: float


@dataclass
class TopicResult:
    """Result of topic extraction."""

    topics: List[Topic]
    keywords: List[str]
    category: Optional[str]


# Common stop words
STOP_WORDS: Set[str] = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
    "be", "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "i", "you",
    "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their", "this", "that", "these",
    "those", "what", "which", "who", "whom", "whose", "where", "when",
    "why", "how", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "no", "not", "only", "same", "so", "than",
    "too", "very", "just", "also", "now", "here", "there", "then",
}

# Topic categories
TOPIC_CATEGORIES: Dict[str, List[str]] = {
    "technology": ["software", "computer", "app", "website", "tech", "digital"],
    "business": ["company", "market", "customer", "service", "product", "sales"],
    "health": ["health", "medical", "doctor", "patient", "treatment", "disease"],
    "education": ["school", "student", "teacher", "learning", "education", "course"],
    "entertainment": ["movie", "music", "game", "show", "entertainment", "fun"],
    "sports": ["sport", "team", "player", "game", "match", "win"],
    "travel": ["travel", "trip", "hotel", "flight", "vacation", "destination"],
    "food": ["food", "restaurant", "meal", "cooking", "recipe", "taste"],
}


class TopicExtractor:
    """Extract topics from text."""

    def __init__(self, min_frequency: int = 1, max_topics: int = 10):
        self.min_frequency = min_frequency
        self.max_topics = max_topics
        self._stop_words = STOP_WORDS.copy()

    def extract(self, text: str) -> TopicResult:
        """Extract topics from text."""
        words = self._tokenize(text)
        word_counts = Counter(words)

        # Filter by frequency
        topics = []
        for word, count in word_counts.most_common(self.max_topics):
            if count >= self.min_frequency:
                relevance = count / len(words) if words else 0
                topics.append(Topic(
                    name=word,
                    frequency=count,
                    relevance=relevance,
                ))

        # Get keywords
        keywords = [t.name for t in topics[:5]]

        # Determine category
        category = self._detect_category(text)

        return TopicResult(
            topics=topics,
            keywords=keywords,
            category=category,
        )

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize and filter text."""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return [w for w in words if w not in self._stop_words]

    def _detect_category(self, text: str) -> Optional[str]:
        """Detect topic category."""
        text_lower = text.lower()
        scores: Dict[str, int] = {}

        for category, keywords in TOPIC_CATEGORIES.items():
            score = sum(1 for k in keywords if k in text_lower)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)
        return None

    def add_stop_word(self, word: str) -> None:
        """Add a stop word."""
        self._stop_words.add(word.lower())

    def extract_from_multiple(self, texts: List[str]) -> TopicResult:
        """Extract topics from multiple texts."""
        combined = " ".join(texts)
        return self.extract(combined)


def extract_topics(text: str, max_topics: int = 5) -> List[str]:
    """Extract topic keywords from text."""
    extractor = TopicExtractor(max_topics=max_topics)
    result = extractor.extract(text)
    return result.keywords
