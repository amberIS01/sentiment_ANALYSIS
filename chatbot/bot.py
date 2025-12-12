"""
Chatbot Response Logic Module

This module provides the chatbot's response generation logic.
It uses a rule-based approach that considers user sentiment and
context to generate appropriate responses.
"""

import random
from typing import List, Optional

from .conversation import ConversationManager, MessageRole
from .sentiment import SentimentLabel, SentimentResult, ConversationSentimentSummary


class Chatbot:
    """
    A chatbot that generates contextual responses based on user input
    and sentiment analysis.

    The chatbot uses a rule-based approach that considers:
    - The sentiment of the user's message
    - Keywords in the message
    - Conversation context

    This design allows for consistent, empathetic responses without
    requiring external API dependencies.
    """

    # Response templates based on sentiment
    POSITIVE_RESPONSES = [
        "That's wonderful to hear! Is there anything else I can help you with?",
        "I'm glad things are going well! How can I assist you further?",
        "Great to hear that! What else would you like to discuss?",
        "That sounds positive! Feel free to share more.",
        "I appreciate your positive feedback! How may I continue to help?",
    ]

    NEGATIVE_RESPONSES = [
        "I'm sorry to hear that. Let me see how I can help address your concern.",
        "I understand your frustration. I'll do my best to assist you.",
        "I apologize for any inconvenience. How can I make things better?",
        "I hear your concern and want to help resolve this issue.",
        "I'm sorry you're experiencing this. Let's work together to find a solution.",
    ]

    NEUTRAL_RESPONSES = [
        "I understand. How can I assist you further?",
        "Thank you for sharing. What else would you like to know?",
        "I see. Is there anything specific you'd like help with?",
        "Got it. Feel free to ask me anything.",
        "Understood. How may I help you today?",
    ]

    # Keyword-based response overrides
    KEYWORD_RESPONSES = {
        "hello": ["Hello! Welcome! How can I assist you today?", "Hi there! How may I help you?"],
        "hi": ["Hello! How can I help you today?", "Hi! What can I do for you?"],
        "bye": ["Goodbye! Thank you for chatting with me.", "Take care! Feel free to return anytime."],
        "goodbye": ["Goodbye! It was nice talking to you.", "Bye! Have a great day!"],
        "thank": ["You're welcome! Is there anything else I can help with?", "Happy to help! Anything else?"],
        "thanks": ["You're welcome! Let me know if you need anything else.", "Glad I could help!"],
        "help": ["I'm here to help! What do you need assistance with?", "Of course! What would you like help with?"],
        "problem": ["I'm sorry to hear about the problem. Can you tell me more?", "Let's solve this together. What's happening?"],
        "issue": ["I understand there's an issue. Please provide more details.", "I'll help you resolve this issue. What's going on?"],
        "complaint": ["I'm sorry you have a complaint. I'll make sure it's addressed.", "Your feedback is important. Please tell me more."],
        "disappointed": ["I'm truly sorry to hear you're disappointed. How can I make it right?", "I apologize for the disappointment. Let me help."],
        "happy": ["I'm glad you're happy! Is there anything else I can do?", "That's great to hear! How else can I assist?"],
        "love": ["Thank you for the kind words! How can I continue to help?", "I appreciate that! What else can I do for you?"],
        "hate": ["I'm sorry you feel that way. Let me try to help improve things.", "I understand your frustration. How can I help?"],
        "angry": ["I apologize for causing any frustration. Let's work this out.", "I'm sorry you're upset. How can I make things better?"],
        "frustrated": ["I understand your frustration. Let me help resolve this.", "I'm sorry for the frustration. What can I do to help?"],
    }

    def __init__(self, conversation_manager: Optional[ConversationManager] = None):
        """
        Initialize the chatbot.

        Args:
            conversation_manager: Optional ConversationManager instance.
                                  Creates one if not provided.
        """
        self._conversation = conversation_manager or ConversationManager()

    @property
    def conversation(self) -> ConversationManager:
        """Get the conversation manager."""
        return self._conversation

    def process_message(self, user_input: str) -> tuple[str, SentimentResult]:
        """
        Process a user message and generate a response.

        Args:
            user_input: The user's input message.

        Returns:
            Tuple of (bot_response, user_sentiment).
        """
        # Add user message and get sentiment
        user_message = self._conversation.add_user_message(user_input)
        sentiment = user_message.sentiment

        # Generate response
        response = self._generate_response(user_input, sentiment)

        # Add bot response to conversation
        self._conversation.add_bot_message(response)

        return response, sentiment

    def _generate_response(
        self,
        user_input: str,
        sentiment: Optional[SentimentResult]
    ) -> str:
        """
        Generate a response based on user input and sentiment.

        Args:
            user_input: The user's input message.
            sentiment: The sentiment analysis result.

        Returns:
            The chatbot's response.
        """
        # First check for keyword matches
        input_lower = user_input.lower()

        for keyword, responses in self.KEYWORD_RESPONSES.items():
            if keyword in input_lower:
                return random.choice(responses)

        # If no keyword match, respond based on sentiment
        if sentiment is None:
            return random.choice(self.NEUTRAL_RESPONSES)

        if sentiment.label == SentimentLabel.POSITIVE:
            return random.choice(self.POSITIVE_RESPONSES)
        elif sentiment.label == SentimentLabel.NEGATIVE:
            return random.choice(self.NEGATIVE_RESPONSES)
        else:
            return random.choice(self.NEUTRAL_RESPONSES)

    def get_conversation_summary(self) -> ConversationSentimentSummary:
        """
        Get the sentiment summary for the entire conversation.

        Returns:
            ConversationSentimentSummary with complete analysis.
        """
        return self._conversation.analyze_conversation()

    def get_formatted_summary(self) -> str:
        """
        Get a formatted string summary of the conversation and sentiment.

        Returns:
            Formatted summary string.
        """
        summary = self.get_conversation_summary()

        lines = [
            "\n" + "=" * 60,
            "CONVERSATION SUMMARY",
            "=" * 60,
            "",
            "Conversation History:",
            "-" * 40,
            self._conversation.get_formatted_history(include_sentiment=True),
            "",
            "-" * 40,
            "Sentiment Statistics:",
            f"  Positive messages: {summary.positive_count}",
            f"  Negative messages: {summary.negative_count}",
            f"  Neutral messages: {summary.neutral_count}",
            f"  Average sentiment score: {summary.average_compound_score:.2f}",
            "",
            f"Mood Trend: {summary.mood_trend}",
            "",
            "=" * 60,
            f"FINAL OUTPUT: {summary}",
            "=" * 60,
        ]

        return "\n".join(lines)

    def reset(self) -> None:
        """Reset the conversation history."""
        self._conversation.clear()

    def chat(self, user_input: str) -> str:
        """
        Simple chat interface that returns just the response.

        Args:
            user_input: The user's input message.

        Returns:
            The chatbot's response.
        """
        response, _ = self.process_message(user_input)
        return response
