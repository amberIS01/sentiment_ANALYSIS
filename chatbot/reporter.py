"""
Reporter Module

Generate sentiment analysis reports.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class ReportFormat(Enum):
    """Report formats."""

    TEXT = "text"
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"


@dataclass
class ReportSection:
    """A section of a report."""

    title: str
    content: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SentimentReport:
    """A complete sentiment report."""

    title: str
    created_at: datetime
    sections: List[ReportSection]
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReportBuilder:
    """Build sentiment reports."""

    def __init__(self, title: str = "Sentiment Analysis Report"):
        """Initialize builder."""
        self.title = title
        self._sections: List[ReportSection] = []
        self._metadata: Dict[str, Any] = {}

    def add_section(
        self,
        title: str,
        content: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> "ReportBuilder":
        """Add a section."""
        self._sections.append(ReportSection(
            title=title,
            content=content,
            data=data or {},
        ))
        return self

    def add_metadata(self, key: str, value: Any) -> "ReportBuilder":
        """Add metadata."""
        self._metadata[key] = value
        return self

    def build(self, summary: str = "") -> SentimentReport:
        """Build the report."""
        return SentimentReport(
            title=self.title,
            created_at=datetime.now(),
            sections=self._sections.copy(),
            summary=summary,
            metadata=self._metadata.copy(),
        )


class ReportFormatter:
    """Format reports to different outputs."""

    def format(
        self,
        report: SentimentReport,
        fmt: ReportFormat = ReportFormat.TEXT,
    ) -> str:
        """Format a report."""
        if fmt == ReportFormat.TEXT:
            return self._format_text(report)
        elif fmt == ReportFormat.MARKDOWN:
            return self._format_markdown(report)
        elif fmt == ReportFormat.HTML:
            return self._format_html(report)
        elif fmt == ReportFormat.JSON:
            return self._format_json(report)
        return self._format_text(report)

    def _format_text(self, report: SentimentReport) -> str:
        """Format as plain text."""
        lines = [
            "=" * 50,
            report.title,
            "=" * 50,
            f"Generated: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]

        for section in report.sections:
            lines.append(f"--- {section.title} ---")
            lines.append(section.content)
            lines.append("")

        if report.summary:
            lines.append("Summary:")
            lines.append(report.summary)

        return "\n".join(lines)

    def _format_markdown(self, report: SentimentReport) -> str:
        """Format as markdown."""
        lines = [
            f"# {report.title}",
            f"*Generated: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}*",
            "",
        ]

        for section in report.sections:
            lines.append(f"## {section.title}")
            lines.append(section.content)
            lines.append("")

        if report.summary:
            lines.append("## Summary")
            lines.append(report.summary)

        return "\n".join(lines)

    def _format_html(self, report: SentimentReport) -> str:
        """Format as HTML."""
        sections_html = ""
        for section in report.sections:
            sections_html += f"<h2>{section.title}</h2><p>{section.content}</p>"

        return f"""
<!DOCTYPE html>
<html>
<head><title>{report.title}</title></head>
<body>
<h1>{report.title}</h1>
<p><em>Generated: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}</em></p>
{sections_html}
<h2>Summary</h2>
<p>{report.summary}</p>
</body>
</html>
"""

    def _format_json(self, report: SentimentReport) -> str:
        """Format as JSON."""
        import json
        return json.dumps({
            "title": report.title,
            "created_at": report.created_at.isoformat(),
            "sections": [
                {"title": s.title, "content": s.content, "data": s.data}
                for s in report.sections
            ],
            "summary": report.summary,
            "metadata": report.metadata,
        }, indent=2)


def create_report(
    title: str,
    sections: List[Dict[str, str]],
    summary: str = "",
) -> SentimentReport:
    """Create a report from sections."""
    builder = ReportBuilder(title)
    for section in sections:
        builder.add_section(
            title=section.get("title", ""),
            content=section.get("content", ""),
        )
    return builder.build(summary)
