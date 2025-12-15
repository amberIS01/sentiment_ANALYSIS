"""
Text Preprocessor Module

Provides text preprocessing utilities for sentiment analysis.
"""

import re
from typing import List, Optional


class TextPreprocessor:
    """Text preprocessing for sentiment analysis."""

    def __init__(self):
        """Initialize preprocessor."""
        self._url_pattern = re.compile(
            r'https?://\S+|www\.\S+'
        )
        self._email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        self._mention_pattern = re.compile(r'@\w+')
        self._hashtag_pattern = re.compile(r'#\w+')
        self._emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF'
            r'\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+'
        )

    def clean(self, text: str) -> str:
        """Clean text by removing noise."""
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.normalize_whitespace(text)
        return text.strip()

    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return self._url_pattern.sub('', text)

    def remove_emails(self, text: str) -> str:
        """Remove email addresses from text."""
        return self._email_pattern.sub('', text)

    def remove_mentions(self, text: str) -> str:
        """Remove @mentions from text."""
        return self._mention_pattern.sub('', text)

    def remove_hashtags(self, text: str) -> str:
        """Remove hashtags from text."""
        return self._hashtag_pattern.sub('', text)

    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text."""
        return self._hashtag_pattern.findall(text)

    def extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text."""
        return self._mention_pattern.findall(text)

    def extract_emojis(self, text: str) -> List[str]:
        """Extract emojis from text."""
        return self._emoji_pattern.findall(text)

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text."""
        return re.sub(r'\s+', ' ', text)

    def lowercase(self, text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()

    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation from text."""
        return re.sub(r'[^\w\s]', '', text)

    def expand_contractions(self, text: str) -> str:
        """Expand common contractions."""
        contractions = {
            "don't": "do not",
            "won't": "will not",
            "can't": "cannot",
            "i'm": "i am",
            "you're": "you are",
            "it's": "it is",
            "that's": "that is",
            "there's": "there is",
            "we're": "we are",
            "they're": "they are",
            "i've": "i have",
            "you've": "you have",
            "we've": "we have",
            "they've": "they have",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "haven't": "have not",
            "hasn't": "has not",
            "hadn't": "had not",
            "doesn't": "does not",
            "didn't": "did not",
            "wouldn't": "would not",
            "shouldn't": "should not",
            "couldn't": "could not",
        }
        text_lower = text.lower()
        for contraction, expansion in contractions.items():
            text_lower = text_lower.replace(contraction, expansion)
        return text_lower


def preprocess(text: str, remove_urls: bool = True) -> str:
    """Preprocess text for sentiment analysis."""
    preprocessor = TextPreprocessor()
    if remove_urls:
        text = preprocessor.remove_urls(text)
    return preprocessor.normalize_whitespace(text).strip()
