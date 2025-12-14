#!/usr/bin/env python3
"""
Basic Usage Example

Demonstrates the basic usage of the sentiment analysis chatbot.
"""

from chatbot import Chatbot, SentimentAnalyzer


def main():
    # Create chatbot instance
    bot = Chatbot()

    # Process some messages
    messages = [
        "Hello, how are you?",
        "I'm feeling great today!",
        "This service is disappointing.",
        "Thank you for your help!",
    ]

    print("=== Basic Chatbot Usage ===\n")

    for msg in messages:
        response, sentiment = bot.process_message(msg)
        print(f"User: {msg}")
        print(f"  Sentiment: {sentiment.label.value} ({sentiment.compound_score:.2f})")
        print(f"Bot: {response}\n")

    # Get conversation summary
    summary = bot.get_conversation_summary()
    print("=== Conversation Summary ===")
    print(f"Overall: {summary.overall_sentiment.value}")
    print(f"Average Score: {summary.average_compound_score:.2f}")
    print(f"Mood Trend: {summary.mood_trend}")


if __name__ == "__main__":
    main()
