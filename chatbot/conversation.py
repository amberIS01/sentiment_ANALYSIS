"""
Conversation Manager Module

This module handles conversation history management and message tracking
for the chatbot with sentiment analysis.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional

from .sentiment import SentimentAnalyzer, SentimentResult, ConversationSentimentSummary


class MessageRole(Enum):
    """Enumeration of message roles in the conversation."""
    USER = "user"
    BOT = "bot"


@dataclass
class Message:
    """Data class representing a single message in the conversation."""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    sentiment: Optional[SentimentResult] = None

    def __str__(self) -> str:
        role_label = "User" if self.role == MessageRole.USER else "Chatbot"
        return f"{role_label}: \"{self.content}\""


class ConversationManager:
    """
    Manages conversation history and provides sentiment analysis capabilities.

    This class maintains the full conversation history and integrates with
    the SentimentAnalyzer to provide both per-message (Tier 2) and
    conversation-level (Tier 1) sentiment analysis.
    """

    def __init__(self, analyzer: Optional[SentimentAnalyzer] = None):
        """
        Initialize the conversation manager.

        Args:
            analyzer: Optional SentimentAnalyzer instance. Creates one if not provided.
        """
        self._messages: List[Message] = []
        self._analyzer = analyzer or SentimentAnalyzer()
        self._started_at = datetime.now()

    @property
    def messages(self) -> List[Message]:
        """Get all messages in the conversation."""
        return self._messages.copy()

    @property
    def user_messages(self) -> List[Message]:
        """Get only user messages from the conversation."""
        return [m for m in self._messages if m.role == MessageRole.USER]

    @property
    def bot_messages(self) -> List[Message]:
        """Get only bot messages from the conversation."""
        return [m for m in self._messages if m.role == MessageRole.BOT]

    @property
    def message_count(self) -> int:
        """Get total number of messages in the conversation."""
        return len(self._messages)

    @property
    def is_empty(self) -> bool:
        """Check if the conversation has no messages."""
        return len(self._messages) == 0

    def add_user_message(self, content: str, analyze: bool = True) -> Message:
        """
        Add a user message to the conversation.

        Args:
            content: The message content.
            analyze: Whether to perform sentiment analysis on the message.

        Returns:
            The created Message object.
        """
        sentiment = self._analyzer.analyze_text(content) if analyze else None

        message = Message(
            role=MessageRole.USER,
            content=content,
            sentiment=sentiment
        )
        self._messages.append(message)
        return message

    def add_bot_message(self, content: str) -> Message:
        """
        Add a bot message to the conversation.

        Args:
            content: The message content.

        Returns:
            The created Message object.
        """
        message = Message(
            role=MessageRole.BOT,
            content=content,
            sentiment=None  # We don't analyze bot messages
        )
        self._messages.append(message)
        return message

    def get_conversation_history(self) -> List[dict]:
        """
        Get the conversation history in a format suitable for the chatbot.

        Returns:
            List of dictionaries with role and content keys.
        """
        return [
            {"role": m.role.value, "content": m.content}
            for m in self._messages
        ]

    def analyze_conversation(self) -> ConversationSentimentSummary:
        """
        Perform sentiment analysis on the entire conversation.

        Returns:
            ConversationSentimentSummary with complete analysis.
        """
        user_message_contents = [m.content for m in self.user_messages]
        return self._analyzer.analyze_conversation(user_message_contents)

    def get_formatted_history(self, include_sentiment: bool = True) -> str:
        """
        Get a formatted string representation of the conversation history.

        Args:
            include_sentiment: Whether to include sentiment info for user messages.

        Returns:
            Formatted conversation history string.
        """
        lines = []
        for message in self._messages:
            if message.role == MessageRole.USER:
                line = f"User: \"{message.content}\""
                if include_sentiment and message.sentiment:
                    line += f"\n  -> Sentiment: {message.sentiment.label.value}"
            else:
                line = f"Chatbot: \"{message.content}\""
            lines.append(line)
        return "\n".join(lines)

    def clear(self) -> None:
        """Clear all messages from the conversation."""
        self._messages.clear()
        self._started_at = datetime.now()

    def get_last_user_message(self) -> Optional[Message]:
        """Get the most recent user message."""
        user_msgs = self.user_messages
        return user_msgs[-1] if user_msgs else None

    def get_last_bot_message(self) -> Optional[Message]:
        """Get the most recent bot message."""
        bot_msgs = self.bot_messages
        return bot_msgs[-1] if bot_msgs else None
