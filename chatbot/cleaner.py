"""
Text Cleaner Module

Clean and sanitize text for analysis.
"""

import re
from dataclasses import dataclass
from typing import List, Set, Optional


@dataclass
class CleaningResult:
    """Result from text cleaning."""

    original: str
    cleaned: str
    removed_count: int
    changes: List[str]


class TextCleaner:
    """Clean text for sentiment analysis."""

    def __init__(self):
        """Initialize cleaner."""
        self._url_pattern = re.compile(r'https?://\S+|www\.\S+')
        self._email_pattern = re.compile(r'\b[\w.-]+@[\w.-]+\.\w+\b')
        self._html_pattern = re.compile(r'<[^>]+>')
        self._special_chars = re.compile(r'[^\w\s.,!?\'"-]')
        self._multiple_spaces = re.compile(r'\s+')
        self._multiple_punctuation = re.compile(r'([.,!?])\1+')

    def clean(self, text: str) -> str:
        """Apply all cleaning operations."""
        text = self.remove_html(text)
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        text = self.normalize_whitespace(text)
        text = self.normalize_punctuation(text)
        return text.strip()

    def remove_html(self, text: str) -> str:
        """Remove HTML tags."""
        return self._html_pattern.sub('', text)

    def remove_urls(self, text: str) -> str:
        """Remove URLs."""
        return self._url_pattern.sub('', text)

    def remove_emails(self, text: str) -> str:
        """Remove email addresses."""
        return self._email_pattern.sub('', text)

    def remove_special_chars(self, text: str) -> str:
        """Remove special characters."""
        return self._special_chars.sub('', text)

    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace."""
        return self._multiple_spaces.sub(' ', text)

    def normalize_punctuation(self, text: str) -> str:
        """Normalize repeated punctuation."""
        return self._multiple_punctuation.sub(r'\1', text)

    def to_lowercase(self, text: str) -> str:
        """Convert to lowercase."""
        return text.lower()

    def remove_numbers(self, text: str) -> str:
        """Remove numbers."""
        return re.sub(r'\d+', '', text)

    def clean_with_report(self, text: str) -> CleaningResult:
        """Clean text and return detailed report."""
        original = text
        changes = []
        removed = 0

        # Track changes
        if self._html_pattern.search(text):
            changes.append("removed_html")
            removed += len(self._html_pattern.findall(text))
        text = self.remove_html(text)

        if self._url_pattern.search(text):
            changes.append("removed_urls")
            removed += len(self._url_pattern.findall(text))
        text = self.remove_urls(text)

        if self._email_pattern.search(text):
            changes.append("removed_emails")
            removed += len(self._email_pattern.findall(text))
        text = self.remove_emails(text)

        if self._multiple_spaces.search(text):
            changes.append("normalized_whitespace")
        text = self.normalize_whitespace(text)

        if self._multiple_punctuation.search(text):
            changes.append("normalized_punctuation")
        text = self.normalize_punctuation(text)

        return CleaningResult(
            original=original,
            cleaned=text.strip(),
            removed_count=removed,
            changes=changes,
        )


class BatchCleaner:
    """Clean multiple texts."""

    def __init__(self, cleaner: Optional[TextCleaner] = None):
        self.cleaner = cleaner or TextCleaner()

    def clean_all(self, texts: List[str]) -> List[str]:
        """Clean a list of texts."""
        return [self.cleaner.clean(text) for text in texts]

    def clean_with_reports(self, texts: List[str]) -> List[CleaningResult]:
        """Clean texts with detailed reports."""
        return [self.cleaner.clean_with_report(text) for text in texts]


def clean_text(text: str) -> str:
    """Clean a single text."""
    cleaner = TextCleaner()
    return cleaner.clean(text)
