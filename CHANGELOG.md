# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Utility helpers module
- Type aliases for better type hints

## [1.1.0] - 2024-12-13

### Added
- Emotion detection module (joy, sadness, anger, fear, surprise, disgust, trust, anticipation)
- Conversation export functionality (JSON, CSV, text formats)
- Statistics tracking module with comprehensive metrics
- Configuration system with JSON file and environment variable support
- Input validation utilities
- Logging module with ChatLogger class
- Custom exceptions module
- Constants module for centralized configuration
- Makefile for common development commands
- GitHub Actions CI workflow
- Pre-commit configuration
- Contributing guidelines
- MIT License
- Example configuration file

### Changed
- Updated package exports in __init__.py
- Improved README with comprehensive documentation
- Bumped version to 1.1.0

## [1.0.0] - 2024-12-12

### Added
- Initial release
- VADER-based sentiment analysis
- Conversation history management
- Tier 1: Conversation-level sentiment analysis
- Tier 2: Statement-level sentiment analysis
- Mood trend detection
- Keyword-based response system
- Sentiment-aware responses
- Interactive CLI interface
- Demo mode
- Comprehensive test suite (90+ tests)

### Features
- Real-time sentiment evaluation for every message
- Overall conversation sentiment summary
- Positive, negative, neutral classification
- Compound sentiment scoring
- Message statistics tracking

[Unreleased]: https://github.com/sahil/sentiment-chatbot/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/sahil/sentiment-chatbot/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/sahil/sentiment-chatbot/releases/tag/v1.0.0
