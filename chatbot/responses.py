"""
Response Generator Module

Generate contextual responses based on sentiment.
"""

import random
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

from .sentiment import SentimentLabel


class ResponseTone(Enum):
    """Tone of response."""

    EMPATHETIC = "empathetic"
    ENCOURAGING = "encouraging"
    NEUTRAL = "neutral"
    CURIOUS = "curious"


@dataclass
class GeneratedResponse:
    """A generated response."""

    text: str
    tone: ResponseTone
    sentiment_match: SentimentLabel


class ResponseGenerator:
    """Generate contextual responses."""

    def __init__(self):
        """Initialize generator with response templates."""
        self._templates: Dict[str, Dict[str, List[str]]] = {
            "positive": {
                "empathetic": [
                    "That's wonderful to hear!",
                    "I'm glad things are going well for you!",
                    "It sounds like you're in a great mood!",
                ],
                "encouraging": [
                    "Keep up that positive energy!",
                    "That's the spirit!",
                    "Great to see such positivity!",
                ],
                "curious": [
                    "That sounds exciting! Tell me more.",
                    "What's making you feel so good?",
                    "I'd love to hear more about that!",
                ],
            },
            "negative": {
                "empathetic": [
                    "I'm sorry to hear that.",
                    "That sounds difficult.",
                    "I understand that must be frustrating.",
                ],
                "encouraging": [
                    "Things will get better.",
                    "You've got this!",
                    "Hang in there!",
                ],
                "curious": [
                    "Would you like to talk about it?",
                    "What's been troubling you?",
                    "Is there anything I can help with?",
                ],
            },
            "neutral": {
                "empathetic": [
                    "I see.",
                    "I understand.",
                    "Thanks for sharing.",
                ],
                "encouraging": [
                    "That's interesting.",
                    "I appreciate you telling me.",
                    "Good to know.",
                ],
                "curious": [
                    "Tell me more about that.",
                    "What else is on your mind?",
                    "How do you feel about that?",
                ],
            },
        }

    def generate(
        self,
        sentiment: SentimentLabel,
        tone: Optional[ResponseTone] = None,
    ) -> GeneratedResponse:
        """Generate a response based on sentiment."""
        sentiment_key = sentiment.value
        tone = tone or random.choice(list(ResponseTone))

        if tone == ResponseTone.NEUTRAL:
            tone = random.choice([
                ResponseTone.EMPATHETIC,
                ResponseTone.ENCOURAGING,
                ResponseTone.CURIOUS,
            ])

        templates = self._templates.get(sentiment_key, {})
        tone_templates = templates.get(tone.value, ["I understand."])

        return GeneratedResponse(
            text=random.choice(tone_templates),
            tone=tone,
            sentiment_match=sentiment,
        )

    def generate_followup(
        self,
        sentiment: SentimentLabel,
    ) -> str:
        """Generate a follow-up question."""
        followups = {
            "positive": [
                "What else is going well?",
                "Any other good news to share?",
                "What are you looking forward to?",
            ],
            "negative": [
                "Is there anything else bothering you?",
                "What would help improve things?",
                "Have you tried talking to someone about this?",
            ],
            "neutral": [
                "What else would you like to discuss?",
                "Anything else on your mind?",
                "What are your thoughts?",
            ],
        }
        options = followups.get(sentiment.value, ["Anything else?"])
        return random.choice(options)

    def add_template(
        self,
        sentiment: str,
        tone: str,
        template: str,
    ) -> None:
        """Add a custom response template."""
        if sentiment not in self._templates:
            self._templates[sentiment] = {}
        if tone not in self._templates[sentiment]:
            self._templates[sentiment][tone] = []
        self._templates[sentiment][tone].append(template)


def generate_response(sentiment: SentimentLabel) -> str:
    """Generate a response for the given sentiment."""
    generator = ResponseGenerator()
    return generator.generate(sentiment).text
