"""
Rate Limiting Module

Provides rate limiting functionality for API calls.
"""

import time
from collections import deque
from dataclasses import dataclass
from typing import Optional
from functools import wraps


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""

    requests: int
    period_seconds: float


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, requests: int = 100, period: float = 60.0):
        """Initialize rate limiter.

        Args:
            requests: Number of requests allowed per period
            period: Time period in seconds
        """
        self.requests = requests
        self.period = period
        self._timestamps: deque = deque()

    def acquire(self) -> bool:
        """Try to acquire a rate limit token.

        Returns:
            True if request is allowed, False if rate limited
        """
        now = time.time()
        cutoff = now - self.period

        # Remove old timestamps
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

        if len(self._timestamps) < self.requests:
            self._timestamps.append(now)
            return True
        return False

    def wait(self) -> None:
        """Wait until a request is allowed."""
        while not self.acquire():
            time.sleep(0.1)

    def remaining(self) -> int:
        """Get remaining requests in current window."""
        now = time.time()
        cutoff = now - self.period

        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

        return max(0, self.requests - len(self._timestamps))

    def reset_time(self) -> Optional[float]:
        """Get time until rate limit resets."""
        if not self._timestamps:
            return None
        oldest = self._timestamps[0]
        return max(0, (oldest + self.period) - time.time())


def rate_limited(requests: int = 10, period: float = 1.0):
    """Decorator to rate limit a function."""
    limiter = RateLimiter(requests=requests, period=period)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.wait()
            return func(*args, **kwargs)
        return wrapper
    return decorator
