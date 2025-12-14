"""
Tests for the Logger Module.
"""

import logging
import pytest
from pathlib import Path

from chatbot.logger import setup_logger, get_logger, ChatLogger


class TestSetupLogger:
    """Test setup_logger function."""

    def test_creates_logger(self):
        logger = setup_logger("test_logger_1")
        assert isinstance(logger, logging.Logger)

    def test_sets_level(self):
        logger = setup_logger("test_logger_2", level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_file_handler(self, tmp_path):
        log_file = tmp_path / "test.log"
        logger = setup_logger("test_logger_3", log_file=str(log_file))
        logger.info("Test message")
        assert log_file.exists()

    def test_no_duplicate_handlers(self):
        logger = setup_logger("test_logger_4")
        handler_count = len(logger.handlers)
        setup_logger("test_logger_4")
        assert len(logger.handlers) == handler_count


class TestGetLogger:
    """Test get_logger function."""

    def test_returns_logger(self):
        logger = get_logger("test_get_logger")
        assert isinstance(logger, logging.Logger)

    def test_creates_default_if_none(self):
        logger = get_logger("new_logger_test")
        assert logger is not None


class TestChatLogger:
    """Test ChatLogger class."""

    @pytest.fixture
    def chat_logger(self, tmp_path):
        log_file = tmp_path / "chat.log"
        return ChatLogger(log_file=str(log_file))

    def test_start_conversation(self, chat_logger):
        conv_id = chat_logger.start_conversation()
        assert conv_id is not None
        assert len(conv_id) > 0

    def test_log_user_message(self, chat_logger):
        chat_logger.start_conversation()
        chat_logger.log_user_message("Hello", "Positive", 0.5)

    def test_log_bot_response(self, chat_logger):
        chat_logger.start_conversation()
        chat_logger.log_bot_response("Hi there!")

    def test_log_summary(self, chat_logger):
        chat_logger.start_conversation()
        chat_logger.log_summary("Positive", 0.5, 10, "Stable")

    def test_end_conversation(self, chat_logger):
        chat_logger.start_conversation()
        chat_logger.end_conversation()
        assert chat_logger._conversation_id is None

    def test_log_error(self, chat_logger):
        chat_logger.start_conversation()
        chat_logger.log_error("Test error")

    def test_log_warning(self, chat_logger):
        chat_logger.start_conversation()
        chat_logger.log_warning("Test warning")
