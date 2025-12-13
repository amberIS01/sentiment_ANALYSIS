"""
Type Aliases Module

This module defines type aliases used throughout the chatbot application
for better type hinting and code readability.
"""

from typing import Dict, List, Tuple, Optional, Union, Callable, Any, TypeVar
from datetime import datetime

# Generic type variable
T = TypeVar('T')

# Sentiment types
SentimentScore = float  # -1.0 to 1.0
CompoundScore = float  # -1.0 to 1.0
PositiveScore = float  # 0.0 to 1.0
NegativeScore = float  # 0.0 to 1.0
NeutralScore = float  # 0.0 to 1.0

# Sentiment scores dictionary (from VADER)
SentimentScores = Dict[str, float]

# Message types
MessageContent = str
MessageTimestamp = datetime
RoleString = str  # "user" or "bot"

# Conversation types
MessageDict = Dict[str, Any]
MessageList = List[MessageDict]
ConversationHistory = List[Tuple[str, str]]  # List of (role, content) tuples

# Response types
ResponseTemplate = str
ResponseList = List[ResponseTemplate]
KeywordResponses = Dict[str, ResponseList]

# Analysis types
MoodTrend = str
EmotionName = str
EmotionScore = float
EmotionDistribution = Dict[EmotionName, EmotionScore]

# Statistics types
StatValue = Union[int, float]
StatDict = Dict[str, StatValue]

# Configuration types
ConfigValue = Union[str, int, float, bool, None]
ConfigDict = Dict[str, Any]

# Export types
ExportFormat = str  # "json", "csv", "text"
FilePath = str

# Callback types
MessageCallback = Callable[[str], None]
SentimentCallback = Callable[[SentimentScore], None]
ResponseCallback = Callable[[str, SentimentScore], str]

# Validation types
ValidationErrors = List[str]
ValidationResult = Tuple[bool, Optional[str]]

# Logger types
LogLevel = str  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
