"""
Tests for the Session Module.
"""

import pytest
from datetime import datetime, timedelta

from chatbot.session import Session, SessionManager


class TestSession:
    """Test Session dataclass."""

    def test_creation(self):
        session = Session(session_id="test-123")
        assert session.session_id == "test-123"
        assert session.created_at is not None

    def test_is_expired_fresh(self):
        session = Session(session_id="test-123")
        assert session.is_expired(timeout_minutes=30) is False

    def test_is_expired_old(self):
        session = Session(session_id="test-123")
        session.last_activity = datetime.now() - timedelta(hours=1)
        assert session.is_expired(timeout_minutes=30) is True

    def test_touch_updates_activity(self):
        session = Session(session_id="test-123")
        old_time = session.last_activity
        session.touch()
        assert session.last_activity >= old_time

    def test_data_storage(self):
        session = Session(session_id="test-123")
        session.data["key"] = "value"
        assert session.data["key"] == "value"


class TestSessionManager:
    """Test SessionManager class."""

    def test_initialization(self):
        manager = SessionManager()
        assert manager.timeout_minutes == 30

    def test_custom_timeout(self):
        manager = SessionManager(timeout_minutes=60)
        assert manager.timeout_minutes == 60

    def test_create_session(self):
        manager = SessionManager()
        session = manager.create_session()
        assert session is not None
        assert session.session_id is not None

    def test_get_session(self):
        manager = SessionManager()
        session = manager.create_session()
        retrieved = manager.get_session(session.session_id)
        assert retrieved is not None
        assert retrieved.session_id == session.session_id

    def test_get_nonexistent_session(self):
        manager = SessionManager()
        result = manager.get_session("nonexistent-id")
        assert result is None

    def test_delete_session(self):
        manager = SessionManager()
        session = manager.create_session()
        result = manager.delete_session(session.session_id)
        assert result is True
        assert manager.get_session(session.session_id) is None

    def test_delete_nonexistent(self):
        manager = SessionManager()
        result = manager.delete_session("nonexistent-id")
        assert result is False

    def test_active_count(self):
        manager = SessionManager()
        manager.create_session()
        manager.create_session()
        assert manager.active_count == 2

    def test_cleanup_expired(self):
        manager = SessionManager(timeout_minutes=0)
        session = manager.create_session()
        session.last_activity = datetime.now() - timedelta(hours=1)
        removed = manager.cleanup_expired()
        assert removed == 1
