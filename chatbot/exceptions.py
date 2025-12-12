"""
Custom Exceptions Module

This module defines custom exception classes for the chatbot application,
providing more specific error handling and better error messages.
"""

from typing import Any, Optional


class ChatbotError(Exception):
    """Base exception for all chatbot-related errors."""

    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class SentimentAnalysisError(ChatbotError):
    """Exception raised when sentiment analysis fails."""

    def __init__(self, message: str = "Sentiment analysis failed", details: Optional[Any] = None):
        super().__init__(message, details)


class VADERInitializationError(SentimentAnalysisError):
    """Exception raised when VADER lexicon cannot be loaded."""

    def __init__(self, message: str = "Failed to initialize VADER sentiment analyzer"):
        super().__init__(message)


class EmptyTextError(SentimentAnalysisError):
    """Exception raised when trying to analyze empty text."""

    def __init__(self, message: str = "Cannot analyze empty or whitespace-only text"):
        super().__init__(message)


class ConversationError(ChatbotError):
    """Exception raised for conversation-related errors."""

    def __init__(self, message: str = "Conversation error occurred", details: Optional[Any] = None):
        super().__init__(message, details)


class EmptyConversationError(ConversationError):
    """Exception raised when operating on an empty conversation."""

    def __init__(self, message: str = "Conversation is empty"):
        super().__init__(message)


class MessageNotFoundError(ConversationError):
    """Exception raised when a requested message is not found."""

    def __init__(self, message_id: Optional[str] = None):
        msg = "Message not found"
        if message_id:
            msg = f"Message with ID '{message_id}' not found"
        super().__init__(msg, message_id)


class ValidationError(ChatbotError):
    """Exception raised for validation failures."""

    def __init__(self, message: str = "Validation failed", field: Optional[str] = None):
        self.field = field
        details = {"field": field} if field else None
        super().__init__(message, details)


class InputTooLongError(ValidationError):
    """Exception raised when input exceeds maximum length."""

    def __init__(self, length: int, max_length: int):
        message = f"Input length ({length}) exceeds maximum allowed ({max_length})"
        super().__init__(message, field="input")
        self.length = length
        self.max_length = max_length


class InputTooShortError(ValidationError):
    """Exception raised when input is below minimum length."""

    def __init__(self, length: int, min_length: int):
        message = f"Input length ({length}) is below minimum required ({min_length})"
        super().__init__(message, field="input")
        self.length = length
        self.min_length = min_length


class ConfigurationError(ChatbotError):
    """Exception raised for configuration-related errors."""

    def __init__(self, message: str = "Configuration error", key: Optional[str] = None):
        self.key = key
        details = {"key": key} if key else None
        super().__init__(message, details)


class ConfigFileNotFoundError(ConfigurationError):
    """Exception raised when configuration file is not found."""

    def __init__(self, filepath: str):
        message = f"Configuration file not found: {filepath}"
        super().__init__(message)
        self.filepath = filepath


class InvalidConfigurationError(ConfigurationError):
    """Exception raised when configuration is invalid."""

    def __init__(self, message: str, errors: Optional[list] = None):
        super().__init__(message, errors)
        self.errors = errors or []


class ExportError(ChatbotError):
    """Exception raised for export-related errors."""

    def __init__(self, message: str = "Export failed", format: Optional[str] = None):
        self.format = format
        details = {"format": format} if format else None
        super().__init__(message, details)


class UnsupportedFormatError(ExportError):
    """Exception raised when an unsupported export format is requested."""

    def __init__(self, format: str, supported_formats: Optional[list] = None):
        supported = supported_formats or ["json", "text", "csv"]
        message = f"Unsupported format '{format}'. Supported formats: {', '.join(supported)}"
        super().__init__(message, format)
        self.supported_formats = supported


class ExportDirectoryError(ExportError):
    """Exception raised when export directory cannot be created."""

    def __init__(self, directory: str):
        message = f"Cannot create export directory: {directory}"
        super().__init__(message)
        self.directory = directory


class EmotionDetectionError(ChatbotError):
    """Exception raised when emotion detection fails."""

    def __init__(self, message: str = "Emotion detection failed", details: Optional[Any] = None):
        super().__init__(message, details)


class ResponseGenerationError(ChatbotError):
    """Exception raised when response generation fails."""

    def __init__(self, message: str = "Failed to generate response", details: Optional[Any] = None):
        super().__init__(message, details)


# Error handling utilities
def handle_sentiment_error(func):
    """Decorator to handle sentiment analysis errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise SentimentAnalysisError(str(e), details={"function": func.__name__})
    return wrapper


def handle_conversation_error(func):
    """Decorator to handle conversation errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ChatbotError:
            raise
        except Exception as e:
            raise ConversationError(str(e), details={"function": func.__name__})
    return wrapper
