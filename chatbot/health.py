"""
Health Check Module for Chatbot.

Provides system health monitoring and status checks.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class HealthStatus:
    """Health status result."""

    healthy: bool
    checks: Dict[str, bool]
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None


class HealthChecker:
    """System health checker."""

    def __init__(self) -> None:
        """Initialize health checker."""
        self._checks: Dict[str, callable] = {}
        self._register_default_checks()

    def _register_default_checks(self) -> None:
        """Register default health checks."""
        self._checks["nltk"] = self._check_nltk
        self._checks["vader"] = self._check_vader

    def _check_nltk(self) -> bool:
        """Check if NLTK is available."""
        try:
            import nltk
            return True
        except ImportError:
            return False

    def _check_vader(self) -> bool:
        """Check if VADER lexicon is available."""
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            SentimentIntensityAnalyzer()
            return True
        except Exception:
            return False

    def register_check(self, name: str, check_func: callable) -> None:
        """Register a custom health check."""
        self._checks[name] = check_func

    def run_checks(self) -> HealthStatus:
        """Run all health checks."""
        results: Dict[str, bool] = {}
        details: Dict[str, Any] = {}

        for name, check_func in self._checks.items():
            try:
                results[name] = check_func()
            except Exception as e:
                results[name] = False
                details[name] = str(e)

        return HealthStatus(
            healthy=all(results.values()),
            checks=results,
            timestamp=datetime.now(),
            details=details if details else None,
        )

    def is_healthy(self) -> bool:
        """Quick health check."""
        return self.run_checks().healthy


def check_health() -> HealthStatus:
    """Run health check and return status."""
    checker = HealthChecker()
    return checker.run_checks()
