"""
Input Validation Module

This module provides validation utilities for user input and data
throughout the chatbot application.
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    is_valid: bool
    message: Optional[str] = None
    cleaned_value: Optional[str] = None

    def __bool__(self) -> bool:
        return self.is_valid


class InputValidator:
    """
    Validator for user input messages.

    Provides validation and sanitization for user messages
    before processing by the chatbot.
    """

    # Maximum message length
    MAX_MESSAGE_LENGTH: int = 5000
    MIN_MESSAGE_LENGTH: int = 1

    # Pattern for detecting potential code injection attempts
    INJECTION_PATTERNS = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
    ]

    def __init__(
        self,
        max_length: int = MAX_MESSAGE_LENGTH,
        min_length: int = MIN_MESSAGE_LENGTH,
        strip_html: bool = True,
    ):
        """
        Initialize the validator.

        Args:
            max_length: Maximum allowed message length.
            min_length: Minimum required message length.
            strip_html: Whether to strip HTML tags.
        """
        self.max_length = max_length
        self.min_length = min_length
        self.strip_html = strip_html

    def validate(self, message: str) -> ValidationResult:
        """
        Validate and sanitize a user message.

        Args:
            message: The message to validate.

        Returns:
            ValidationResult with validation status and cleaned message.
        """
        if message is None:
            return ValidationResult(
                is_valid=False,
                message="Message cannot be None",
            )

        # Strip whitespace
        cleaned = message.strip()

        # Check minimum length
        if len(cleaned) < self.min_length:
            return ValidationResult(
                is_valid=False,
                message="Message is too short",
            )

        # Check maximum length
        if len(cleaned) > self.max_length:
            return ValidationResult(
                is_valid=False,
                message=f"Message exceeds maximum length of {self.max_length} characters",
            )

        # Strip HTML if enabled
        if self.strip_html:
            cleaned = self._strip_html_tags(cleaned)

        # Check for injection patterns (warn but allow)
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, cleaned, re.IGNORECASE):
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # Re-check length after cleaning
        if len(cleaned.strip()) < self.min_length:
            return ValidationResult(
                is_valid=False,
                message="Message is empty after sanitization",
            )

        return ValidationResult(
            is_valid=True,
            cleaned_value=cleaned.strip(),
        )

    def _strip_html_tags(self, text: str) -> str:
        """Remove HTML tags from text."""
        clean = re.sub(r"<[^>]+>", "", text)
        return clean

    def is_command(self, message: str) -> Tuple[bool, Optional[str]]:
        """
        Check if the message is a command.

        Args:
            message: The message to check.

        Returns:
            Tuple of (is_command, command_name).
        """
        if not message:
            return False, None

        cleaned = message.strip().lower()
        commands = ["quit", "exit", "summary", "clear", "help", "export"]

        if cleaned in commands:
            return True, cleaned

        return False, None


class SentimentScoreValidator:
    """Validator for sentiment scores."""

    @staticmethod
    def validate_score(score: float, name: str = "score") -> ValidationResult:
        """
        Validate a sentiment score is in valid range.

        Args:
            score: The score to validate.
            name: Name of the score for error messages.

        Returns:
            ValidationResult with validation status.
        """
        if not isinstance(score, (int, float)):
            return ValidationResult(
                is_valid=False,
                message=f"{name} must be a number",
            )

        if score < -1.0 or score > 1.0:
            return ValidationResult(
                is_valid=False,
                message=f"{name} must be between -1.0 and 1.0",
            )

        return ValidationResult(is_valid=True)

    @staticmethod
    def validate_percentage(value: float, name: str = "value") -> ValidationResult:
        """
        Validate a percentage value (0.0 to 1.0).

        Args:
            value: The value to validate.
            name: Name of the value for error messages.

        Returns:
            ValidationResult with validation status.
        """
        if not isinstance(value, (int, float)):
            return ValidationResult(
                is_valid=False,
                message=f"{name} must be a number",
            )

        if value < 0.0 or value > 1.0:
            return ValidationResult(
                is_valid=False,
                message=f"{name} must be between 0.0 and 1.0",
            )

        return ValidationResult(is_valid=True)


class MessageListValidator:
    """Validator for message lists."""

    @staticmethod
    def validate(messages: list) -> ValidationResult:
        """
        Validate a list of messages.

        Args:
            messages: The list to validate.

        Returns:
            ValidationResult with validation status.
        """
        if messages is None:
            return ValidationResult(
                is_valid=False,
                message="Messages list cannot be None",
            )

        if not isinstance(messages, list):
            return ValidationResult(
                is_valid=False,
                message="Messages must be a list",
            )

        return ValidationResult(is_valid=True)


def sanitize_for_display(text: str, max_length: int = 100) -> str:
    """
    Sanitize text for safe display.

    Args:
        text: The text to sanitize.
        max_length: Maximum length for display.

    Returns:
        Sanitized text string.
    """
    if not text:
        return ""

    # Remove control characters
    cleaned = "".join(char for char in text if ord(char) >= 32 or char in "\n\t")

    # Truncate if needed
    if len(cleaned) > max_length:
        cleaned = cleaned[: max_length - 3] + "..."

    return cleaned


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Args:
        text: The text to normalize.

    Returns:
        Text with normalized whitespace.
    """
    if not text:
        return ""

    # Replace multiple spaces with single space
    normalized = re.sub(r" +", " ", text)

    # Replace multiple newlines with double newline
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)

    return normalized.strip()
