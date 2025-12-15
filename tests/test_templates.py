"""
Tests for the Templates Module.
"""

import pytest

from chatbot.templates import ResponseTemplates, TemplateManager


class TestResponseTemplates:
    """Test ResponseTemplates class."""

    def test_get_greeting(self):
        templates = ResponseTemplates()
        greeting = templates.get_greeting()
        assert isinstance(greeting, str)
        assert len(greeting) > 0

    def test_get_farewell(self):
        templates = ResponseTemplates()
        farewell = templates.get_farewell()
        assert isinstance(farewell, str)

    def test_get_positive_response(self):
        templates = ResponseTemplates()
        response = templates.get_positive_response()
        assert isinstance(response, str)

    def test_get_negative_response(self):
        templates = ResponseTemplates()
        response = templates.get_negative_response()
        assert isinstance(response, str)

    def test_get_neutral_response(self):
        templates = ResponseTemplates()
        response = templates.get_neutral_response()
        assert isinstance(response, str)


class TestTemplateManager:
    """Test TemplateManager class."""

    def test_initialization(self):
        manager = TemplateManager()
        assert manager is not None

    def test_register_template(self):
        manager = TemplateManager()
        manager.register("custom", ["Hello {name}!"])
        result = manager.get("custom", name="World")
        assert "World" in result

    def test_get_random(self):
        manager = TemplateManager()
        manager.register("greetings", ["Hi", "Hello", "Hey"])
        result = manager.get("greetings")
        assert result in ["Hi", "Hello", "Hey"]

    def test_get_nonexistent(self):
        manager = TemplateManager()
        result = manager.get("nonexistent")
        assert result is None

    def test_list_categories(self):
        manager = TemplateManager()
        manager.register("cat1", ["test"])
        manager.register("cat2", ["test"])
        categories = manager.list_categories()
        assert "cat1" in categories
        assert "cat2" in categories
