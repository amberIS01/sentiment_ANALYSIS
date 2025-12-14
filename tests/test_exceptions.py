"""
Tests for the Exceptions Module.
"""

import pytest
from chatbot.exceptions import (
    ChatbotError,
    SentimentAnalysisError,
    VADERInitializationError,
    EmptyTextError,
    ConversationError,
    EmptyConversationError,
    MessageNotFoundError,
    ValidationError,
    InputTooLongError,
    InputTooShortError,
    ConfigurationError,
    ConfigFileNotFoundError,
    InvalidConfigurationError,
    ExportError,
    UnsupportedFormatError,
    ExportDirectoryError,
)


class TestChatbotError:
    """Test base ChatbotError."""

    def test_basic_error(self):
        error = ChatbotError("Test error")
        assert str(error) == "Test error"

    def test_error_with_details(self):
        error = ChatbotError("Test error", details={"key": "value"})
        assert "Details" in str(error)


class TestSentimentErrors:
    """Test sentiment-related errors."""

    def test_sentiment_analysis_error(self):
        error = SentimentAnalysisError()
        assert "Sentiment analysis failed" in str(error)

    def test_vader_init_error(self):
        error = VADERInitializationError()
        assert "VADER" in str(error)

    def test_empty_text_error(self):
        error = EmptyTextError()
        assert "empty" in str(error).lower()


class TestConversationErrors:
    """Test conversation-related errors."""

    def test_conversation_error(self):
        error = ConversationError()
        assert "Conversation" in str(error)

    def test_empty_conversation_error(self):
        error = EmptyConversationError()
        assert "empty" in str(error).lower()

    def test_message_not_found_error(self):
        error = MessageNotFoundError("msg123")
        assert "msg123" in str(error)


class TestValidationErrors:
    """Test validation-related errors."""

    def test_validation_error(self):
        error = ValidationError("Invalid input", field="username")
        assert error.field == "username"

    def test_input_too_long(self):
        error = InputTooLongError(1000, 500)
        assert error.length == 1000
        assert error.max_length == 500

    def test_input_too_short(self):
        error = InputTooShortError(2, 5)
        assert error.length == 2
        assert error.min_length == 5


class TestConfigErrors:
    """Test configuration-related errors."""

    def test_configuration_error(self):
        error = ConfigurationError("Bad config", key="api_key")
        assert error.key == "api_key"

    def test_config_file_not_found(self):
        error = ConfigFileNotFoundError("/path/to/config.json")
        assert error.filepath == "/path/to/config.json"

    def test_invalid_configuration(self):
        errors_list = ["Error 1", "Error 2"]
        error = InvalidConfigurationError("Invalid", errors=errors_list)
        assert len(error.errors) == 2


class TestExportErrors:
    """Test export-related errors."""

    def test_export_error(self):
        error = ExportError("Export failed", format="json")
        assert error.format == "json"

    def test_unsupported_format(self):
        error = UnsupportedFormatError("xml")
        assert "xml" in str(error)
        assert "json" in str(error)

    def test_export_directory_error(self):
        error = ExportDirectoryError("/invalid/path")
        assert error.directory == "/invalid/path"
