#!/usr/bin/env python3
"""
Streaming Example

Demonstrates streaming sentiment analysis for real-time data.
"""

from dataclasses import dataclass
from typing import Iterator, Generator, List, Callable, Optional
import time
import random

from chatbot import SentimentAnalyzer
from chatbot.history import SentimentHistory
from chatbot.trends import TrendAnalyzer


@dataclass
class StreamItem:
    """A single item in the stream."""

    id: int
    text: str
    timestamp: float


@dataclass
class StreamResult:
    """Result from processing a stream item."""

    item: StreamItem
    sentiment_score: float
    sentiment_label: str
    processing_time: float


class SentimentStream:
    """Process streaming sentiment data."""

    def __init__(self):
        """Initialize stream processor."""
        self.analyzer = SentimentAnalyzer()
        self.history = SentimentHistory()
        self.trends = TrendAnalyzer()
        self._callbacks: List[Callable[[StreamResult], None]] = []

    def on_result(self, callback: Callable[[StreamResult], None]) -> None:
        """Register a callback for results."""
        self._callbacks.append(callback)

    def process_item(self, item: StreamItem) -> StreamResult:
        """Process a single stream item."""
        start = time.perf_counter()
        result = self.analyzer.analyze(item.text)
        elapsed = time.perf_counter() - start

        # Track history and trends
        self.history.add(result.compound, result.label.value, item.text)
        self.trends.add_point(result.compound, result.label.value)

        stream_result = StreamResult(
            item=item,
            sentiment_score=result.compound,
            sentiment_label=result.label.value,
            processing_time=elapsed,
        )

        # Notify callbacks
        for callback in self._callbacks:
            callback(stream_result)

        return stream_result

    def process_stream(
        self,
        stream: Iterator[StreamItem],
    ) -> Generator[StreamResult, None, None]:
        """Process a stream of items."""
        for item in stream:
            yield self.process_item(item)

    def get_running_average(self) -> float:
        """Get running average sentiment."""
        return self.history.average_score()

    def get_current_trend(self) -> str:
        """Get current trend direction."""
        return self.history.trend()


def generate_sample_stream(count: int = 20) -> Iterator[StreamItem]:
    """Generate sample stream data."""
    samples = [
        "I love this product! It's amazing!",
        "This is okay, nothing special.",
        "Terrible experience, very disappointed.",
        "Great customer service today!",
        "Meh, could be better.",
        "Absolutely fantastic results!",
        "Not happy with the quality.",
        "Best purchase I've ever made!",
        "It works fine I guess.",
        "Complete waste of money.",
        "Exceeded my expectations!",
        "Pretty average overall.",
        "Highly recommend this!",
        "Would not buy again.",
        "Pleasantly surprised!",
    ]

    for i in range(count):
        yield StreamItem(
            id=i + 1,
            text=random.choice(samples),
            timestamp=time.time(),
        )
        time.sleep(0.1)  # Simulate streaming delay


def main():
    """Run streaming example."""
    print("Streaming Sentiment Analysis Example")
    print("=" * 50)

    stream = SentimentStream()

    # Register callback
    def on_result(result: StreamResult):
        print(f"[{result.item.id:3}] {result.sentiment_label:8} "
              f"({result.sentiment_score:+.2f}) - "
              f"{result.item.text[:40]}...")

    stream.on_result(on_result)

    # Process stream
    print("\nProcessing stream...\n")
    results = list(stream.process_stream(generate_sample_stream(15)))

    # Show summary
    print("\n" + "=" * 50)
    print("Stream Summary")
    print("=" * 50)
    print(f"Items processed: {len(results)}")
    print(f"Running average: {stream.get_running_average():.3f}")
    print(f"Current trend: {stream.get_current_trend()}")

    # Show distribution
    labels = [r.sentiment_label for r in results]
    for label in ["positive", "negative", "neutral"]:
        count = labels.count(label)
        pct = count / len(labels) * 100
        print(f"  {label}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
