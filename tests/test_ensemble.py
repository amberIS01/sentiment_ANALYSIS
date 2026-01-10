"""Tests for ensemble module."""

import pytest
from chatbot.ensemble import (
    EnsemblePrediction,
    AverageEnsemble,
    WeightedEnsemble,
    VotingEnsemble,
    MaxConfidenceEnsemble,
    SentimentEnsemble,
    create_ensemble,
)


class TestAverageEnsemble:
    """Tests for AverageEnsemble."""

    def test_average(self):
        """Test averaging scores."""
        method = AverageEnsemble()
        result = method.combine([0.3, 0.5, 0.7], [1, 1, 1])
        
        assert result == pytest.approx(0.5)

    def test_empty(self):
        """Test empty scores."""
        method = AverageEnsemble()
        result = method.combine([], [])
        
        assert result == 0.0


class TestWeightedEnsemble:
    """Tests for WeightedEnsemble."""

    def test_weighted(self):
        """Test weighted average."""
        method = WeightedEnsemble()
        result = method.combine([0.0, 1.0], [1.0, 3.0])
        
        assert result == pytest.approx(0.75)

    def test_equal_weights(self):
        """Test equal weights."""
        method = WeightedEnsemble()
        result = method.combine([0.4, 0.6], [1.0, 1.0])
        
        assert result == pytest.approx(0.5)


class TestVotingEnsemble:
    """Tests for VotingEnsemble."""

    def test_positive_majority(self):
        """Test positive majority."""
        method = VotingEnsemble()
        result = method.combine([0.5, 0.6, -0.3], [1, 1, 1])
        
        assert result > 0

    def test_negative_majority(self):
        """Test negative majority."""
        method = VotingEnsemble()
        result = method.combine([-0.5, -0.6, 0.3], [1, 1, 1])
        
        assert result < 0


class TestMaxConfidenceEnsemble:
    """Tests for MaxConfidenceEnsemble."""

    def test_max_confidence(self):
        """Test selecting max confidence."""
        method = MaxConfidenceEnsemble()
        result = method.combine([0.3, -0.9, 0.5], [1, 1, 1])
        
        assert result == -0.9


class TestSentimentEnsemble:
    """Tests for SentimentEnsemble."""

    def test_add_analyzer(self):
        """Test adding analyzer."""
        ensemble = SentimentEnsemble()
        ensemble.add_analyzer(lambda x: 0.5, "test")
        
        result = ensemble.predict("hello")
        assert "test" in result.individual_scores

    def test_predict(self):
        """Test making prediction."""
        ensemble = SentimentEnsemble()
        ensemble.add_analyzer(lambda x: 0.5, "a")
        ensemble.add_analyzer(lambda x: 0.7, "b")
        
        result = ensemble.predict("hello")
        
        assert isinstance(result, EnsemblePrediction)
        assert result.final_score == pytest.approx(0.6)

    def test_set_method(self):
        """Test setting method."""
        ensemble = SentimentEnsemble()
        ensemble.set_method(MaxConfidenceEnsemble())
        ensemble.add_analyzer(lambda x: 0.3, "a")
        ensemble.add_analyzer(lambda x: 0.9, "b")
        
        result = ensemble.predict("test")
        
        assert result.final_score == 0.9

    def test_confidence(self):
        """Test confidence calculation."""
        ensemble = SentimentEnsemble()
        ensemble.add_analyzer(lambda x: 0.5, "a")
        ensemble.add_analyzer(lambda x: 0.5, "b")
        
        result = ensemble.predict("test")
        
        assert result.confidence == pytest.approx(1.0)


class TestCreateEnsemble:
    """Tests for create_ensemble function."""

    def test_create(self):
        """Test creating ensemble."""
        analyzers = [lambda x: 0.5, lambda x: 0.6]
        ensemble = create_ensemble(analyzers, method="average")
        
        result = ensemble.predict("test")
        assert result.final_score == pytest.approx(0.55)
