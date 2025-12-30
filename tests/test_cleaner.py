"""Tests for cleaner module."""

import pytest
from chatbot.cleaner import (
    TextCleaner,
    clean_text,
    remove_html,
    remove_urls,
    remove_emails,
    normalize_whitespace,
)


class TestTextCleaner:
    """Tests for TextCleaner."""

    def test_clean_basic(self):
        """Test basic cleaning."""
        cleaner = TextCleaner()
        result = cleaner.clean("  Hello   World  ")
        
        assert result == "Hello World"

    def test_remove_html(self):
        """Test HTML removal."""
        cleaner = TextCleaner()
        result = cleaner.clean("<p>Hello</p> <b>World</b>")
        
        assert "<p>" not in result
        assert "Hello" in result

    def test_remove_urls(self):
        """Test URL removal."""
        cleaner = TextCleaner()
        result = cleaner.clean("Visit https://example.com for more")
        
        assert "https://" not in result

    def test_remove_emails(self):
        """Test email removal."""
        cleaner = TextCleaner()
        result = cleaner.clean("Contact test@example.com")
        
        assert "@" not in result

    def test_lowercase(self):
        """Test lowercase option."""
        cleaner = TextCleaner(lowercase=True)
        result = cleaner.clean("HELLO World")
        
        assert result == "hello world"

    def test_custom_patterns(self):
        """Test custom patterns."""
        cleaner = TextCleaner()
        cleaner.add_pattern(r'\d+', '')
        
        result = cleaner.clean("Hello 123 World")
        assert "123" not in result

    def test_chain_cleaning(self):
        """Test chaining clean operations."""
        cleaner = TextCleaner(lowercase=True)
        result = cleaner.clean("<p>HELLO</p> https://test.com test@email.com")
        
        assert result == "hello"


class TestCleanText:
    """Tests for clean_text function."""

    def test_clean(self):
        """Test clean function."""
        result = clean_text("  Hello   World  ")
        
        assert result == "Hello World"


class TestRemoveHtml:
    """Tests for remove_html function."""

    def test_remove(self):
        """Test HTML removal."""
        result = remove_html("<div>Test</div>")
        
        assert "<div>" not in result
        assert "Test" in result


class TestRemoveUrls:
    """Tests for remove_urls function."""

    def test_remove(self):
        """Test URL removal."""
        result = remove_urls("See http://example.com here")
        
        assert "http://" not in result


class TestRemoveEmails:
    """Tests for remove_emails function."""

    def test_remove(self):
        """Test email removal."""
        result = remove_emails("Email: user@domain.com")
        
        assert "@" not in result


class TestNormalizeWhitespace:
    """Tests for normalize_whitespace function."""

    def test_normalize(self):
        """Test whitespace normalization."""
        result = normalize_whitespace("  too   many   spaces  ")
        
        assert result == "too many spaces"
