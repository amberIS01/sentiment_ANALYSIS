"""
Tests for the Preprocessor Module.
"""

import pytest

from chatbot.preprocessor import TextPreprocessor, preprocess


class TestTextPreprocessor:
    """Test TextPreprocessor class."""

    def test_initialization(self):
        preprocessor = TextPreprocessor()
        assert preprocessor is not None

    def test_clean(self):
        preprocessor = TextPreprocessor()
        text = "Hello   world   https://example.com"
        result = preprocessor.clean(text)
        assert "https://" not in result
        assert "  " not in result

    def test_remove_urls(self):
        preprocessor = TextPreprocessor()
        text = "Check out https://example.com for more"
        result = preprocessor.remove_urls(text)
        assert "https://example.com" not in result

    def test_remove_emails(self):
        preprocessor = TextPreprocessor()
        text = "Contact me at test@example.com"
        result = preprocessor.remove_emails(text)
        assert "test@example.com" not in result

    def test_remove_mentions(self):
        preprocessor = TextPreprocessor()
        text = "Hey @user check this out"
        result = preprocessor.remove_mentions(text)
        assert "@user" not in result

    def test_remove_hashtags(self):
        preprocessor = TextPreprocessor()
        text = "This is #awesome content"
        result = preprocessor.remove_hashtags(text)
        assert "#awesome" not in result

    def test_extract_hashtags(self):
        preprocessor = TextPreprocessor()
        text = "Love #python and #coding"
        hashtags = preprocessor.extract_hashtags(text)
        assert "#python" in hashtags
        assert "#coding" in hashtags

    def test_extract_mentions(self):
        preprocessor = TextPreprocessor()
        text = "Thanks @alice and @bob"
        mentions = preprocessor.extract_mentions(text)
        assert "@alice" in mentions
        assert "@bob" in mentions

    def test_normalize_whitespace(self):
        preprocessor = TextPreprocessor()
        text = "Hello    world\n\ntest"
        result = preprocessor.normalize_whitespace(text)
        assert result == "Hello world test"

    def test_lowercase(self):
        preprocessor = TextPreprocessor()
        result = preprocessor.lowercase("HELLO World")
        assert result == "hello world"

    def test_remove_punctuation(self):
        preprocessor = TextPreprocessor()
        result = preprocessor.remove_punctuation("Hello, world!")
        assert result == "Hello world"

    def test_expand_contractions(self):
        preprocessor = TextPreprocessor()
        result = preprocessor.expand_contractions("I don't know")
        assert "do not" in result


class TestPreprocessFunction:
    """Test preprocess function."""

    def test_basic_preprocess(self):
        text = "Hello   world"
        result = preprocess(text)
        assert result == "Hello world"

    def test_removes_urls(self):
        text = "Visit https://test.com now"
        result = preprocess(text, remove_urls=True)
        assert "https://" not in result

    def test_keeps_urls(self):
        text = "Visit https://test.com now"
        result = preprocess(text, remove_urls=False)
        assert "https://test.com" in result
