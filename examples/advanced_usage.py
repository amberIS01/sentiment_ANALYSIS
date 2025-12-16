#!/usr/bin/env python3
"""
Advanced Usage Example

Demonstrates advanced features of the sentiment analysis chatbot.
"""

from chatbot import (
    Chatbot,
    SentimentAnalyzer,
    EmotionDetector,
    ConversationManager,
    StatisticsTracker,
)
from chatbot.session import SessionManager
from chatbot.cache import SentimentCache
from chatbot.history import SentimentHistory
from chatbot.events import EventEmitter, ChatEvents
from chatbot.middleware import MiddlewareChain, TrimMiddleware, Context
from chatbot.trends import TrendAnalyzer


def setup_event_handlers(emitter: EventEmitter) -> None:
    """Set up event handlers for logging."""
    def on_message(event):
        print(f"[EVENT] Message received: {event.data[:50]}...")

    def on_sentiment(event):
        print(f"[EVENT] Sentiment analyzed: {event.data}")

    emitter.on(ChatEvents.MESSAGE_RECEIVED, on_message)
    emitter.on(ChatEvents.SENTIMENT_ANALYZED, on_sentiment)


def main():
    """Run advanced example."""
    print("=" * 50)
    print("Advanced Sentiment Analysis Example")
    print("=" * 50)

    # Initialize components
    analyzer = SentimentAnalyzer()
    detector = EmotionDetector()
    cache = SentimentCache()
    history = SentimentHistory()
    trends = TrendAnalyzer()
    emitter = EventEmitter()
    session_manager = SessionManager()
    stats = StatisticsTracker()

    # Set up event handlers
    setup_event_handlers(emitter)

    # Create middleware chain
    chain = (
        MiddlewareChain()
        .use(TrimMiddleware())
        .set_handler(lambda ctx: analyzer.analyze(ctx.message))
    )

    # Create session
    session = session_manager.create_session()
    print(f"\nSession created: {session.session_id[:8]}...")

    # Sample messages
    messages = [
        "I'm really excited about this new project!",
        "The weather today is just okay, nothing special.",
        "I'm frustrated with all these bugs in the code.",
        "Finally fixed the issue! Feeling accomplished!",
        "This is getting tedious and boring.",
    ]

    print("\nProcessing messages:\n")

    for msg in messages:
        # Emit event
        emitter.emit(ChatEvents.MESSAGE_RECEIVED, msg)

        # Check cache first
        cached = cache.get(msg)
        if cached:
            result = cached
            print(f"[CACHE HIT] {msg[:30]}...")
        else:
            # Process through middleware
            ctx = Context(message=msg, session_id=session.session_id)
            result = chain.process(ctx)
            cache.set(msg, result)

        # Detect emotions
        emotions = detector.detect(msg)

        # Track history and trends
        history.add(result.compound, result.label.value, msg)
        trends.add_point(result.compound, result.label.value)

        # Update stats
        stats.record_message("user", len(msg))
        stats.record_sentiment(result.compound)

        # Emit sentiment event
        emitter.emit(ChatEvents.SENTIMENT_ANALYZED, result.label.value)

        # Display results
        print(f"\nMessage: {msg}")
        print(f"  Sentiment: {result.label.value} ({result.compound:.3f})")
        print(f"  Emotions: {[e.name for e in emotions.emotions[:3]]}")

    # Show summary
    print("\n" + "=" * 50)
    print("Analysis Summary")
    print("=" * 50)

    print(f"\nSentiment History:")
    print(f"  Average Score: {history.average_score():.3f}")
    print(f"  Trend: {history.trend()}")
    print(f"  Label Counts: {history.label_counts()}")

    trend_analysis = trends.analyze()
    if trend_analysis:
        print(f"\nTrend Analysis:")
        print(f"  Direction: {trend_analysis.direction.value}")
        print(f"  Volatility: {trend_analysis.volatility:.3f}")

    cache_stats = cache.stats()
    print(f"\nCache Stats:")
    print(f"  Hits: {cache_stats['hits']}")
    print(f"  Misses: {cache_stats['misses']}")

    summary = stats.get_summary()
    print(f"\nConversation Stats:")
    print(f"  Total Messages: {summary.total_messages}")
    print(f"  Average Sentiment: {summary.average_sentiment:.3f}")


if __name__ == "__main__":
    main()
