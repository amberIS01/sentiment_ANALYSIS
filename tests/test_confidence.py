"""Tests for confidence module."""

import pytest
from chatbot.confidence import (
    ConfidenceResult,
    DistanceConfidence,
    ConsistencyConfidence,
    TextLengthConfidence,
    CompositeConfidence,
    calculate_confidence,
    get_confidence_level,
)


class TestDistanceConfidence:
    """Tests for DistanceConfidence."""

    def test_high_score(self):
        """Test high sentiment score."""
        calc = DistanceConfidence()
        result = calc.calculate(0.9)
        
        assert result == pytest.approx(0.9)

    def test_low_score(self):
        """Test low sentiment score."""
        calc = DistanceConfidence()
        result = calc.calculate(-0.8)
        
        assert result == pytest.approx(0.8)

    def test_neutral_score(self):
        """Test neutral score."""
        calc = DistanceConfidence()
        result = calc.calculate(0.0)
        
        assert result == 0.0


class TestConsistencyConfidence:
    """Tests for ConsistencyConfidence."""

    def test_consistent_scores(self):
        """Test consistent scores."""
        calc = ConsistencyConfidence()
        result = calc.calculate(0.5, scores=[0.5, 0.5, 0.5])
        
        assert result == pytest.approx(1.0)

    def test_inconsistent_scores(self):
        """Test inconsistent scores."""
        calc = ConsistencyConfidence()
        result = calc.calculate(0.5, scores=[0.1, 0.9, 0.2, 0.8])
        
        assert result < 1.0

    def test_no_scores(self):
        """Test with no scores."""
        calc = ConsistencyConfidence()
        result = calc.calculate(0.5)
        
        assert result == 0.5


class TestTextLengthConfidence:
    """Tests for TextLengthConfidence."""

    def test_optimal_length(self):
        """Test optimal length text."""
        calc = TextLengthConfidence(optimal_length=10)
        result = calc.calculate(0.5, text="one two three four five six seven eight nine ten")
        
        assert result == pytest.approx(1.0)

    def test_short_text(self):
        """Test short text."""
        calc = TextLengthConfidence(optimal_length=50)
        result = calc.calculate(0.5, text="short")
        
        assert result < 1.0

    def test_empty_text(self):
        """Test empty text."""
        calc = TextLengthConfidence()
        result = calc.calculate(0.5, text="")
        
        assert result == 0.0


class TestCompositeConfidence:
    """Tests for CompositeConfidence."""

    def test_combine_calculators(self):
        """Test combining calculators."""
        composite = CompositeConfidence()
        composite.add(DistanceConfidence(), 0.5)
        composite.add(TextLengthConfidence(), 0.5)
        
        result = composite.calculate(0.8, text="hello world test")
        
        assert isinstance(result, ConfidenceResult)
        assert 0 <= result.score <= 1

    def test_empty_composite(self):
        """Test empty composite."""
        composite = CompositeConfidence()
        result = composite.calculate(0.5)
        
        assert result.score == 0.5

    def test_confidence_levels(self):
        """Test confidence levels."""
        composite = CompositeConfidence()
        composite.add(DistanceConfidence(), 1.0)
        
        high = composite.calculate(0.9)
        assert high.level == "high"


class TestCalculateConfidence:
    """Tests for calculate_confidence function."""

    def test_calculate(self):
        """Test calculate function."""
        result = calculate_confidence(0.8, "This is a test sentence")
        
        assert 0 <= result <= 1


class TestGetConfidenceLevel:
    """Tests for get_confidence_level function."""

    def test_high_level(self):
        """Test high confidence level."""
        assert get_confidence_level(0.9) == "high"

    def test_medium_level(self):
        """Test medium confidence level."""
        assert get_confidence_level(0.6) == "medium"

    def test_low_level(self):
        """Test low confidence level."""
        assert get_confidence_level(0.3) == "low"
