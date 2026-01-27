"""
Insight Models - Concerns, needs, quotes, themes, and conflicts
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from models.enums import (
    Sentiment,
    Severity,
    Priority,
    ConcernCategory,
    NeedCategory,
)


@dataclass
class Quote:
    """A direct quote from a stakeholder"""

    text: str                              # The exact quote
    context: str = ""                      # What prompted this statement
    topic: str = ""                        # What topic this relates to
    sentiment: Sentiment = Sentiment.NEUTRAL
    is_highlight: bool = False             # Particularly important/impactful

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "context": self.context,
            "topic": self.topic,
            "sentiment": self.sentiment.value,
            "is_highlight": self.is_highlight,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        return cls(
            text=data["text"],
            context=data.get("context", ""),
            topic=data.get("topic", ""),
            sentiment=Sentiment(data.get("sentiment", "neutral")),
            is_highlight=data.get("is_highlight", False),
        )


@dataclass
class Concern:
    """A specific concern raised by a stakeholder"""

    description: str                                 # The concern itself
    category: ConcernCategory = ConcernCategory.OTHER
    severity: Severity = Severity.MEDIUM
    quote: Optional[str] = None                      # Supporting quote

    # For tracking resolution
    is_addressed: bool = False
    resolution_notes: str = ""

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "category": self.category.value,
            "severity": self.severity.value,
            "quote": self.quote,
            "is_addressed": self.is_addressed,
            "resolution_notes": self.resolution_notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Concern":
        return cls(
            description=data["description"],
            category=ConcernCategory(data.get("category", "other")),
            severity=Severity(data.get("severity", "medium")),
            quote=data.get("quote"),
            is_addressed=data.get("is_addressed", False),
            resolution_notes=data.get("resolution_notes", ""),
        )


@dataclass
class Need:
    """A specific need expressed by a stakeholder"""

    description: str                                   # The need itself
    category: NeedCategory = NeedCategory.FUNCTIONAL
    priority: Priority = Priority.SHOULD_HAVE
    quote: Optional[str] = None                        # Supporting quote

    # For tracking fulfillment
    is_fulfilled: bool = False
    fulfillment_notes: str = ""

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "category": self.category.value,
            "priority": self.priority.value,
            "quote": self.quote,
            "is_fulfilled": self.is_fulfilled,
            "fulfillment_notes": self.fulfillment_notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Need":
        return cls(
            description=data["description"],
            category=NeedCategory(data.get("category", "functional")),
            priority=Priority(data.get("priority", "should_have")),
            quote=data.get("quote"),
            is_fulfilled=data.get("is_fulfilled", False),
            fulfillment_notes=data.get("fulfillment_notes", ""),
        )


@dataclass
class MentionedStakeholder:
    """A stakeholder mentioned by another stakeholder"""

    name: str
    context: str = ""                  # Why they were mentioned
    relationship_hint: str = ""        # e.g., "works closely with", "reports to"
    sentiment_toward: Sentiment = Sentiment.NEUTRAL


@dataclass
class Theme:
    """A recurring theme identified across multiple stakeholders"""

    name: str                                          # Theme name
    description: str                                   # Detailed description
    category: str = ""                                 # "concern", "need", "opportunity", "risk"

    # Evidence
    frequency: int = 0                                 # How many stakeholders mentioned
    stakeholders: List[str] = field(default_factory=list)
    supporting_quotes: List[Quote] = field(default_factory=list)

    # Analysis
    severity: Severity = Severity.MEDIUM
    urgency: str = "short-term"                        # "immediate", "short-term", "long-term"

    # Recommendations
    recommended_actions: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "frequency": self.frequency,
            "stakeholders": self.stakeholders,
            "supporting_quotes": [q.to_dict() for q in self.supporting_quotes],
            "severity": self.severity.value,
            "urgency": self.urgency,
            "recommended_actions": self.recommended_actions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Theme":
        return cls(
            name=data["name"],
            description=data["description"],
            category=data.get("category", ""),
            frequency=data.get("frequency", 0),
            stakeholders=data.get("stakeholders", []),
            supporting_quotes=[Quote.from_dict(q) for q in data.get("supporting_quotes", [])],
            severity=Severity(data.get("severity", "medium")),
            urgency=data.get("urgency", "short-term"),
            recommended_actions=data.get("recommended_actions", []),
        )


@dataclass
class Conflict:
    """Identified conflict or tension between stakeholders/groups"""

    description: str                                   # What the conflict is about
    parties: List[str] = field(default_factory=list)  # Stakeholders involved

    # Nature of conflict
    conflict_type: str = "priority"                    # "priority", "resource", "approach", "political"
    severity: Severity = Severity.MEDIUM

    # Evidence
    evidence: List[str] = field(default_factory=list) # Quotes/observations

    # Impact
    impact_on_initiative: str = ""                     # How this affects the project

    # Resolution
    resolution_status: str = "unresolved"             # "unresolved", "in_progress", "resolved"
    resolution_approach: str = ""                      # Recommended approach

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "parties": self.parties,
            "conflict_type": self.conflict_type,
            "severity": self.severity.value,
            "evidence": self.evidence,
            "impact_on_initiative": self.impact_on_initiative,
            "resolution_status": self.resolution_status,
            "resolution_approach": self.resolution_approach,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Conflict":
        return cls(
            description=data["description"],
            parties=data.get("parties", []),
            conflict_type=data.get("conflict_type", "priority"),
            severity=Severity(data.get("severity", "medium")),
            evidence=data.get("evidence", []),
            impact_on_initiative=data.get("impact_on_initiative", ""),
            resolution_status=data.get("resolution_status", "unresolved"),
            resolution_approach=data.get("resolution_approach", ""),
        )
