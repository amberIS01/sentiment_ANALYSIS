"""
Configuration Module

This module provides configuration management for the chatbot application,
supporting both programmatic configuration and loading from files.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SentimentConfig:
    """Configuration for sentiment analysis."""

    positive_threshold: float = 0.05
    negative_threshold: float = -0.05
    mood_trend_significant_change: float = 0.2
    mood_trend_slight_change: float = 0.1
    variance_threshold: float = 0.2


@dataclass
class ResponseConfig:
    """Configuration for chatbot responses."""

    use_keyword_matching: bool = True
    randomize_responses: bool = True
    include_sentiment_in_response: bool = True


@dataclass
class LoggingConfig:
    """Configuration for logging."""

    enabled: bool = True
    level: str = "INFO"
    log_file: Optional[str] = None
    log_to_console: bool = False
    debug_mode: bool = False


@dataclass
class ExportConfig:
    """Configuration for export functionality."""

    export_directory: str = "exports"
    default_format: str = "json"
    include_timestamps: bool = True
    include_sentiment: bool = True


@dataclass
class CLIConfig:
    """Configuration for CLI interface."""

    show_banner: bool = True
    show_sentiment: bool = True
    separator_width: int = 60
    prompt_string: str = "You: "


@dataclass
class ChatbotConfig:
    """Main configuration class for the chatbot."""

    # Component configurations
    sentiment: SentimentConfig = field(default_factory=SentimentConfig)
    response: ResponseConfig = field(default_factory=ResponseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    export: ExportConfig = field(default_factory=ExportConfig)
    cli: CLIConfig = field(default_factory=CLIConfig)

    # Application settings
    app_name: str = "Sentiment Analysis Chatbot"
    version: str = "1.1.0"
    debug: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatbotConfig":
        """
        Create configuration from a dictionary.

        Args:
            data: Configuration dictionary.

        Returns:
            ChatbotConfig instance.
        """
        config = cls()

        if "sentiment" in data:
            config.sentiment = SentimentConfig(**data["sentiment"])
        if "response" in data:
            config.response = ResponseConfig(**data["response"])
        if "logging" in data:
            config.logging = LoggingConfig(**data["logging"])
        if "export" in data:
            config.export = ExportConfig(**data["export"])
        if "cli" in data:
            config.cli = CLIConfig(**data["cli"])

        # Top-level settings
        if "app_name" in data:
            config.app_name = data["app_name"]
        if "version" in data:
            config.version = data["version"]
        if "debug" in data:
            config.debug = data["debug"]

        return config

    @classmethod
    def from_json_file(cls, filepath: str) -> "ChatbotConfig":
        """
        Load configuration from a JSON file.

        Args:
            filepath: Path to the JSON configuration file.

        Returns:
            ChatbotConfig instance.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

    @classmethod
    def from_env(cls) -> "ChatbotConfig":
        """
        Create configuration from environment variables.

        Environment variables are prefixed with CHATBOT_.
        Example: CHATBOT_DEBUG=true

        Returns:
            ChatbotConfig instance.
        """
        config = cls()

        # Check for environment variables
        if os.getenv("CHATBOT_DEBUG"):
            config.debug = os.getenv("CHATBOT_DEBUG", "").lower() == "true"

        if os.getenv("CHATBOT_LOG_LEVEL"):
            config.logging.level = os.getenv("CHATBOT_LOG_LEVEL", "INFO")

        if os.getenv("CHATBOT_LOG_FILE"):
            config.logging.log_file = os.getenv("CHATBOT_LOG_FILE")

        if os.getenv("CHATBOT_EXPORT_DIR"):
            config.export.export_directory = os.getenv("CHATBOT_EXPORT_DIR", "exports")

        return config

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.

        Returns:
            Configuration as a dictionary.
        """
        return {
            "app_name": self.app_name,
            "version": self.version,
            "debug": self.debug,
            "sentiment": asdict(self.sentiment),
            "response": asdict(self.response),
            "logging": asdict(self.logging),
            "export": asdict(self.export),
            "cli": asdict(self.cli),
        }

    def save_to_json(self, filepath: str) -> None:
        """
        Save configuration to a JSON file.

        Args:
            filepath: Path to save the configuration.
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    def validate(self) -> List[str]:
        """
        Validate the configuration.

        Returns:
            List of validation error messages (empty if valid).
        """
        errors = []

        # Validate sentiment thresholds
        if not -1.0 <= self.sentiment.positive_threshold <= 1.0:
            errors.append("positive_threshold must be between -1.0 and 1.0")
        if not -1.0 <= self.sentiment.negative_threshold <= 1.0:
            errors.append("negative_threshold must be between -1.0 and 1.0")
        if self.sentiment.negative_threshold >= self.sentiment.positive_threshold:
            errors.append("negative_threshold must be less than positive_threshold")

        # Validate logging level
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.logging.level.upper() not in valid_levels:
            errors.append(f"logging.level must be one of: {', '.join(valid_levels)}")

        # Validate export format
        valid_formats = {"json", "text", "csv"}
        if self.export.default_format not in valid_formats:
            errors.append(f"export.default_format must be one of: {', '.join(valid_formats)}")

        return errors


# Global configuration instance
_global_config: Optional[ChatbotConfig] = None


def get_config() -> ChatbotConfig:
    """
    Get the global configuration instance.

    Returns:
        The global ChatbotConfig instance.
    """
    global _global_config
    if _global_config is None:
        _global_config = ChatbotConfig()
    return _global_config


def set_config(config: ChatbotConfig) -> None:
    """
    Set the global configuration instance.

    Args:
        config: The configuration to set.
    """
    global _global_config
    _global_config = config


def load_config(filepath: Optional[str] = None) -> ChatbotConfig:
    """
    Load configuration from file or environment.

    Args:
        filepath: Optional path to configuration file.

    Returns:
        Loaded ChatbotConfig instance.
    """
    if filepath:
        config = ChatbotConfig.from_json_file(filepath)
    else:
        # Try default locations
        default_paths = [
            "chatbot.json",
            "config/chatbot.json",
            Path.home() / ".chatbot" / "config.json",
        ]

        config = None
        for path in default_paths:
            try:
                config = ChatbotConfig.from_json_file(str(path))
                break
            except FileNotFoundError:
                continue

        if config is None:
            # Fall back to environment variables
            config = ChatbotConfig.from_env()

    set_config(config)
    return config
