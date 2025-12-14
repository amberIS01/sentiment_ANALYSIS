"""
Conversation Persistence Module

This module provides functionality to save and load conversations
to/from persistent storage.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class ConversationStorage:
    """Handle conversation persistence to JSON files."""

    def __init__(self, storage_dir: str = "conversations"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self, conversation_id: str, data: Dict[str, Any]) -> str:
        """Save conversation to file."""
        filepath = self.storage_dir / f"{conversation_id}.json"
        data["saved_at"] = datetime.now().isoformat()

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def load(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Load conversation from file."""
        filepath = self.storage_dir / f"{conversation_id}.json"

        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def delete(self, conversation_id: str) -> bool:
        """Delete conversation file."""
        filepath = self.storage_dir / f"{conversation_id}.json"

        if filepath.exists():
            filepath.unlink()
            return True
        return False

    def list_conversations(self) -> List[str]:
        """List all saved conversation IDs."""
        return [f.stem for f in self.storage_dir.glob("*.json")]

    def exists(self, conversation_id: str) -> bool:
        """Check if conversation exists."""
        filepath = self.storage_dir / f"{conversation_id}.json"
        return filepath.exists()


class AutoSaveManager:
    """Automatically save conversations at intervals."""

    def __init__(self, storage: ConversationStorage, interval: int = 5):
        self.storage = storage
        self.interval = interval
        self._message_count = 0
        self._conversation_id: Optional[str] = None

    def set_conversation_id(self, conv_id: str) -> None:
        """Set current conversation ID."""
        self._conversation_id = conv_id
        self._message_count = 0

    def on_message(self, data: Dict[str, Any]) -> None:
        """Called on each message to check for auto-save."""
        self._message_count += 1

        if self._message_count >= self.interval and self._conversation_id:
            self.storage.save(self._conversation_id, data)
            self._message_count = 0
