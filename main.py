#!/usr/bin/env python3
"""
Chatbot with Sentiment Analysis - Main Entry Point

This script provides a command-line interface for the chatbot with
both Tier 1 (conversation-level) and Tier 2 (statement-level) sentiment analysis.

Usage:
    python main.py              # Interactive chat mode
    python main.py --help       # Show help

Commands during chat:
    'quit' or 'exit'  - End the conversation and show summary
    'summary'         - Show current conversation summary
    'clear'           - Clear conversation history
    'help'            - Show available commands
"""

import argparse
import sys

from chatbot import Chatbot, SentimentAnalyzer


def print_banner():
    """Print the welcome banner."""
    print("\n" + "=" * 60)
    print("  CHATBOT WITH SENTIMENT ANALYSIS")
    print("  Tier 1 & Tier 2 Implementation")
    print("=" * 60)
    print("\nType 'help' for available commands, 'quit' to exit.\n")


def print_help():
    """Print available commands."""
    print("\nAvailable commands:")
    print("  quit, exit  - End conversation and show final summary")
    print("  summary     - Show current conversation summary")
    print("  clear       - Clear conversation history and start fresh")
    print("  help        - Show this help message")
    print()


def run_interactive_chat():
    """Run the interactive chat session."""
    print_banner()

    bot = Chatbot()

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle commands
            command = user_input.lower()

            if command in ('quit', 'exit'):
                # End conversation and show summary
                if not bot.conversation.is_empty:
                    print(bot.get_formatted_summary())
                print("\nThank you for chatting! Goodbye.\n")
                break

            elif command == 'summary':
                # Show current summary
                if bot.conversation.is_empty:
                    print("\nNo messages yet. Start chatting to see the summary.\n")
                else:
                    print(bot.get_formatted_summary())
                continue

            elif command == 'clear':
                # Clear conversation
                bot.reset()
                print("\nConversation cleared. Starting fresh!\n")
                continue

            elif command == 'help':
                print_help()
                continue

            # Process message and get response
            response, sentiment = bot.process_message(user_input)

            # Display sentiment for the user's message (Tier 2)
            print(f"  -> Sentiment: {sentiment.label.value}")

            # Display bot response
            print(f"Bot: {response}\n")

        except KeyboardInterrupt:
            print("\n")
            if not bot.conversation.is_empty:
                print(bot.get_formatted_summary())
            print("Chat interrupted. Goodbye!\n")
            break
        except EOFError:
            print("\n")
            if not bot.conversation.is_empty:
                print(bot.get_formatted_summary())
            print("Chat ended. Goodbye!\n")
            break


def run_demo():
    """Run a demonstration of the chatbot functionality."""
    print("\n" + "=" * 60)
    print("  CHATBOT DEMO - Sentiment Analysis Demonstration")
    print("=" * 60 + "\n")

    bot = Chatbot()

    # Demo conversation (similar to the example in the assignment)
    demo_messages = [
        "Your service disappoints me",
        "Last experience was better",
        "I hope things improve",
        "Thank you for listening to my concerns"
    ]

    print("Demo conversation:\n")

    for message in demo_messages:
        print(f"User: \"{message}\"")
        response, sentiment = bot.process_message(message)
        print(f"  -> Sentiment: {sentiment.label.value}")
        print(f"Chatbot: \"{response}\"\n")

    # Show final summary
    print(bot.get_formatted_summary())


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Chatbot with Sentiment Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py           Run interactive chat
  python main.py --demo    Run demonstration mode

During interactive chat:
  Type your message and press Enter
  Type 'quit' or 'exit' to end and see summary
  Type 'summary' to see current analysis
  Type 'clear' to start fresh
  Type 'help' for more commands
        """
    )

    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run demonstration mode with sample conversation'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Chatbot with Sentiment Analysis v1.0.0'
    )

    args = parser.parse_args()

    try:
        if args.demo:
            run_demo()
        else:
            run_interactive_chat()
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
