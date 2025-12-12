# Contributing to Sentiment Analysis Chatbot

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all experience levels.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your changes

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/sentiment-chatbot.git
cd sentiment-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
make install-dev

# Or manually:
pip install -e ".[dev]"
python -c "import nltk; nltk.download('vader_lexicon')"

# Set up pre-commit hooks
pre-commit install
```

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-emotion-detection` - for new features
- `fix/sentiment-threshold-bug` - for bug fixes
- `docs/update-readme` - for documentation
- `refactor/improve-logging` - for refactoring

### Commit Messages

Write clear, descriptive commit messages:

```text
Add emotion detection module

Implement keyword-based emotion analysis:
- Support for 8 emotion types
- Intensity modifier handling
- Negation detection
```

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

- Maximum line length: 100 characters
- Use type hints for function signatures
- Use docstrings for all public functions and classes

### Code Formatting

We use automated formatters:

```bash
# Format code
make format

# Check formatting without changes
make check
```

### Type Hints

Add type hints to all function signatures:

```python
def analyze_text(self, text: str) -> SentimentResult:
    """Analyze sentiment of text."""
    ...
```

### Documentation

- Use Google-style docstrings
- Document all public APIs
- Include examples where helpful

```python
def process_message(self, message: str) -> tuple[str, SentimentResult]:
    """
    Process a user message and generate a response.

    Args:
        message: The user's input message.

    Returns:
        Tuple of (bot_response, sentiment_result).

    Example:
        >>> bot = Chatbot()
        >>> response, sentiment = bot.process_message("Hello!")
    """
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_sentiment.py -v

# Run specific test
pytest tests/test_sentiment.py::TestSentimentAnalyzer::test_positive_text -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names

```python
def test_analyze_text_returns_positive_for_happy_message():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_text("I am very happy!")
    assert result.label == SentimentLabel.POSITIVE
```

### Test Coverage

Aim for high test coverage:

- All public functions should have tests
- Test edge cases and error conditions
- Test integration between components

## Submitting Changes

### Pull Request Process

1. Ensure all tests pass: `make test`
2. Run linters: `make lint`
3. Format code: `make format`
4. Update documentation if needed
5. Create a pull request with a clear description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
Describe how you tested the changes

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
```

## Issue Guidelines

### Bug Reports

Include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

### Feature Requests

Include:

- Clear description of the feature
- Use case / motivation
- Proposed implementation (optional)

## Project Structure

```text
sentiment_ANALYSIS/
├── chatbot/              # Main package
│   ├── __init__.py
│   ├── sentiment.py      # Sentiment analysis
│   ├── conversation.py   # Conversation management
│   ├── bot.py            # Chatbot logic
│   ├── constants.py      # Configuration constants
│   ├── emotions.py       # Emotion detection
│   ├── exporter.py       # Export functionality
│   ├── logger.py         # Logging utilities
│   ├── statistics.py     # Statistics tracking
│   └── validators.py     # Input validation
├── tests/                # Test suite
├── main.py               # CLI entry point
├── pyproject.toml        # Project configuration
├── Makefile              # Development commands
└── README.md             # Documentation
```

## Questions?

Feel free to open an issue for any questions about contributing.

Thank you for contributing!
