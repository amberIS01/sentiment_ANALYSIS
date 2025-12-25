"""
Alerts Module

Alert on sentiment thresholds.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from enum import Enum
from datetime import datetime


class AlertLevel(Enum):
    """Alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of alerts."""

    THRESHOLD = "threshold"
    TREND = "trend"
    ANOMALY = "anomaly"
    VOLUME = "volume"


@dataclass
class AlertRule:
    """An alert rule."""

    id: str
    name: str
    alert_type: AlertType
    level: AlertLevel
    threshold: float
    condition: str  # "above", "below", "equals"
    enabled: bool = True
    cooldown: int = 60


@dataclass
class Alert:
    """A triggered alert."""

    rule_id: str
    rule_name: str
    level: AlertLevel
    message: str
    value: float
    threshold: float
    triggered_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class AlertManager:
    """Manage sentiment alerts."""

    def __init__(self):
        """Initialize manager."""
        self._rules: Dict[str, AlertRule] = {}
        self._handlers: List[Callable[[Alert], None]] = []
        self._history: List[Alert] = []
        self._last_triggered: Dict[str, datetime] = {}

    def add_rule(self, rule: AlertRule) -> None:
        """Add alert rule."""
        self._rules[rule.id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove alert rule."""
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False

    def add_handler(self, handler: Callable[[Alert], None]) -> None:
        """Add alert handler."""
        self._handlers.append(handler)

    def _check_cooldown(self, rule: AlertRule) -> bool:
        """Check if rule is in cooldown."""
        last = self._last_triggered.get(rule.id)
        if last is None:
            return False
        elapsed = (datetime.now() - last).total_seconds()
        return elapsed < rule.cooldown

    def _evaluate_rule(self, rule: AlertRule, value: float) -> bool:
        """Evaluate if rule triggers."""
        if rule.condition == "above":
            return value > rule.threshold
        elif rule.condition == "below":
            return value < rule.threshold
        elif rule.condition == "equals":
            return abs(value - rule.threshold) < 0.01
        return False

    def check(
        self,
        value: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Alert]:
        """Check value against rules."""
        alerts = []

        for rule in self._rules.values():
            if not rule.enabled:
                continue

            if self._check_cooldown(rule):
                continue

            if self._evaluate_rule(rule, value):
                alert = Alert(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    level=rule.level,
                    message=f"{rule.name}: {value} is {rule.condition} {rule.threshold}",
                    value=value,
                    threshold=rule.threshold,
                    triggered_at=datetime.now(),
                    metadata=metadata or {},
                )

                self._last_triggered[rule.id] = datetime.now()
                self._history.append(alert)
                alerts.append(alert)

                for handler in self._handlers:
                    handler(alert)

        return alerts

    def get_history(
        self,
        level: Optional[AlertLevel] = None,
        limit: int = 100,
    ) -> List[Alert]:
        """Get alert history."""
        history = self._history
        if level:
            history = [a for a in history if a.level == level]
        return history[-limit:]

    def clear_history(self) -> None:
        """Clear alert history."""
        self._history.clear()


def create_threshold_alert(
    name: str,
    threshold: float,
    condition: str = "above",
    level: AlertLevel = AlertLevel.WARNING,
) -> AlertRule:
    """Create a threshold alert rule."""
    return AlertRule(
        id=f"alert_{name.lower().replace(' ', '_')}",
        name=name,
        alert_type=AlertType.THRESHOLD,
        level=level,
        threshold=threshold,
        condition=condition,
    )


def check_sentiment_alerts(
    value: float,
    rules: List[AlertRule],
) -> List[Alert]:
    """Check sentiment against rules."""
    manager = AlertManager()
    for rule in rules:
        manager.add_rule(rule)
    return manager.check(value)
