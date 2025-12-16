"""
Tests for the Word Cloud Module.
"""

import pytest

from chatbot.wordcloud import (
    WordCloudGenerator,
    WordFrequency,
    generate_word_cloud,
    STOP_WORDS,
)


class TestWordFrequency:
    """Test WordFrequency dataclass."""

    def test_creation(self):
        freq = WordFrequency(word="hello", count=10, percentage=25.0)
        assert freq.word == "hello"
        assert freq.count == 10
        assert freq.percentage == 25.0


class TestWordCloudGenerator:
    """Test WordCloudGenerator class."""

    def test_initialization(self):
        generator = WordCloudGenerator()
        assert generator.min_length == 3
        assert generator.max_words == 100

    def test_custom_settings(self):
        generator = WordCloudGenerator(min_length=5, max_words=50)
        assert generator.min_length == 5
        assert generator.max_words == 50

    def test_generate(self):
        generator = WordCloudGenerator()
        text = "hello world hello python python python"
        result = generator.generate(text)
        assert len(result) > 0
        assert result[0].word == "python"
        assert result[0].count == 3

    def test_excludes_stop_words(self):
        generator = WordCloudGenerator(exclude_stop_words=True)
        text = "the quick brown fox jumps over the lazy dog"
        result = generator.generate(text)
        words = [f.word for f in result]
        assert "the" not in words

    def test_min_length_filter(self):
        generator = WordCloudGenerator(min_length=5)
        text = "hi hello world programming"
        result = generator.generate(text)
        words = [f.word for f in result]
        assert "hi" not in words
        assert "hello" in words

    def test_max_words_limit(self):
        generator = WordCloudGenerator(max_words=3)
        text = "one two three four five six seven eight nine ten"
        result = generator.generate(text)
        assert len(result) <= 3

    def test_add_stop_word(self):
        generator = WordCloudGenerator()
        generator.add_stop_word("python")
        text = "python programming python code"
        result = generator.generate(text)
        words = [f.word for f in result]
        assert "python" not in words

    def test_add_stop_words(self):
        generator = WordCloudGenerator()
        generator.add_stop_words(["python", "code"])
        text = "python code programming"
        result = generator.generate(text)
        words = [f.word for f in result]
        assert "python" not in words
        assert "code" not in words

    def test_generate_from_messages(self):
        generator = WordCloudGenerator()
        messages = ["hello world", "hello python", "world programming"]
        result = generator.generate_from_messages(messages)
        assert len(result) > 0

    def test_to_dict(self):
        generator = WordCloudGenerator()
        text = "hello world hello"
        frequencies = generator.generate(text)
        result = generator.to_dict(frequencies)
        assert isinstance(result, dict)
        assert "hello" in result


class TestGenerateWordCloud:
    """Test generate_word_cloud function."""

    def test_basic_usage(self):
        text = "python programming python code python"
        result = generate_word_cloud(text)
        assert len(result) > 0
        assert result[0].word == "python"

    def test_max_words(self):
        text = "one two three four five"
        result = generate_word_cloud(text, max_words=2)
        assert len(result) <= 2


class TestStopWords:
    """Test stop words set."""

    def test_common_words(self):
        assert "the" in STOP_WORDS
        assert "and" in STOP_WORDS
        assert "is" in STOP_WORDS
