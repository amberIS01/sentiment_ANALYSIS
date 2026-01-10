"""Tests for serializer module."""

import pytest
import json
from chatbot.serializer import (
    JsonSerializer,
    DataclassSerializer,
    ListSerializer,
    SentimentData,
    SentimentSerializer,
    to_json,
    from_json,
)


class TestJsonSerializer:
    """Tests for JsonSerializer."""

    def test_serialize_dict(self):
        """Test serializing dict."""
        serializer = JsonSerializer()
        result = serializer.serialize({"key": "value"})
        
        assert '"key"' in result
        assert '"value"' in result

    def test_deserialize_dict(self):
        """Test deserializing dict."""
        serializer = JsonSerializer()
        result = serializer.deserialize('{"key": "value"}')
        
        assert result["key"] == "value"

    def test_serialize_pretty(self):
        """Test pretty serialization."""
        serializer = JsonSerializer(indent=2)
        result = serializer.serialize({"key": "value"})
        
        assert "\n" in result


class TestDataclassSerializer:
    """Tests for DataclassSerializer."""

    def test_serialize(self):
        """Test serializing dataclass."""
        serializer = DataclassSerializer(SentimentData)
        data = SentimentData(
            text="Hello",
            score=0.5,
            label="positive",
        )
        
        result = serializer.serialize(data)
        
        assert "Hello" in result
        assert "0.5" in result

    def test_deserialize(self):
        """Test deserializing dataclass."""
        serializer = DataclassSerializer(SentimentData)
        json_str = '{"text": "Hi", "score": 0.8, "label": "positive", "confidence": 0.9}'
        
        result = serializer.deserialize(json_str)
        
        assert result.text == "Hi"
        assert result.score == 0.8


class TestSentimentData:
    """Tests for SentimentData."""

    def test_create(self):
        """Test creating sentiment data."""
        data = SentimentData(
            text="Test",
            score=0.5,
            label="neutral",
        )
        
        assert data.text == "Test"
        assert data.metadata == {}

    def test_with_metadata(self):
        """Test with metadata."""
        data = SentimentData(
            text="Test",
            score=0.5,
            label="neutral",
            metadata={"source": "api"},
        )
        
        assert data.metadata["source"] == "api"


class TestSentimentSerializer:
    """Tests for SentimentSerializer."""

    def test_serialize_result(self):
        """Test serializing single result."""
        serializer = SentimentSerializer()
        data = SentimentData("Hello", 0.5, "positive")
        
        result = serializer.serialize_result(data)
        
        assert "Hello" in result

    def test_deserialize_result(self):
        """Test deserializing single result."""
        serializer = SentimentSerializer()
        json_str = '{"text": "Hi", "score": 0.5, "label": "neutral", "confidence": 0.0, "timestamp": null, "metadata": {}}'
        
        result = serializer.deserialize_result(json_str)
        
        assert result.text == "Hi"

    def test_serialize_results(self):
        """Test serializing multiple results."""
        serializer = SentimentSerializer()
        data = [
            SentimentData("A", 0.5, "positive"),
            SentimentData("B", -0.5, "negative"),
        ]
        
        result = serializer.serialize_results(data)
        
        assert "A" in result
        assert "B" in result

    def test_deserialize_results(self):
        """Test deserializing multiple results."""
        serializer = SentimentSerializer()
        json_str = '[{"text": "A", "score": 0.5, "label": "p", "confidence": 0, "timestamp": null, "metadata": {}}]'
        
        results = serializer.deserialize_results(json_str)
        
        assert len(results) == 1


class TestToJson:
    """Tests for to_json function."""

    def test_convert(self):
        """Test conversion."""
        result = to_json({"key": "value"})
        
        assert '"key"' in result


class TestFromJson:
    """Tests for from_json function."""

    def test_parse(self):
        """Test parsing."""
        result = from_json('{"key": "value"}')
        
        assert result["key"] == "value"
