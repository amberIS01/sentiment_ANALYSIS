"""
Constants Module

This module contains all constants and configuration values used
throughout the chatbot application.
"""

from typing import Dict, List, Final


# =============================================================================
# Sentiment Analysis Constants
# =============================================================================

# Thresholds for sentiment classification
POSITIVE_THRESHOLD: Final[float] = 0.05
NEGATIVE_THRESHOLD: Final[float] = -0.05

# Mood trend analysis thresholds
MOOD_TREND_SIGNIFICANT_CHANGE: Final[float] = 0.2
MOOD_TREND_SLIGHT_CHANGE: Final[float] = 0.1
MOOD_TREND_START_END_SIGNIFICANT: Final[float] = 0.3
MOOD_TREND_START_END_SLIGHT: Final[float] = 0.15
MOOD_VARIANCE_THRESHOLD: Final[float] = 0.2


# =============================================================================
# Response Templates
# =============================================================================

POSITIVE_RESPONSES: Final[List[str]] = [
    "That's wonderful to hear! Is there anything else I can help you with?",
    "I'm glad things are going well! How can I assist you further?",
    "Great to hear that! What else would you like to discuss?",
    "That sounds positive! Feel free to share more.",
    "I appreciate your positive feedback! How may I continue to help?",
]

NEGATIVE_RESPONSES: Final[List[str]] = [
    "I'm sorry to hear that. Let me see how I can help address your concern.",
    "I understand your frustration. I'll do my best to assist you.",
    "I apologize for any inconvenience. How can I make things better?",
    "I hear your concern and want to help resolve this issue.",
    "I'm sorry you're experiencing this. Let's work together to find a solution.",
]

NEUTRAL_RESPONSES: Final[List[str]] = [
    "I understand. How can I assist you further?",
    "Thank you for sharing. What else would you like to know?",
    "I see. Is there anything specific you'd like help with?",
    "Got it. Feel free to ask me anything.",
    "Understood. How may I help you today?",
]


# =============================================================================
# Keyword Response Mappings
# =============================================================================

