"""
Async Support Module

Asynchronous sentiment analysis operations.
"""

import asyncio
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Callable, Awaitable
from concurrent.futures import ThreadPoolExecutor


@dataclass
class AsyncResult:
    """Result from async operation."""

    text: str
    result: Any
    success: bool
    error: Optional[str] = None


class AsyncAnalyzer:
    """Async wrapper for sentiment analysis."""

    def __init__(
        self,
        analyzer: Callable[[str], Any],
        max_concurrent: int = 10,
    ):
        """Initialize async analyzer."""
        self.analyzer = analyzer
        self.max_concurrent = max_concurrent
        self._semaphore: Optional[asyncio.Semaphore] = None
        self._executor = ThreadPoolExecutor(max_workers=max_concurrent)

    async def analyze(self, text: str) -> AsyncResult:
        """Analyze text asynchronously."""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)

        async with self._semaphore:
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self._executor,
                    self.analyzer,
                    text,
                )
                return AsyncResult(
                    text=text,
                    result=result,
                    success=True,
                )
            except Exception as e:
                return AsyncResult(
                    text=text,
                    result=None,
                    success=False,
                    error=str(e),
                )

    async def analyze_many(
        self,
        texts: List[str],
        callback: Optional[Callable[[AsyncResult], None]] = None,
    ) -> List[AsyncResult]:
        """Analyze multiple texts concurrently."""
        tasks = [self.analyze(text) for text in texts]
        results = []

        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)
            if callback:
                callback(result)

        return results

    async def analyze_stream(
        self,
        texts: List[str],
    ):
        """Stream results as they complete."""
        tasks = [self.analyze(text) for text in texts]
        for coro in asyncio.as_completed(tasks):
            yield await coro

    def close(self) -> None:
        """Close executor."""
        self._executor.shutdown(wait=False)


class AsyncBatchProcessor:
    """Async batch processor."""

    def __init__(
        self,
        processor: Callable[[str], Any],
        batch_size: int = 10,
    ):
        """Initialize processor."""
        self.processor = processor
        self.batch_size = batch_size
        self._analyzer = AsyncAnalyzer(processor)

    async def process_batch(self, texts: List[str]) -> List[AsyncResult]:
        """Process a batch of texts."""
        return await self._analyzer.analyze_many(texts)

    async def process_all(
        self,
        texts: List[str],
        on_batch_complete: Optional[Callable[[List[AsyncResult]], None]] = None,
    ) -> List[AsyncResult]:
        """Process all texts in batches."""
        all_results = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            results = await self.process_batch(batch)
            all_results.extend(results)
            if on_batch_complete:
                on_batch_complete(results)

        return all_results


async def analyze_async(
    text: str,
    analyzer: Callable[[str], Any],
) -> AsyncResult:
    """Analyze text asynchronously."""
    async_analyzer = AsyncAnalyzer(analyzer)
    try:
        return await async_analyzer.analyze(text)
    finally:
        async_analyzer.close()


async def analyze_many_async(
    texts: List[str],
    analyzer: Callable[[str], Any],
) -> List[AsyncResult]:
    """Analyze multiple texts asynchronously."""
    async_analyzer = AsyncAnalyzer(analyzer)
    try:
        return await async_analyzer.analyze_many(texts)
    finally:
        async_analyzer.close()


def run_async(coro: Awaitable[Any]) -> Any:
    """Run async coroutine synchronously."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)
