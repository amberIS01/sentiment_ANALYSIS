"""
Chatbot with Sentiment Analysis Package

This package provides a modular chatbot implementation with both
conversation-level and statement-level sentiment analysis capabilities.
"""

from .sentiment import SentimentAnalyzer
from .conversation import ConversationManager
from .bot import Chatbot

__all__ = ["SentimentAnalyzer", "ConversationManager", "Chatbot"]
__version__ = "1.0.0"
