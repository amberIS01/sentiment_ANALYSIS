"""
Language Detection Module

Simple language detection for text analysis.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from collections import Counter


@dataclass
class LanguageResult:
    """Result of language detection."""

    language: str
    confidence: float
    is_supported: bool


# Common words for language detection
LANGUAGE_MARKERS: Dict[str, List[str]] = {
    "english": [
        "the", "is", "are", "was", "were", "have", "has", "had",
        "will", "would", "could", "should", "can", "may", "might",
        "this", "that", "these", "those", "what", "which", "who",
        "how", "when", "where", "why", "and", "but", "or", "not",
    ],
    "spanish": [
        "el", "la", "los", "las", "un", "una", "de", "en", "que",
        "es", "por", "con", "para", "como", "pero", "si", "no",
        "muy", "mas", "este", "esta", "esto", "ese", "esa", "eso",
    ],
    "french": [
        "le", "la", "les", "un", "une", "de", "du", "des", "en",
        "est", "sont", "avec", "pour", "dans", "sur", "qui", "que",
        "ne", "pas", "plus", "mais", "ou", "et", "ce", "cette",
    ],
    "german": [
        "der", "die", "das", "ein", "eine", "ist", "sind", "war",
        "haben", "hat", "werden", "wird", "nicht", "auch", "auf",
        "mit", "und", "oder", "aber", "wenn", "dass", "von", "zu",
    ],
}

SUPPORTED_LANGUAGES = list(LANGUAGE_MARKERS.keys())


class LanguageDetector:
    """Detect language of text."""

    def __init__(self):
        """Initialize detector."""
        self._markers = LANGUAGE_MARKERS.copy()

    def detect(self, text: str) -> LanguageResult:
        """Detect language of text."""
        words = self._tokenize(text)
        if not words:
            return LanguageResult(
                language="unknown",
                confidence=0.0,
                is_supported=False,
            )

        scores: Dict[str, int] = {}
        for lang, markers in self._markers.items():
            marker_set = set(markers)
            score = sum(1 for w in words if w in marker_set)
            scores[lang] = score

        if not any(scores.values()):
            return LanguageResult(
                language="unknown",
                confidence=0.0,
                is_supported=False,
            )

        best_lang = max(scores, key=scores.get)
        total_markers = sum(scores.values())
        confidence = scores[best_lang] / total_markers if total_markers else 0

        return LanguageResult(
            language=best_lang,
            confidence=confidence,
            is_supported=best_lang in SUPPORTED_LANGUAGES,
        )

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase words."""
        return re.findall(r'\b[a-zA-Z]+\b', text.lower())

    def is_english(self, text: str) -> bool:
        """Check if text is in English."""
        result = self.detect(text)
        return result.language == "english" and result.confidence > 0.3

    def add_language(self, name: str, markers: List[str]) -> None:
        """Add a custom language with markers."""
        self._markers[name] = markers

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return list(self._markers.keys())


def detect_language(text: str) -> str:
    """Detect language of text."""
    detector = LanguageDetector()
    result = detector.detect(text)
    return result.language


def is_english(text: str) -> bool:
    """Check if text is in English."""
    detector = LanguageDetector()
    return detector.is_english(text)
