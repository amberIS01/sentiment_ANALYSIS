"""
Batch Processing Module

Process multiple texts in batches.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


@dataclass
class BatchItem:
    """A single item in a batch."""

    id: str
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchResult:
    """Result for a single batch item."""

    item_id: str
    result: Any
    success: bool
    error: Optional[str] = None
    processing_time: float = 0.0


@dataclass
class BatchSummary:
    """Summary of batch processing."""

    total_items: int
    successful: int
    failed: int
    total_time: float
    avg_time_per_item: float


class BatchProcessor:
    """Process items in batches."""

    def __init__(
        self,
        processor: Callable[[str], Any],
        batch_size: int = 10,
        max_workers: int = 4,
    ):
        """Initialize batch processor."""
        self.processor = processor
        self.batch_size = batch_size
        self.max_workers = max_workers
        self._results: List[BatchResult] = []

    def process_single(self, item: BatchItem) -> BatchResult:
        """Process a single item."""
        start = time.time()
        try:
            result = self.processor(item.text)
            return BatchResult(
                item_id=item.id,
                result=result,
                success=True,
                processing_time=time.time() - start,
            )
        except Exception as e:
            return BatchResult(
                item_id=item.id,
                result=None,
                success=False,
                error=str(e),
                processing_time=time.time() - start,
            )

    def process_batch(
        self,
        items: List[BatchItem],
        parallel: bool = True,
    ) -> List[BatchResult]:
        """Process a batch of items."""
        if parallel:
            return self._process_parallel(items)
        return self._process_sequential(items)

    def _process_sequential(self, items: List[BatchItem]) -> List[BatchResult]:
        """Process items sequentially."""
        return [self.process_single(item) for item in items]

    def _process_parallel(self, items: List[BatchItem]) -> List[BatchResult]:
        """Process items in parallel."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.process_single, item): item
                for item in items
            }
            for future in as_completed(futures):
                results.append(future.result())
        return results

    def process_all(
        self,
        items: List[BatchItem],
        parallel: bool = True,
        callback: Optional[Callable[[BatchResult], None]] = None,
    ) -> List[BatchResult]:
        """Process all items in batches."""
        self._results = []
        
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_results = self.process_batch(batch, parallel)
            
            for result in batch_results:
                self._results.append(result)
                if callback:
                    callback(result)

        return self._results

    def get_summary(self) -> BatchSummary:
        """Get processing summary."""
        total = len(self._results)
        successful = sum(1 for r in self._results if r.success)
        total_time = sum(r.processing_time for r in self._results)

        return BatchSummary(
            total_items=total,
            successful=successful,
            failed=total - successful,
            total_time=total_time,
            avg_time_per_item=total_time / total if total > 0 else 0.0,
        )

    def iter_batches(self, items: List[BatchItem]) -> Iterator[List[BatchItem]]:
        """Iterate over items in batches."""
        for i in range(0, len(items), self.batch_size):
            yield items[i:i + self.batch_size]


def process_texts(
    texts: List[str],
    processor: Callable[[str], Any],
    batch_size: int = 10,
) -> List[BatchResult]:
    """Process a list of texts."""
    items = [
        BatchItem(id=f"item_{i}", text=text)
        for i, text in enumerate(texts)
    ]
    batch_processor = BatchProcessor(processor, batch_size)
    return batch_processor.process_all(items)
