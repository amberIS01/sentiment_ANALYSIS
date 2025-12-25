"""
Sentiment Rules Module

Rule-based sentiment adjustments.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum


class RuleAction(Enum):
    """Actions a rule can take."""

    ADJUST_SCORE = "adjust_score"
    SET_LABEL = "set_label"
    ADD_FLAG = "add_flag"
    BLOCK = "block"


@dataclass
class RuleMatch:
    """Result of rule matching."""

    rule_name: str
    matched: bool
    action: Optional[RuleAction] = None
    adjustment: float = 0.0
    message: Optional[str] = None


class Rule(ABC):
    """Base rule class."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def evaluate(self, text: str, score: float) -> RuleMatch:
        """Evaluate the rule against text."""
        pass


class KeywordRule(Rule):
    """Rule based on keyword presence."""

    def __init__(
        self,
        name: str,
        keywords: List[str],
        adjustment: float,
        require_all: bool = False,
    ):
        super().__init__(name)
        self.keywords = [k.lower() for k in keywords]
        self.adjustment = adjustment
        self.require_all = require_all

    def evaluate(self, text: str, score: float) -> RuleMatch:
        text_lower = text.lower()
        matches = [k for k in self.keywords if k in text_lower]

        if self.require_all:
            matched = len(matches) == len(self.keywords)
        else:
            matched = len(matches) > 0

        return RuleMatch(
            rule_name=self.name,
            matched=matched,
            action=RuleAction.ADJUST_SCORE if matched else None,
            adjustment=self.adjustment if matched else 0.0,
            message=f"Matched keywords: {matches}" if matched else None,
        )


class ThresholdRule(Rule):
    """Rule based on score thresholds."""

    def __init__(
        self,
        name: str,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        adjustment: float = 0.0,
    ):
        super().__init__(name)
        self.min_score = min_score
        self.max_score = max_score
        self.adjustment = adjustment

    def evaluate(self, text: str, score: float) -> RuleMatch:
        matched = True

        if self.min_score is not None and score < self.min_score:
            matched = False
        if self.max_score is not None and score > self.max_score:
            matched = False

        return RuleMatch(
            rule_name=self.name,
            matched=matched,
            action=RuleAction.ADJUST_SCORE if matched else None,
            adjustment=self.adjustment if matched else 0.0,
        )


class PatternRule(Rule):
    """Rule based on regex pattern."""

    def __init__(self, name: str, pattern: str, adjustment: float):
        super().__init__(name)
        import re
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.adjustment = adjustment

    def evaluate(self, text: str, score: float) -> RuleMatch:
        matched = bool(self.pattern.search(text))
        return RuleMatch(
            rule_name=self.name,
            matched=matched,
            action=RuleAction.ADJUST_SCORE if matched else None,
            adjustment=self.adjustment if matched else 0.0,
        )


class RuleEngine:
    """Engine for evaluating rules."""

    def __init__(self):
        self._rules: List[Rule] = []

    def add_rule(self, rule: Rule) -> None:
        """Add a rule."""
        self._rules.append(rule)

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name."""
        for i, rule in enumerate(self._rules):
            if rule.name == name:
                self._rules.pop(i)
                return True
        return False

    def evaluate(self, text: str, score: float) -> List[RuleMatch]:
        """Evaluate all rules."""
        return [rule.evaluate(text, score) for rule in self._rules]

    def apply(self, text: str, score: float) -> float:
        """Apply all rules and return adjusted score."""
        matches = self.evaluate(text, score)
        adjustment = sum(m.adjustment for m in matches if m.matched)
        return max(-1.0, min(1.0, score + adjustment))

    def get_rules(self) -> List[str]:
        """Get names of all rules."""
        return [rule.name for rule in self._rules]


def create_default_rules() -> RuleEngine:
    """Create engine with default rules."""
    engine = RuleEngine()

    # Add boost for emphatic positive language
    engine.add_rule(KeywordRule(
        "emphatic_positive",
        ["amazing", "incredible", "fantastic", "wonderful"],
        adjustment=0.1,
    ))

    # Add penalty for emphatic negative language
    engine.add_rule(KeywordRule(
        "emphatic_negative",
        ["terrible", "horrible", "awful", "disgusting"],
        adjustment=-0.1,
    ))

    return engine
