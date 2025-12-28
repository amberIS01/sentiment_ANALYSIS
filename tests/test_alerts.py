"""Tests for alerts module."""

import pytest
from chatbot.alerts import (
    AlertLevel,
    AlertType,
    AlertRule,
    Alert,
    AlertManager,
    create_threshold_alert,
    check_sentiment_alerts,
)


class TestAlertManager:
    """Tests for AlertManager."""

    def test_add_rule(self):
        """Test adding rule."""
        manager = AlertManager()
        rule = AlertRule(
            id="test",
            name="Test Alert",
            alert_type=AlertType.THRESHOLD,
            level=AlertLevel.WARNING,
            threshold=0.5,
            condition="above",
        )
        manager.add_rule(rule)
        
        assert len(manager._rules) == 1

    def test_remove_rule(self):
        """Test removing rule."""
        manager = AlertManager()
        rule = AlertRule(
            id="test",
            name="Test",
            alert_type=AlertType.THRESHOLD,
            level=AlertLevel.WARNING,
            threshold=0.5,
            condition="above",
        )
        manager.add_rule(rule)
        
        result = manager.remove_rule("test")
        assert result is True
        assert len(manager._rules) == 0

    def test_check_triggers(self):
        """Test checking triggers alert."""
        manager = AlertManager()
        rule = AlertRule(
            id="high",
            name="High Sentiment",
            alert_type=AlertType.THRESHOLD,
            level=AlertLevel.INFO,
            threshold=0.8,
            condition="above",
        )
        manager.add_rule(rule)
        
        alerts = manager.check(0.9)
        
        assert len(alerts) == 1
        assert alerts[0].rule_id == "high"

    def test_check_no_trigger(self):
        """Test check without trigger."""
        manager = AlertManager()
        rule = AlertRule(
            id="high",
            name="High",
            alert_type=AlertType.THRESHOLD,
            level=AlertLevel.WARNING,
            threshold=0.8,
            condition="above",
        )
        manager.add_rule(rule)
        
        alerts = manager.check(0.5)
        
        assert len(alerts) == 0

    def test_handler(self):
        """Test alert handler."""
        manager = AlertManager()
        rule = AlertRule(
            id="test",
            name="Test",
            alert_type=AlertType.THRESHOLD,
            level=AlertLevel.WARNING,
            threshold=0.5,
            condition="above",
        )
        manager.add_rule(rule)
        
        received = []
        manager.add_handler(lambda a: received.append(a))
        manager.check(0.9)
        
        assert len(received) == 1

    def test_get_history(self):
        """Test getting history."""
        manager = AlertManager()
        rule = AlertRule(
            id="test",
            name="Test",
            alert_type=AlertType.THRESHOLD,
            level=AlertLevel.WARNING,
            threshold=0.5,
            condition="above",
            cooldown=0,
        )
        manager.add_rule(rule)
        
        manager.check(0.9)
        history = manager.get_history()
        
        assert len(history) == 1

    def test_condition_below(self):
        """Test below condition."""
        manager = AlertManager()
        rule = AlertRule(
            id="low",
            name="Low",
            alert_type=AlertType.THRESHOLD,
            level=AlertLevel.WARNING,
            threshold=-0.5,
            condition="below",
        )
        manager.add_rule(rule)
        
        alerts = manager.check(-0.8)
        
        assert len(alerts) == 1


class TestCreateThresholdAlert:
    """Tests for create_threshold_alert."""

    def test_create(self):
        """Test creating alert."""
        rule = create_threshold_alert("High Score", 0.8)
        
        assert rule.name == "High Score"
        assert rule.threshold == 0.8


class TestCheckSentimentAlerts:
    """Tests for check_sentiment_alerts."""

    def test_check(self):
        """Test checking alerts."""
        rules = [
            create_threshold_alert("High", 0.8, "above"),
        ]
        alerts = check_sentiment_alerts(0.9, rules)
        
        assert len(alerts) == 1
