"""
Constants Module

Constants and configuration values.
"""

from enum import Enum
from typing import Dict, List, Set


# Version info
VERSION = "1.9.0"
VERSION_MAJOR = 1
VERSION_MINOR = 9
VERSION_PATCH = 0


# Sentiment thresholds
class SentimentThreshold:
    """Sentiment threshold constants."""

    VERY_NEGATIVE = -0.6
    NEGATIVE = -0.2
    NEUTRAL_LOW = -0.05
    NEUTRAL_HIGH = 0.05
    POSITIVE = 0.2
    VERY_POSITIVE = 0.6


# Score ranges
class ScoreRange:
    """Score range constants."""

    MIN = -1.0
    MAX = 1.0
    NEUTRAL = 0.0


# Text limits
class TextLimit:
    """Text length limits."""

    MIN_LENGTH = 1
    MAX_LENGTH = 10000
    OPTIMAL_LENGTH = 100
    TRUNCATE_LENGTH = 500


# Default configurations
class DefaultConfig:
    """Default configuration values."""

    CACHE_SIZE = 1000
    CACHE_TTL = 3600
    BATCH_SIZE = 10
    MAX_WORKERS = 4
    RETRY_ATTEMPTS = 3
    RETRY_DELAY = 1.0
    TIMEOUT = 30.0


# Sentiment labels
SENTIMENT_LABELS: Dict[str, str] = {
    "very_negative": "Very Negative",
    "negative": "Negative",
    "neutral": "Neutral",
    "positive": "Positive",
    "very_positive": "Very Positive",
}


# Emotion categories
EMOTIONS: List[str] = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
    "trust",
    "anticipation",
]


# Intent keywords
GREETING_KEYWORDS: Set[str] = {
    "hello", "hi", "hey", "greetings", "good morning",
    "good afternoon", "good evening", "howdy",
}

FAREWELL_KEYWORDS: Set[str] = {
    "goodbye", "bye", "farewell", "see you", "take care",
    "later", "goodnight", "cya",
}

QUESTION_KEYWORDS: Set[str] = {
    "what", "where", "when", "why", "how", "who",
    "which", "whose", "whom",
}


# File extensions
SUPPORTED_FORMATS: List[str] = [
    "json",
    "csv",
    "txt",
    "xml",
    "yaml",
]


# API defaults
class APIDefaults:
    """API configuration defaults."""

    TIMEOUT = 30
    MAX_RETRIES = 3
    RATE_LIMIT = 100
    PAGE_SIZE = 50


# Error messages
class ErrorMessage:
    """Error message constants."""

    EMPTY_TEXT = "Text cannot be empty"
    TEXT_TOO_LONG = "Text exceeds maximum length"
    INVALID_SCORE = "Score must be between -1 and 1"
    ANALYSIS_FAILED = "Sentiment analysis failed"
    CACHE_ERROR = "Cache operation failed"


# Status codes
class Status:
    """Status constants."""

    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


def get_version() -> str:
    """Get version string."""
    return VERSION


def get_sentiment_label(category: str) -> str:
    """Get sentiment label."""
    return SENTIMENT_LABELS.get(category, "Unknown")
