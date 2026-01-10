"""Tests for preprocessing module."""

import pytest
from chatbot.preprocessing import (
    PreprocessResult,
    LowercaseStep,
    StripWhitespaceStep,
    RemovePunctuationStep,
    RemoveNumbersStep,
    RemoveUrlsStep,
    RemoveEmailsStep,
    RemoveHtmlStep,
    PreprocessPipeline,
    create_default_pipeline,
    preprocess_text,
)


class TestLowercaseStep:
    """Tests for LowercaseStep."""

    def test_lowercase(self):
        """Test lowercasing."""
        step = LowercaseStep()
        result = step.process("HELLO World")
        
        assert result == "hello world"


class TestStripWhitespaceStep:
    """Tests for StripWhitespaceStep."""

    def test_strip(self):
        """Test stripping whitespace."""
        step = StripWhitespaceStep()
        result = step.process("  hello   world  ")
        
        assert result == "hello world"


class TestRemovePunctuationStep:
    """Tests for RemovePunctuationStep."""

    def test_remove(self):
        """Test removing punctuation."""
        step = RemovePunctuationStep()
        result = step.process("Hello, world!")
        
        assert result == "Hello world"

    def test_keep_chars(self):
        """Test keeping certain chars."""
        step = RemovePunctuationStep(keep="!")
        result = step.process("Hello, world!")
        
        assert "!" in result


class TestRemoveNumbersStep:
    """Tests for RemoveNumbersStep."""

    def test_remove(self):
        """Test removing numbers."""
        step = RemoveNumbersStep()
        result = step.process("Hello 123 world 456")
        
        assert "123" not in result


class TestRemoveUrlsStep:
    """Tests for RemoveUrlsStep."""

    def test_remove_http(self):
        """Test removing HTTP URLs."""
        step = RemoveUrlsStep()
        result = step.process("Visit http://example.com today")
        
        assert "http://" not in result

    def test_remove_https(self):
        """Test removing HTTPS URLs."""
        step = RemoveUrlsStep()
        result = step.process("See https://example.com")
        
        assert "https://" not in result


class TestRemoveEmailsStep:
    """Tests for RemoveEmailsStep."""

    def test_remove(self):
        """Test removing emails."""
        step = RemoveEmailsStep()
        result = step.process("Contact test@example.com")
        
        assert "@" not in result


class TestRemoveHtmlStep:
    """Tests for RemoveHtmlStep."""

    def test_remove(self):
        """Test removing HTML."""
        step = RemoveHtmlStep()
        result = step.process("<p>Hello</p> <b>world</b>")
        
        assert "<p>" not in result
        assert "Hello" in result


class TestPreprocessPipeline:
    """Tests for PreprocessPipeline."""

    def test_add_step(self):
        """Test adding step."""
        pipeline = PreprocessPipeline()
        pipeline.add_step(LowercaseStep())
        
        result = pipeline.process("HELLO")
        assert result.processed == "hello"

    def test_chain_steps(self):
        """Test chaining steps."""
        pipeline = (
            PreprocessPipeline()
            .add_step(LowercaseStep())
            .add_step(StripWhitespaceStep())
        )
        
        result = pipeline.process("  HELLO  WORLD  ")
        assert result.processed == "hello world"

    def test_remove_step(self):
        """Test removing step."""
        pipeline = PreprocessPipeline()
        pipeline.add_step(LowercaseStep())
        pipeline.remove_step("lowercase")
        
        result = pipeline.process("HELLO")
        assert result.processed == "HELLO"

    def test_process_many(self):
        """Test processing multiple texts."""
        pipeline = PreprocessPipeline().add_step(LowercaseStep())
        
        results = pipeline.process_many(["HELLO", "WORLD"])
        
        assert len(results) == 2


class TestPreprocessText:
    """Tests for preprocess_text function."""

    def test_preprocess(self):
        """Test preprocessing."""
        result = preprocess_text("<p>Hello</p> http://test.com")
        
        assert "<p>" not in result
        assert "http://" not in result
