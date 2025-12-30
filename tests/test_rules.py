"""Tests for rules module."""

import pytest
from chatbot.rules import (
    RuleType,
    RuleAction,
    SentimentRule,
    KeywordRule,
    ThresholdRule,
    PatternRule,
    RuleEngine,
    apply_rules,
)


class TestKeywordRule:
    """Tests for KeywordRule."""

    def test_match_positive(self):
        """Test positive keyword matching."""
        rule = KeywordRule(
            keywords=["happy", "great"],
            adjustment=0.2,
        )
        
        result = rule.apply("I am happy today", 0.5)
        assert result == pytest.approx(0.7)

    def test_no_match(self):
        """Test no keyword match."""
        rule = KeywordRule(
            keywords=["happy", "great"],
            adjustment=0.2,
        )
        
        result = rule.apply("Normal text", 0.5)
        assert result == pytest.approx(0.5)


class TestThresholdRule:
    """Tests for ThresholdRule."""

    def test_above_threshold(self):
        """Test above threshold."""
        rule = ThresholdRule(
            threshold=0.7,
            condition="above",
            adjustment=0.1,
        )
        
        result = rule.apply("Text", 0.8)
        assert result == pytest.approx(0.9)

    def test_below_threshold(self):
        """Test below threshold."""
        rule = ThresholdRule(
            threshold=0.3,
            condition="below",
            adjustment=-0.1,
        )
        
        result = rule.apply("Text", 0.2)
        assert result == pytest.approx(0.1)


class TestPatternRule:
    """Tests for PatternRule."""

    def test_pattern_match(self):
        """Test pattern matching."""
        rule = PatternRule(
            pattern=r"!\s*$",
            adjustment=0.1,
        )
        
        result = rule.apply("Great news!", 0.5)
        assert result == pytest.approx(0.6)

    def test_no_pattern_match(self):
        """Test no pattern match."""
        rule = PatternRule(
            pattern=r"!\s*$",
            adjustment=0.1,
        )
        
        result = rule.apply("Normal text", 0.5)
        assert result == pytest.approx(0.5)


class TestRuleEngine:
    """Tests for RuleEngine."""

    def test_add_rule(self):
        """Test adding rule."""
        engine = RuleEngine()
        rule = KeywordRule(keywords=["test"], adjustment=0.1)
        
        engine.add_rule(rule)
        
        assert len(engine.rules) == 1

    def test_apply_rules(self):
        """Test applying all rules."""
        engine = RuleEngine()
        engine.add_rule(KeywordRule(["happy"], 0.1))
        engine.add_rule(PatternRule(r"!", 0.05))
        
        result = engine.apply("I am happy!", 0.5)
        
        assert result > 0.5

    def test_remove_rule(self):
        """Test removing rule."""
        engine = RuleEngine()
        rule = KeywordRule(keywords=["test"], adjustment=0.1)
        engine.add_rule(rule)
        
        engine.remove_rule(rule)
        
        assert len(engine.rules) == 0

    def test_clear_rules(self):
        """Test clearing rules."""
        engine = RuleEngine()
        engine.add_rule(KeywordRule(["a"], 0.1))
        engine.add_rule(KeywordRule(["b"], 0.1))
        
        engine.clear()
        
        assert len(engine.rules) == 0


class TestApplyRules:
    """Tests for apply_rules function."""

    def test_apply(self):
        """Test applying rules."""
        rules = [
            KeywordRule(["good"], 0.1),
        ]
        
        result = apply_rules("good day", 0.5, rules)
        
        assert result == pytest.approx(0.6)
