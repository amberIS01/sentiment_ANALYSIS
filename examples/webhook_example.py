#!/usr/bin/env python3
"""
Webhook Example

Demonstrates how to use the chatbot with webhook-style processing.
"""

from dataclasses import dataclass
from typing import Callable, Dict, Any, List, Optional
import json

from chatbot import SentimentAnalyzer, EmotionDetector
from chatbot.events import EventEmitter, Event


@dataclass
class WebhookPayload:
    """Webhook payload structure."""

    event_type: str
    data: Dict[str, Any]
    timestamp: str


@dataclass
class WebhookResponse:
    """Webhook response structure."""

    success: bool
    result: Dict[str, Any]
    error: Optional[str] = None


class WebhookHandler:
    """Handle webhook-style requests."""

    def __init__(self):
        """Initialize handler."""
        self.analyzer = SentimentAnalyzer()
        self.detector = EmotionDetector()
        self.emitter = EventEmitter()
        self._handlers: Dict[str, Callable] = {}
        self._register_default_handlers()

    def _register_default_handlers(self):
        """Register default event handlers."""
        self._handlers["analyze_sentiment"] = self._handle_sentiment
        self._handlers["detect_emotions"] = self._handle_emotions
        self._handlers["full_analysis"] = self._handle_full_analysis

    def _handle_sentiment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sentiment analysis request."""
        text = data.get("text", "")
        result = self.analyzer.analyze(text)
        return {
            "text": text,
            "sentiment": {
                "label": result.label.value,
                "compound": result.compound,
                "positive": result.positive,
                "negative": result.negative,
                "neutral": result.neutral,
            },
        }

    def _handle_emotions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle emotion detection request."""
        text = data.get("text", "")
        result = self.detector.detect(text)
        return {
            "text": text,
            "emotions": [
                {"name": e.name, "intensity": e.intensity}
                for e in result.emotions
            ],
        }

    def _handle_full_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle full analysis request."""
        sentiment = self._handle_sentiment(data)
        emotions = self._handle_emotions(data)
        return {
            "text": data.get("text", ""),
            "sentiment": sentiment["sentiment"],
            "emotions": emotions["emotions"],
        }

    def register_handler(
        self,
        event_type: str,
        handler: Callable[[Dict], Dict],
    ) -> None:
        """Register a custom handler."""
        self._handlers[event_type] = handler

    def process(self, payload: WebhookPayload) -> WebhookResponse:
        """Process a webhook payload."""
        handler = self._handlers.get(payload.event_type)

        if not handler:
            return WebhookResponse(
                success=False,
                result={},
                error=f"Unknown event type: {payload.event_type}",
            )

        try:
            result = handler(payload.data)
            self.emitter.emit("webhook_processed", {
                "event_type": payload.event_type,
                "success": True,
            })
            return WebhookResponse(success=True, result=result)
        except Exception as e:
            return WebhookResponse(
                success=False,
                result={},
                error=str(e),
            )

    def process_json(self, json_str: str) -> str:
        """Process JSON webhook payload."""
        data = json.loads(json_str)
        payload = WebhookPayload(
            event_type=data["event_type"],
            data=data["data"],
            timestamp=data.get("timestamp", ""),
        )
        response = self.process(payload)
        return json.dumps({
            "success": response.success,
            "result": response.result,
            "error": response.error,
        })


def main():
    """Run webhook example."""
    handler = WebhookHandler()

    # Example payloads
    payloads = [
        {
            "event_type": "analyze_sentiment",
            "data": {"text": "I absolutely love this product!"},
            "timestamp": "2024-01-01T00:00:00Z",
        },
        {
            "event_type": "detect_emotions",
            "data": {"text": "I'm so frustrated with this service"},
            "timestamp": "2024-01-01T00:00:01Z",
        },
        {
            "event_type": "full_analysis",
            "data": {"text": "Today was an amazing day!"},
            "timestamp": "2024-01-01T00:00:02Z",
        },
    ]

    print("Webhook Processing Example")
    print("=" * 50)

    for payload_data in payloads:
        json_payload = json.dumps(payload_data)
        response = handler.process_json(json_payload)
        result = json.loads(response)

        print(f"\nEvent: {payload_data['event_type']}")
        print(f"Input: {payload_data['data']['text']}")
        print(f"Result: {json.dumps(result['result'], indent=2)}")


if __name__ == "__main__":
    main()
