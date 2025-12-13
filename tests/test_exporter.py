"""
Tests for the Exporter Module.
"""

import json
import os
import tempfile
import pytest
from pathlib import Path

from chatbot.exporter import ConversationExporter, export_conversation
from chatbot.conversation import ConversationManager


class TestConversationExporter:
    """Test cases for ConversationExporter."""

    @pytest.fixture
    def exporter(self, tmp_path):
        """Create an exporter with temp directory."""
        return ConversationExporter(export_dir=str(tmp_path))

    @pytest.fixture
    def conversation(self):
        """Create a conversation with messages."""
        conv = ConversationManager()
        conv.add_user_message("Hello, how are you?")
        conv.add_bot_message("I'm doing well, thank you!")
        conv.add_user_message("That's great to hear!")
        conv.add_bot_message("How can I help you today?")
        return conv

    @pytest.fixture
    def empty_conversation(self):
        """Create an empty conversation."""
        return ConversationManager()

    def test_export_to_json(self, exporter, conversation):
        """Test exporting to JSON format."""
        filepath = exporter.export_to_json(conversation)
        assert os.path.exists(filepath)
        assert filepath.endswith('.json')

        with open(filepath, 'r') as f:
            data = json.load(f)

        assert 'messages' in data
        assert 'exported_at' in data
        assert len(data['messages']) == 4

    def test_export_to_json_with_summary(self, exporter, conversation):
        """Test JSON export includes summary."""
        filepath = exporter.export_to_json(conversation, include_summary=True)

        with open(filepath, 'r') as f:
            data = json.load(f)

        assert 'summary' in data
        assert 'overall_sentiment' in data['summary']

    def test_export_to_json_without_summary(self, exporter, conversation):
        """Test JSON export without summary."""
        filepath = exporter.export_to_json(conversation, include_summary=False)

        with open(filepath, 'r') as f:
            data = json.load(f)

        assert 'summary' not in data

    def test_export_to_json_custom_filename(self, exporter, conversation):
        """Test JSON export with custom filename."""
        filepath = exporter.export_to_json(conversation, filename="custom.json")
        assert filepath.endswith('custom.json')

    def test_export_to_text(self, exporter, conversation):
        """Test exporting to text format."""
        filepath = exporter.export_to_text(conversation)
        assert os.path.exists(filepath)
        assert filepath.endswith('.txt')

        with open(filepath, 'r') as f:
            content = f.read()

        assert 'User:' in content
        assert 'Bot:' in content

    def test_export_to_text_with_sentiment(self, exporter, conversation):
        """Test text export includes sentiment."""
        filepath = exporter.export_to_text(conversation, include_sentiment=True)

        with open(filepath, 'r') as f:
            content = f.read()

        assert 'Sentiment:' in content

    def test_export_to_csv(self, exporter, conversation):
        """Test exporting to CSV format."""
        filepath = exporter.export_to_csv(conversation)
        assert os.path.exists(filepath)
        assert filepath.endswith('.csv')

        with open(filepath, 'r') as f:
            content = f.read()

        assert 'timestamp' in content
        assert 'role' in content
        assert 'content' in content

    def test_export_empty_conversation_json(self, exporter, empty_conversation):
        """Test exporting empty conversation to JSON."""
        filepath = exporter.export_to_json(empty_conversation)

        with open(filepath, 'r') as f:
            data = json.load(f)

        assert data['message_count'] == 0
        assert len(data['messages']) == 0

    def test_export_empty_conversation_text(self, exporter, empty_conversation):
        """Test exporting empty conversation to text."""
        filepath = exporter.export_to_text(empty_conversation)
        assert os.path.exists(filepath)

    def test_generate_filename(self, exporter):
        """Test filename generation."""
        filename = exporter._generate_filename("test", "json")
        assert filename.startswith("test_")
        assert filename.endswith(".json")

    def test_creates_export_directory(self, tmp_path):
        """Test that export directory is created."""
        new_dir = tmp_path / "new_exports"
        exporter = ConversationExporter(export_dir=str(new_dir))
        conv = ConversationManager()
        conv.add_user_message("Test")

        filepath = exporter.export_to_json(conv)
        assert new_dir.exists()


class TestExportConversationFunction:
    """Test the convenience function."""

    @pytest.fixture
    def conversation(self):
        """Create a test conversation."""
        conv = ConversationManager()
        conv.add_user_message("Hello!")
        conv.add_bot_message("Hi there!")
        return conv

    def test_export_json_format(self, conversation, tmp_path):
        """Test export function with JSON format."""
        filepath = export_conversation(
            conversation,
            format="json",
            export_dir=str(tmp_path)
        )
        assert filepath.endswith('.json')

    def test_export_text_format(self, conversation, tmp_path):
        """Test export function with text format."""
        filepath = export_conversation(
            conversation,
            format="text",
            export_dir=str(tmp_path)
        )
        assert filepath.endswith('.txt')

    def test_export_csv_format(self, conversation, tmp_path):
        """Test export function with CSV format."""
        filepath = export_conversation(
            conversation,
            format="csv",
            export_dir=str(tmp_path)
        )
        assert filepath.endswith('.csv')

    def test_export_invalid_format(self, conversation, tmp_path):
        """Test export function with invalid format."""
        with pytest.raises(ValueError):
            export_conversation(
                conversation,
                format="invalid",
                export_dir=str(tmp_path)
            )
