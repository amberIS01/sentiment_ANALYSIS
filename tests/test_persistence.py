"""
Tests for the Persistence Module.
"""

import pytest
import tempfile
import os
import json

from chatbot.persistence import ConversationStore


class TestConversationStore:
    """Test ConversationStore class."""

    def test_initialization(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)
            assert store is not None

    def test_save_conversation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)
            data = {"messages": [{"role": "user", "content": "hello"}]}
            store.save("conv-1", data)
            assert os.path.exists(os.path.join(tmpdir, "conv-1.json"))

    def test_load_conversation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)
            data = {"messages": [{"role": "user", "content": "hello"}]}
            store.save("conv-1", data)
            loaded = store.load("conv-1")
            assert loaded == data

    def test_load_nonexistent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)
            result = store.load("nonexistent")
            assert result is None

    def test_delete_conversation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)
            store.save("conv-1", {"data": "test"})
            result = store.delete("conv-1")
            assert result is True
            assert store.load("conv-1") is None

    def test_list_conversations(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)
            store.save("conv-1", {"data": "1"})
            store.save("conv-2", {"data": "2"})
            conversations = store.list_all()
            assert len(conversations) == 2

    def test_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = ConversationStore(storage_dir=tmpdir)
            store.save("conv-1", {"data": "test"})
            assert store.exists("conv-1") is True
            assert store.exists("conv-2") is False
