"""
Tests for the Responses Module.
"""

import pytest

from chatbot.responses import (
    ResponseGenerator,
    ResponseTone,
    GeneratedResponse,
    generate_response,
)
from chatbot.sentiment import SentimentLabel


class TestResponseTone:
    """Test ResponseTone enum."""

    def test_values(self):
        assert ResponseTone.EMPATHETIC.value == "empathetic"
        assert ResponseTone.ENCOURAGING.value == "encouraging"
        assert ResponseTone.NEUTRAL.value == "neutral"
        assert ResponseTone.CURIOUS.value == "curious"


class TestGeneratedResponse:
    """Test GeneratedResponse dataclass."""

    def test_creation(self):
        response = GeneratedResponse(
            text="That's great!",
            tone=ResponseTone.ENCOURAGING,
            sentiment_match=SentimentLabel.POSITIVE,
        )
        assert response.text == "That's great!"
        assert response.tone == ResponseTone.ENCOURAGING


class TestResponseGenerator:
    """Test ResponseGenerator class."""

    def test_initialization(self):
        generator = ResponseGenerator()
        assert generator is not None

    def test_generate_positive(self):
        generator = ResponseGenerator()
        response = generator.generate(SentimentLabel.POSITIVE)
        assert isinstance(response, GeneratedResponse)
        assert response.sentiment_match == SentimentLabel.POSITIVE

    def test_generate_negative(self):
        generator = ResponseGenerator()
        response = generator.generate(SentimentLabel.NEGATIVE)
        assert response.sentiment_match == SentimentLabel.NEGATIVE

    def test_generate_neutral(self):
        generator = ResponseGenerator()
        response = generator.generate(SentimentLabel.NEUTRAL)
        assert response.sentiment_match == SentimentLabel.NEUTRAL

    def test_generate_with_tone(self):
        generator = ResponseGenerator()
        response = generator.generate(
            SentimentLabel.POSITIVE,
            tone=ResponseTone.EMPATHETIC,
        )
        assert response.tone == ResponseTone.EMPATHETIC

    def test_generate_followup_positive(self):
        generator = ResponseGenerator()
        followup = generator.generate_followup(SentimentLabel.POSITIVE)
        assert isinstance(followup, str)
        assert len(followup) > 0

    def test_generate_followup_negative(self):
        generator = ResponseGenerator()
        followup = generator.generate_followup(SentimentLabel.NEGATIVE)
        assert isinstance(followup, str)

    def test_add_template(self):
        generator = ResponseGenerator()
        generator.add_template("positive", "empathetic", "Custom response!")
        response = generator.generate(
            SentimentLabel.POSITIVE,
            tone=ResponseTone.EMPATHETIC,
        )
        # Custom template should be in the pool
        assert response.text is not None


class TestGenerateResponse:
    """Test generate_response function."""

    def test_positive(self):
        response = generate_response(SentimentLabel.POSITIVE)
        assert isinstance(response, str)
        assert len(response) > 0

    def test_negative(self):
        response = generate_response(SentimentLabel.NEGATIVE)
        assert isinstance(response, str)

    def test_neutral(self):
        response = generate_response(SentimentLabel.NEUTRAL)
        assert isinstance(response, str)
