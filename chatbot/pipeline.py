"""
Processing Pipeline Module

Create and execute processing pipelines.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Any, Optional, Callable, Dict, Generic, TypeVar
from enum import Enum


T = TypeVar('T')


class PipelineStage(ABC):
    """Base class for pipeline stages."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Stage name."""
        pass

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data through this stage."""
        pass


@dataclass
class StageResult:
    """Result from a pipeline stage."""

    stage_name: str
    input_data: Any
    output_data: Any
    success: bool
    error: Optional[str] = None


@dataclass
class PipelineResult:
    """Result from pipeline execution."""

    success: bool
    final_output: Any
    stage_results: List[StageResult]
    total_stages: int
    completed_stages: int


class Pipeline:
    """Processing pipeline."""

    def __init__(self, name: str = "pipeline"):
        """Initialize pipeline."""
        self.name = name
        self._stages: List[PipelineStage] = []

    def add_stage(self, stage: PipelineStage) -> "Pipeline":
        """Add a stage to the pipeline."""
        self._stages.append(stage)
        return self

    def add_function(
        self,
        name: str,
        func: Callable[[Any], Any],
    ) -> "Pipeline":
        """Add a function as a pipeline stage."""
        stage = FunctionStage(name, func)
        return self.add_stage(stage)

    def execute(self, data: Any) -> PipelineResult:
        """Execute the pipeline."""
        results: List[StageResult] = []
        current_data = data
        completed = 0

        for stage in self._stages:
            try:
                output = stage.process(current_data)
                results.append(StageResult(
                    stage_name=stage.name,
                    input_data=current_data,
                    output_data=output,
                    success=True,
                ))
                current_data = output
                completed += 1
            except Exception as e:
                results.append(StageResult(
                    stage_name=stage.name,
                    input_data=current_data,
                    output_data=None,
                    success=False,
                    error=str(e),
                ))
                return PipelineResult(
                    success=False,
                    final_output=None,
                    stage_results=results,
                    total_stages=len(self._stages),
                    completed_stages=completed,
                )

        return PipelineResult(
            success=True,
            final_output=current_data,
            stage_results=results,
            total_stages=len(self._stages),
            completed_stages=completed,
        )

    def __len__(self) -> int:
        return len(self._stages)


class FunctionStage(PipelineStage):
    """Pipeline stage wrapping a function."""

    def __init__(self, name: str, func: Callable[[Any], Any]):
        self._name = name
        self._func = func

    @property
    def name(self) -> str:
        return self._name

    def process(self, data: Any) -> Any:
        return self._func(data)


class SentimentPipeline(Pipeline):
    """Pre-configured sentiment analysis pipeline."""

    def __init__(self):
        super().__init__("sentiment_pipeline")
        from .preprocessor import TextPreprocessor
        from .sentiment import SentimentAnalyzer

        self._preprocessor = TextPreprocessor()
        self._analyzer = SentimentAnalyzer()

        self.add_function("clean", self._preprocessor.clean)
        self.add_function("analyze", lambda t: self._analyzer.analyze(t))


def create_pipeline(*functions: Callable) -> Pipeline:
    """Create a pipeline from functions."""
    pipeline = Pipeline()
    for i, func in enumerate(functions):
        name = getattr(func, '__name__', f'stage_{i}')
        pipeline.add_function(name, func)
    return pipeline
