"""Tests for batch module."""

import pytest
from chatbot.batch import (
    BatchItem,
    BatchResult,
    BatchProcessor,
    process_texts,
)


class TestBatchProcessor:
    """Tests for BatchProcessor."""

    def test_process_single(self):
        """Test processing single item."""
        processor = BatchProcessor(lambda x: x.upper())
        item = BatchItem(id="1", text="hello")
        
        result = processor.process_single(item)
        
        assert result.success is True
        assert result.result == "HELLO"

    def test_process_batch_sequential(self):
        """Test sequential batch processing."""
        processor = BatchProcessor(lambda x: len(x), batch_size=5)
        items = [BatchItem(id=str(i), text=f"text{i}") for i in range(3)]
        
        results = processor.process_batch(items, parallel=False)
        
        assert len(results) == 3
        assert all(r.success for r in results)

    def test_process_batch_parallel(self):
        """Test parallel batch processing."""
        processor = BatchProcessor(lambda x: len(x), batch_size=5)
        items = [BatchItem(id=str(i), text=f"text{i}") for i in range(3)]
        
        results = processor.process_batch(items, parallel=True)
        
        assert len(results) == 3

    def test_process_all(self):
        """Test processing all items."""
        processor = BatchProcessor(lambda x: x.upper(), batch_size=2)
        items = [BatchItem(id=str(i), text=f"t{i}") for i in range(5)]
        
        results = processor.process_all(items, parallel=False)
        
        assert len(results) == 5

    def test_get_summary(self):
        """Test getting summary."""
        processor = BatchProcessor(lambda x: x)
        items = [BatchItem(id="1", text="test")]
        processor.process_all(items)
        
        summary = processor.get_summary()
        
        assert summary.total_items == 1
        assert summary.successful == 1

    def test_error_handling(self):
        """Test error handling."""
        def fail(x):
            raise ValueError("Test error")
        
        processor = BatchProcessor(fail)
        item = BatchItem(id="1", text="test")
        
        result = processor.process_single(item)
        
        assert result.success is False
        assert "Test error" in result.error

    def test_callback(self):
        """Test callback on results."""
        processor = BatchProcessor(lambda x: x)
        items = [BatchItem(id="1", text="test")]
        results_collected = []
        
        processor.process_all(items, callback=results_collected.append)
        
        assert len(results_collected) == 1


class TestProcessTexts:
    """Tests for process_texts function."""

    def test_process_texts(self):
        """Test processing text list."""
        texts = ["hello", "world"]
        results = process_texts(texts, lambda x: x.upper())
        
        assert len(results) == 2
        assert results[0].result == "HELLO"
