"""
Tests for the Reporter Module.
"""

import pytest
import json

from chatbot.reporter import (
    SentimentReporter,
    SentimentReport,
    ReportSection,
    create_report,
)


class TestReportSection:
    """Test ReportSection dataclass."""

    def test_creation(self):
        section = ReportSection(
            title="Summary",
            content="This is the summary",
        )
        assert section.title == "Summary"

    def test_with_data(self):
        section = ReportSection(
            title="Stats",
            content="Statistics here",
            data={"count": 10},
        )
        assert section.data["count"] == 10


class TestSentimentReport:
    """Test SentimentReport dataclass."""

    def test_to_dict(self):
        from datetime import datetime
        report = SentimentReport(
            title="Test Report",
            generated_at=datetime.now(),
            sections=[],
            metadata={},
        )
        result = report.to_dict()
        assert "title" in result
        assert "generated_at" in result

    def test_to_json(self):
        from datetime import datetime
        report = SentimentReport(
            title="Test Report",
            generated_at=datetime.now(),
            sections=[],
            metadata={},
        )
        json_str = report.to_json()
        data = json.loads(json_str)
        assert data["title"] == "Test Report"

    def test_to_text(self):
        from datetime import datetime
        report = SentimentReport(
            title="Test Report",
            generated_at=datetime.now(),
            sections=[
                ReportSection("Section 1", "Content 1"),
            ],
            metadata={},
        )
        text = report.to_text()
        assert "Test Report" in text
        assert "Section 1" in text


class TestSentimentReporter:
    """Test SentimentReporter class."""

    def test_initialization(self):
        reporter = SentimentReporter()
        assert reporter.title == "Sentiment Analysis Report"

    def test_custom_title(self):
        reporter = SentimentReporter("Custom Report")
        assert reporter.title == "Custom Report"

    def test_add_section(self):
        reporter = SentimentReporter()
        reporter.add_section("Test", "Content")
        report = reporter.generate()
        assert len(report.sections) == 1

    def test_add_summary(self):
        reporter = SentimentReporter()
        reporter.add_summary(
            total_analyzed=100,
            avg_sentiment=0.5,
            positive_pct=0.6,
            negative_pct=0.2,
        )
        report = reporter.generate()
        assert any(s.title == "Summary" for s in report.sections)

    def test_add_distribution(self):
        reporter = SentimentReporter()
        reporter.add_distribution({
            "positive": 60,
            "negative": 20,
            "neutral": 20,
        })
        report = reporter.generate()
        assert any(s.title == "Sentiment Distribution" for s in report.sections)

    def test_add_highlights(self):
        reporter = SentimentReporter()
        reporter.add_highlights(
            most_positive="Great product!",
            most_negative="Terrible service",
        )
        report = reporter.generate()
        assert any(s.title == "Highlights" for s in report.sections)

    def test_add_metadata(self):
        reporter = SentimentReporter()
        reporter.add_metadata("source", "test")
        report = reporter.generate()
        assert report.metadata["source"] == "test"

    def test_chaining(self):
        report = (
            SentimentReporter("Test")
            .add_section("Intro", "Hello")
            .add_metadata("key", "value")
            .generate()
        )
        assert report.title == "Test"

    def test_reset(self):
        reporter = SentimentReporter()
        reporter.add_section("Test", "Content")
        reporter.reset()
        report = reporter.generate()
        assert len(report.sections) == 0


class TestCreateReport:
    """Test create_report function."""

    def test_basic_report(self):
        report = create_report(
            title="Test",
            total=100,
            avg_sentiment=0.5,
            distribution={"positive": 60, "negative": 20, "neutral": 20},
        )
        assert isinstance(report, SentimentReport)
        assert report.title == "Test"
