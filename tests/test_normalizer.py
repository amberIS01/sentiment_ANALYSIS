"""Tests for normalizer module."""

import pytest
from chatbot.normalizer import (
    NormalizationResult,
    RangeNormalizer,
    ZScoreNormalizer,
    MinMaxNormalizer,
    normalize_score,
    normalize_scores,
)


class TestRangeNormalizer:
    """Tests for RangeNormalizer."""

    def test_normalize_default(self):
        """Test default normalization."""
        normalizer = RangeNormalizer()
        result = normalizer.normalize(0.0)
        assert result == pytest.approx(0.5)

    def test_normalize_min(self):
        """Test normalizing min value."""
        normalizer = RangeNormalizer()
        result = normalizer.normalize(-1.0)
        assert result == pytest.approx(0.0)

    def test_normalize_max(self):
        """Test normalizing max value."""
        normalizer = RangeNormalizer()
        result = normalizer.normalize(1.0)
        assert result == pytest.approx(1.0)

    def test_denormalize(self):
        """Test denormalization."""
        normalizer = RangeNormalizer()
        result = normalizer.denormalize(0.5)
        assert result == pytest.approx(0.0)


class TestZScoreNormalizer:
    """Tests for ZScoreNormalizer."""

    def test_normalize(self):
        """Test z-score normalization."""
        normalizer = ZScoreNormalizer(mean=50, std=10)
        result = normalizer.normalize(60)
        assert result == pytest.approx(1.0)

    def test_fit(self):
        """Test fitting to data."""
        normalizer = ZScoreNormalizer()
        normalizer.fit([10, 20, 30, 40, 50])
        assert normalizer.mean == pytest.approx(30.0)


class TestMinMaxNormalizer:
    """Tests for MinMaxNormalizer."""

    def test_normalize(self):
        """Test min-max normalization."""
        normalizer = MinMaxNormalizer()
        normalizer.fit([0, 50, 100])
        
        assert normalizer.normalize(50) == pytest.approx(0.5)

    def test_custom_range(self):
        """Test custom output range."""
        normalizer = MinMaxNormalizer(min_val=0, max_val=10)
        normalizer.fit([0, 100])
        
        assert normalizer.normalize(50) == pytest.approx(5.0)


class TestNormalizeScore:
    """Tests for normalize_score function."""

    def test_normalize(self):
        """Test normalize function."""
        result = normalize_score(0.0, (-1, 1), (0, 100))
        assert result == pytest.approx(50.0)


class TestNormalizeScores:
    """Tests for normalize_scores function."""

    def test_normalize_list(self):
        """Test normalizing list."""
        scores = [0, 50, 100]
        result = normalize_scores(scores)
        
        assert result[0] == pytest.approx(0.0)
        assert result[2] == pytest.approx(1.0)
