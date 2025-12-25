"""
Tests for the Language Module.
"""

import pytest

from chatbot.language import (
    LanguageDetector,
    LanguageResult,
    detect_language,
    is_english,
    SUPPORTED_LANGUAGES,
)


class TestLanguageResult:
    """Test LanguageResult dataclass."""

    def test_creation(self):
        result = LanguageResult(
            language="english",
            confidence=0.8,
            is_supported=True,
        )
        assert result.language == "english"
        assert result.confidence == 0.8


class TestLanguageDetector:
    """Test LanguageDetector class."""

    def test_initialization(self):
        detector = LanguageDetector()
        assert detector is not None

    def test_detect_english(self):
        detector = LanguageDetector()
        result = detector.detect("The quick brown fox jumps over the lazy dog")
        assert result.language == "english"
        assert result.is_supported is True

    def test_detect_spanish(self):
        detector = LanguageDetector()
        result = detector.detect("El gato es muy bonito y grande")
        assert result.language == "spanish"

    def test_detect_french(self):
        detector = LanguageDetector()
        result = detector.detect("Je suis un homme et elle est une femme")
        assert result.language == "french"

    def test_detect_german(self):
        detector = LanguageDetector()
        result = detector.detect("Das ist ein gutes Buch und der Mann ist hier")
        assert result.language == "german"

    def test_detect_empty(self):
        detector = LanguageDetector()
        result = detector.detect("")
        assert result.language == "unknown"
        assert result.confidence == 0.0

    def test_is_english_true(self):
        detector = LanguageDetector()
        assert detector.is_english("This is an English sentence") is True

    def test_is_english_false(self):
        detector = LanguageDetector()
        assert detector.is_english("Das ist Deutsch") is False

    def test_add_language(self):
        detector = LanguageDetector()
        detector.add_language("italian", ["il", "la", "di", "che", "sono"])
        languages = detector.get_supported_languages()
        assert "italian" in languages

    def test_get_supported_languages(self):
        detector = LanguageDetector()
        languages = detector.get_supported_languages()
        assert "english" in languages
        assert "spanish" in languages


class TestDetectLanguage:
    """Test detect_language function."""

    def test_english(self):
        result = detect_language("Hello world how are you today")
        assert result == "english"


class TestIsEnglish:
    """Test is_english function."""

    def test_english_text(self):
        assert is_english("The weather is nice today") is True

    def test_non_english(self):
        assert is_english("Bonjour le monde") is False