KEYWORD_RESPONSES: Final[Dict[str, List[str]]] = {
    # Greetings
    "hello": [
        "Hello! Welcome! How can I assist you today?",
        "Hi there! How may I help you?",
    ],
    "hi": [
        "Hello! How can I help you today?",
        "Hi! What can I do for you?",
    ],
    "hey": [
        "Hey there! How can I help?",
        "Hey! What's on your mind?",
    ],
    "good morning": [
        "Good morning! How can I assist you today?",
        "Good morning! What can I do for you?",
    ],
    "good afternoon": [
        "Good afternoon! How may I help you?",
        "Good afternoon! What can I assist you with?",
    ],
    "good evening": [
        "Good evening! How can I be of service?",
        "Good evening! What brings you here?",
    ],

    # Farewells
    "bye": [
        "Goodbye! Thank you for chatting with me.",
        "Take care! Feel free to return anytime.",
    ],
    "goodbye": [
        "Goodbye! It was nice talking to you.",
        "Bye! Have a great day!",
    ],
    "see you": [
        "See you later! Take care!",
        "Looking forward to chatting again!",
    ],

    # Gratitude
    "thank": [
        "You're welcome! Is there anything else I can help with?",
        "Happy to help! Anything else?",
    ],
    "thanks": [
        "You're welcome! Let me know if you need anything else.",
        "Glad I could help!",
    ],
    "appreciate": [
        "I appreciate your kind words! How else can I assist?",
        "Thank you! Is there anything more I can do?",
    ],

    # Help requests
    "help": [
        "I'm here to help! What do you need assistance with?",
        "Of course! What would you like help with?",
    ],
    "assist": [
        "I'd be happy to assist! What do you need?",
        "Sure, I can assist you. What's the issue?",
    ],
    "support": [
        "I'm here to support you. What's going on?",
        "How can I support you today?",
    ],

    # Problem/Issue keywords
    "problem": [
        "I'm sorry to hear about the problem. Can you tell me more?",
        "Let's solve this together. What's happening?",
    ],
    "issue": [
        "I understand there's an issue. Please provide more details.",
        "I'll help you resolve this issue. What's going on?",
    ],
    "complaint": [
        "I'm sorry you have a complaint. I'll make sure it's addressed.",
        "Your feedback is important. Please tell me more.",
    ],
    "bug": [
        "I'm sorry about the bug. Can you describe what's happening?",
        "Let me help you with this bug. What did you encounter?",
    ],
    "error": [
        "I'm sorry you encountered an error. What happened?",
        "Let's troubleshoot this error together.",
    ],

    # Emotional keywords - Negative
    "disappointed": [
        "I'm truly sorry to hear you're disappointed. How can I make it right?",
        "I apologize for the disappointment. Let me help.",
    ],
    "frustrated": [
        "I understand your frustration. Let me help resolve this.",
        "I'm sorry for the frustration. What can I do to help?",
    ],
    "angry": [
        "I apologize for causing any frustration. Let's work this out.",
        "I'm sorry you're upset. How can I make things better?",
    ],
    "upset": [
        "I'm sorry you're upset. Let me help address your concerns.",
        "I understand you're upset. How can I assist?",
    ],
    "hate": [
        "I'm sorry you feel that way. Let me try to help improve things.",
        "I understand your frustration. How can I help?",
    ],
    "terrible": [
        "I'm very sorry to hear that. Let me see what I can do.",
        "That's concerning. How can I help make things better?",
    ],
    "awful": [
        "I apologize for this experience. Let me help.",
        "I'm sorry things have been awful. What can I do?",
    ],

    # Emotional keywords - Positive
    "happy": [
        "I'm glad you're happy! Is there anything else I can do?",
        "That's great to hear! How else can I assist?",
    ],
    "love": [
        "Thank you for the kind words! How can I continue to help?",
        "I appreciate that! What else can I do for you?",
    ],
    "great": [
        "Wonderful! Is there anything more I can help with?",
        "That's great! Feel free to ask anything else.",
    ],
    "amazing": [
        "Thank you! I'm happy to hear that! How else can I help?",
        "That's wonderful feedback! Anything else I can do?",
    ],
    "excellent": [
        "Thank you for the kind words! How can I assist further?",
        "I'm glad! What else would you like help with?",
    ],

    # Questions
    "how are you": [
        "I'm doing well, thank you for asking! How can I help you?",
        "I'm great! What can I do for you today?",
    ],
    "what can you do": [
        "I can chat with you and analyze the sentiment of our conversation!",
        "I'm a sentiment-aware chatbot. I can discuss anything you'd like!",
    ],
    "who are you": [
        "I'm a chatbot with sentiment analysis capabilities!",
        "I'm your friendly sentiment-aware chatbot assistant!",
    ],
}


# =============================================================================
# Mood Trend Messages
# =============================================================================

MOOD_TREND_MESSAGES: Final[Dict[str, str]] = {
    "insufficient_data": "Insufficient data for trend analysis",
    "no_messages": "No messages to analyze",
    "stable": "Stable mood throughout the conversation",
    "improved_significantly": "Mood improved significantly during the conversation",
    "improved_slightly": "Slight improvement in mood over the conversation",
    "declined_significantly": "Mood declined significantly during the conversation",
    "declined_slightly": "Slight decline in mood over the conversation",
    "fluctuating": "Fluctuating mood throughout the conversation",
    "stable_minor": "Relatively stable mood with minor variations",
}


# =============================================================================
# CLI Constants
# =============================================================================

VERSION: Final[str] = "1.0.0"
APP_NAME: Final[str] = "Chatbot with Sentiment Analysis"

CLI_COMMANDS: Final[Dict[str, str]] = {
    "quit": "End conversation and show final summary",
    "exit": "End conversation and show final summary",
    "summary": "Show current conversation summary",
    "clear": "Clear conversation history and start fresh",
    "help": "Show available commands",
    "export": "Export conversation to JSON file",
}

# UI Constants
SEPARATOR_WIDTH: Final[int] = 60
SEPARATOR_CHAR: Final[str] = "="
SUBSEPARATOR_CHAR: Final[str] = "-"
