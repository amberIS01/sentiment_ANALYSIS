"""Tests for cache module."""

import pytest
import time
from chatbot.cache import (
    CacheEntry,
    CacheStats,
    SentimentCache,
    CachedAnalyzer,
    cached,
)


class TestSentimentCache:
    """Tests for SentimentCache."""

    def test_set_and_get(self):
        """Test setting and getting."""
        cache = SentimentCache()
        cache.set("hello", 0.5)
        
        result = cache.get("hello")
        assert result == 0.5

    def test_get_miss(self):
        """Test cache miss."""
        cache = SentimentCache()
        result = cache.get("nonexistent")
        
        assert result is None

    def test_delete(self):
        """Test deleting entry."""
        cache = SentimentCache()
        cache.set("test", 0.5)
        
        result = cache.delete("test")
        assert result is True
        assert cache.get("test") is None

    def test_clear(self):
        """Test clearing cache."""
        cache = SentimentCache()
        cache.set("a", 0.1)
        cache.set("b", 0.2)
        cache.clear()
        
        assert cache.get("a") is None
        assert cache.get("b") is None

    def test_get_stats(self):
        """Test getting statistics."""
        cache = SentimentCache()
        cache.set("test", 0.5)
        cache.get("test")  # hit
        cache.get("miss")  # miss
        
        stats = cache.get_stats()
        
        assert stats.total_entries == 1
        assert stats.hits == 1
        assert stats.misses == 1

    def test_max_size(self):
        """Test max size eviction."""
        cache = SentimentCache(max_size=2)
        cache.set("a", 0.1)
        cache.set("b", 0.2)
        cache.set("c", 0.3)
        
        stats = cache.get_stats()
        assert stats.total_entries <= 2


class TestCachedAnalyzer:
    """Tests for CachedAnalyzer."""

    def test_analyze_caches(self):
        """Test that analyze caches results."""
        call_count = [0]
        
        def analyzer(text):
            call_count[0] += 1
            return len(text)
        
        cached_analyzer = CachedAnalyzer(analyzer)
        
        result1 = cached_analyzer.analyze("hello")
        result2 = cached_analyzer.analyze("hello")
        
        assert result1 == result2
        assert call_count[0] == 1  # Only called once

    def test_skip_cache(self):
        """Test skipping cache."""
        call_count = [0]
        
        def analyzer(text):
            call_count[0] += 1
            return len(text)
        
        cached_analyzer = CachedAnalyzer(analyzer)
        
        cached_analyzer.analyze("hello", use_cache=False)
        cached_analyzer.analyze("hello", use_cache=False)
        
        assert call_count[0] == 2


class TestCachedDecorator:
    """Tests for cached decorator."""

    def test_decorator(self):
        """Test cached decorator."""
        call_count = [0]
        
        @cached
        def analyze(text):
            call_count[0] += 1
            return text.upper()
        
        result1 = analyze("hello")
        result2 = analyze("hello")
        
        assert result1 == "HELLO"
        assert call_count[0] == 1
