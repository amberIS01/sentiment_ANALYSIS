"""
Tests for the API Module.
"""

import pytest
from chatbot.api import ChatbotAPI, APIResponse, create_api


class TestAPIResponse:
    """Test APIResponse dataclass."""

    def test_success_response(self):
        response = APIResponse(success=True, data={"key": "value"})
        assert response.success is True
        assert response.data["key"] == "value"

    def test_error_response(self):
        response = APIResponse(success=False, error="Something went wrong")
        assert response.success is False
        assert response.error == "Something went wrong"

    def test_to_dict(self):
        response = APIResponse(success=True, data={"test": 1})
        result = response.to_dict()
        assert isinstance(result, dict)
        assert result["success"] is True


class TestChatbotAPI:
    """Test ChatbotAPI class."""

    @pytest.fixture
    def api(self):
        return ChatbotAPI()

    def test_send_message(self, api):
        response = api.send_message("Hello!")
        assert response.success is True
        assert "response" in response.data
        assert "sentiment" in response.data

    def test_send_message_returns_sentiment(self, api):
        response = api.send_message("I love this!")
        assert response.data["sentiment"]["label"] in ["Positive", "Negative", "Neutral"]

    def test_get_summary_empty(self, api):
        api.reset()
        response = api.get_summary()
        assert response.success is True

    def test_get_summary_with_messages(self, api):
        api.send_message("Hello!")
        api.send_message("I'm happy!")
        response = api.get_summary()
        assert response.success is True
        assert "overall_sentiment" in response.data

    def test_reset(self, api):
        api.send_message("Test message")
        response = api.reset()
        assert response.success is True

    def test_health_check(self, api):
        response = api.health_check()
        assert response.success is True
        assert response.data["status"] == "healthy"


class TestCreateAPI:
    """Test create_api factory function."""

    def test_creates_api(self):
        api = create_api()
        assert isinstance(api, ChatbotAPI)
