"""
Text Tokenizer Module

Tokenize text for analysis.
"""

import re
from dataclasses import dataclass
from typing import List, Iterator, Optional
from enum import Enum


class TokenType(Enum):
    """Type of token."""

    WORD = "word"
    NUMBER = "number"
    PUNCTUATION = "punctuation"
    EMOJI = "emoji"
    HASHTAG = "hashtag"
    MENTION = "mention"
    URL = "url"
    WHITESPACE = "whitespace"
    UNKNOWN = "unknown"


@dataclass
class Token:
    """A single token."""

    text: str
    token_type: TokenType
    start: int
    end: int
    normalized: Optional[str] = None


class Tokenizer:
    """Text tokenizer."""

    def __init__(self, lowercase: bool = True):
        """Initialize tokenizer."""
        self.lowercase = lowercase
        self._patterns = [
            (TokenType.URL, r'https?://\S+|www\.\S+'),
            (TokenType.MENTION, r'@\w+'),
            (TokenType.HASHTAG, r'#\w+'),
            (TokenType.NUMBER, r'\d+(?:\.\d+)?'),
            (TokenType.WORD, r'[a-zA-Z]+(?:\'[a-zA-Z]+)?'),
            (TokenType.PUNCTUATION, r'[^\w\s]'),
            (TokenType.WHITESPACE, r'\s+'),
        ]

    def tokenize(self, text: str) -> List[Token]:
        """Tokenize text into tokens."""
        tokens = []
        pos = 0

        while pos < len(text):
            match = None
            token_type = TokenType.UNKNOWN

            for ttype, pattern in self._patterns:
                regex = re.compile(pattern)
                m = regex.match(text, pos)
                if m:
                    match = m
                    token_type = ttype
                    break

            if match:
                token_text = match.group()
                normalized = token_text.lower() if self.lowercase else token_text

                tokens.append(Token(
                    text=token_text,
                    token_type=token_type,
                    start=pos,
                    end=match.end(),
                    normalized=normalized,
                ))
                pos = match.end()
            else:
                tokens.append(Token(
                    text=text[pos],
                    token_type=TokenType.UNKNOWN,
                    start=pos,
                    end=pos + 1,
                ))
                pos += 1

        return tokens

    def tokenize_words(self, text: str) -> List[str]:
        """Get only word tokens."""
        tokens = self.tokenize(text)
        return [
            t.normalized or t.text
            for t in tokens
            if t.token_type == TokenType.WORD
        ]

    def tokenize_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        pattern = r'(?<=[.!?])\s+'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]

    def iter_tokens(self, text: str) -> Iterator[Token]:
        """Iterate over tokens."""
        yield from self.tokenize(text)

    def count_tokens(self, text: str) -> int:
        """Count number of word tokens."""
        return len(self.tokenize_words(text))

    def filter_tokens(
        self,
        tokens: List[Token],
        types: List[TokenType],
    ) -> List[Token]:
        """Filter tokens by type."""
        return [t for t in tokens if t.token_type in types]


class SentenceTokenizer:
    """Tokenize text into sentences."""

    def __init__(self):
        """Initialize sentence tokenizer."""
        self._abbreviations = {
            "mr.", "mrs.", "ms.", "dr.", "prof.",
            "sr.", "jr.", "vs.", "etc.", "e.g.", "i.e.",
        }

    def tokenize(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        pattern = r'(?<=[.!?])\s+(?=[A-Z])'
        sentences = re.split(pattern, text)
        return [s.strip() for s in sentences if s.strip()]


def tokenize(text: str) -> List[str]:
    """Tokenize text into words."""
    tokenizer = Tokenizer()
    return tokenizer.tokenize_words(text)


def count_words(text: str) -> int:
    """Count words in text."""
    tokenizer = Tokenizer()
    return tokenizer.count_tokens(text)
