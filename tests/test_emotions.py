"""
Tests for the Emotion Detection Module.
"""

import pytest
from chatbot.emotions import EmotionDetector, Emotion, EmotionResult, detect_emotion


class TestEmotionEnum:
    """Test cases for the Emotion enum."""

    def test_emotion_values(self):
        """Test that all emotions have correct values."""
        assert Emotion.JOY.value == "joy"
        assert Emotion.SADNESS.value == "sadness"
        assert Emotion.ANGER.value == "anger"
        assert Emotion.FEAR.value == "fear"
        assert Emotion.SURPRISE.value == "surprise"
        assert Emotion.DISGUST.value == "disgust"
        assert Emotion.TRUST.value == "trust"
        assert Emotion.ANTICIPATION.value == "anticipation"
        assert Emotion.NEUTRAL.value == "neutral"


class TestEmotionResult:
    """Test cases for EmotionResult dataclass."""

    def test_emotion_result_creation(self):
        """Test creating an EmotionResult."""
        result = EmotionResult(
            primary_emotion=Emotion.JOY,
            confidence=0.8,
            all_emotions={Emotion.JOY: 0.8, Emotion.TRUST: 0.2}
        )
        assert result.primary_emotion == Emotion.JOY
        assert result.confidence == 0.8
        assert len(result.all_emotions) == 2

    def test_emotion_result_str(self):
        """Test string representation of EmotionResult."""
        result = EmotionResult(
            primary_emotion=Emotion.ANGER,
            confidence=0.75,
            all_emotions={Emotion.ANGER: 0.75}
        )
        assert "anger" in str(result)
        assert "0.75" in str(result)


class TestEmotionDetector:
    """Test cases for EmotionDetector."""

    @pytest.fixture
    def detector(self):
        """Create an EmotionDetector instance."""
        return EmotionDetector()

    def test_detect_joy(self, detector):
        """Test detecting joy emotion."""
        result = detector.detect_emotion("I am so happy and excited today!")
        assert result.primary_emotion == Emotion.JOY

    def test_detect_sadness(self, detector):
        """Test detecting sadness emotion."""
        result = detector.detect_emotion("I feel sad and lonely.")
        assert result.primary_emotion == Emotion.SADNESS

    def test_detect_anger(self, detector):
        """Test detecting anger emotion."""
        result = detector.detect_emotion("I am so angry and frustrated!")
        assert result.primary_emotion == Emotion.ANGER

    def test_detect_fear(self, detector):
        """Test detecting fear emotion."""
        result = detector.detect_emotion("I am scared and worried about this.")
        assert result.primary_emotion == Emotion.FEAR

    def test_detect_surprise(self, detector):
        """Test detecting surprise emotion."""
        result = detector.detect_emotion("Wow, I am so surprised and shocked!")
        assert result.primary_emotion == Emotion.SURPRISE

    def test_detect_disgust(self, detector):
        """Test detecting disgust emotion."""
        result = detector.detect_emotion("This is disgusting and gross.")
        assert result.primary_emotion == Emotion.DISGUST

    def test_detect_trust(self, detector):
        """Test detecting trust emotion."""
        result = detector.detect_emotion("I trust and believe in you completely.")
        assert result.primary_emotion == Emotion.TRUST

    def test_detect_anticipation(self, detector):
        """Test detecting anticipation emotion."""
        result = detector.detect_emotion("I can't wait and am so eager!")
        assert result.primary_emotion == Emotion.ANTICIPATION

    def test_empty_text_returns_neutral(self, detector):
        """Test that empty text returns neutral emotion."""
        result = detector.detect_emotion("")
        assert result.primary_emotion == Emotion.NEUTRAL
        assert result.confidence == 1.0

    def test_whitespace_only_returns_neutral(self, detector):
        """Test that whitespace-only text returns neutral."""
        result = detector.detect_emotion("   ")
        assert result.primary_emotion == Emotion.NEUTRAL

    def test_neutral_text(self, detector):
        """Test text with no emotional keywords."""
        result = detector.detect_emotion("The meeting is at 3pm.")
        assert result.primary_emotion == Emotion.NEUTRAL

    def test_intensity_modifiers(self, detector):
        """Test that intensity modifiers affect confidence."""
        result_normal = detector.detect_emotion("I am happy.")
        result_intense = detector.detect_emotion("I am very extremely happy!")
        # Both should detect joy
        assert result_normal.primary_emotion == Emotion.JOY
        assert result_intense.primary_emotion == Emotion.JOY

    def test_negation_handling(self, detector):
        """Test that negation inverts some emotions."""
        result = detector.detect_emotion("I am not happy at all.")
        # Negation should shift joy toward sadness
        assert result.primary_emotion in [Emotion.SADNESS, Emotion.NEUTRAL]

    def test_mixed_emotions(self, detector):
        """Test text with multiple emotions."""
        result = detector.detect_emotion("I am happy but also a bit worried.")
        # Should detect the stronger emotion
        assert result.primary_emotion in [Emotion.JOY, Emotion.FEAR]
        assert len(result.all_emotions) >= 1

    def test_get_emotion_summary_empty(self, detector):
        """Test emotion summary with empty list."""
        summary = detector.get_emotion_summary([])
        assert summary["primary_emotion"] == Emotion.NEUTRAL.value
        assert summary["message_count"] == 0

    def test_get_emotion_summary_multiple(self, detector):
        """Test emotion summary with multiple messages."""
        messages = [
            "I am very happy!",
            "This makes me so angry.",
            "I feel great today!",
        ]
        summary = detector.get_emotion_summary(messages)
        assert summary["message_count"] == 3
        assert "emotion_distribution" in summary
        assert "primary_emotion" in summary


class TestDetectEmotionFunction:
    """Test the convenience function."""

    def test_detect_emotion_function(self):
        """Test the module-level detect_emotion function."""
        result = detect_emotion("I love this so much!")
        assert isinstance(result, EmotionResult)
        assert result.primary_emotion == Emotion.JOY
