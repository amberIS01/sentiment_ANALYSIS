"""Tests for intent module."""

import pytest
from chatbot.intent import (
    IntentType,
    IntentResult,
    IntentDetector,
    detect_intent,
    get_intent_keywords,
)


class TestIntentDetector:
    """Tests for IntentDetector."""

    def test_detect_greeting(self):
        """Test detecting greeting."""
        detector = IntentDetector()
        result = detector.detect("Hello there!")
        
        assert result.intent == IntentType.GREETING

    def test_detect_farewell(self):
        """Test detecting farewell."""
        detector = IntentDetector()
        result = detector.detect("Goodbye, see you later")
        
        assert result.intent == IntentType.FAREWELL

    def test_detect_question(self):
        """Test detecting question."""
        detector = IntentDetector()
        result = detector.detect("What time is it?")
        
        assert result.intent == IntentType.QUESTION

    def test_detect_complaint(self):
        """Test detecting complaint."""
        detector = IntentDetector()
        result = detector.detect("This is terrible, I hate it")
        
        assert result.intent == IntentType.COMPLAINT

    def test_detect_compliment(self):
        """Test detecting compliment."""
        detector = IntentDetector()
        result = detector.detect("Great job, well done!")
        
        assert result.intent == IntentType.COMPLIMENT

    def test_confidence_score(self):
        """Test confidence score."""
        detector = IntentDetector()
        result = detector.detect("Hello!")
        
        assert 0 <= result.confidence <= 1

    def test_detect_unknown(self):
        """Test unknown intent."""
        detector = IntentDetector()
        result = detector.detect("asdfghjkl")
        
        assert result.intent == IntentType.UNKNOWN

    def test_add_custom_intent(self):
        """Test adding custom intent."""
        detector = IntentDetector()
        detector.add_keywords(IntentType.REQUEST, ["please", "could you"])
        
        result = detector.detect("Could you help me please?")
        
        assert result.intent == IntentType.REQUEST

    def test_detect_many(self):
        """Test detecting multiple texts."""
        detector = IntentDetector()
        texts = ["Hello", "Goodbye", "What?"]
        
        results = detector.detect_many(texts)
        
        assert len(results) == 3


class TestDetectIntent:
    """Tests for detect_intent function."""

    def test_detect(self):
        """Test detect function."""
        result = detect_intent("Hello world")
        
        assert isinstance(result, IntentResult)


class TestGetIntentKeywords:
    """Tests for get_intent_keywords function."""

    def test_get_greeting(self):
        """Test getting greeting keywords."""
        keywords = get_intent_keywords(IntentType.GREETING)
        
        assert "hello" in keywords

    def test_get_farewell(self):
        """Test getting farewell keywords."""
        keywords = get_intent_keywords(IntentType.FAREWELL)
        
        assert "goodbye" in keywords
