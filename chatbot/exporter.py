"""
Conversation Exporter Module

This module provides functionality to export conversations to various formats
including JSON and plain text.
"""

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import ConversationManager, Message
    from .sentiment import ConversationSentimentSummary


class ConversationExporter:
    """
    Export conversations to various formats.

    Supports exporting conversation history with sentiment analysis
    to JSON, plain text, and CSV formats.
    """

    def __init__(self, export_dir: str = "exports"):
        """
        Initialize the exporter.

        Args:
            export_dir: Directory to save exported files.
        """
        self.export_dir = Path(export_dir)

    def _ensure_export_dir(self) -> None:
        """Create export directory if it doesn't exist."""
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, prefix: str, extension: str) -> str:
        """
        Generate a unique filename with timestamp.

        Args:
            prefix: Filename prefix.
            extension: File extension.

        Returns:
            Generated filename.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"

    def _message_to_dict(self, message: "Message") -> Dict[str, Any]:
        """
        Convert a Message object to a dictionary.

        Args:
            message: The message to convert.

        Returns:
            Dictionary representation.
        """
        result = {
            "role": message.role.value,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
        }

        if message.sentiment:
            result["sentiment"] = {
                "label": message.sentiment.label.value,
                "compound_score": message.sentiment.compound_score,
                "positive_score": message.sentiment.positive_score,
                "negative_score": message.sentiment.negative_score,
                "neutral_score": message.sentiment.neutral_score,
            }

        return result

    def _summary_to_dict(
        self, summary: "ConversationSentimentSummary"
    ) -> Dict[str, Any]:
        """
        Convert a ConversationSentimentSummary to a dictionary.

        Args:
            summary: The summary to convert.

        Returns:
            Dictionary representation.
        """
        return {
            "overall_sentiment": summary.overall_sentiment.value,
            "average_compound_score": summary.average_compound_score,
            "mood_trend": summary.mood_trend,
            "positive_count": summary.positive_count,
            "negative_count": summary.negative_count,
            "neutral_count": summary.neutral_count,
            "total_messages": (
                summary.positive_count
                + summary.negative_count
                + summary.neutral_count
            ),
        }

    def export_to_json(
        self,
        conversation: "ConversationManager",
        filename: Optional[str] = None,
        include_summary: bool = True,
    ) -> str:
        """
        Export conversation to JSON format.

        Args:
            conversation: The conversation manager.
            filename: Optional custom filename.
            include_summary: Whether to include sentiment summary.

        Returns:
            Path to the exported file.
        """
        self._ensure_export_dir()

        if filename is None:
            filename = self._generate_filename("conversation", "json")

        filepath = self.export_dir / filename

        export_data: Dict[str, Any] = {
            "exported_at": datetime.now().isoformat(),
            "message_count": conversation.message_count,
            "messages": [
                self._message_to_dict(msg) for msg in conversation.messages
            ],
        }

        if include_summary and not conversation.is_empty:
            summary = conversation.analyze_conversation()
            export_data["summary"] = self._summary_to_dict(summary)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def export_to_text(
        self,
        conversation: "ConversationManager",
        filename: Optional[str] = None,
        include_sentiment: bool = True,
    ) -> str:
        """
        Export conversation to plain text format.

        Args:
            conversation: The conversation manager.
            filename: Optional custom filename.
            include_sentiment: Whether to include sentiment info.

        Returns:
            Path to the exported file.
        """
        self._ensure_export_dir()

        if filename is None:
            filename = self._generate_filename("conversation", "txt")

        filepath = self.export_dir / filename

        lines = [
            "=" * 60,
            "CONVERSATION EXPORT",
            f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Messages: {conversation.message_count}",
            "=" * 60,
            "",
        ]

        for message in conversation.messages:
            role_label = "User" if message.role.value == "user" else "Bot"
            lines.append(f"{role_label}: {message.content}")

            if include_sentiment and message.sentiment:
                lines.append(
                    f"  -> Sentiment: {message.sentiment.label.value} "
                    f"(score: {message.sentiment.compound_score:.2f})"
                )

            lines.append("")

        # Add summary
        if not conversation.is_empty:
            summary = conversation.analyze_conversation()
            lines.extend([
                "-" * 60,
                "SUMMARY",
                "-" * 60,
                f"Overall Sentiment: {summary.overall_sentiment.value}",
                f"Average Score: {summary.average_compound_score:.2f}",
                f"Mood Trend: {summary.mood_trend}",
                "",
                f"Positive: {summary.positive_count}",
                f"Negative: {summary.negative_count}",
                f"Neutral: {summary.neutral_count}",
                "=" * 60,
            ])

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return str(filepath)

    def export_to_csv(
        self,
        conversation: "ConversationManager",
        filename: Optional[str] = None,
    ) -> str:
        """
        Export conversation to CSV format.

        Args:
            conversation: The conversation manager.
            filename: Optional custom filename.

        Returns:
            Path to the exported file.
        """
        import csv

        self._ensure_export_dir()

        if filename is None:
            filename = self._generate_filename("conversation", "csv")

        filepath = self.export_dir / filename

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                "timestamp",
                "role",
                "content",
                "sentiment_label",
                "compound_score",
                "positive_score",
                "negative_score",
                "neutral_score",
            ])

            # Data rows
            for message in conversation.messages:
                sentiment = message.sentiment
                writer.writerow([
                    message.timestamp.isoformat(),
                    message.role.value,
                    message.content,
                    sentiment.label.value if sentiment else "",
                    f"{sentiment.compound_score:.4f}" if sentiment else "",
                    f"{sentiment.positive_score:.4f}" if sentiment else "",
                    f"{sentiment.negative_score:.4f}" if sentiment else "",
                    f"{sentiment.neutral_score:.4f}" if sentiment else "",
                ])

        return str(filepath)


def export_conversation(
    conversation: "ConversationManager",
    format: str = "json",
    export_dir: str = "exports",
    filename: Optional[str] = None,
) -> str:
    """
    Convenience function to export a conversation.

    Args:
        conversation: The conversation manager.
        format: Export format ('json', 'text', or 'csv').
        export_dir: Directory for exports.
        filename: Optional custom filename.

    Returns:
        Path to the exported file.

    Raises:
        ValueError: If format is not supported.
    """
    exporter = ConversationExporter(export_dir)

    if format == "json":
        return exporter.export_to_json(conversation, filename)
    elif format == "text":
        return exporter.export_to_text(conversation, filename)
    elif format == "csv":
        return exporter.export_to_csv(conversation, filename)
    else:
        raise ValueError(f"Unsupported export format: {format}")
