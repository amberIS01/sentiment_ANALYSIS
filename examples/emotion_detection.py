#!/usr/bin/env python3
"""
Emotion Detection Example

Demonstrates the emotion detection functionality.
"""

from chatbot import EmotionDetector


def main():
    detector = EmotionDetector()

    messages = [
        "I am so happy and excited about this!",
        "This makes me really angry and frustrated.",
        "I'm scared about what might happen.",
        "Wow, I can't believe this happened!",
        "I feel sad and lonely today.",
        "I trust you completely.",
    ]

    print("=== Emotion Detection ===\n")

    for msg in messages:
        result = detector.detect_emotion(msg)
        print(f"Text: {msg}")
        print(f"  Primary Emotion: {result.primary_emotion.value}")
        print(f"  Confidence: {result.confidence:.2f}")
        print()

    # Get summary for all messages
    summary = detector.get_emotion_summary(messages)
    print("=== Emotion Summary ===")
    print(f"Primary Emotion: {summary['primary_emotion']}")
    print(f"Distribution: {summary['emotion_distribution']}")


if __name__ == "__main__":
    main()
