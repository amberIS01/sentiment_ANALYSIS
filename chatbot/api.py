"""
API Module

This module provides a simple API interface for the chatbot.
Can be extended to support REST API frameworks like Flask or FastAPI.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

from .bot import Chatbot
from .sentiment import SentimentResult


@dataclass
class APIResponse:
    """Standard API response format."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ChatbotAPI:
    """API wrapper for chatbot functionality."""

    def __init__(self):
        self._bot = Chatbot()

    def send_message(self, message: str) -> APIResponse:
        """Send a message and get response."""
        try:
            response, sentiment = self._bot.process_message(message)
            return APIResponse(
                success=True,
                data={
                    "response": response,
                    "sentiment": {
                        "label": sentiment.label.value,
                        "score": sentiment.compound_score,
                    }
                }
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def get_summary(self) -> APIResponse:
        """Get conversation summary."""
        try:
            summary = self._bot.get_conversation_summary()
            return APIResponse(
                success=True,
                data={
                    "overall_sentiment": summary.overall_sentiment.value,
                    "average_score": summary.average_compound_score,
                    "mood_trend": summary.mood_trend,
                    "message_count": {
                        "positive": summary.positive_count,
                        "negative": summary.negative_count,
                        "neutral": summary.neutral_count,
                    }
                }
            )
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def reset(self) -> APIResponse:
        """Reset conversation."""
        try:
            self._bot.reset()
            return APIResponse(success=True, data={"message": "Conversation reset"})
        except Exception as e:
            return APIResponse(success=False, error=str(e))

    def health_check(self) -> APIResponse:
        """Check API health."""
        return APIResponse(
            success=True,
            data={
                "status": "healthy",
                "version": "1.3.0",
            }
        )


def create_api() -> ChatbotAPI:
    """Factory function to create API instance."""
    return ChatbotAPI()
