"""
Caching Module

This module provides caching functionality for sentiment analysis results.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any, TypeVar, Generic
from dataclasses import dataclass
import hashlib

T = TypeVar('T')


@dataclass
class CacheEntry(Generic[T]):
    """A cache entry with expiration."""
    value: T
    created_at: datetime
    expires_at: datetime

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at


class LRUCache(Generic[T]):
    """Least Recently Used cache implementation."""

    def __init__(self, max_size: int = 100, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, CacheEntry[T]] = {}
        self._access_order: list = []

    def _generate_key(self, text: str) -> str:
        """Generate cache key from text."""
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, key: str) -> Optional[T]:
        """Get value from cache."""
        entry = self._cache.get(key)

        if entry is None:
            return None

        if entry.is_expired():
            self.delete(key)
            return None

        # Update access order
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

        return entry.value

    def set(self, key: str, value: T) -> None:
        """Set value in cache."""
        # Evict if at capacity
        while len(self._cache) >= self.max_size:
            self._evict_oldest()

        now = datetime.now()
        entry = CacheEntry(
            value=value,
            created_at=now,
            expires_at=now + timedelta(seconds=self.ttl_seconds)
        )
        self._cache[key] = entry
        self._access_order.append(key)

    def delete(self, key: str) -> bool:
        """Delete entry from cache."""
        if key in self._cache:
            del self._cache[key]
            if key in self._access_order:
                self._access_order.remove(key)
            return True
        return False

    def _evict_oldest(self) -> None:
        """Evict the oldest entry."""
        if self._access_order:
            oldest = self._access_order.pop(0)
            self._cache.pop(oldest, None)

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._access_order.clear()

    @property
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": self.size,
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
        }


class SentimentCache:
    """Cache specifically for sentiment results."""

    def __init__(self, max_size: int = 500, ttl_seconds: int = 600):
        self._cache = LRUCache(max_size=max_size, ttl_seconds=ttl_seconds)
        self._hits = 0
        self._misses = 0

    def get_sentiment(self, text: str) -> Optional[Any]:
        """Get cached sentiment result."""
        key = self._cache._generate_key(text)
        result = self._cache.get(key)

        if result is not None:
            self._hits += 1
        else:
            self._misses += 1

        return result

    def cache_sentiment(self, text: str, result: Any) -> None:
        """Cache a sentiment result."""
        key = self._cache._generate_key(text)
        self._cache.set(key, result)

    @property
    def hit_rate(self) -> float:
        """Get cache hit rate."""
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0
