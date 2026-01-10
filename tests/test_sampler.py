"""Tests for sampler module."""

import pytest
from chatbot.sampler import (
    Sample,
    SampleResult,
    TextSampler,
    sample_texts,
)


class TestTextSampler:
    """Tests for TextSampler."""

    def test_random_sample(self):
        """Test random sampling."""
        sampler = TextSampler(seed=42)
        texts = ["a", "b", "c", "d", "e"]
        
        result = sampler.random_sample(texts, 3)
        
        assert result.sample_count == 3
        assert result.total_count == 5

    def test_random_sample_larger_n(self):
        """Test sampling more than available."""
        sampler = TextSampler()
        texts = ["a", "b"]
        
        result = sampler.random_sample(texts, 10)
        
        assert result.sample_count == 2

    def test_stratified_sample(self):
        """Test stratified sampling."""
        sampler = TextSampler(seed=42)
        texts = ["short", "medium text", "a very long text here"]
        
        result = sampler.stratified_sample(
            texts, 3,
            strata_fn=lambda x: "short" if len(x) < 10 else "long"
        )
        
        assert result.sample_count <= 3

    def test_weighted_sample(self):
        """Test weighted sampling."""
        sampler = TextSampler(seed=42)
        texts = ["a", "b", "c"]
        weights = [1.0, 2.0, 3.0]
        
        result = sampler.weighted_sample(texts, weights, 2)
        
        assert result.sample_count == 2

    def test_systematic_sample(self):
        """Test systematic sampling."""
        sampler = TextSampler(seed=42)
        texts = [f"text{i}" for i in range(10)]
        
        result = sampler.systematic_sample(texts, 3)
        
        assert result.sample_count == 3

    def test_sample_result_structure(self):
        """Test sample result structure."""
        sampler = TextSampler()
        texts = ["hello", "world"]
        
        result = sampler.random_sample(texts, 1)
        
        assert len(result.samples) == 1
        assert isinstance(result.samples[0], Sample)
        assert result.samples[0].text in texts


class TestSampleTexts:
    """Tests for sample_texts function."""

    def test_random_method(self):
        """Test random sampling method."""
        texts = ["a", "b", "c", "d"]
        result = sample_texts(texts, 2, method="random")
        
        assert len(result) == 2

    def test_systematic_method(self):
        """Test systematic method."""
        texts = ["a", "b", "c", "d", "e"]
        result = sample_texts(texts, 2, method="systematic")
        
        assert len(result) == 2
