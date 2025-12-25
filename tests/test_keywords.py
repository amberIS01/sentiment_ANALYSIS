"""
Tests for the Keywords Module.
"""

import pytest

from chatbot.keywords import (
    KeywordAnalyzer,
    KeywordMatch,
    KeywordCategory,
    extract_keywords,
    POSITIVE_KEYWORDS,
    NEGATIVE_KEYWORDS,
)


class TestKeywordCategory:
    """Test KeywordCategory enum."""

    def test_values(self):
        assert KeywordCategory.POSITIVE.value == "positive"
        assert KeywordCategory.NEGATIVE.value == "negative"
        assert KeywordCategory.INTENSIFIER.value == "intensifier"


class TestKeywordMatch:
    """Test KeywordMatch dataclass."""

    def test_creation(self):
        match = KeywordMatch(
            word="love",
            category=KeywordCategory.POSITIVE,
            score=0.8,
            position=0,
        )
        assert match.word == "love"
        assert match.score == 0.8


class TestKeywordAnalyzer:
    """Test KeywordAnalyzer class."""

    def test_initialization(self):
        analyzer = KeywordAnalyzer()
        assert analyzer is not None

    def test_find_positive_keywords(self):
        analyzer = KeywordAnalyzer()
        matches = analyzer.find_keywords("I love this amazing product")
        positive = [m for m in matches if m.category == KeywordCategory.POSITIVE]
        assert len(positive) >= 2

    def test_find_negative_keywords(self):
        analyzer = KeywordAnalyzer()
        matches = analyzer.find_keywords("I hate this terrible service")
        negative = [m for m in matches if m.category == KeywordCategory.NEGATIVE]
        assert len(negative) >= 2

    def test_find_intensifiers(self):
        analyzer = KeywordAnalyzer()
        matches = analyzer.find_keywords("This is very extremely good")
        intensifiers = [m for m in matches if m.category == KeywordCategory.INTENSIFIER]
        assert len(intensifiers) >= 2

    def test_find_negations(self):
        analyzer = KeywordAnalyzer()
        matches = analyzer.find_keywords("I do not like this")
        negations = [m for m in matches if m.category == KeywordCategory.NEGATION]
        assert len(negations) >= 1

    def test_add_keyword(self):
        analyzer = KeywordAnalyzer()
        analyzer.add_keyword("fantastic", KeywordCategory.POSITIVE, 0.9)
        matches = analyzer.find_keywords("This is fantastic")
        assert any(m.word == "fantastic" for m in matches)

    def test_calculate_score_positive(self):
        analyzer = KeywordAnalyzer()
        score = analyzer.calculate_score("I love this amazing wonderful product")
        assert score > 0

    def test_calculate_score_negative(self):
        analyzer = KeywordAnalyzer()
        score = analyzer.calculate_score("I hate this terrible awful thing")
        assert score < 0

    def test_calculate_score_with_negation(self):
        analyzer = KeywordAnalyzer()
        score1 = analyzer.calculate_score("I love this")
        score2 = analyzer.calculate_score("I do not love this")
        assert score2 < score1

    def test_calculate_score_with_intensifier(self):
        analyzer = KeywordAnalyzer()
        score1 = analyzer.calculate_score("This is good")
        score2 = analyzer.calculate_score("This is very good")
        assert score2 > score1

    def test_get_summary(self):
        analyzer = KeywordAnalyzer()
        summary = analyzer.get_summary("I love this but hate that")
        assert "total_keywords" in summary
        assert "positive_count" in summary
        assert "negative_count" in summary
        assert "score" in summary


class TestExtractKeywords:
    """Test extract_keywords function."""

    def test_basic(self):
        keywords = extract_keywords("I love this amazing product")
        assert "love" in keywords
        assert "amazing" in keywords

    def test_empty(self):
        keywords = extract_keywords("Just some regular text")
        assert len(keywords) == 0 or all(
            k not in POSITIVE_KEYWORDS and k not in NEGATIVE_KEYWORDS
            for k in keywords
        )
