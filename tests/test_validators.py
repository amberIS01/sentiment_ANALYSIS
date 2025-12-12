"""
Tests for the Validators Module.
"""

import pytest
from chatbot.validators import (
    InputValidator,
    ValidationResult,
    SentimentScoreValidator,
    MessageListValidator,
    sanitize_for_display,
    normalize_whitespace,
)


class TestValidationResult:
    """Test cases for ValidationResult dataclass."""

    def test_valid_result(self):
        """Test creating a valid result."""
        result = ValidationResult(is_valid=True, cleaned_value="test")
        assert result.is_valid is True
        assert result.cleaned_value == "test"
        assert result.message is None

    def test_invalid_result(self):
        """Test creating an invalid result."""
        result = ValidationResult(is_valid=False, message="Error occurred")
        assert result.is_valid is False
        assert result.message == "Error occurred"

    def test_bool_conversion(self):
        """Test boolean conversion of ValidationResult."""
        valid = ValidationResult(is_valid=True)
        invalid = ValidationResult(is_valid=False)
        assert bool(valid) is True
        assert bool(invalid) is False


class TestInputValidator:
    """Test cases for InputValidator."""

    @pytest.fixture
    def validator(self):
        """Create an InputValidator instance."""
        return InputValidator()

    def test_valid_message(self, validator):
        """Test validating a normal message."""
        result = validator.validate("Hello, how are you?")
        assert result.is_valid
        assert result.cleaned_value == "Hello, how are you?"

    def test_empty_message(self, validator):
        """Test that empty messages are invalid."""
        result = validator.validate("")
        assert not result.is_valid
        assert "too short" in result.message.lower()

    def test_whitespace_only(self, validator):
        """Test that whitespace-only messages are invalid."""
        result = validator.validate("   \t\n   ")
        assert not result.is_valid

    def test_none_message(self, validator):
        """Test that None messages are invalid."""
        result = validator.validate(None)
        assert not result.is_valid
        assert "None" in result.message

    def test_message_too_long(self):
        """Test that messages exceeding max length are invalid."""
        validator = InputValidator(max_length=10)
        result = validator.validate("This is a very long message")
        assert not result.is_valid
        assert "exceeds maximum" in result.message.lower()

    def test_strips_whitespace(self, validator):
        """Test that leading/trailing whitespace is stripped."""
        result = validator.validate("  Hello  ")
        assert result.is_valid
        assert result.cleaned_value == "Hello"

    def test_strips_html_tags(self, validator):
        """Test that HTML tags are stripped."""
        result = validator.validate("Hello <b>world</b>!")
        assert result.is_valid
        assert "<b>" not in result.cleaned_value
        assert "Hello world!" in result.cleaned_value

    def test_custom_max_length(self):
        """Test custom maximum length."""
        validator = InputValidator(max_length=50)
        result = validator.validate("A" * 60)
        assert not result.is_valid

    def test_custom_min_length(self):
        """Test custom minimum length."""
        validator = InputValidator(min_length=5)
        result = validator.validate("Hi")
        assert not result.is_valid

    def test_is_command_detection(self, validator):
        """Test command detection."""
        assert validator.is_command("quit") == (True, "quit")
        assert validator.is_command("exit") == (True, "exit")
        assert validator.is_command("summary") == (True, "summary")
        assert validator.is_command("help") == (True, "help")
        assert validator.is_command("clear") == (True, "clear")

    def test_is_not_command(self, validator):
        """Test non-command messages."""
        assert validator.is_command("hello") == (False, None)
        assert validator.is_command("how are you?") == (False, None)

    def test_is_command_case_insensitive(self, validator):
        """Test that command detection is case insensitive."""
        assert validator.is_command("QUIT") == (True, "quit")
        assert validator.is_command("Exit") == (True, "exit")


class TestSentimentScoreValidator:
    """Test cases for SentimentScoreValidator."""

    def test_valid_score(self):
        """Test validating a valid score."""
        result = SentimentScoreValidator.validate_score(0.5)
        assert result.is_valid

    def test_score_at_boundaries(self):
        """Test scores at valid boundaries."""
        assert SentimentScoreValidator.validate_score(-1.0).is_valid
        assert SentimentScoreValidator.validate_score(1.0).is_valid
        assert SentimentScoreValidator.validate_score(0.0).is_valid

    def test_score_out_of_range(self):
        """Test scores outside valid range."""
        result_high = SentimentScoreValidator.validate_score(1.5)
        result_low = SentimentScoreValidator.validate_score(-1.5)
        assert not result_high.is_valid
        assert not result_low.is_valid

    def test_non_numeric_score(self):
        """Test non-numeric score values."""
        result = SentimentScoreValidator.validate_score("not a number")
        assert not result.is_valid

    def test_valid_percentage(self):
        """Test validating a valid percentage."""
        result = SentimentScoreValidator.validate_percentage(0.75)
        assert result.is_valid

    def test_percentage_at_boundaries(self):
        """Test percentages at boundaries."""
        assert SentimentScoreValidator.validate_percentage(0.0).is_valid
        assert SentimentScoreValidator.validate_percentage(1.0).is_valid

    def test_percentage_out_of_range(self):
        """Test percentages outside valid range."""
        assert not SentimentScoreValidator.validate_percentage(-0.1).is_valid
        assert not SentimentScoreValidator.validate_percentage(1.1).is_valid


class TestMessageListValidator:
    """Test cases for MessageListValidator."""

    def test_valid_list(self):
        """Test validating a valid list."""
        result = MessageListValidator.validate(["msg1", "msg2"])
        assert result.is_valid

    def test_empty_list(self):
        """Test that empty list is valid."""
        result = MessageListValidator.validate([])
        assert result.is_valid

    def test_none_list(self):
        """Test that None is invalid."""
        result = MessageListValidator.validate(None)
        assert not result.is_valid

    def test_non_list(self):
        """Test that non-list types are invalid."""
        result = MessageListValidator.validate("not a list")
        assert not result.is_valid


class TestSanitizeFunctions:
    """Test cases for sanitization functions."""

    def test_sanitize_for_display(self):
        """Test sanitize_for_display function."""
        result = sanitize_for_display("Hello, world!")
        assert result == "Hello, world!"

    def test_sanitize_truncates_long_text(self):
        """Test that long text is truncated."""
        long_text = "A" * 200
        result = sanitize_for_display(long_text, max_length=50)
        assert len(result) == 50
        assert result.endswith("...")

    def test_sanitize_empty_string(self):
        """Test sanitizing empty string."""
        result = sanitize_for_display("")
        assert result == ""

    def test_sanitize_removes_control_chars(self):
        """Test that control characters are removed."""
        text_with_control = "Hello\x00World"
        result = sanitize_for_display(text_with_control)
        assert "\x00" not in result

    def test_normalize_whitespace(self):
        """Test normalize_whitespace function."""
        text = "Hello    world"
        result = normalize_whitespace(text)
        assert result == "Hello world"

    def test_normalize_multiple_newlines(self):
        """Test normalizing multiple newlines."""
        text = "Hello\n\n\n\nWorld"
        result = normalize_whitespace(text)
        assert "\n\n\n" not in result

    def test_normalize_strips_whitespace(self):
        """Test that normalize_whitespace strips leading/trailing."""
        text = "  Hello  "
        result = normalize_whitespace(text)
        assert result == "Hello"

    def test_normalize_empty_string(self):
        """Test normalizing empty string."""
        result = normalize_whitespace("")
        assert result == ""
