#!/usr/bin/env python3
"""
Setup script for Sentiment Analysis Chatbot.

This provides backward compatibility for pip install.
The main configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

# Read requirements
requirements = [
    "nltk>=3.8.1",
]

dev_requirements = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.5.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
    "pre-commit>=3.4.0",
]

setup(
    name="sentiment-chatbot",
    version="1.1.0",
    author="Sahil",
    description="A chatbot with conversation-level and statement-level sentiment analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sahil/sentiment-chatbot",
    project_urls={
        "Bug Tracker": "https://github.com/sahil/sentiment-chatbot/issues",
        "Documentation": "https://github.com/sahil/sentiment-chatbot#readme",
    },
    license="MIT",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sentiment-chatbot=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords=[
        "chatbot",
        "sentiment-analysis",
        "nlp",
        "vader",
        "natural-language-processing",
    ],
    include_package_data=True,
    zip_safe=False,
)
