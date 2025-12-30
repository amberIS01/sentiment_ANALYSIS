"""
Serializer Module

Serialize and deserialize sentiment data.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Type, TypeVar
import json
from datetime import datetime


T = TypeVar("T")


class SerializationError(Exception):
    """Serialization error."""
    pass


class Serializer:
    """Base serializer class."""

    def serialize(self, data: Any) -> str:
        """Serialize data to string."""
        raise NotImplementedError

    def deserialize(self, data: str) -> Any:
        """Deserialize string to data."""
        raise NotImplementedError


class JsonSerializer(Serializer):
    """JSON serializer."""

    def __init__(self, indent: Optional[int] = None):
        """Initialize serializer."""
        self.indent = indent

    def serialize(self, data: Any) -> str:
        """Serialize to JSON."""
        def handler(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            raise TypeError(f"Cannot serialize {type(obj)}")

        return json.dumps(data, default=handler, indent=self.indent)

    def deserialize(self, data: str) -> Any:
        """Deserialize from JSON."""
        return json.loads(data)


class DataclassSerializer(Serializer):
    """Serialize dataclasses."""

    def __init__(self, cls: Type[T]):
        """Initialize with dataclass type."""
        self.cls = cls

    def serialize(self, data: T) -> str:
        """Serialize dataclass to JSON."""
        return json.dumps(asdict(data), default=str)

    def deserialize(self, data: str) -> T:
        """Deserialize JSON to dataclass."""
        parsed = json.loads(data)
        return self.cls(**parsed)


class ListSerializer(Serializer):
    """Serialize lists of items."""

    def __init__(self, item_serializer: Serializer):
        """Initialize with item serializer."""
        self.item_serializer = item_serializer

    def serialize(self, data: List[Any]) -> str:
        """Serialize list."""
        items = [json.loads(self.item_serializer.serialize(item)) for item in data]
        return json.dumps(items)

    def deserialize(self, data: str) -> List[Any]:
        """Deserialize list."""
        items = json.loads(data)
        return [
            self.item_serializer.deserialize(json.dumps(item))
            for item in items
        ]


@dataclass
class SentimentData:
    """Sentiment data for serialization."""

    text: str
    score: float
    label: str
    confidence: float = 0.0
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SentimentSerializer:
    """Serialize sentiment analysis results."""

    def __init__(self):
        """Initialize serializer."""
        self._json = JsonSerializer()

    def serialize_result(self, result: SentimentData) -> str:
        """Serialize single result."""
        return self._json.serialize(asdict(result))

    def deserialize_result(self, data: str) -> SentimentData:
        """Deserialize single result."""
        parsed = self._json.deserialize(data)
        return SentimentData(**parsed)

    def serialize_results(self, results: List[SentimentData]) -> str:
        """Serialize multiple results."""
        return self._json.serialize([asdict(r) for r in results])

    def deserialize_results(self, data: str) -> List[SentimentData]:
        """Deserialize multiple results."""
        parsed = self._json.deserialize(data)
        return [SentimentData(**r) for r in parsed]


def to_json(data: Any) -> str:
    """Convert data to JSON string."""
    serializer = JsonSerializer()
    return serializer.serialize(data)


def from_json(data: str) -> Any:
    """Parse JSON string to data."""
    serializer = JsonSerializer()
    return serializer.deserialize(data)
