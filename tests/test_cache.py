"""
Tests for the Cache Module.
"""

import pytest
from chatbot.cache import SentimentCache, cached_sentiment


class TestSentimentCache:
    """Test SentimentCache class."""

    def test_initialization(self):
        cache = SentimentCache(maxsize=100)
        assert cache is not None

    def test_get_miss(self):
        cache = SentimentCache()
        result = cache.get("nonexistent")
        assert result is None

    def test_set_and_get(self):
        cache = SentimentCache()
        cache.set("test_key", {"score": 0.5})
        result = cache.get("test_key")
        assert result == {"score": 0.5}

    def test_clear(self):
        cache = SentimentCache()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_stats(self):
        cache = SentimentCache()
        cache.set("key", "value")
        cache.get("key")
        cache.get("missing")
        stats = cache.stats()
        assert "hits" in stats
        assert "misses" in stats

    def test_maxsize_eviction(self):
        cache = SentimentCache(maxsize=2)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        # First key should be evicted
        assert cache.size() <= 2


class TestCachedSentiment:
    """Test cached_sentiment decorator."""

    def test_caches_result(self):
        call_count = 0

        @cached_sentiment
        def analyze(text: str) -> dict:
            nonlocal call_count
            call_count += 1
            return {"text": text}

        result1 = analyze("hello")
        result2 = analyze("hello")
        assert result1 == result2
        assert call_count == 1

    def test_different_inputs(self):
        @cached_sentiment
        def analyze(text: str) -> dict:
            return {"text": text}

        result1 = analyze("hello")
        result2 = analyze("world")
        assert result1 != result2
