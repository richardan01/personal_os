"""
Action Models - Action items and interaction summaries
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

from models.enums import (
    Priority,
    ActionStatus,
    Sentiment,
)


@dataclass
class ActionItem:
    """A follow-up action item"""

    id: str = ""
    title: str = ""
    description: str = ""

    # Assignment
    owner: str = ""                                    # Who owns this action
    stakeholder: str = ""                              # Related stakeholder

    # Timing
    due_date: Optional[datetime] = None
    priority: Priority = Priority.SHOULD_HAVE

    # Status
    status: ActionStatus = ActionStatus.PENDING

    # Source
    source_doc_id: str = ""                            # Where this came from
    source_meeting_date: Optional[datetime] = None

    # Google Tasks integration
    google_task_id: Optional[str] = None               # If synced to Google Tasks

    def __post_init__(self):
        """Generate ID if not provided"""
        if not self.id:
            self.id = str(uuid.uuid4())[:8]

    @property
    def is_overdue(self) -> bool:
        """Check if action item is overdue"""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status not in [
            ActionStatus.COMPLETED, ActionStatus.CANCELLED
        ]

    @property
    def days_until_due(self) -> Optional[int]:
        """Get days until due date"""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.utcnow()
        return delta.days

    def complete(self) -> None:
        """Mark as completed"""
        self.status = ActionStatus.COMPLETED

    def cancel(self) -> None:
        """Mark as cancelled"""
        self.status = ActionStatus.CANCELLED

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner": self.owner,
            "stakeholder": self.stakeholder,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority.value,
            "status": self.status.value,
            "source_doc_id": self.source_doc_id,
            "source_meeting_date": self.source_meeting_date.isoformat() if self.source_meeting_date else None,
            "google_task_id": self.google_task_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ActionItem":
        due_date = None
        if data.get("due_date"):
            due_date = datetime.fromisoformat(data["due_date"])

        source_meeting_date = None
        if data.get("source_meeting_date"):
            source_meeting_date = datetime.fromisoformat(data["source_meeting_date"])

        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            owner=data.get("owner", ""),
            stakeholder=data.get("stakeholder", ""),
            due_date=due_date,
            priority=Priority(data.get("priority", "should_have")),
            status=ActionStatus(data.get("status", "pending")),
            source_doc_id=data.get("source_doc_id", ""),
            source_meeting_date=source_meeting_date,
            google_task_id=data.get("google_task_id"),
        )


@dataclass
class InteractionSummary:
    """Summary of a single interaction with a stakeholder"""

    date: Optional[datetime] = None
    type: str = "meeting"                              # "interview", "meeting", "email", "workshop"
    duration_minutes: int = 0
    summary: str = ""                                  # Brief summary of interaction
    sentiment: Sentiment = Sentiment.NEUTRAL           # How it went
    key_takeaways: list = field(default_factory=list)  # Main points
    follow_ups: list = field(default_factory=list)     # Action items generated
    source_doc_id: str = ""                            # Reference to source document

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat() if self.date else None,
            "type": self.type,
            "duration_minutes": self.duration_minutes,
            "summary": self.summary,
            "sentiment": self.sentiment.value,
            "key_takeaways": self.key_takeaways,
            "follow_ups": self.follow_ups,
            "source_doc_id": self.source_doc_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "InteractionSummary":
        date = None
        if data.get("date"):
            date = datetime.fromisoformat(data["date"])

        return cls(
            date=date,
            type=data.get("type", "meeting"),
            duration_minutes=data.get("duration_minutes", 0),
            summary=data.get("summary", ""),
            sentiment=Sentiment(data.get("sentiment", "neutral")),
            key_takeaways=data.get("key_takeaways", []),
            follow_ups=data.get("follow_ups", []),
            source_doc_id=data.get("source_doc_id", ""),
        )
