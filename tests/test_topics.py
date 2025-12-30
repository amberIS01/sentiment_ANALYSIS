"""Tests for topics module."""

import pytest
from chatbot.topics import (
    Topic,
    TopicResult,
    TopicExtractor,
    extract_topics,
    get_topic_keywords,
)


class TestTopicExtractor:
    """Tests for TopicExtractor."""

    def test_extract_weather(self):
        """Test extracting weather topic."""
        extractor = TopicExtractor()
        result = extractor.extract("The weather is sunny today")
        
        assert Topic.WEATHER in [t.topic for t in result.topics]

    def test_extract_technology(self):
        """Test extracting technology topic."""
        extractor = TopicExtractor()
        result = extractor.extract("I love programming and software")
        
        assert Topic.TECHNOLOGY in [t.topic for t in result.topics]

    def test_extract_sports(self):
        """Test extracting sports topic."""
        extractor = TopicExtractor()
        result = extractor.extract("The football game was exciting")
        
        assert Topic.SPORTS in [t.topic for t in result.topics]

    def test_extract_health(self):
        """Test extracting health topic."""
        extractor = TopicExtractor()
        result = extractor.extract("I need to see a doctor about my health")
        
        assert Topic.HEALTH in [t.topic for t in result.topics]

    def test_multiple_topics(self):
        """Test extracting multiple topics."""
        extractor = TopicExtractor()
        result = extractor.extract("The tech conference discussed programming and business")
        
        assert len(result.topics) >= 2

    def test_no_topics(self):
        """Test text with no clear topic."""
        extractor = TopicExtractor()
        result = extractor.extract("asdfghjkl")
        
        assert len(result.topics) == 0

    def test_confidence_scores(self):
        """Test confidence scores."""
        extractor = TopicExtractor()
        result = extractor.extract("Software development is great")
        
        for topic in result.topics:
            assert 0 <= topic.confidence <= 1

    def test_add_custom_topic(self):
        """Test adding custom topic keywords."""
        extractor = TopicExtractor()
        extractor.add_keywords(Topic.ENTERTAINMENT, ["movie", "film", "cinema"])
        
        result = extractor.extract("I watched a great movie")
        
        assert Topic.ENTERTAINMENT in [t.topic for t in result.topics]

    def test_extract_many(self):
        """Test extracting from multiple texts."""
        extractor = TopicExtractor()
        texts = ["Weather is nice", "Tech is cool", "Sports are fun"]
        
        results = extractor.extract_many(texts)
        
        assert len(results) == 3


class TestExtractTopics:
    """Tests for extract_topics function."""

    def test_extract(self):
        """Test extract function."""
        result = extract_topics("Technology and business news")
        
        assert isinstance(result, TopicResult)


class TestGetTopicKeywords:
    """Tests for get_topic_keywords function."""

    def test_get_technology(self):
        """Test getting technology keywords."""
        keywords = get_topic_keywords(Topic.TECHNOLOGY)
        
        assert len(keywords) > 0

    def test_get_weather(self):
        """Test getting weather keywords."""
        keywords = get_topic_keywords(Topic.WEATHER)
        
        assert "weather" in keywords or "rain" in keywords
