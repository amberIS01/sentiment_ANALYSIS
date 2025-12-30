"""
Decorators Module

Utility decorators for sentiment analysis.
"""

from functools import wraps
from typing import Callable, Any, Optional, TypeVar, Dict
import time
import logging


F = TypeVar("F", bound=Callable[..., Any])


def timed(func: F) -> F:
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        wrapper.last_time = elapsed
        return result
    wrapper.last_time = 0.0
    return wrapper


def logged(logger: Optional[logging.Logger] = None) -> Callable[[F], F]:
    """Log function calls."""
    log = logger or logging.getLogger(__name__)

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.debug(f"Calling {func.__name__}")
            try:
                result = func(*args, **kwargs)
                log.debug(f"{func.__name__} returned successfully")
                return result
            except Exception as e:
                log.error(f"{func.__name__} raised {type(e).__name__}: {e}")
                raise
        return wrapper
    return decorator


def cached(maxsize: int = 128) -> Callable[[F], F]:
    """Cache function results."""
    def decorator(func: F) -> F:
        cache: Dict[str, Any] = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str((args, sorted(kwargs.items())))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            if len(cache) >= maxsize:
                cache.pop(next(iter(cache)))
            cache[key] = result
            return result

        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (Exception,),
) -> Callable[[F], F]:
    """Retry function on failure."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def validate_input(validator: Callable[[Any], bool]) -> Callable[[F], F]:
    """Validate first argument."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(first_arg, *args, **kwargs):
            if not validator(first_arg):
                raise ValueError(f"Invalid input: {first_arg}")
            return func(first_arg, *args, **kwargs)
        return wrapper
    return decorator


def deprecated(message: str = "") -> Callable[[F], F]:
    """Mark function as deprecated."""
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import warnings
            msg = message or f"{func.__name__} is deprecated"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def singleton(cls):
    """Make class a singleton."""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def rate_limited(calls: int, period: float) -> Callable[[F], F]:
    """Rate limit function calls."""
    def decorator(func: F) -> F:
        call_times: list = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            call_times[:] = [t for t in call_times if now - t < period]
            if len(call_times) >= calls:
                wait = period - (now - call_times[0])
                if wait > 0:
                    time.sleep(wait)
            call_times.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator


def async_to_sync(func: Callable) -> Callable:
    """Convert async function to sync."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import asyncio
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(func(*args, **kwargs))
        finally:
            loop.close()
    return wrapper
