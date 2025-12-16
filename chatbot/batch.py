"""
Batch Processing Module

Process multiple texts efficiently.
"""

from dataclasses import dataclass
from typing import List, Iterator, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from .sentiment import SentimentAnalyzer, SentimentResult


@dataclass
class BatchResult:
    """Result from batch processing."""

    text: str
    result: SentimentResult
    processing_time: float
    index: int


@dataclass
class BatchSummary:
    """Summary of batch processing."""

    total_items: int
    successful: int
    failed: int
    total_time: float
    avg_time_per_item: float
    positive_count: int
    negative_count: int
    neutral_count: int


class BatchProcessor:
    """Process texts in batches."""

    def __init__(
        self,
        batch_size: int = 100,
        max_workers: int = 4,
    ):
        """Initialize batch processor.

        Args:
            batch_size: Number of items per batch
            max_workers: Maximum concurrent workers
        """
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.analyzer = SentimentAnalyzer()

    def process(
        self,
        texts: List[str],
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> List[BatchResult]:
        """Process a list of texts."""
        results = []
        total = len(texts)

        for i, text in enumerate(texts):
            start = time.perf_counter()
            sentiment = self.analyzer.analyze(text)
            elapsed = time.perf_counter() - start

            results.append(BatchResult(
                text=text,
                result=sentiment,
                processing_time=elapsed,
                index=i,
            ))

            if progress_callback:
                progress_callback(i + 1, total)

        return results

    def process_parallel(
        self,
        texts: List[str],
    ) -> List[BatchResult]:
        """Process texts in parallel using thread pool."""
        results = [None] * len(texts)

        def process_one(args):
            index, text = args
            start = time.perf_counter()
            sentiment = self.analyzer.analyze(text)
            elapsed = time.perf_counter() - start
            return BatchResult(
                text=text,
                result=sentiment,
                processing_time=elapsed,
                index=index,
            )

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(process_one, (i, text)): i
                for i, text in enumerate(texts)
            }

            for future in as_completed(futures):
                result = future.result()
                results[result.index] = result

        return results

    def process_batches(
        self,
        texts: List[str],
    ) -> Iterator[List[BatchResult]]:
        """Process texts in batches, yielding results per batch."""
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            yield self.process(batch)

    def get_summary(self, results: List[BatchResult]) -> BatchSummary:
        """Get summary of batch results."""
        total = len(results)
        successful = sum(1 for r in results if r.result is not None)
        total_time = sum(r.processing_time for r in results)

        positive = sum(
            1 for r in results
            if r.result and r.result.label.value == "positive"
        )
        negative = sum(
            1 for r in results
            if r.result and r.result.label.value == "negative"
        )
        neutral = sum(
            1 for r in results
            if r.result and r.result.label.value == "neutral"
        )

        return BatchSummary(
            total_items=total,
            successful=successful,
            failed=total - successful,
            total_time=total_time,
            avg_time_per_item=total_time / total if total > 0 else 0,
            positive_count=positive,
            negative_count=negative,
            neutral_count=neutral,
        )


def process_batch(texts: List[str]) -> List[BatchResult]:
    """Process a batch of texts."""
    processor = BatchProcessor()
    return processor.process(texts)
