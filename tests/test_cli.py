"""
Tests for the CLI Module.
"""

import pytest
from unittest.mock import patch, MagicMock

from chatbot.cli import (
    ChatbotCLI,
    CLIConfig,
    create_parser,
    main,
)


class TestCLIConfig:
    """Test CLIConfig dataclass."""

    def test_defaults(self):
        config = CLIConfig()
        assert config.verbose is False
        assert config.show_emotions is True
        assert config.show_scores is True
        assert config.color_output is True

    def test_custom_values(self):
        config = CLIConfig(verbose=True, show_emotions=False)
        assert config.verbose is True
        assert config.show_emotions is False


class TestChatbotCLI:
    """Test ChatbotCLI class."""

    def test_initialization(self):
        cli = ChatbotCLI()
        assert cli.chatbot is not None
        assert cli.analyzer is not None

    def test_with_config(self):
        config = CLIConfig(verbose=True)
        cli = ChatbotCLI(config=config)
        assert cli.config.verbose is True

    def test_analyze_text(self):
        cli = ChatbotCLI()
        result = cli.analyze_text("I am happy!")
        assert "text" in result
        assert "sentiment" in result
        assert "emotions" in result

    def test_analyze_text_sentiment(self):
        cli = ChatbotCLI()
        result = cli.analyze_text("This is wonderful!")
        assert result["sentiment"]["label"] in ["positive", "negative", "neutral"]
        assert "compound" in result["sentiment"]

    def test_process_input(self):
        config = CLIConfig(show_scores=False, show_emotions=False)
        cli = ChatbotCLI(config=config)
        response = cli.process_input("Hello there!")
        assert isinstance(response, str)


class TestCreateParser:
    """Test create_parser function."""

    def test_creates_parser(self):
        parser = create_parser()
        assert parser is not None

    def test_interactive_flag(self):
        parser = create_parser()
        args = parser.parse_args(["-i"])
        assert args.interactive is True

    def test_text_argument(self):
        parser = create_parser()
        args = parser.parse_args(["-t", "Hello world"])
        assert args.text == "Hello world"

    def test_file_argument(self):
        parser = create_parser()
        args = parser.parse_args(["-f", "test.txt"])
        assert args.file == "test.txt"

    def test_verbose_flag(self):
        parser = create_parser()
        args = parser.parse_args(["-v"])
        assert args.verbose is True

    def test_no_emotions_flag(self):
        parser = create_parser()
        args = parser.parse_args(["--no-emotions"])
        assert args.no_emotions is True


class TestMain:
    """Test main function."""

    def test_with_text_arg(self):
        result = main(["-t", "I am happy"])
        assert result == 0

    def test_returns_zero(self):
        result = main(["-t", "Test message"])
        assert result == 0
