"""
Messaging client for Personal OS - Logging-only implementation.

This module provides a messaging abstraction that logs all messages
to files instead of sending them to external services like Slack.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum


class Severity(Enum):
    """Message severity levels."""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MessagingClient:
    """
    Logging-only messaging client.

    All messages are written to log files in the automation/logs directory
    instead of being sent to external messaging services.
    """

    def __init__(self, log_dir: Optional[str] = None):
        """
        Initialize the messaging client.

        Args:
            log_dir: Directory to write log files. Defaults to automation/logs/
        """
        if log_dir is None:
            # Default to automation/logs relative to this file
            current_dir = Path(__file__).parent.parent
            log_dir = current_dir / "logs"

        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Create separate log files for different message types
        self.dm_log = self.log_dir / "direct_messages.log"
        self.alert_log = self.log_dir / "alerts.log"
        self.plan_log = self.log_dir / "daily_plans.log"
        self.status_log = self.log_dir / "status_updates.log"

    def _write_log(self, log_file: Path, message: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Write a log entry to the specified file.

        Args:
            log_file: Path to the log file
            message: Message to log
            metadata: Optional metadata to include
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"[{timestamp}]\n")

            if metadata:
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n")

            f.write(f"{message}\n")

    def send_dm(self, message: str, recipient: Optional[str] = None) -> bool:
        """
        Send a direct message (logs to file).

        Args:
            message: Message content
            recipient: Optional recipient identifier

        Returns:
            True if logged successfully
        """
        metadata = {}
        if recipient:
            metadata["Recipient"] = recipient

        self._write_log(self.dm_log, message, metadata)
        return True

    def send_alert(
        self,
        title: str,
        message: str,
        severity: Severity = Severity.INFO,
        **kwargs
    ) -> bool:
        """
        Send an alert message (logs to file).

        Args:
            title: Alert title
            message: Alert message
            severity: Alert severity level
            **kwargs: Additional metadata

        Returns:
            True if logged successfully
        """
        metadata = {
            "Title": title,
            "Severity": severity.value,
            **kwargs
        }

        self._write_log(self.alert_log, message, metadata)
        return True

    def send_daily_plan(self, plan: str, date: Optional[str] = None) -> bool:
        """
        Send a daily plan (logs to file).

        Args:
            plan: Daily plan content
            date: Date for the plan (defaults to today)

        Returns:
            True if logged successfully
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        metadata = {"Date": date}
        self._write_log(self.plan_log, plan, metadata)
        return True

    def send_status_update(
        self,
        update: str,
        project: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        Send a status update (logs to file).

        Args:
            update: Status update content
            project: Optional project identifier
            **kwargs: Additional metadata

        Returns:
            True if logged successfully
        """
        metadata = {}
        if project:
            metadata["Project"] = project
        metadata.update(kwargs)

        self._write_log(self.status_log, update, metadata)
        return True

    def send_summary(self, summary: str, summary_type: str = "general") -> bool:
        """
        Send a summary message (logs to file).

        Args:
            summary: Summary content
            summary_type: Type of summary (daily, weekly, etc.)

        Returns:
            True if logged successfully
        """
        metadata = {"Type": summary_type}
        self._write_log(self.status_log, summary, metadata)
        return True

    def send_metrics_report(
        self,
        report: str,
        metrics: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send a metrics report (logs to file).

        Args:
            report: Report content
            metrics: Optional metrics data

        Returns:
            True if logged successfully
        """
        metadata = {"Type": "Metrics Report"}
        if metrics:
            metadata.update(metrics)

        self._write_log(self.status_log, report, metadata)
        return True


# Global singleton instance
messaging_client = MessagingClient()
