"""Tests for slang module."""

import pytest
from chatbot.slang import (
    SlangMatch,
    SlangAnalysis,
    SlangDetector,
    detect_slang,
    normalize_slang,
)


class TestSlangDetector:
    """Tests for SlangDetector."""

    def test_detect_slang(self):
        """Test detecting slang."""
        detector = SlangDetector()
        matches = detector.detect("lol that was funny")
        
        assert len(matches) == 1
        assert matches[0].term == "lol"

    def test_detect_multiple(self):
        """Test detecting multiple slang."""
        detector = SlangDetector()
        matches = detector.detect("omg lol btw")
        
        assert len(matches) == 3

    def test_normalize(self):
        """Test normalizing slang."""
        detector = SlangDetector()
        result = detector.normalize("lol that was funny")
        
        assert "laughing out loud" in result

    def test_add_custom_slang(self):
        """Test adding custom slang."""
        detector = SlangDetector()
        detector.add_slang("bruh", "bro", 0.1)
        
        matches = detector.detect("bruh moment")
        assert len(matches) == 1

    def test_analyze(self):
        """Test analyzing slang."""
        detector = SlangDetector()
        result = detector.analyze("lol omg")
        
        assert result.total_count == 2
        assert "laughing out loud" in result.normalized_text

    def test_get_known_slang(self):
        """Test getting known slang."""
        detector = SlangDetector()
        known = detector.get_known_slang()
        
        assert "lol" in known
        assert "omg" in known

    def test_no_slang(self):
        """Test text without slang."""
        detector = SlangDetector()
        matches = detector.detect("Hello world")
        
        assert len(matches) == 0


class TestDetectSlang:
    """Tests for detect_slang function."""

    def test_detect(self):
        """Test detect function."""
        matches = detect_slang("lol")
        
        assert len(matches) == 1


class TestNormalizeSlang:
    """Tests for normalize_slang function."""

    def test_normalize(self):
        """Test normalize function."""
        result = normalize_slang("idk what to say")
        
        assert "i do not know" in result
