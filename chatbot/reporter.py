"""
Sentiment Reporter Module

Generate reports from sentiment analysis data.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
import json


@dataclass
class ReportSection:
    """A section of a report."""

    title: str
    content: str
    data: Optional[Dict[str, Any]] = None


@dataclass
class SentimentReport:
    """A complete sentiment analysis report."""

    title: str
    generated_at: datetime
    sections: List[ReportSection]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "title": self.title,
            "generated_at": self.generated_at.isoformat(),
            "sections": [
                {
                    "title": s.title,
                    "content": s.content,
                    "data": s.data,
                }
                for s in self.sections
            ],
            "metadata": self.metadata,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_text(self) -> str:
        """Convert report to plain text."""
        lines = [
            "=" * 60,
            self.title,
            f"Generated: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 60,
            "",
        ]

        for section in self.sections:
            lines.append(f"## {section.title}")
            lines.append("-" * 40)
            lines.append(section.content)
            lines.append("")

        return "\n".join(lines)


class SentimentReporter:
    """Generate sentiment analysis reports."""

    def __init__(self, title: str = "Sentiment Analysis Report"):
        """Initialize reporter."""
        self.title = title
        self._sections: List[ReportSection] = []
        self._metadata: Dict[str, Any] = {}

    def add_section(
        self,
        title: str,
        content: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> "SentimentReporter":
        """Add a section to the report."""
        self._sections.append(ReportSection(
            title=title,
            content=content,
            data=data,
        ))
        return self

    def add_summary(
        self,
        total_analyzed: int,
        avg_sentiment: float,
        positive_pct: float,
        negative_pct: float,
    ) -> "SentimentReporter":
        """Add summary section."""
        content = (
            f"Total items analyzed: {total_analyzed}\n"
            f"Average sentiment score: {avg_sentiment:.3f}\n"
            f"Positive: {positive_pct:.1%}\n"
            f"Negative: {negative_pct:.1%}\n"
            f"Neutral: {1 - positive_pct - negative_pct:.1%}"
        )
        return self.add_section(
            "Summary",
            content,
            {
                "total": total_analyzed,
                "avg_sentiment": avg_sentiment,
                "positive_pct": positive_pct,
                "negative_pct": negative_pct,
            },
        )

    def add_distribution(
        self,
        distribution: Dict[str, int],
    ) -> "SentimentReporter":
        """Add sentiment distribution section."""
        total = sum(distribution.values())
        lines = []
        for label, count in distribution.items():
            pct = (count / total * 100) if total > 0 else 0
            bar = "#" * int(pct / 5)
            lines.append(f"{label:10}: {count:4} ({pct:5.1f}%) {bar}")

        return self.add_section(
            "Sentiment Distribution",
            "\n".join(lines),
            distribution,
        )

    def add_highlights(
        self,
        most_positive: str,
        most_negative: str,
    ) -> "SentimentReporter":
        """Add highlights section."""
        content = (
            f"Most Positive:\n  \"{most_positive[:100]}...\"\n\n"
            f"Most Negative:\n  \"{most_negative[:100]}...\""
        )
        return self.add_section("Highlights", content)

    def add_metadata(self, key: str, value: Any) -> "SentimentReporter":
        """Add metadata to report."""
        self._metadata[key] = value
        return self

    def generate(self) -> SentimentReport:
        """Generate the final report."""
        return SentimentReport(
            title=self.title,
            generated_at=datetime.now(),
            sections=self._sections.copy(),
            metadata=self._metadata.copy(),
        )

    def reset(self) -> "SentimentReporter":
        """Reset the reporter for a new report."""
        self._sections.clear()
        self._metadata.clear()
        return self


def create_report(
    title: str,
    total: int,
    avg_sentiment: float,
    distribution: Dict[str, int],
) -> SentimentReport:
    """Create a simple sentiment report."""
    total_count = sum(distribution.values())
    positive_pct = distribution.get("positive", 0) / total_count if total_count else 0
    negative_pct = distribution.get("negative", 0) / total_count if total_count else 0

    return (
        SentimentReporter(title)
        .add_summary(total, avg_sentiment, positive_pct, negative_pct)
        .add_distribution(distribution)
        .generate()
    )
