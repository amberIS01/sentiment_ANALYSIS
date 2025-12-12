"""
Logging Module

This module provides centralized logging configuration for the chatbot application.
It supports both console and file logging with customizable formats and levels.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEBUG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"


def setup_logger(
    name: str = "chatbot",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True,
    debug_mode: bool = False,
) -> logging.Logger:
    """
    Set up and configure a logger instance.

    Args:
        name: The name of the logger.
        level: The logging level (default: INFO).
        log_file: Optional path to a log file.
        console_output: Whether to output to console (default: True).
        debug_mode: Whether to use debug format with extra details.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Choose format based on mode
    log_format = DEBUG_FORMAT if debug_mode else DEFAULT_FORMAT
    formatter = logging.Formatter(log_format)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "chatbot") -> logging.Logger:
    """
    Get an existing logger or create a default one.

    Args:
        name: The name of the logger.

    Returns:
        Logger instance.
    """
    logger = logging.getLogger(name)

    # If no handlers configured, set up with defaults
    if not logger.handlers:
        return setup_logger(name)

    return logger


class ChatLogger:
    """
    A specialized logger for chatbot conversations.

    This logger provides structured logging for chat events,
    sentiment analysis results, and conversation statistics.
    """

    def __init__(
        self,
        name: str = "chatbot.conversation",
        log_file: Optional[str] = None,
        debug_mode: bool = False,
    ):
        """
        Initialize the chat logger.

        Args:
            name: The logger name.
            log_file: Optional path for conversation logs.
            debug_mode: Enable debug-level logging.
        """
        level = logging.DEBUG if debug_mode else logging.INFO
        self._logger = setup_logger(
            name=name,
            level=level,
            log_file=log_file,
            console_output=False,  # Chat logger typically writes to file only
            debug_mode=debug_mode,
        )
        self._conversation_id: Optional[str] = None

    def start_conversation(self) -> str:
        """
        Log the start of a new conversation.

        Returns:
            The conversation ID.
        """
        self._conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._logger.info(f"Conversation started: {self._conversation_id}")
        return self._conversation_id

    def log_user_message(self, message: str, sentiment_label: str, score: float) -> None:
        """
        Log a user message with its sentiment.

        Args:
            message: The user's message.
            sentiment_label: The sentiment classification.
            score: The sentiment score.
        """
        self._logger.info(
            f"[{self._conversation_id}] USER: {message[:100]}... | "
            f"Sentiment: {sentiment_label} ({score:.2f})"
        )

    def log_bot_response(self, response: str) -> None:
        """
        Log a bot response.

        Args:
            response: The bot's response.
        """
        self._logger.info(f"[{self._conversation_id}] BOT: {response[:100]}...")

    def log_summary(
        self,
        overall_sentiment: str,
        avg_score: float,
        message_count: int,
        mood_trend: str,
    ) -> None:
        """
        Log the conversation summary.

        Args:
            overall_sentiment: The overall sentiment label.
            avg_score: Average sentiment score.
            message_count: Total message count.
            mood_trend: The detected mood trend.
        """
        self._logger.info(
            f"[{self._conversation_id}] SUMMARY: "
            f"Overall={overall_sentiment}, AvgScore={avg_score:.2f}, "
            f"Messages={message_count}, Trend={mood_trend}"
        )

    def end_conversation(self) -> None:
        """Log the end of a conversation."""
        self._logger.info(f"Conversation ended: {self._conversation_id}")
        self._conversation_id = None

    def log_error(self, error: str, exc_info: bool = False) -> None:
        """
        Log an error.

        Args:
            error: The error message.
            exc_info: Whether to include exception info.
        """
        self._logger.error(f"[{self._conversation_id}] ERROR: {error}", exc_info=exc_info)

    def log_warning(self, warning: str) -> None:
        """
        Log a warning.

        Args:
            warning: The warning message.
        """
        self._logger.warning(f"[{self._conversation_id}] WARNING: {warning}")


# Module-level default logger
_default_logger: Optional[logging.Logger] = None


def get_default_logger() -> logging.Logger:
    """Get the module-level default logger."""
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logger("chatbot", console_output=False)
    return _default_logger
