"""
Response Templates Module

This module provides customizable response templates for the chatbot.
"""

from typing import Dict, List
from dataclasses import dataclass, field
import random


@dataclass
class ResponseTemplate:
    """A response template with variants."""
    category: str
    templates: List[str] = field(default_factory=list)

    def get_random(self) -> str:
        """Get a random template."""
        if not self.templates:
            return ""
        return random.choice(self.templates)


class TemplateManager:
    """Manage response templates."""

    def __init__(self):
        self._templates: Dict[str, ResponseTemplate] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Load default templates."""
        defaults = {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Welcome! How may I assist you?",
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "Take care! Come back anytime.",
                "Bye! It was nice chatting with you.",
            ],
            "thanks": [
                "You're welcome!",
                "Happy to help!",
                "Glad I could assist!",
            ],
            "positive": [
                "That's wonderful to hear!",
                "I'm glad things are going well!",
                "Great to hear that!",
            ],
            "negative": [
                "I'm sorry to hear that.",
                "I understand your frustration.",
                "Let me help address your concern.",
            ],
            "neutral": [
                "I understand.",
                "I see.",
                "Got it.",
            ],
            "confused": [
                "Could you please clarify?",
                "I'm not sure I understand.",
                "Can you tell me more?",
            ],
            "error": [
                "Something went wrong.",
                "An error occurred.",
                "Please try again.",
            ],
        }

        for category, templates in defaults.items():
            self._templates[category] = ResponseTemplate(
                category=category,
                templates=templates
            )

    def get(self, category: str) -> str:
        """Get a random response for category."""
        template = self._templates.get(category)
        if template:
            return template.get_random()
        return ""

    def add_template(self, category: str, template: str) -> None:
        """Add a template to a category."""
        if category not in self._templates:
            self._templates[category] = ResponseTemplate(category=category)
        self._templates[category].templates.append(template)

    def set_templates(self, category: str, templates: List[str]) -> None:
        """Set all templates for a category."""
        self._templates[category] = ResponseTemplate(
            category=category,
            templates=templates
        )

    def list_categories(self) -> List[str]:
        """List all template categories."""
        return list(self._templates.keys())


# Global template manager
_manager: TemplateManager = None


def get_template_manager() -> TemplateManager:
    """Get global template manager."""
    global _manager
    if _manager is None:
        _manager = TemplateManager()
    return _manager
