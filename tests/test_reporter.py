"""Tests for reporter module."""

import pytest
from datetime import datetime
from chatbot.reporter import (
    ReportFormat,
    ReportSection,
    SentimentReport,
    ReportBuilder,
    ReportFormatter,
    create_report,
)


class TestReportBuilder:
    """Tests for ReportBuilder."""

    def test_add_section(self):
        """Test adding section."""
        builder = ReportBuilder("Test Report")
        builder.add_section("Overview", "This is the overview")
        
        report = builder.build()
        assert len(report.sections) == 1

    def test_add_metadata(self):
        """Test adding metadata."""
        builder = ReportBuilder()
        builder.add_metadata("author", "test")
        
        report = builder.build()
        assert report.metadata["author"] == "test"

    def test_build(self):
        """Test building report."""
        builder = ReportBuilder("My Report")
        builder.add_section("Intro", "Introduction text")
        
        report = builder.build("Summary here")
        
        assert report.title == "My Report"
        assert report.summary == "Summary here"

    def test_chaining(self):
        """Test method chaining."""
        report = (
            ReportBuilder("Chain Test")
            .add_section("A", "Content A")
            .add_section("B", "Content B")
            .add_metadata("key", "value")
            .build()
        )
        
        assert len(report.sections) == 2


class TestReportFormatter:
    """Tests for ReportFormatter."""

    def test_format_text(self):
        """Test text formatting."""
        report = ReportBuilder("Test").add_section("S", "Content").build()
        formatter = ReportFormatter()
        
        result = formatter.format(report, ReportFormat.TEXT)
        
        assert "Test" in result
        assert "Content" in result

    def test_format_markdown(self):
        """Test markdown formatting."""
        report = ReportBuilder("Test").add_section("S", "Content").build()
        formatter = ReportFormatter()
        
        result = formatter.format(report, ReportFormat.MARKDOWN)
        
        assert "# Test" in result
        assert "## S" in result

    def test_format_html(self):
        """Test HTML formatting."""
        report = ReportBuilder("Test").add_section("S", "Content").build()
        formatter = ReportFormatter()
        
        result = formatter.format(report, ReportFormat.HTML)
        
        assert "<h1>Test</h1>" in result
        assert "<html>" in result

    def test_format_json(self):
        """Test JSON formatting."""
        report = ReportBuilder("Test").add_section("S", "Content").build()
        formatter = ReportFormatter()
        
        result = formatter.format(report, ReportFormat.JSON)
        
        assert '"title": "Test"' in result


class TestCreateReport:
    """Tests for create_report function."""

    def test_create(self):
        """Test creating report."""
        sections = [
            {"title": "A", "content": "Content A"},
            {"title": "B", "content": "Content B"},
        ]
        
        report = create_report("My Report", sections, "Summary")
        
        assert report.title == "My Report"
        assert len(report.sections) == 2
