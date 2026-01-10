"""Tests for postprocessing module."""

import pytest
from chatbot.postprocessing import (
    PostprocessResult,
    ClampScoreStep,
    RoundScoreStep,
    NeutralizeSmallStep,
    ScaleScoreStep,
    ContextAdjustStep,
    PostprocessPipeline,
    create_default_pipeline,
    postprocess_score,
)


class TestClampScoreStep:
    """Tests for ClampScoreStep."""

    def test_clamp_high(self):
        """Test clamping high values."""
        step = ClampScoreStep()
        result = step.process(1.5, "", {})
        
        assert result == 1.0

    def test_clamp_low(self):
        """Test clamping low values."""
        step = ClampScoreStep()
        result = step.process(-1.5, "", {})
        
        assert result == -1.0

    def test_no_clamp(self):
        """Test value within range."""
        step = ClampScoreStep()
        result = step.process(0.5, "", {})
        
        assert result == 0.5


class TestRoundScoreStep:
    """Tests for RoundScoreStep."""

    def test_round(self):
        """Test rounding."""
        step = RoundScoreStep(decimals=2)
        result = step.process(0.12345, "", {})
        
        assert result == 0.12


class TestNeutralizeSmallStep:
    """Tests for NeutralizeSmallStep."""

    def test_neutralize(self):
        """Test neutralizing small values."""
        step = NeutralizeSmallStep(threshold=0.1)
        result = step.process(0.05, "", {})
        
        assert result == 0.0

    def test_keep_large(self):
        """Test keeping large values."""
        step = NeutralizeSmallStep(threshold=0.1)
        result = step.process(0.5, "", {})
        
        assert result == 0.5


class TestScaleScoreStep:
    """Tests for ScaleScoreStep."""

    def test_scale(self):
        """Test scaling."""
        step = ScaleScoreStep(factor=2.0)
        result = step.process(0.3, "", {})
        
        assert result == pytest.approx(0.6)


class TestContextAdjustStep:
    """Tests for ContextAdjustStep."""

    def test_adjust(self):
        """Test context adjustment."""
        step = ContextAdjustStep({"urgent": 0.1})
        result = step.process(0.5, "", {"urgent": True})
        
        assert result == pytest.approx(0.6)

    def test_no_adjust(self):
        """Test no adjustment."""
        step = ContextAdjustStep({"urgent": 0.1})
        result = step.process(0.5, "", {})
        
        assert result == 0.5


class TestPostprocessPipeline:
    """Tests for PostprocessPipeline."""

    def test_add_step(self):
        """Test adding step."""
        pipeline = PostprocessPipeline()
        pipeline.add_step(RoundScoreStep(2))
        
        result = pipeline.process(0.12345)
        assert result.final_score == 0.12

    def test_chain_steps(self):
        """Test chaining steps."""
        pipeline = (
            PostprocessPipeline()
            .add_step(ScaleScoreStep(2.0))
            .add_step(ClampScoreStep())
        )
        
        result = pipeline.process(0.8)
        assert result.final_score == 1.0

    def test_result_structure(self):
        """Test result structure."""
        pipeline = PostprocessPipeline()
        pipeline.add_step(RoundScoreStep(2))
        
        result = pipeline.process(0.12345)
        
        assert isinstance(result, PostprocessResult)
        assert result.original_score == 0.12345


class TestCreateDefaultPipeline:
    """Tests for create_default_pipeline."""

    def test_create(self):
        """Test creating default pipeline."""
        pipeline = create_default_pipeline()
        result = pipeline.process(0.01234)
        
        assert result.final_score == 0.0  # Neutralized


class TestPostprocessScore:
    """Tests for postprocess_score function."""

    def test_postprocess(self):
        """Test postprocessing."""
        result = postprocess_score(1.5)
        
        assert result == 1.0  # Clamped
