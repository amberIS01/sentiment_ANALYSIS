"""
Tests for the Batch Module.
"""

import pytest

from chatbot.batch import (
    BatchProcessor,
    BatchResult,
    BatchSummary,
    process_batch,
)


class TestBatchResult:
    """Test BatchResult dataclass."""

    def test_creation(self):
        from chatbot.sentiment import SentimentResult, SentimentLabel
        result = BatchResult(
            text="test",
            result=SentimentResult(
                positive=0.5,
                negative=0.1,
                neutral=0.4,
                compound=0.5,
                label=SentimentLabel.POSITIVE,
            ),
            processing_time=0.01,
            index=0,
        )
        assert result.text == "test"
        assert result.index == 0


class TestBatchSummary:
    """Test BatchSummary dataclass."""

    def test_creation(self):
        summary = BatchSummary(
            total_items=10,
            successful=10,
            failed=0,
            total_time=1.0,
            avg_time_per_item=0.1,
            positive_count=5,
            negative_count=3,
            neutral_count=2,
        )
        assert summary.total_items == 10
        assert summary.positive_count == 5


class TestBatchProcessor:
    """Test BatchProcessor class."""

    def test_initialization(self):
        processor = BatchProcessor()
        assert processor.batch_size == 100
        assert processor.max_workers == 4

    def test_custom_settings(self):
        processor = BatchProcessor(batch_size=50, max_workers=2)
        assert processor.batch_size == 50
        assert processor.max_workers == 2

    def test_process(self):
        processor = BatchProcessor()
        texts = ["I am happy", "I am sad", "This is okay"]
        results = processor.process(texts)
        assert len(results) == 3
        assert all(isinstance(r, BatchResult) for r in results)

    def test_process_with_callback(self):
        processor = BatchProcessor()
        progress = []

        def callback(current, total):
            progress.append((current, total))

        texts = ["Text 1", "Text 2", "Text 3"]
        processor.process(texts, progress_callback=callback)
        assert len(progress) == 3

    def test_process_parallel(self):
        processor = BatchProcessor(max_workers=2)
        texts = ["Happy text", "Sad text", "Neutral text"]
        results = processor.process_parallel(texts)
        assert len(results) == 3

    def test_process_batches(self):
        processor = BatchProcessor(batch_size=2)
        texts = ["Text 1", "Text 2", "Text 3", "Text 4", "Text 5"]
        batches = list(processor.process_batches(texts))
        assert len(batches) == 3  # 2, 2, 1

    def test_get_summary(self):
        processor = BatchProcessor()
        texts = ["I love this!", "I hate this", "This is fine"]
        results = processor.process(texts)
        summary = processor.get_summary(results)
        assert isinstance(summary, BatchSummary)
        assert summary.total_items == 3


class TestProcessBatch:
    """Test process_batch function."""

    def test_basic_processing(self):
        texts = ["Good day", "Bad day"]
        results = process_batch(texts)
        assert len(results) == 2
