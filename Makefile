.PHONY: help install install-dev test test-cov lint format clean run demo build

# Default target
help:
	@echo "Sentiment Analysis Chatbot - Available Commands"
	@echo "================================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install production dependencies"
	@echo "  make install-dev  Install development dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run          Run interactive chat"
	@echo "  make demo         Run demonstration mode"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run all tests"
	@echo "  make test-cov     Run tests with coverage report"
	@echo "  make test-verbose Run tests with verbose output"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Run linters (flake8, mypy)"
	@echo "  make format       Format code (black, isort)"
	@echo "  make check        Run all checks without modifying"
	@echo ""
	@echo "Build:"
	@echo "  make build        Build distribution packages"
	@echo "  make clean        Remove build artifacts"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	python -c "import nltk; nltk.download('vader_lexicon', quiet=True)"

# Running the application
run:
	python main.py

demo:
	python main.py --demo

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=chatbot --cov-report=html --cov-report=term-missing

test-verbose:
	pytest tests/ -vv --tb=long

test-quick:
	pytest tests/ -x -q

# Linting and formatting
lint:
	@echo "Running flake8..."
	flake8 chatbot/ tests/ main.py --max-line-length=100 --ignore=E501,W503
	@echo "Running mypy..."
	mypy chatbot/ --ignore-missing-imports

format:
	@echo "Running isort..."
	isort chatbot/ tests/ main.py
	@echo "Running black..."
	black chatbot/ tests/ main.py --line-length=100

check:
	@echo "Checking code format..."
	black chatbot/ tests/ main.py --check --line-length=100
	isort chatbot/ tests/ main.py --check-only
	@echo "Running linters..."
	flake8 chatbot/ tests/ main.py --max-line-length=100 --ignore=E501,W503

# Building
build: clean
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Development helpers
setup-hooks:
	pre-commit install

nltk-data:
	python -c "import nltk; nltk.download('vader_lexicon')"

# Docker (if needed in future)
docker-build:
	docker build -t sentiment-chatbot .

docker-run:
	docker run -it sentiment-chatbot

# Version info
version:
	python main.py --version
