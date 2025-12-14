#!/usr/bin/env python3
"""
Benchmark Script

Measures performance of sentiment analysis operations.
"""

import time
import sys
sys.path.insert(0, '.')

from chatbot import SentimentAnalyzer, EmotionDetector


def benchmark_sentiment(iterations: int = 1000):
    """Benchmark sentiment analysis."""
    analyzer = SentimentAnalyzer()
    messages = [
        "I love this product!",
        "This is terrible service.",
        "The weather is nice today.",
        "I am so frustrated with this.",
        "Thank you for your help!",
    ]

    start = time.perf_counter()
    for _ in range(iterations):
        for msg in messages:
            analyzer.analyze_text(msg)
    elapsed = time.perf_counter() - start

    ops = (iterations * len(messages)) / elapsed
    print(f"Sentiment Analysis: {ops:.2f} ops/sec")


def benchmark_emotion(iterations: int = 1000):
    """Benchmark emotion detection."""
    detector = EmotionDetector()
    messages = [
        "I am so happy today!",
        "This makes me angry.",
        "I'm scared about this.",
    ]

    start = time.perf_counter()
    for _ in range(iterations):
        for msg in messages:
            detector.detect_emotion(msg)
    elapsed = time.perf_counter() - start

    ops = (iterations * len(messages)) / elapsed
    print(f"Emotion Detection: {ops:.2f} ops/sec")


if __name__ == "__main__":
    print("Running benchmarks...\n")
    benchmark_sentiment()
    benchmark_emotion()
    print("\nDone!")
