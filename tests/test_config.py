"""
Tests for the Configuration Module.
"""

import json
import os
import pytest
from pathlib import Path

from chatbot.config import (
    ChatbotConfig,
    SentimentConfig,
    ResponseConfig,
    LoggingConfig,
    ExportConfig,
    CLIConfig,
    get_config,
    set_config,
    load_config,
)


class TestSentimentConfig:
    """Test cases for SentimentConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = SentimentConfig()
        assert config.positive_threshold == 0.05
        assert config.negative_threshold == -0.05

    def test_custom_values(self):
        """Test custom configuration values."""
        config = SentimentConfig(
            positive_threshold=0.1,
            negative_threshold=-0.1
        )
        assert config.positive_threshold == 0.1
        assert config.negative_threshold == -0.1


class TestChatbotConfig:
    """Test cases for ChatbotConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = ChatbotConfig()
        assert config.version == "1.1.0"
        assert config.debug is False
        assert isinstance(config.sentiment, SentimentConfig)

    def test_from_dict(self):
        """Test creating config from dictionary."""
        data = {
            "debug": True,
            "sentiment": {
                "positive_threshold": 0.1
            }
        }
        config = ChatbotConfig.from_dict(data)
        assert config.debug is True
        assert config.sentiment.positive_threshold == 0.1

    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = ChatbotConfig()
        data = config.to_dict()

        assert "sentiment" in data
        assert "logging" in data
        assert "export" in data

    def test_from_json_file(self, tmp_path):
        """Test loading config from JSON file."""
        config_data = {
            "debug": True,
            "sentiment": {"positive_threshold": 0.2}
        }
        config_file = tmp_path / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f)

        config = ChatbotConfig.from_json_file(str(config_file))
        assert config.debug is True
        assert config.sentiment.positive_threshold == 0.2

    def test_from_json_file_not_found(self):
        """Test error when config file not found."""
        with pytest.raises(FileNotFoundError):
            ChatbotConfig.from_json_file("nonexistent.json")

    def test_save_to_json(self, tmp_path):
        """Test saving config to JSON file."""
        config = ChatbotConfig()
        config.debug = True

        filepath = tmp_path / "saved_config.json"
        config.save_to_json(str(filepath))

        assert filepath.exists()
        with open(filepath, 'r') as f:
            data = json.load(f)
        assert data["debug"] is True

    def test_validate_valid_config(self):
        """Test validation of valid config."""
        config = ChatbotConfig()
        errors = config.validate()
        assert len(errors) == 0

    def test_validate_invalid_threshold(self):
        """Test validation catches invalid thresholds."""
        config = ChatbotConfig()
        config.sentiment.positive_threshold = 2.0  # Invalid
        errors = config.validate()
        assert len(errors) > 0

    def test_validate_invalid_log_level(self):
        """Test validation catches invalid log level."""
        config = ChatbotConfig()
        config.logging.level = "INVALID"
        errors = config.validate()
        assert len(errors) > 0

    def test_from_env(self, monkeypatch):
        """Test creating config from environment variables."""
        monkeypatch.setenv("CHATBOT_DEBUG", "true")
        monkeypatch.setenv("CHATBOT_LOG_LEVEL", "DEBUG")

        config = ChatbotConfig.from_env()
        assert config.debug is True
        assert config.logging.level == "DEBUG"


class TestGlobalConfig:
    """Test global configuration functions."""

    def test_get_config_default(self):
        """Test getting default config."""
        # Reset global config
        import chatbot.config as config_module
        config_module._global_config = None

        config = get_config()
        assert isinstance(config, ChatbotConfig)

    def test_set_config(self):
        """Test setting global config."""
        custom_config = ChatbotConfig()
        custom_config.debug = True

        set_config(custom_config)
        config = get_config()
        assert config.debug is True

    def test_load_config_from_file(self, tmp_path):
        """Test loading config from file."""
        config_data = {"debug": True}
        config_file = tmp_path / "test_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f)

        config = load_config(str(config_file))
        assert config.debug is True


class TestLoggingConfig:
    """Test cases for LoggingConfig."""

    def test_default_values(self):
        """Test default logging config."""
        config = LoggingConfig()
        assert config.enabled is True
        assert config.level == "INFO"
        assert config.log_file is None

    def test_custom_values(self):
        """Test custom logging config."""
        config = LoggingConfig(
            level="DEBUG",
            log_file="/tmp/test.log"
        )
        assert config.level == "DEBUG"
        assert config.log_file == "/tmp/test.log"


class TestExportConfig:
    """Test cases for ExportConfig."""

    def test_default_values(self):
        """Test default export config."""
        config = ExportConfig()
        assert config.export_directory == "exports"
        assert config.default_format == "json"

    def test_custom_values(self):
        """Test custom export config."""
        config = ExportConfig(
            export_directory="/custom/path",
            default_format="csv"
        )
        assert config.export_directory == "/custom/path"
        assert config.default_format == "csv"
