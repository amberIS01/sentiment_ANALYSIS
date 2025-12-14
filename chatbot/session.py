"""
Session Management Module

This module handles user session management for the chatbot.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Session:
    """Represents a user session."""
    session_id: str
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session has expired."""
        elapsed = datetime.now() - self.last_activity
        return elapsed > timedelta(minutes=timeout_minutes)

    def touch(self) -> None:
        """Update last activity time."""
        self.last_activity = datetime.now()


class SessionManager:
    """Manage user sessions."""

    def __init__(self, timeout_minutes: int = 30):
        self._sessions: Dict[str, Session] = {}
        self.timeout_minutes = timeout_minutes

    def create_session(self) -> Session:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id)
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID."""
        session = self._sessions.get(session_id)
        if session and not session.is_expired(self.timeout_minutes):
            session.touch()
            return session
        return None

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    def cleanup_expired(self) -> int:
        """Remove expired sessions."""
        expired = [
            sid for sid, s in self._sessions.items()
            if s.is_expired(self.timeout_minutes)
        ]
        for sid in expired:
            del self._sessions[sid]
        return len(expired)

    @property
    def active_count(self) -> int:
        """Get count of active sessions."""
        return len([
            s for s in self._sessions.values()
            if not s.is_expired(self.timeout_minutes)
        ])
