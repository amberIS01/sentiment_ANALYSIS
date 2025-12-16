"""
CLI Wrapper Module

Provides command-line interface utilities for the chatbot.
"""

import argparse
import sys
from typing import Optional, List
from dataclasses import dataclass

from .bot import Chatbot
from .sentiment import SentimentAnalyzer
from .emotions import EmotionDetector


@dataclass
class CLIConfig:
    """CLI configuration."""

    verbose: bool = False
    show_emotions: bool = True
    show_scores: bool = True
    color_output: bool = True


class ChatbotCLI:
    """Command-line interface for the chatbot."""

    def __init__(self, config: Optional[CLIConfig] = None):
        """Initialize CLI."""
        self.config = config or CLIConfig()
        self.chatbot = Chatbot()
        self.analyzer = SentimentAnalyzer()
        self.detector = EmotionDetector()

    def run_interactive(self) -> None:
        """Run interactive chat session."""
        print("Sentiment Analysis Chatbot")
        print("Type 'quit' or 'exit' to end the session")
        print("-" * 40)

        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ("quit", "exit", "bye"):
                    print("\nGoodbye!")
                    break

                response = self.process_input(user_input)
                print(f"\nBot: {response}")

            except KeyboardInterrupt:
                print("\n\nSession ended.")
                break
            except EOFError:
                print("\n\nSession ended.")
                break

    def process_input(self, text: str) -> str:
        """Process user input and return response."""
        # Get chatbot response
        response = self.chatbot.process_message(text)

        # Show sentiment if configured
        if self.config.show_scores:
            sentiment = self.analyzer.analyze(text)
            print(f"  [Sentiment: {sentiment.label.value} ({sentiment.compound:.2f})]")

        # Show emotions if configured
        if self.config.show_emotions:
            emotions = self.detector.detect(text)
            if emotions.emotions:
                emotion_str = ", ".join(e.name for e in emotions.emotions[:3])
                print(f"  [Emotions: {emotion_str}]")

        return response

    def analyze_text(self, text: str) -> dict:
        """Analyze text and return results."""
        sentiment = self.analyzer.analyze(text)
        emotions = self.detector.detect(text)

        return {
            "text": text,
            "sentiment": {
                "label": sentiment.label.value,
                "compound": sentiment.compound,
                "positive": sentiment.positive,
                "negative": sentiment.negative,
                "neutral": sentiment.neutral,
            },
            "emotions": [
                {"name": e.name, "intensity": e.intensity}
                for e in emotions.emotions
            ],
        }

    def analyze_file(self, filepath: str) -> List[dict]:
        """Analyze text from a file."""
        results = []
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    results.append(self.analyze_text(line))
        return results


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Sentiment Analysis Chatbot CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode",
    )

    parser.add_argument(
        "-t", "--text",
        type=str,
        help="Analyze a single text string",
    )

    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Analyze text from a file (one per line)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--no-emotions",
        action="store_true",
        help="Disable emotion detection",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    parsed = parser.parse_args(args)

    config = CLIConfig(
        verbose=parsed.verbose,
        show_emotions=not parsed.no_emotions,
        color_output=not parsed.no_color,
    )

    cli = ChatbotCLI(config=config)

    if parsed.text:
        result = cli.analyze_text(parsed.text)
        print(f"Text: {result['text']}")
        print(f"Sentiment: {result['sentiment']['label']}")
        print(f"Score: {result['sentiment']['compound']:.3f}")
        return 0

    if parsed.file:
        results = cli.analyze_file(parsed.file)
        for result in results:
            print(f"{result['sentiment']['label']}: {result['text'][:50]}...")
        return 0

    # Default to interactive mode
    cli.run_interactive()
    return 0


if __name__ == "__main__":
    sys.exit(main())
