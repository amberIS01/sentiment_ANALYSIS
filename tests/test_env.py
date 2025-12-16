"""
Tests for the Environment Module.
"""

import pytest
import os

from chatbot.env import (
    get_env,
    get_env_bool,
    get_env_int,
    get_env_float,
    get_required_env,
    load_env_config,
    EnvConfig,
    EnvLoader,
)


class TestGetEnv:
    """Test get_env function."""

    def test_existing_var(self, monkeypatch):
        monkeypatch.setenv("TEST_VAR", "value")
        assert get_env("TEST_VAR") == "value"

    def test_missing_var(self):
        assert get_env("NONEXISTENT_VAR") is None

    def test_default_value(self):
        assert get_env("NONEXISTENT_VAR", "default") == "default"


class TestGetEnvBool:
    """Test get_env_bool function."""

    def test_true_values(self, monkeypatch):
        for val in ["true", "1", "yes", "on"]:
            monkeypatch.setenv("TEST_BOOL", val)
            assert get_env_bool("TEST_BOOL") is True

    def test_false_value(self, monkeypatch):
        monkeypatch.setenv("TEST_BOOL", "false")
        assert get_env_bool("TEST_BOOL") is False

    def test_default(self):
        assert get_env_bool("NONEXISTENT") is False
        assert get_env_bool("NONEXISTENT", True) is True


class TestGetEnvInt:
    """Test get_env_int function."""

    def test_valid_int(self, monkeypatch):
        monkeypatch.setenv("TEST_INT", "42")
        assert get_env_int("TEST_INT") == 42

    def test_invalid_int(self, monkeypatch):
        monkeypatch.setenv("TEST_INT", "not_a_number")
        assert get_env_int("TEST_INT", 10) == 10

    def test_default(self):
        assert get_env_int("NONEXISTENT", 5) == 5


class TestGetEnvFloat:
    """Test get_env_float function."""

    def test_valid_float(self, monkeypatch):
        monkeypatch.setenv("TEST_FLOAT", "3.14")
        assert get_env_float("TEST_FLOAT") == 3.14

    def test_default(self):
        assert get_env_float("NONEXISTENT", 1.5) == 1.5


class TestGetRequiredEnv:
    """Test get_required_env function."""

    def test_existing(self, monkeypatch):
        monkeypatch.setenv("REQUIRED_VAR", "value")
        assert get_required_env("REQUIRED_VAR") == "value"

    def test_missing_raises(self):
        with pytest.raises(ValueError):
            get_required_env("DEFINITELY_NOT_SET_VAR")


class TestEnvConfig:
    """Test EnvConfig dataclass."""

    def test_defaults(self):
        config = EnvConfig()
        assert config.debug is False
        assert config.log_level == "INFO"
        assert config.cache_enabled is True


class TestEnvLoader:
    """Test EnvLoader class."""

    def test_initialization(self):
        loader = EnvLoader(prefix="TEST")
        assert loader.prefix == "TEST"

    def test_get_with_prefix(self, monkeypatch):
        monkeypatch.setenv("TEST_VALUE", "hello")
        loader = EnvLoader(prefix="TEST")
        assert loader.get("VALUE") == "hello"

    def test_get_bool(self, monkeypatch):
        monkeypatch.setenv("TEST_ENABLED", "true")
        loader = EnvLoader(prefix="TEST")
        assert loader.get_bool("ENABLED") is True

    def test_to_dict(self, monkeypatch):
        monkeypatch.setenv("TEST_A", "1")
        monkeypatch.setenv("TEST_B", "2")
        loader = EnvLoader(prefix="TEST")
        result = loader.to_dict()
        assert "a" in result
        assert "b" in result
