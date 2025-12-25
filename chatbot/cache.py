"""
Caching Module

Cache sentiment analysis results.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any, Callable
from datetime import datetime, timedelta
import hashlib
import threading


@dataclass
class CacheEntry:
    """A cached entry."""

    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime]
    hits: int = 0


@dataclass
class CacheStats:
    """Cache statistics."""

    total_entries: int
    hits: int
    misses: int
    hit_rate: float
    size_bytes: int


class SentimentCache:
    """Cache for sentiment results."""

    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: int = 3600,
    ):
        """Initialize cache."""
        self._cache: Dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._ttl = timedelta(seconds=ttl_seconds)
        self._hits = 0
        self._misses = 0
        self._lock = threading.Lock()

    def _make_key(self, text: str) -> str:
        """Generate cache key."""
        return hashlib.md5(text.encode()).hexdigest()

    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if entry is expired."""
        if entry.expires_at is None:
            return False
        return datetime.now() > entry.expires_at

    def get(self, text: str) -> Optional[Any]:
        """Get cached result."""
        key = self._make_key(text)
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._misses += 1
                return None

            if self._is_expired(entry):
                del self._cache[key]
                self._misses += 1
                return None

            entry.hits += 1
            self._hits += 1
            return entry.value

    def set(
        self,
        text: str,
        value: Any,
        ttl_seconds: Optional[int] = None,
    ) -> None:
        """Set cached result."""
        key = self._make_key(text)
        ttl = timedelta(seconds=ttl_seconds) if ttl_seconds else self._ttl

        with self._lock:
            if len(self._cache) >= self._max_size:
                self._evict()

            self._cache[key] = CacheEntry(
                key=key,
                value=value,
                created_at=datetime.now(),
                expires_at=datetime.now() + ttl,
            )

    def _evict(self) -> None:
        """Evict oldest entries."""
        if not self._cache:
            return

        # Remove expired first
        expired = [k for k, v in self._cache.items() if self._is_expired(v)]
        for key in expired:
            del self._cache[key]

        # Remove oldest if still full
        if len(self._cache) >= self._max_size:
            oldest = min(self._cache.values(), key=lambda e: e.created_at)
            del self._cache[oldest.key]

    def delete(self, text: str) -> bool:
        """Delete cached entry."""
        key = self._make_key(text)
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all entries."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def get_stats(self) -> CacheStats:
        """Get cache statistics."""
        total = self._hits + self._misses
        return CacheStats(
            total_entries=len(self._cache),
            hits=self._hits,
            misses=self._misses,
            hit_rate=self._hits / total if total > 0 else 0.0,
            size_bytes=0,
        )


class CachedAnalyzer:
    """Analyzer with caching."""

    def __init__(
        self,
        analyzer: Callable[[str], Any],
        cache: Optional[SentimentCache] = None,
    ):
        """Initialize cached analyzer."""
        self.analyzer = analyzer
        self.cache = cache or SentimentCache()

    def analyze(self, text: str, use_cache: bool = True) -> Any:
        """Analyze with caching."""
        if use_cache:
            cached = self.cache.get(text)
            if cached is not None:
                return cached

        result = self.analyzer(text)

        if use_cache:
            self.cache.set(text, result)

        return result


def cached(func: Callable[[str], Any]) -> Callable[[str], Any]:
    """Decorator for caching."""
    cache = SentimentCache()

    def wrapper(text: str) -> Any:
        cached_result = cache.get(text)
        if cached_result is not None:
            return cached_result
        result = func(text)
        cache.set(text, result)
        return result

    return wrapper
