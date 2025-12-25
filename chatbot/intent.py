"""
Intent Detector Module

Detect user intent from text.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Set
from enum import Enum
import re


class Intent(Enum):
    """Common intents."""

    GREETING = "greeting"
    FAREWELL = "farewell"
    QUESTION = "question"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    REQUEST = "request"
    FEEDBACK = "feedback"
    HELP = "help"
    UNKNOWN = "unknown"


@dataclass
class IntentMatch:
    """Result of intent detection."""

    intent: Intent
    confidence: float
    matched_patterns: List[str]


# Intent patterns
INTENT_PATTERNS: Dict[Intent, List[str]] = {
    Intent.GREETING: [
        r'\b(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))\b',
        r'^(hi|hello|hey)\b',
    ],
    Intent.FAREWELL: [
        r'\b(bye|goodbye|farewell|see\s+you|take\s+care)\b',
        r'\b(gotta\s+go|have\s+to\s+go|leaving)\b',
    ],
    Intent.QUESTION: [
        r'\?$',
        r'^(what|where|when|why|how|who|which|can|could|would|should|is|are|do|does)\b',
    ],
    Intent.COMPLAINT: [
        r'\b(hate|terrible|awful|horrible|worst|disappointed|frustrated|angry)\b',
        r'\b(not\s+working|doesn\'t\s+work|broken|bug|issue|problem)\b',
    ],
    Intent.COMPLIMENT: [
        r'\b(love|great|amazing|awesome|excellent|fantastic|wonderful)\b',
        r'\b(thank|thanks|appreciate|grateful)\b',
    ],
    Intent.REQUEST: [
        r'\b(please|could\s+you|can\s+you|would\s+you|i\s+need|i\s+want)\b',
        r'\b(help\s+me|show\s+me|tell\s+me|give\s+me)\b',
    ],
    Intent.HELP: [
        r'\b(help|assist|support|guide)\b',
        r'\b(how\s+do\s+i|how\s+can\s+i|how\s+to)\b',
    ],
    Intent.FEEDBACK: [
        r'\b(feedback|suggestion|recommend|opinion|think)\b',
        r'\b(i\s+think|in\s+my\s+opinion|i\s+feel)\b',
    ],
}


class IntentDetector:
    """Detect intent from text."""

    def __init__(self):
        self._patterns = {
            intent: [re.compile(p, re.IGNORECASE) for p in patterns]
            for intent, patterns in INTENT_PATTERNS.items()
        }
        self._custom_patterns: Dict[Intent, List[re.Pattern]] = {}

    def detect(self, text: str) -> IntentMatch:
        """Detect intent from text."""
        scores: Dict[Intent, int] = {}
        matches: Dict[Intent, List[str]] = {}

        for intent, patterns in self._patterns.items():
            scores[intent] = 0
            matches[intent] = []

            for pattern in patterns:
                if pattern.search(text):
                    scores[intent] += 1
                    matches[intent].append(pattern.pattern)

        # Check custom patterns
        for intent, patterns in self._custom_patterns.items():
            if intent not in scores:
                scores[intent] = 0
                matches[intent] = []

            for pattern in patterns:
                if pattern.search(text):
                    scores[intent] += 1
                    matches[intent].append(pattern.pattern)

        # Find best match
        if not any(scores.values()):
            return IntentMatch(
                intent=Intent.UNKNOWN,
                confidence=0.0,
                matched_patterns=[],
            )

        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        total_patterns = len(self._patterns.get(best_intent, [])) + \
                        len(self._custom_patterns.get(best_intent, []))

        confidence = max_score / total_patterns if total_patterns > 0 else 0.0

        return IntentMatch(
            intent=best_intent,
            confidence=min(1.0, confidence),
            matched_patterns=matches[best_intent],
        )

    def add_pattern(self, intent: Intent, pattern: str) -> None:
        """Add a custom pattern for an intent."""
        if intent not in self._custom_patterns:
            self._custom_patterns[intent] = []
        self._custom_patterns[intent].append(re.compile(pattern, re.IGNORECASE))

    def is_question(self, text: str) -> bool:
        """Check if text is a question."""
        result = self.detect(text)
        return result.intent == Intent.QUESTION

    def is_greeting(self, text: str) -> bool:
        """Check if text is a greeting."""
        result = self.detect(text)
        return result.intent == Intent.GREETING


def detect_intent(text: str) -> Intent:
    """Detect intent from text."""
    detector = IntentDetector()
    result = detector.detect(text)
    return result.intent
