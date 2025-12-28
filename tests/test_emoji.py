"""Tests for emoji module."""

import pytest
from chatbot.emoji import (
    EmojiMatch,
    EmojiAnalysis,
    EmojiAnalyzer,
    analyze_emojis,
    get_emoji_score,
)


class TestEmojiAnalyzer:
    """Tests for EmojiAnalyzer."""

    def test_find_positive_emojis(self):
        """Test finding positive emojis."""
        analyzer = EmojiAnalyzer()
        matches = analyzer.find_emojis("I love this! 😀😊")
        
        assert len(matches) == 2
        assert all(m.score > 0 for m in matches)

    def test_find_negative_emojis(self):
        """Test finding negative emojis."""
        analyzer = EmojiAnalyzer()
        matches = analyzer.find_emojis("So sad 😢😭")
        
        assert len(matches) == 2
        assert all(m.score < 0 for m in matches)

    def test_analyze_positive(self):
        """Test analyzing positive text."""
        analyzer = EmojiAnalyzer()
        result = analyzer.analyze("Great! 😀👍")
        
        assert result.positive_count == 2
        assert result.avg_score > 0

    def test_analyze_negative(self):
        """Test analyzing negative text."""
        analyzer = EmojiAnalyzer()
        result = analyzer.analyze("Bad 😢😡")
        
        assert result.negative_count == 2
        assert result.avg_score < 0

    def test_analyze_empty(self):
        """Test analyzing text without emojis."""
        analyzer = EmojiAnalyzer()
        result = analyzer.analyze("No emojis here")
        
        assert result.total_count == 0
        assert result.avg_score == 0.0

    def test_add_custom_emoji(self):
        """Test adding custom emoji."""
        analyzer = EmojiAnalyzer()
        analyzer.add_emoji("🆕", 0.5)
        
        matches = analyzer.find_emojis("New! 🆕")
        assert len(matches) == 1

    def test_get_score(self):
        """Test getting score."""
        analyzer = EmojiAnalyzer()
        score = analyzer.get_score("Happy 😀")
        
        assert score > 0

    def test_strip_emojis(self):
        """Test stripping emojis."""
        analyzer = EmojiAnalyzer()
        result = analyzer.strip_emojis("Hello 😀 World 😊")
        
        assert "😀" not in result
        assert "Hello" in result


class TestAnalyzeEmojis:
    """Tests for analyze_emojis function."""

    def test_analyze(self):
        """Test analyze function."""
        result = analyze_emojis("Test 😀")
        
        assert isinstance(result, EmojiAnalysis)
        assert result.total_count == 1


class TestGetEmojiScore:
    """Tests for get_emoji_score function."""

    def test_score(self):
        """Test getting score."""
        score = get_emoji_score("Great 😀👍")
        
        assert score > 0
