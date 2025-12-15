"""
Retry Utilities Module

Provides retry decorators and utilities for handling transient failures.
"""

import time
import random
from functools import wraps
from typing import Type, Tuple, Callable, Optional


class RetryError(Exception):
    """Raised when all retry attempts fail."""

    def __init__(self, message: str, last_exception: Optional[Exception] = None):
        super().__init__(message)
        self.last_exception = last_exception


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True,
) -> Callable:
    """Retry decorator with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
        jitter: Add random jitter to delay

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        raise RetryError(
                            f"Failed after {max_attempts} attempts",
                            last_exception=e,
                        )

                    wait_time = current_delay
                    if jitter:
                        wait_time += random.uniform(0, current_delay * 0.1)

                    time.sleep(wait_time)
                    current_delay *= backoff

        return wrapper
    return decorator


def retry_on_exception(
    exception_type: Type[Exception],
    max_attempts: int = 3,
) -> Callable:
    """Simple retry decorator for specific exception.

    Args:
        exception_type: Exception type to retry on
        max_attempts: Maximum number of attempts

    Returns:
        Decorated function
    """
    return retry(max_attempts=max_attempts, exceptions=(exception_type,))


class RetryContext:
    """Context manager for retry logic."""

    def __init__(
        self,
        max_attempts: int = 3,
        delay: float = 1.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
    ):
        self.max_attempts = max_attempts
        self.delay = delay
        self.exceptions = exceptions
        self.attempt = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.attempt >= self.max_attempts:
            raise StopIteration

        if self.attempt > 0:
            time.sleep(self.delay)

        self.attempt += 1
        return self.attempt
