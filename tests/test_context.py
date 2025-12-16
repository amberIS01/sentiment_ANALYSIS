"""
Tests for the Context Module.
"""

import pytest

from chatbot.context import (
    ChatContext,
    ContextVar,
    ContextManager,
    chat_context,
    temporary_context,
    get_current_context,
    set_current_context,
)


class TestChatContext:
    """Test ChatContext dataclass."""

    def test_creation(self):
        ctx = ChatContext(session_id="sess-123")
        assert ctx.session_id == "sess-123"
        assert ctx.message_count == 0

    def test_with_user_id(self):
        ctx = ChatContext(session_id="sess-123", user_id="user-456")
        assert ctx.user_id == "user-456"

    def test_increment_messages(self):
        ctx = ChatContext(session_id="sess-123")
        ctx.increment_messages()
        ctx.increment_messages()
        assert ctx.message_count == 2

    def test_metadata(self):
        ctx = ChatContext(session_id="sess-123")
        ctx.metadata["key"] = "value"
        assert ctx.metadata["key"] == "value"


class TestContextVar:
    """Test ContextVar class."""

    def test_default_value(self):
        var = ContextVar("test", default="default")
        assert var.get() == "default"

    def test_set_and_get(self):
        var = ContextVar("test")
        var.set("value")
        assert var.get() == "value"

    def test_set_returns_previous(self):
        var = ContextVar("test", default="old")
        previous = var.set("new")
        assert previous == "old"

    def test_reset(self):
        var = ContextVar("test", default="default")
        var.set("value")
        var.reset()
        assert var.get() == "default"


class TestContextManager:
    """Test ContextManager class."""

    def test_initialization(self):
        manager = ContextManager()
        assert manager is not None

    def test_create(self):
        manager = ContextManager()
        ctx = manager.create("sess-123")
        assert ctx.session_id == "sess-123"

    def test_get(self):
        manager = ContextManager()
        manager.create("sess-123")
        ctx = manager.get("sess-123")
        assert ctx is not None

    def test_get_nonexistent(self):
        manager = ContextManager()
        ctx = manager.get("nonexistent")
        assert ctx is None

    def test_remove(self):
        manager = ContextManager()
        manager.create("sess-123")
        result = manager.remove("sess-123")
        assert result is True
        assert manager.get("sess-123") is None

    def test_list_all(self):
        manager = ContextManager()
        manager.create("sess-1")
        manager.create("sess-2")
        all_contexts = manager.list_all()
        assert len(all_contexts) == 2


class TestChatContextManager:
    """Test chat_context context manager."""

    def test_sets_context(self):
        with chat_context("sess-123") as ctx:
            current = get_current_context()
            assert current is not None
            assert current.session_id == "sess-123"

    def test_restores_previous(self):
        set_current_context(None)
        with chat_context("sess-123"):
            pass
        assert get_current_context() is None


class TestTemporaryContext:
    """Test temporary_context context manager."""

    def test_creates_context(self):
        with temporary_context(key="value") as ctx:
            assert ctx.metadata["key"] == "value"

    def test_inherits_from_current(self):
        with chat_context("sess-123", "user-456"):
            with temporary_context(extra="data") as ctx:
                assert ctx.session_id == "sess-123"
                assert ctx.user_id == "user-456"
                assert ctx.metadata["extra"] == "data"
