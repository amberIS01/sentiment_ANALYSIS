"""Tests for scorer module."""

import pytest
from chatbot.scorer import (
    ScoringStrategy,
    ScorerConfig,
    SentimentScorer,
    LinearScorer,
    ExponentialScorer,
    WeightedScorer,
    create_scorer,
)


class TestLinearScorer:
    """Tests for LinearScorer."""

    def test_score(self):
        """Test linear scoring."""
        scorer = LinearScorer()
        result = scorer.score(0.5)
        
        assert result == pytest.approx(0.5)

    def test_score_with_scale(self):
        """Test with scale factor."""
        scorer = LinearScorer(scale=2.0)
        result = scorer.score(0.5)
        
        assert result == pytest.approx(1.0)

    def test_score_clipping(self):
        """Test score clipping."""
        scorer = LinearScorer(scale=3.0)
        result = scorer.score(0.5)
        
        assert result <= 1.0


class TestExponentialScorer:
    """Tests for ExponentialScorer."""

    def test_score_positive(self):
        """Test positive score."""
        scorer = ExponentialScorer()
        result = scorer.score(0.5)
        
        assert result > 0.5

    def test_score_negative(self):
        """Test negative score."""
        scorer = ExponentialScorer()
        result = scorer.score(-0.5)
        
        assert result < -0.5

    def test_score_zero(self):
        """Test zero score."""
        scorer = ExponentialScorer()
        result = scorer.score(0.0)
        
        assert result == pytest.approx(0.0)


class TestWeightedScorer:
    """Tests for WeightedScorer."""

    def test_score(self):
        """Test weighted scoring."""
        scorer = WeightedScorer()
        result = scorer.score(0.5)
        
        assert isinstance(result, float)

    def test_custom_weights(self):
        """Test with custom weights."""
        scorer = WeightedScorer(
            positive_weight=1.5,
            negative_weight=0.5,
        )
        
        pos = scorer.score(0.5)
        neg = scorer.score(-0.5)
        
        assert abs(pos) > abs(neg)


class TestSentimentScorer:
    """Tests for SentimentScorer."""

    def test_default_strategy(self):
        """Test default strategy."""
        scorer = SentimentScorer()
        result = scorer.score(0.5)
        
        assert isinstance(result, float)

    def test_set_strategy(self):
        """Test setting strategy."""
        scorer = SentimentScorer()
        scorer.set_strategy(ScoringStrategy.EXPONENTIAL)
        
        result = scorer.score(0.5)
        assert result > 0.5

    def test_score_many(self):
        """Test scoring multiple values."""
        scorer = SentimentScorer()
        results = scorer.score_many([0.3, 0.5, 0.7])
        
        assert len(results) == 3


class TestCreateScorer:
    """Tests for create_scorer function."""

    def test_create_linear(self):
        """Test creating linear scorer."""
        scorer = create_scorer(ScoringStrategy.LINEAR)
        
        assert isinstance(scorer, LinearScorer)

    def test_create_exponential(self):
        """Test creating exponential scorer."""
        scorer = create_scorer(ScoringStrategy.EXPONENTIAL)
        
        assert isinstance(scorer, ExponentialScorer)
