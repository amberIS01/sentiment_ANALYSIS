"""
Utility Helpers Module

This module provides common utility functions used throughout
the chatbot application.
"""

import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TypeVar, Callable
from functools import wraps
import time


T = TypeVar('T')


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: The text to truncate.
        max_length: Maximum length including suffix.
        suffix: Suffix to append when truncated.

    Returns:
        Truncated text.
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_timestamp(dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object as a string.

    Args:
        dt: Datetime to format. Uses current time if None.
        fmt: Format string.

    Returns:
        Formatted datetime string.
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)


def format_duration(duration: timedelta) -> str:
    """
    Format a timedelta as a human-readable string.

    Args:
        duration: The duration to format.

    Returns:
        Formatted duration string.
    """
    total_seconds = int(duration.total_seconds())

    if total_seconds < 0:
        return "0s"

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format a decimal value as a percentage string.

    Args:
        value: Value between 0 and 1.
        decimal_places: Number of decimal places.

    Returns:
        Formatted percentage string.
    """
    return f"{value * 100:.{decimal_places}f}%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.

    Args:
        numerator: The numerator.
        denominator: The denominator.
        default: Value to return if division by zero.

    Returns:
        Result of division or default.
    """
    if denominator == 0:
        return default
    return numerator / denominator


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp a value between minimum and maximum bounds.

    Args:
        value: The value to clamp.
        min_value: Minimum bound.
        max_value: Maximum bound.

    Returns:
        Clamped value.
    """
    return max(min_value, min(max_value, value))


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.

    Args:
        d: Dictionary to flatten.
        parent_key: Parent key for recursion.
        sep: Separator between keys.

    Returns:
        Flattened dictionary.
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Decorator to retry a function on failure.

    Args:
        max_attempts: Maximum number of attempts.
        delay: Delay between attempts in seconds.
        exceptions: Tuple of exceptions to catch.

    Returns:
        Decorated function.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
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


def timing(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to measure function execution time.

    Args:
        func: Function to time.

    Returns:
        Decorated function that prints execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def remove_emojis(text: str) -> str:
    """
    Remove emojis from text.

    Args:
        text: Text containing emojis.

    Returns:
        Text with emojis removed.
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)


def word_count(text: str) -> int:
    """
    Count words in text.

    Args:
        text: The text to count words in.

    Returns:
        Number of words.
    """
    if not text:
        return 0
    return len(text.split())


def sentence_count(text: str) -> int:
    """
    Count sentences in text.

    Args:
        text: The text to count sentences in.

    Returns:
        Number of sentences.
    """
    if not text:
        return 0
    # Count sentence-ending punctuation
    count = text.count('.') + text.count('!') + text.count('?')
    return max(1, count)


def average(values: List[float]) -> float:
    """
    Calculate the average of a list of values.

    Args:
        values: List of numeric values.

    Returns:
        Average value or 0 if empty.
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID based on timestamp.

    Args:
        prefix: Optional prefix for the ID.

    Returns:
        Unique ID string.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if prefix:
        return f"{prefix}_{timestamp}"
    return timestamp
