"""
Emotion Detection Module

This module provides emotion detection capabilities beyond basic sentiment
analysis, identifying specific emotions like joy, anger, fear, sadness, etc.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set
import re


class Emotion(Enum):
    """Enumeration of detectable emotions."""

    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    NEUTRAL = "neutral"


@dataclass
class EmotionResult:
    """Result of emotion detection."""

    primary_emotion: Emotion
    confidence: float
    all_emotions: Dict[Emotion, float]

    def __str__(self) -> str:
        return f"{self.primary_emotion.value} (confidence: {self.confidence:.2f})"


class EmotionDetector:
    """
    Detect emotions in text using keyword-based analysis.

    This detector uses curated emotion lexicons to identify
    specific emotions beyond basic positive/negative sentiment.
    """

    # Emotion keyword lexicons
    EMOTION_LEXICONS: Dict[Emotion, Set[str]] = {
        Emotion.JOY: {
            "happy", "joy", "joyful", "delighted", "pleased", "glad",
            "cheerful", "thrilled", "excited", "ecstatic", "elated",
            "wonderful", "amazing", "fantastic", "great", "awesome",
            "love", "loving", "loved", "enjoy", "enjoying", "fun",
            "laugh", "laughing", "smile", "smiling", "celebrate",
            "blessed", "grateful", "thankful", "content", "satisfied",
            "yay", "hurray", "woohoo", "excellent", "perfect",
        },
        Emotion.SADNESS: {
            "sad", "unhappy", "depressed", "miserable", "sorrowful",
            "heartbroken", "grief", "grieving", "mourning", "crying",
            "tears", "weeping", "disappointed", "upset", "down",
            "lonely", "alone", "isolated", "hopeless", "despair",
            "melancholy", "blue", "gloomy", "tragic", "unfortunate",
            "regret", "regretful", "miss", "missing", "lost",
        },
        Emotion.ANGER: {
            "angry", "mad", "furious", "rage", "raging", "outraged",
            "annoyed", "irritated", "frustrated", "infuriated",
            "livid", "hostile", "aggressive", "hate", "hating",
            "resent", "resentful", "bitter", "spite", "spiteful",
            "fed up", "pissed", "fuming", "seething", "enraged",
        },
        Emotion.FEAR: {
            "afraid", "scared", "frightened", "terrified", "fearful",
            "anxious", "worried", "nervous", "panicked", "panic",
            "dread", "dreading", "horror", "horrified", "terror",
            "phobia", "alarmed", "uneasy", "tense", "stressed",
            "concern", "concerned", "apprehensive", "paranoid",
        },
        Emotion.SURPRISE: {
            "surprised", "shocking", "shocked", "astonished", "amazed",
            "stunned", "startled", "unexpected", "unbelievable",
            "incredible", "wow", "whoa", "omg", "oh my", "really",
            "no way", "seriously", "speechless", "mind-blown",
        },
        Emotion.DISGUST: {
            "disgusted", "disgusting", "gross", "revolting", "repulsive",
            "sickening", "nauseating", "vile", "awful", "terrible",
            "horrible", "dreadful", "appalling", "offensive", "yuck",
            "ugh", "eww", "nasty", "foul", "repugnant",
        },
        Emotion.TRUST: {
            "trust", "trusting", "believe", "believing", "faith",
            "reliable", "dependable", "honest", "sincere", "loyal",
            "confident", "certain", "sure", "secure", "safe",
            "assured", "comfortable", "calm", "peaceful", "relaxed",
        },
        Emotion.ANTICIPATION: {
            "excited", "eager", "looking forward", "can't wait",
            "anticipate", "anticipating", "expect", "expecting",
            "hope", "hoping", "hopeful", "optimistic", "curious",
            "interested", "intrigued", "wonder", "wondering",
        },
    }

    # Intensity modifiers
    INTENSIFIERS: Set[str] = {
        "very", "really", "extremely", "absolutely", "totally",
        "completely", "incredibly", "so", "too", "super", "highly",
    }

    DIMINISHERS: Set[str] = {
        "slightly", "somewhat", "a bit", "a little", "kind of",
        "sort of", "barely", "hardly", "mildly",
    }

    # Negation words
    NEGATIONS: Set[str] = {
        "not", "no", "never", "neither", "nobody", "nothing",
        "nowhere", "none", "don't", "doesn't", "didn't", "won't",
        "wouldn't", "couldn't", "shouldn't", "can't", "cannot",
    }

    def __init__(self):
        """Initialize the emotion detector."""
        # Build reverse lookup for faster detection
        self._word_to_emotions: Dict[str, Emotion] = {}
        for emotion, words in self.EMOTION_LEXICONS.items():
            for word in words:
                self._word_to_emotions[word.lower()] = emotion

    def detect_emotion(self, text: str) -> EmotionResult:
        """
        Detect the primary emotion in text.

        Args:
            text: The text to analyze.

        Returns:
            EmotionResult with detected emotions.
        """
        if not text or not text.strip():
            return EmotionResult(
                primary_emotion=Emotion.NEUTRAL,
                confidence=1.0,
                all_emotions={Emotion.NEUTRAL: 1.0},
            )

        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))

        # Count emotion matches
        emotion_scores: Dict[Emotion, float] = {e: 0.0 for e in Emotion}

        # Check for negation context
        has_negation = bool(words & self.NEGATIONS)

        # Check for intensity modifiers
        intensity_modifier = 1.0
        if words & self.INTENSIFIERS:
            intensity_modifier = 1.5
        elif words & self.DIMINISHERS:
            intensity_modifier = 0.5

        # Score each emotion based on keyword matches
        for word in words:
            if word in self._word_to_emotions:
                emotion = self._word_to_emotions[word]
                score = 1.0 * intensity_modifier

                # Handle negation (invert certain emotions)
                if has_negation:
                    if emotion == Emotion.JOY:
                        emotion = Emotion.SADNESS
                        score *= 0.7
                    elif emotion == Emotion.SADNESS:
                        emotion = Emotion.JOY
                        score *= 0.7
                    elif emotion == Emotion.ANGER:
                        score *= 0.5

                emotion_scores[emotion] += score

        # Also check for multi-word expressions
        for emotion, phrases in self.EMOTION_LEXICONS.items():
            for phrase in phrases:
                if " " in phrase and phrase in text_lower:
                    emotion_scores[emotion] += 1.0 * intensity_modifier

        # Find primary emotion
        total_score = sum(emotion_scores.values())

        if total_score == 0:
            return EmotionResult(
                primary_emotion=Emotion.NEUTRAL,
                confidence=0.8,
                all_emotions={Emotion.NEUTRAL: 1.0},
            )

        # Normalize scores
        normalized_scores = {
            e: score / total_score
            for e, score in emotion_scores.items()
            if score > 0
        }

        if not normalized_scores:
            return EmotionResult(
                primary_emotion=Emotion.NEUTRAL,
                confidence=0.8,
                all_emotions={Emotion.NEUTRAL: 1.0},
            )

        # Get primary emotion
        primary_emotion = max(normalized_scores, key=normalized_scores.get)
        confidence = normalized_scores[primary_emotion]

        return EmotionResult(
            primary_emotion=primary_emotion,
            confidence=confidence,
            all_emotions=normalized_scores,
        )

    def get_emotion_summary(
        self, messages: List[str]
    ) -> Dict[str, any]:
        """
        Get emotion summary for multiple messages.

        Args:
            messages: List of messages to analyze.

        Returns:
            Dictionary with emotion statistics.
        """
        if not messages:
            return {
                "primary_emotion": Emotion.NEUTRAL.value,
                "emotion_distribution": {},
                "message_count": 0,
            }

        all_emotions: Dict[Emotion, int] = {e: 0 for e in Emotion}

        for message in messages:
            result = self.detect_emotion(message)
            all_emotions[result.primary_emotion] += 1

        total = len(messages)
        distribution = {
            e.value: count / total
            for e, count in all_emotions.items()
            if count > 0
        }

        primary = max(all_emotions, key=all_emotions.get)

        return {
            "primary_emotion": primary.value,
            "emotion_distribution": distribution,
            "message_count": total,
            "emotion_counts": {e.value: c for e, c in all_emotions.items() if c > 0},
        }


# Module-level convenience function
def detect_emotion(text: str) -> EmotionResult:
    """
    Convenience function to detect emotion in text.

    Args:
        text: The text to analyze.

    Returns:
        EmotionResult with detected emotion.
    """
    detector = EmotionDetector()
    return detector.detect_emotion(text)
