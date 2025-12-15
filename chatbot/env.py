"""
Environment Loader Module

Load configuration from environment variables.
"""

import os
from typing import Optional, Dict, Any, TypeVar, Type
from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class EnvConfig:
    """Environment configuration."""

    debug: bool = False
    log_level: str = "INFO"
    cache_enabled: bool = True
    cache_ttl: int = 300
    session_timeout: int = 30
    max_message_length: int = 5000


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with optional default."""
    return os.environ.get(key, default)


def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean from environment variable."""
    value = os.environ.get(key)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes", "on")


def get_env_int(key: str, default: int = 0) -> int:
    """Get integer from environment variable."""
    value = os.environ.get(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def get_env_float(key: str, default: float = 0.0) -> float:
    """Get float from environment variable."""
    value = os.environ.get(key)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def load_env_config() -> EnvConfig:
    """Load configuration from environment."""
    return EnvConfig(
        debug=get_env_bool("CHATBOT_DEBUG", False),
        log_level=get_env("CHATBOT_LOG_LEVEL", "INFO") or "INFO",
        cache_enabled=get_env_bool("CHATBOT_CACHE_ENABLED", True),
        cache_ttl=get_env_int("CHATBOT_CACHE_TTL", 300),
        session_timeout=get_env_int("CHATBOT_SESSION_TIMEOUT", 30),
        max_message_length=get_env_int("CHATBOT_MAX_MESSAGE_LENGTH", 5000),
    )


def get_required_env(key: str) -> str:
    """Get required environment variable or raise error."""
    value = os.environ.get(key)
    if value is None:
        raise ValueError(f"Required environment variable {key} not set")
    return value


class EnvLoader:
    """Environment variable loader with prefix support."""

    def __init__(self, prefix: str = "CHATBOT"):
        """Initialize with prefix."""
        self.prefix = prefix

    def _key(self, name: str) -> str:
        """Build full key with prefix."""
        return f"{self.prefix}_{name}".upper()

    def get(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """Get string value."""
        return get_env(self._key(name), default)

    def get_bool(self, name: str, default: bool = False) -> bool:
        """Get boolean value."""
        return get_env_bool(self._key(name), default)

    def get_int(self, name: str, default: int = 0) -> int:
        """Get integer value."""
        return get_env_int(self._key(name), default)

    def get_float(self, name: str, default: float = 0.0) -> float:
        """Get float value."""
        return get_env_float(self._key(name), default)

    def to_dict(self) -> Dict[str, Any]:
        """Get all prefixed environment variables."""
        prefix = f"{self.prefix}_"
        return {
            k[len(prefix):].lower(): v
            for k, v in os.environ.items()
            if k.startswith(prefix)
        }
