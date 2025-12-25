"""
Retry Logic Module

Retry failed operations with backoff.
"""

from dataclasses import dataclass
from typing import Callable, Any, Optional, List, Type
from enum import Enum
import time
import random


class BackoffStrategy(Enum):
    """Backoff strategies."""

    CONSTANT = "constant"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    JITTERED = "jittered"


@dataclass
class RetryConfig:
    """Retry configuration."""

    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    backoff: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    multiplier: float = 2.0
    jitter: float = 0.1


@dataclass
class RetryResult:
    """Result of retry operation."""

    success: bool
    value: Any
    attempts: int
    total_time: float
    errors: List[str]


class RetryError(Exception):
    """Retry exhausted error."""

    def __init__(self, message: str, attempts: int, errors: List[str]):
        super().__init__(message)
        self.attempts = attempts
        self.errors = errors


class Retrier:
    """Retry operations with backoff."""

    def __init__(self, config: Optional[RetryConfig] = None):
        """Initialize retrier."""
        self.config = config or RetryConfig()
        self._exceptions: List[Type[Exception]] = [Exception]

    def retry_on(self, *exceptions: Type[Exception]) -> "Retrier":
        """Set exceptions to retry on."""
        self._exceptions = list(exceptions)
        return self

    def _get_delay(self, attempt: int) -> float:
        """Calculate delay for attempt."""
        config = self.config

        if config.backoff == BackoffStrategy.CONSTANT:
            delay = config.initial_delay
        elif config.backoff == BackoffStrategy.LINEAR:
            delay = config.initial_delay * attempt
        elif config.backoff == BackoffStrategy.EXPONENTIAL:
            delay = config.initial_delay * (config.multiplier ** (attempt - 1))
        elif config.backoff == BackoffStrategy.JITTERED:
            base = config.initial_delay * (config.multiplier ** (attempt - 1))
            jitter = random.uniform(-config.jitter, config.jitter)
            delay = base * (1 + jitter)
        else:
            delay = config.initial_delay

        return min(delay, config.max_delay)

    def execute(self, func: Callable[[], Any]) -> RetryResult:
        """Execute with retry."""
        errors: List[str] = []
        start_time = time.time()

        for attempt in range(1, self.config.max_attempts + 1):
            try:
                result = func()
                return RetryResult(
                    success=True,
                    value=result,
                    attempts=attempt,
                    total_time=time.time() - start_time,
                    errors=errors,
                )
            except tuple(self._exceptions) as e:
                errors.append(str(e))
                if attempt < self.config.max_attempts:
                    delay = self._get_delay(attempt)
                    time.sleep(delay)

        return RetryResult(
            success=False,
            value=None,
            attempts=self.config.max_attempts,
            total_time=time.time() - start_time,
            errors=errors,
        )

    def __call__(self, func: Callable[[], Any]) -> Any:
        """Execute and raise on failure."""
        result = self.execute(func)
        if not result.success:
            raise RetryError(
                f"Failed after {result.attempts} attempts",
                result.attempts,
                result.errors,
            )
        return result.value


def retry(
    func: Callable[[], Any],
    max_attempts: int = 3,
    delay: float = 1.0,
) -> Any:
    """Retry a function."""
    config = RetryConfig(max_attempts=max_attempts, initial_delay=delay)
    retrier = Retrier(config)
    return retrier(func)


def with_retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: BackoffStrategy = BackoffStrategy.EXPONENTIAL,
) -> Callable:
    """Decorator for retry."""
    config = RetryConfig(
        max_attempts=max_attempts,
        initial_delay=delay,
        backoff=backoff,
    )

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            retrier = Retrier(config)
            return retrier(lambda: func(*args, **kwargs))
        return wrapper

    return decorator
