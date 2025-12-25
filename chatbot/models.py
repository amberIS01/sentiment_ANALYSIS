"""
Data Models Module

Common data models for the chatbot.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class Priority(Enum):
    """Priority levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Status(Enum):
    """Processing status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TextDocument:
    """A text document for analysis."""

    id: str
    content: str
    source: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def word_count(self) -> int:
        """Get word count."""
        return len(self.content.split())

    def char_count(self) -> int:
        """Get character count."""
        return len(self.content)


@dataclass
class AnalysisRequest:
    """Request for sentiment analysis."""

    id: str
    text: str
    priority: Priority = Priority.MEDIUM
    options: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AnalysisResult:
    """Result of sentiment analysis."""

    request_id: str
    text: str
    sentiment_score: float
    sentiment_label: str
    emotions: List[str] = field(default_factory=list)
    confidence: float = 1.0
    processing_time: float = 0.0
    completed_at: datetime = field(default_factory=datetime.now)


@dataclass
class ConversationTurn:
    """A single turn in a conversation."""

    speaker: str
    text: str
    timestamp: datetime = field(default_factory=datetime.now)
    sentiment: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Conversation:
    """A full conversation."""

    id: str
    turns: List[ConversationTurn] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_turn(self, speaker: str, text: str) -> ConversationTurn:
        """Add a turn to the conversation."""
        turn = ConversationTurn(speaker=speaker, text=text)
        self.turns.append(turn)
        return turn

    def end(self) -> None:
        """Mark conversation as ended."""
        self.ended_at = datetime.now()

    @property
    def turn_count(self) -> int:
        """Get number of turns."""
        return len(self.turns)

    @property
    def duration(self) -> Optional[float]:
        """Get conversation duration in seconds."""
        if self.ended_at:
            return (self.ended_at - self.started_at).total_seconds()
        return None


@dataclass
class UserProfile:
    """User profile for personalization."""

    user_id: str
    name: Optional[str] = None
    preferences: Dict[str, Any] = field(default_factory=dict)
    sentiment_history: List[float] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def add_sentiment(self, score: float) -> None:
        """Add sentiment to history."""
        self.sentiment_history.append(score)

    @property
    def average_sentiment(self) -> float:
        """Get average sentiment."""
        if not self.sentiment_history:
            return 0.0
        return sum(self.sentiment_history) / len(self.sentiment_history)


@dataclass
class AnalysisBatch:
    """Batch of analysis requests."""

    id: str
    requests: List[AnalysisRequest] = field(default_factory=list)
    results: List[AnalysisResult] = field(default_factory=list)
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def add_request(self, text: str) -> str:
        """Add a request to the batch."""
        request_id = f"{self.id}_{len(self.requests)}"
        request = AnalysisRequest(id=request_id, text=text)
        self.requests.append(request)
        return request_id

    @property
    def size(self) -> int:
        """Get batch size."""
        return len(self.requests)

    @property
    def is_complete(self) -> bool:
        """Check if batch is complete."""
        return len(self.results) == len(self.requests)
