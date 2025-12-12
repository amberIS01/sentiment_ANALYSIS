# Chatbot with Sentiment Analysis

A Python chatbot that maintains conversation history and performs sentiment analysis at both the statement level (Tier 2) and conversation level (Tier 1).

## Features

### Tier 1 - Conversation-Level Sentiment Analysis (Mandatory)
- Maintains full conversation history throughout the session
- Generates comprehensive sentiment analysis at the end of the interaction
- Provides overall emotional direction based on the complete exchange

### Tier 2 - Statement-Level Sentiment Analysis (Additional Credit)
- Real-time sentiment evaluation for every user message
- Displays each message alongside its sentiment output
- Mood trend analysis showing sentiment shifts across the conversation

## How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd liaplus
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the chatbot:
```bash
python main.py
```

### Usage Options

**Interactive Mode (default):**
```bash
python main.py
```

**Demo Mode:**
```bash
python main.py --demo
```

### Commands During Chat
- `quit` or `exit` - End conversation and display final summary
- `summary` - View current conversation sentiment analysis
- `clear` - Clear conversation history and start fresh
- `help` - Display available commands

## Chosen Technologies

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Primary programming language |
| **NLTK** | Natural Language Toolkit for NLP operations |
| **VADER Sentiment** | Sentiment analysis engine (part of NLTK) |
| **pytest** | Testing framework |

### Why VADER?

VADER (Valence Aware Dictionary and sEntiment Reasoner) was chosen for sentiment analysis because:

1. **Designed for Social Media/Chat**: Specifically attuned to sentiments expressed in conversational text
2. **Handles Informal Language**: Recognizes slang, emoticons, and internet-speak
3. **Emphasis Detection**: Understands punctuation (!!!), capitalization (GREAT), and degree modifiers
4. **No Training Required**: Lexicon-based approach works out-of-the-box
5. **Lightweight**: No large model downloads or external API calls needed

## Explanation of Sentiment Logic

### Sentiment Classification

The sentiment analyzer classifies text into three categories based on VADER's compound score:

| Compound Score | Classification |
|----------------|----------------|
| >= 0.05 | Positive |
| <= -0.05 | Negative |
| Between -0.05 and 0.05 | Neutral |

### Per-Message Analysis (Tier 2)

Each user message is analyzed immediately upon input:
```
User: "Your service disappoints me"
  -> Sentiment: Negative
```

### Conversation Analysis (Tier 1)

At conversation end, the system:
1. Aggregates all user message sentiments
2. Calculates average compound score
3. Determines overall sentiment direction
4. Analyzes mood trends across the conversation

### Mood Trend Detection

The system analyzes sentiment evolution by:
1. Comparing first-half vs second-half average scores
2. Comparing start vs end sentiment
3. Detecting patterns: improving, declining, stable, or fluctuating

## Status of Tier 2 Implementation

**Tier 2 is FULLY IMPLEMENTED** with all features:

| Feature | Status |
|---------|--------|
| Per-message sentiment evaluation | ✅ Complete |
| Display sentiment with each message | ✅ Complete |
| Mood trend summarization | ✅ Complete |

## Project Structure

```
liaplus/
├── main.py                 # Entry point with CLI
├── requirements.txt        # Project dependencies
├── README.md              # This documentation
├── chatbot/               # Main package
│   ├── __init__.py        # Package exports
│   ├── sentiment.py       # Sentiment analysis module
│   ├── conversation.py    # Conversation management
│   └── bot.py             # Chatbot response logic
└── tests/                 # Test suite
    ├── __init__.py
    ├── test_sentiment.py  # Sentiment analyzer tests
    ├── test_conversation.py # Conversation manager tests
    └── test_bot.py        # Chatbot tests
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_sentiment.py

# Run with coverage
pytest --cov=chatbot
```

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

Conversation History:
----------------------------------------
User: "Your service disappoints me"
  -> Sentiment: Negative
Chatbot: "I'm sorry to hear that..."
User: "Last experience was better"
  -> Sentiment: Positive
Chatbot: "I appreciate your feedback!..."

----------------------------------------
Sentiment Statistics:
  Positive messages: 1
  Negative messages: 1
  Neutral messages: 0
  Average sentiment score: -0.12

Mood Trend: Slight improvement in mood over the conversation

============================================================
FINAL OUTPUT: Overall conversation sentiment: Negative - Slight improvement in mood over the conversation
============================================================
```

## Additional Features & Enhancements

1. **Modular Architecture**: Clean separation of concerns allows easy extension
2. **Comprehensive Test Suite**: 40+ tests covering all modules
3. **Keyword-Based Responses**: Smart responses for common phrases (greetings, thanks, complaints)
4. **Sentiment-Aware Responses**: Bot adapts tone based on user sentiment
5. **Detailed Statistics**: Message counts, average scores, trend analysis
6. **Demo Mode**: Quick demonstration of functionality
7. **Session Commands**: View summary, clear history, get help mid-conversation

## API Usage

The chatbot can also be used programmatically:

```python
from chatbot import Chatbot

bot = Chatbot()

# Process messages
response, sentiment = bot.process_message("I love your service!")
print(f"Sentiment: {sentiment.label.value}")
print(f"Response: {response}")

# Get summary
summary = bot.get_conversation_summary()
print(f"Overall: {summary.overall_sentiment.value}")
print(f"Mood trend: {summary.mood_trend}")
```

## License

This project was created for the LiaPlus AI assignment.
