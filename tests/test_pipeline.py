"""
Tests for the Pipeline Module.
"""

import pytest

from chatbot.pipeline import (
    Pipeline,
    PipelineStage,
    FunctionStage,
    PipelineResult,
    StageResult,
    SentimentPipeline,
    create_pipeline,
)


class TestFunctionStage:
    """Test FunctionStage class."""

    def test_creation(self):
        stage = FunctionStage("test", lambda x: x * 2)
        assert stage.name == "test"

    def test_process(self):
        stage = FunctionStage("double", lambda x: x * 2)
        result = stage.process(5)
        assert result == 10


class TestPipeline:
    """Test Pipeline class."""

    def test_initialization(self):
        pipeline = Pipeline()
        assert pipeline.name == "pipeline"

    def test_custom_name(self):
        pipeline = Pipeline(name="my_pipeline")
        assert pipeline.name == "my_pipeline"

    def test_add_stage(self):
        pipeline = Pipeline()
        stage = FunctionStage("test", lambda x: x)
        pipeline.add_stage(stage)
        assert len(pipeline) == 1

    def test_add_function(self):
        pipeline = Pipeline()
        pipeline.add_function("double", lambda x: x * 2)
        assert len(pipeline) == 1

    def test_execute_single_stage(self):
        pipeline = Pipeline()
        pipeline.add_function("double", lambda x: x * 2)
        result = pipeline.execute(5)
        assert result.success is True
        assert result.final_output == 10

    def test_execute_multiple_stages(self):
        pipeline = Pipeline()
        pipeline.add_function("double", lambda x: x * 2)
        pipeline.add_function("add_one", lambda x: x + 1)
        result = pipeline.execute(5)
        assert result.final_output == 11

    def test_execute_failure(self):
        pipeline = Pipeline()
        pipeline.add_function("fail", lambda x: 1 / 0)
        result = pipeline.execute(5)
        assert result.success is False
        assert result.completed_stages == 0

    def test_chaining(self):
        pipeline = (
            Pipeline()
            .add_function("a", lambda x: x + 1)
            .add_function("b", lambda x: x * 2)
        )
        assert len(pipeline) == 2


class TestPipelineResult:
    """Test PipelineResult dataclass."""

    def test_creation(self):
        result = PipelineResult(
            success=True,
            final_output=42,
            stage_results=[],
            total_stages=2,
            completed_stages=2,
        )
        assert result.success is True
        assert result.final_output == 42


class TestStageResult:
    """Test StageResult dataclass."""

    def test_creation(self):
        result = StageResult(
            stage_name="test",
            input_data=1,
            output_data=2,
            success=True,
        )
        assert result.stage_name == "test"


class TestCreatePipeline:
    """Test create_pipeline function."""

    def test_from_functions(self):
        def add_one(x):
            return x + 1

        def double(x):
            return x * 2

        pipeline = create_pipeline(add_one, double)
        result = pipeline.execute(5)
        assert result.final_output == 12
