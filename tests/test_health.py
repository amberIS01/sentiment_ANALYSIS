"""
Tests for the Health Check Module.
"""

import pytest
from datetime import datetime

from chatbot.health import HealthChecker, HealthStatus, check_health


class TestHealthStatus:
    """Test HealthStatus dataclass."""

    def test_healthy_status(self):
        status = HealthStatus(
            healthy=True,
            checks={"test": True},
            timestamp=datetime.now(),
        )
        assert status.healthy is True
        assert status.checks["test"] is True

    def test_unhealthy_status(self):
        status = HealthStatus(
            healthy=False,
            checks={"test": False},
            timestamp=datetime.now(),
            details={"test": "Error message"},
        )
        assert status.healthy is False
        assert status.details is not None


class TestHealthChecker:
    """Test HealthChecker class."""

    def test_initialization(self):
        checker = HealthChecker()
        assert checker is not None

    def test_run_checks(self):
        checker = HealthChecker()
        status = checker.run_checks()
        assert isinstance(status, HealthStatus)
        assert isinstance(status.checks, dict)

    def test_is_healthy(self):
        checker = HealthChecker()
        result = checker.is_healthy()
        assert isinstance(result, bool)

    def test_register_custom_check(self):
        checker = HealthChecker()
        checker.register_check("custom", lambda: True)
        status = checker.run_checks()
        assert "custom" in status.checks

    def test_custom_check_failure(self):
        checker = HealthChecker()
        checker.register_check("failing", lambda: False)
        status = checker.run_checks()
        assert status.checks["failing"] is False

    def test_check_with_exception(self):
        checker = HealthChecker()
        checker.register_check("error", lambda: 1 / 0)
        status = checker.run_checks()
        assert status.checks["error"] is False


class TestCheckHealth:
    """Test check_health function."""

    def test_returns_health_status(self):
        status = check_health()
        assert isinstance(status, HealthStatus)

    def test_has_timestamp(self):
        status = check_health()
        assert status.timestamp is not None
