"""
Chatbot with Sentiment Analysis Package

This package provides a modular chatbot implementation with both
conversation-level and statement-level sentiment analysis capabilities.

Features:
- VADER-based sentiment analysis
- Emotion detection (joy, sadness, anger, fear, etc.)
- Conversation history management
- Statistics tracking and analysis
- Export to JSON, CSV, and text formats
"""

from .sentiment import (
    SentimentAnalyzer,
    SentimentResult,
    SentimentLabel,
    ConversationSentimentSummary,
)
from .conversation import ConversationManager, Message, MessageRole
from .bot import Chatbot
from .emotions import EmotionDetector, Emotion, EmotionResult
from .exporter import ConversationExporter, export_conversation
from .statistics import StatisticsTracker, ConversationStatistics
from .validators import InputValidator, ValidationResult
from .logger import setup_logger, get_logger, ChatLogger
from .config import ChatbotConfig, get_config, load_config
from .utils import truncate_text, format_duration, safe_divide

__all__ = [
    # Core classes
    "SentimentAnalyzer",
    "SentimentResult",
    "SentimentLabel",
    "ConversationSentimentSummary",
    "ConversationManager",
    "Message",
    "MessageRole",
    "Chatbot",
    # Emotion detection
    "EmotionDetector",
    "Emotion",
    "EmotionResult",
    # Export functionality
    "ConversationExporter",
    "export_conversation",
    # Statistics
    "StatisticsTracker",
    "ConversationStatistics",
    # Validation
    "InputValidator",
    "ValidationResult",
    # Logging
    "setup_logger",
    "get_logger",
    "ChatLogger",
    # Configuration
    "ChatbotConfig",
    "get_config",
    "load_config",
    # Utilities
    "truncate_text",
    "format_duration",
    "safe_divide",
]

__version__ = "1.4.0"
