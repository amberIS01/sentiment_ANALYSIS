"""
Tests for the Tokenizer Module.
"""

import pytest

from chatbot.tokenizer import (
    Tokenizer,
    Token,
    TokenType,
    SentenceTokenizer,
    tokenize,
    count_words,
)


class TestTokenType:
    """Test TokenType enum."""

    def test_values(self):
        assert TokenType.WORD.value == "word"
        assert TokenType.NUMBER.value == "number"
        assert TokenType.URL.value == "url"


class TestToken:
    """Test Token dataclass."""

    def test_creation(self):
        token = Token(
            text="hello",
            token_type=TokenType.WORD,
            start=0,
            end=5,
        )
        assert token.text == "hello"
        assert token.token_type == TokenType.WORD


class TestTokenizer:
    """Test Tokenizer class."""

    def test_initialization(self):
        tokenizer = Tokenizer()
        assert tokenizer.lowercase is True

    def test_tokenize_words(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("Hello world")
        word_tokens = [t for t in tokens if t.token_type == TokenType.WORD]
        assert len(word_tokens) == 2

    def test_tokenize_with_numbers(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("I have 5 apples")
        number_tokens = [t for t in tokens if t.token_type == TokenType.NUMBER]
        assert len(number_tokens) == 1

    def test_tokenize_with_url(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("Visit https://example.com today")
        url_tokens = [t for t in tokens if t.token_type == TokenType.URL]
        assert len(url_tokens) == 1

    def test_tokenize_with_mention(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("Hello @user")
        mention_tokens = [t for t in tokens if t.token_type == TokenType.MENTION]
        assert len(mention_tokens) == 1

    def test_tokenize_with_hashtag(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("Love #python")
        hashtag_tokens = [t for t in tokens if t.token_type == TokenType.HASHTAG]
        assert len(hashtag_tokens) == 1

    def test_tokenize_words_only(self):
        tokenizer = Tokenizer()
        words = tokenizer.tokenize_words("Hello world!")
        assert words == ["hello", "world"]

    def test_tokenize_sentences(self):
        tokenizer = Tokenizer()
        sentences = tokenizer.tokenize_sentences("Hello. How are you? I am fine!")
        assert len(sentences) == 3

    def test_count_tokens(self):
        tokenizer = Tokenizer()
        count = tokenizer.count_tokens("One two three four five")
        assert count == 5

    def test_filter_tokens(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("Hello 123 world")
        words = tokenizer.filter_tokens(tokens, [TokenType.WORD])
        assert len(words) == 2


class TestSentenceTokenizer:
    """Test SentenceTokenizer class."""

    def test_tokenize(self):
        tokenizer = SentenceTokenizer()
        sentences = tokenizer.tokenize("Hello there. How are you?")
        assert len(sentences) >= 1


class TestTokenizeFunction:
    """Test tokenize function."""

    def test_basic(self):
        words = tokenize("Hello world")
        assert "hello" in words
        assert "world" in words


class TestCountWords:
    """Test count_words function."""

    def test_basic(self):
        count = count_words("One two three")
        assert count == 3
