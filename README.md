# Chatbot with Sentiment Analysis

[![CI](https://github.com/sahil/sentiment-chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/sahil/sentiment-chatbot/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python chatbot that maintains conversation history and performs sentiment analysis at both the statement level (Tier 2) and conversation level (Tier 1). Features emotion detection, conversation export, and comprehensive statistics tracking.

## Features

### Core Features

#### Tier 1 - Conversation-Level Sentiment Analysis
- Maintains full conversation history throughout the session
- Generates comprehensive sentiment analysis at the end of the interaction
- Provides overall emotional direction based on the complete exchange

#### Tier 2 - Statement-Level Sentiment Analysis
- Real-time sentiment evaluation for every user message
- Displays each message alongside its sentiment output
- Mood trend analysis showing sentiment shifts across the conversation

### New Features (v1.1.0)

- **Emotion Detection**: Beyond basic sentiment, detect specific emotions (joy, sadness, anger, fear, surprise, disgust, trust, anticipation)
- **Conversation Export**: Export conversations to JSON, CSV, or plain text
- **Statistics Tracking**: Comprehensive metrics including response times, engagement ratios, and sentiment variance
- **Configuration System**: JSON-based configuration with environment variable support
- **Input Validation**: Robust input validation and sanitization
- **Logging**: Structured logging for debugging and monitoring

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/sahil/sentiment-chatbot.git
cd sentiment-chatbot

# Install with pip
pip install -e .

# Or use make
make install
```

### Running

```bash
# Interactive mode
python main.py

# Demo mode
python main.py --demo

# Using make
make run
make demo
```

## Usage

### Interactive Commands

| Command | Description |
|---------|-------------|
| `quit` / `exit` | End conversation and display summary |
| `summary` | View current conversation analysis |
| `clear` | Clear history and start fresh |
| `help` | Display available commands |
| `export` | Export conversation to file |

### Programmatic API

```python
from chatbot import Chatbot, EmotionDetector, export_conversation

# Basic usage
bot = Chatbot()
response, sentiment = bot.process_message("I love your service!")
print(f"Sentiment: {sentiment.label.value}")
print(f"Response: {response}")

# Get conversation summary
summary = bot.get_conversation_summary()
print(f"Overall: {summary.overall_sentiment.value}")
print(f"Mood trend: {summary.mood_trend}")

# Emotion detection
detector = EmotionDetector()
emotion = detector.detect_emotion("I am so happy and excited!")
print(f"Emotion: {emotion.primary_emotion.value}")

# Export conversation
filepath = export_conversation(bot.conversation, format="json")
print(f"Exported to: {filepath}")
```

### Advanced Usage

```python
from chatbot import (
    Chatbot,
    ConversationManager,
    SentimentAnalyzer,
    StatisticsTracker,
    InputValidator,
)

# Custom conversation manager
manager = ConversationManager()
bot = Chatbot(conversation_manager=manager)

# Input validation
validator = InputValidator(max_length=1000)
result = validator.validate(user_input)
if result.is_valid:
    bot.process_message(result.cleaned_value)

# Statistics tracking
tracker = StatisticsTracker()
stats = tracker.calculate_statistics(bot.conversation)
print(f"Messages per minute: {stats.messages_per_minute:.2f}")
print(f"Sentiment variance: {stats.sentiment_variance:.2f}")
```

## Configuration

Create a `chatbot.json` file or copy from `chatbot.example.json`:

```json
{
  "sentiment": {
    "positive_threshold": 0.05,
    "negative_threshold": -0.05
  },
  "response": {
    "use_keyword_matching": true,
    "randomize_responses": true
  },
  "logging": {
    "enabled": true,
    "level": "INFO"
  },
  "export": {
    "export_directory": "exports",
    "default_format": "json"
  }
}
```

Environment variables (prefixed with `CHATBOT_`):
- `CHATBOT_DEBUG=true`
- `CHATBOT_LOG_LEVEL=DEBUG`
- `CHATBOT_EXPORT_DIR=my_exports`

## Project Structure

```
sentiment_ANALYSIS/
├── chatbot/                # Main package
│   ├── __init__.py         # Package exports
│   ├── sentiment.py        # Sentiment analysis (VADER)
│   ├── conversation.py     # Conversation management
│   ├── bot.py              # Chatbot response logic
│   ├── emotions.py         # Emotion detection
│   ├── exporter.py         # Export functionality
│   ├── statistics.py       # Statistics tracking
│   ├── validators.py       # Input validation
│   ├── logger.py           # Logging utilities
│   ├── config.py           # Configuration management
│   ├── constants.py        # Constants and defaults
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test suite (90+ tests)
│   ├── test_sentiment.py
│   ├── test_conversation.py
│   ├── test_bot.py
│   ├── test_emotions.py
│   └── test_validators.py
├── .github/workflows/      # CI/CD
│   └── ci.yml
├── main.py                 # CLI entry point
├── pyproject.toml          # Project configuration
├── setup.py                # Installation script
├── Makefile                # Development commands
├── requirements.txt        # Dependencies
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # Contribution guidelines
└── README.md               # This file
```

## Development

### Setup Development Environment

```bash
# Install dev dependencies
make install-dev

# Set up pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Specific test file
pytest tests/test_emotions.py -v
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Check without modifying
make check
```

## Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Primary language |
| **NLTK/VADER** | Sentiment analysis |
| **pytest** | Testing framework |
| **black/isort** | Code formatting |
| **flake8/mypy** | Linting and type checking |
| **GitHub Actions** | CI/CD pipeline |

### Why VADER?

VADER (Valence Aware Dictionary and sEntiment Reasoner) is ideal for chatbot sentiment analysis:

- **Conversational Text**: Designed for social media and chat
- **Informal Language**: Handles slang, emoticons, abbreviations
- **Emphasis Detection**: Understands punctuation, capitalization
- **Zero Training**: Lexicon-based, works immediately
- **Lightweight**: No large models or API calls

## Sentiment Logic

### Classification Thresholds

| Compound Score | Classification |
|----------------|----------------|
| >= 0.05 | Positive |
| <= -0.05 | Negative |
| -0.05 to 0.05 | Neutral |

### Emotion Detection

Beyond positive/negative/neutral, the system detects:
- **Joy**: happiness, excitement, delight
- **Sadness**: grief, disappointment, loneliness
- **Anger**: frustration, rage, annoyance
- **Fear**: anxiety, worry, nervousness
- **Surprise**: shock, amazement
- **Disgust**: revulsion, distaste
- **Trust**: confidence, belief
- **Anticipation**: eagerness, expectation

## Example Session

```
You: Your service disappoints me
  -> Sentiment: Negative
Bot: I'm sorry to hear that. Let me see how I can help address your concern.

You: Last experience was better
  -> Sentiment: Positive
Bot: I appreciate your feedback! How may I continue to help?

You: quit

============================================================
CONVERSATION SUMMARY
============================================================

Sentiment Statistics:
  Positive messages: 1
  Negative messages: 1
  Neutral messages: 0
  Average sentiment score: -0.12

Mood Trend: Slight improvement in mood over the conversation

============================================================
FINAL OUTPUT: Overall conversation sentiment: Negative
============================================================
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
