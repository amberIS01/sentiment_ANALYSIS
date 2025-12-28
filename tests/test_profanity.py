"""Tests for profanity module."""

import pytest
from chatbot.profanity import (
    ProfanityMatch,
    ProfanityAnalysis,
    ProfanityFilter,
    filter_profanity,
    check_profanity,
)


class TestProfanityFilter:
    """Tests for ProfanityFilter."""

    def test_detect(self):
        """Test detecting profanity."""
        pf = ProfanityFilter()
        matches = pf.detect("What the hell")
        
        assert len(matches) == 1
        assert matches[0].word == "hell"

    def test_filter(self):
        """Test filtering profanity."""
        pf = ProfanityFilter()
        result = pf.filter("damn it")
        
        assert "damn" not in result.lower()
        assert "d**n" in result or "d*n" in result

    def test_add_word(self):
        """Test adding custom word."""
        pf = ProfanityFilter()
        pf.add_word("badword", 4)
        
        matches = pf.detect("that badword")
        assert len(matches) == 1

    def test_remove_word(self):
        """Test removing word."""
        pf = ProfanityFilter()
        pf.remove_word("hell")
        
        matches = pf.detect("what the hell")
        assert len(matches) == 0

    def test_whitelist(self):
        """Test whitelisting word."""
        pf = ProfanityFilter()
        pf.add_whitelist("hell")
        
        matches = pf.detect("what the hell")
        assert len(matches) == 0

    def test_analyze(self):
        """Test analyzing text."""
        pf = ProfanityFilter()
        result = pf.analyze("damn and hell")
        
        assert result.total_count == 2
        assert not result.is_clean

    def test_is_clean(self):
        """Test is_clean method."""
        pf = ProfanityFilter()
        
        assert pf.is_clean("Hello world") is True
        assert pf.is_clean("What the hell") is False

    def test_get_severity(self):
        """Test getting severity."""
        pf = ProfanityFilter()
        severity = pf.get_severity("damn")
        
        assert severity > 0

    def test_custom_mask(self):
        """Test custom mask character."""
        pf = ProfanityFilter(mask_char="#")
        result = pf.filter("damn")
        
        assert "#" in result


class TestFilterProfanity:
    """Tests for filter_profanity function."""

    def test_filter(self):
        """Test filter function."""
        result = filter_profanity("what the hell")
        
        assert "hell" not in result.lower()


class TestCheckProfanity:
    """Tests for check_profanity function."""

    def test_has_profanity(self):
        """Test detecting profanity."""
        assert check_profanity("damn it") is True

    def test_no_profanity(self):
        """Test clean text."""
        assert check_profanity("Hello world") is False
