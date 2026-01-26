"""
Stakeholder Models - Stakeholder profiles and insights
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict

from models.enums import (
    Sentiment,
    Severity,
    InfluenceLevel,
    Stance,
)
from models.insight import (
    Concern,
    Need,
    Quote,
    MentionedStakeholder,
)
from models.action import ActionItem
from models.relationship import Relationship


@dataclass
class StakeholderInsight:
    """Insights extracted from a single meeting/interview"""

    # Source tracking
    source_doc_id: str                               # Which document this came from
    source_doc_title: str = ""                       # Document title for reference
    meeting_date: Optional[datetime] = None          # When the meeting occurred
    meeting_type: str = "interview"                  # "interview", "workshop", "1:1", "group"

    # Stakeholder identification
    stakeholder_name: str = ""
    stakeholder_role: str = ""
    stakeholder_department: str = ""
    stakeholder_email: str = ""

    # Extracted insights
    concerns: List[Concern] = field(default_factory=list)
    needs: List[Need] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)

    # Sentiment analysis
    overall_sentiment: Sentiment = Sentiment.NEUTRAL
    sentiment_details: str = ""

    # Evidence
    key_quotes: List[Quote] = field(default_factory=list)

    # Relationships mentioned
    mentioned_stakeholders: List[MentionedStakeholder] = field(default_factory=list)

    # Action items
    action_items: List[ActionItem] = field(default_factory=list)

    # AI confidence
    extraction_confidence: float = 0.0               # 0.0-1.0 confidence score

    # Timestamp
    extracted_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "source_doc_id": self.source_doc_id,
            "source_doc_title": self.source_doc_title,
            "meeting_date": self.meeting_date.isoformat() if self.meeting_date else None,
            "meeting_type": self.meeting_type,
            "stakeholder_name": self.stakeholder_name,
            "stakeholder_role": self.stakeholder_role,
            "stakeholder_department": self.stakeholder_department,
            "stakeholder_email": self.stakeholder_email,
            "concerns": [c.to_dict() for c in self.concerns],
            "needs": [n.to_dict() for n in self.needs],
            "goals": self.goals,
            "constraints": self.constraints,
            "overall_sentiment": self.overall_sentiment.value,
            "sentiment_details": self.sentiment_details,
            "key_quotes": [q.to_dict() for q in self.key_quotes],
            "action_items": [a.to_dict() for a in self.action_items],
            "extraction_confidence": self.extraction_confidence,
            "extracted_at": self.extracted_at.isoformat() if self.extracted_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StakeholderInsight":
        meeting_date = None
        if data.get("meeting_date"):
            meeting_date = datetime.fromisoformat(data["meeting_date"])

        extracted_at = None
        if data.get("extracted_at"):
            extracted_at = datetime.fromisoformat(data["extracted_at"])

        return cls(
            source_doc_id=data["source_doc_id"],
            source_doc_title=data.get("source_doc_title", ""),
            meeting_date=meeting_date,
            meeting_type=data.get("meeting_type", "interview"),
            stakeholder_name=data.get("stakeholder_name", ""),
            stakeholder_role=data.get("stakeholder_role", ""),
            stakeholder_department=data.get("stakeholder_department", ""),
            stakeholder_email=data.get("stakeholder_email", ""),
            concerns=[Concern.from_dict(c) for c in data.get("concerns", [])],
            needs=[Need.from_dict(n) for n in data.get("needs", [])],
            goals=data.get("goals", []),
            constraints=data.get("constraints", []),
            overall_sentiment=Sentiment(data.get("overall_sentiment", "neutral")),
            sentiment_details=data.get("sentiment_details", ""),
            key_quotes=[Quote.from_dict(q) for q in data.get("key_quotes", [])],
            action_items=[ActionItem.from_dict(a) for a in data.get("action_items", [])],
            extraction_confidence=data.get("extraction_confidence", 0.0),
            extracted_at=extracted_at,
        )


@dataclass
class StakeholderProfile:
    """Comprehensive profile of a stakeholder (aggregated from multiple sources)"""

    # Identity
    id: str = ""                                     # Unique identifier
    name: str = ""
    role: str = ""
    department: str = ""
    email: str = ""

    # Influence & Position
    influence_level: InfluenceLevel = InfluenceLevel.CONTRIBUTOR
    influence_scope: str = ""                        # What they influence
    stance: Stance = Stance.NEUTRAL
    stance_confidence: float = 0.5                   # How confident we are

    # Aggregated insights (from all interactions)
    all_concerns: List[Concern] = field(default_factory=list)
    top_concerns: List[Concern] = field(default_factory=list)
    all_needs: List[Need] = field(default_factory=list)
    top_needs: List[Need] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    success_metrics: List[str] = field(default_factory=list)

    # Communication style
    communication_preference: str = "detailed"       # "detailed", "executive_summary", "visual"
    decision_style: str = "data-driven"              # "data-driven", "consensus", "gut_feel"

    # Key quotes (most impactful)
    highlight_quotes: List[Quote] = field(default_factory=list)

    # Relationships
    relationships: List[Relationship] = field(default_factory=list)
    reports_to: Optional[str] = None                 # Manager name
    direct_reports: List[str] = field(default_factory=list)

    # Interaction history
    interactions: List[Dict] = field(default_factory=list)  # InteractionSummary dicts
    total_interactions: int = 0
    first_contact: Optional[datetime] = None
    last_contact: Optional[datetime] = None

    # Engagement tracking
    engagement_score: float = 0.5                    # 0.0-1.0 how engaged they are
    responsiveness: str = "medium"                   # "high", "medium", "low"

    # Source tracking
    source_documents: List[str] = field(default_factory=list)

    # Metadata
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_reviewed_by: str = ""

    def __post_init__(self):
        """Generate ID if not provided"""
        if not self.id and self.name:
            self.id = self.name.lower().replace(" ", "_")

    def add_insight(self, insight: StakeholderInsight) -> None:
        """Add insights from a new interaction"""
        self.all_concerns.extend(insight.concerns)
        self.all_needs.extend(insight.needs)
        self.goals.extend([g for g in insight.goals if g not in self.goals])
        self.highlight_quotes.extend([q for q in insight.key_quotes if q.is_highlight])

        if insight.source_doc_id not in self.source_documents:
            self.source_documents.append(insight.source_doc_id)

        self.total_interactions += 1

        if insight.meeting_date:
            if not self.first_contact or insight.meeting_date < self.first_contact:
                self.first_contact = insight.meeting_date
            if not self.last_contact or insight.meeting_date > self.last_contact:
                self.last_contact = insight.meeting_date

        self.updated_at = datetime.utcnow()

        # Update top concerns/needs (by frequency and severity)
        self._update_top_items()

    def _update_top_items(self) -> None:
        """Update top concerns and needs based on frequency and severity"""
        # Group concerns by description
        concern_freq: Dict[str, List[Concern]] = {}
        for c in self.all_concerns:
            key = c.description.lower()
            if key not in concern_freq:
                concern_freq[key] = []
            concern_freq[key].append(c)

        # Sort by frequency and take top 5
        sorted_concerns = sorted(
            concern_freq.items(),
            key=lambda x: (len(x[1]), max(c.severity.value for c in x[1])),
            reverse=True
        )
        self.top_concerns = [items[0] for _, items in sorted_concerns[:5]]

        # Same for needs
        need_freq: Dict[str, List[Need]] = {}
        for n in self.all_needs:
            key = n.description.lower()
            if key not in need_freq:
                need_freq[key] = []
            need_freq[key].append(n)

        sorted_needs = sorted(
            need_freq.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        self.top_needs = [items[0] for _, items in sorted_needs[:5]]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "email": self.email,
            "influence_level": self.influence_level.value,
            "influence_scope": self.influence_scope,
            "stance": self.stance.value,
            "stance_confidence": self.stance_confidence,
            "all_concerns": [c.to_dict() for c in self.all_concerns],
            "top_concerns": [c.to_dict() for c in self.top_concerns],
            "all_needs": [n.to_dict() for n in self.all_needs],
            "top_needs": [n.to_dict() for n in self.top_needs],
            "goals": self.goals,
            "success_metrics": self.success_metrics,
            "communication_preference": self.communication_preference,
            "decision_style": self.decision_style,
            "highlight_quotes": [q.to_dict() for q in self.highlight_quotes],
            "relationships": [r.to_dict() for r in self.relationships],
            "reports_to": self.reports_to,
            "direct_reports": self.direct_reports,
            "interactions": self.interactions,
            "total_interactions": self.total_interactions,
            "first_contact": self.first_contact.isoformat() if self.first_contact else None,
            "last_contact": self.last_contact.isoformat() if self.last_contact else None,
            "engagement_score": self.engagement_score,
            "responsiveness": self.responsiveness,
            "source_documents": self.source_documents,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_reviewed_by": self.last_reviewed_by,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StakeholderProfile":
        first_contact = None
        if data.get("first_contact"):
            first_contact = datetime.fromisoformat(data["first_contact"])

        last_contact = None
        if data.get("last_contact"):
            last_contact = datetime.fromisoformat(data["last_contact"])

        created_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])

        updated_at = None
        if data.get("updated_at"):
            updated_at = datetime.fromisoformat(data["updated_at"])

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            role=data.get("role", ""),
            department=data.get("department", ""),
            email=data.get("email", ""),
            influence_level=InfluenceLevel(data.get("influence_level", "contributor")),
            influence_scope=data.get("influence_scope", ""),
            stance=Stance(data.get("stance", "neutral")),
            stance_confidence=data.get("stance_confidence", 0.5),
            all_concerns=[Concern.from_dict(c) for c in data.get("all_concerns", [])],
            top_concerns=[Concern.from_dict(c) for c in data.get("top_concerns", [])],
            all_needs=[Need.from_dict(n) for n in data.get("all_needs", [])],
            top_needs=[Need.from_dict(n) for n in data.get("top_needs", [])],
            goals=data.get("goals", []),
            success_metrics=data.get("success_metrics", []),
            communication_preference=data.get("communication_preference", "detailed"),
            decision_style=data.get("decision_style", "data-driven"),
            highlight_quotes=[Quote.from_dict(q) for q in data.get("highlight_quotes", [])],
            relationships=[Relationship.from_dict(r) for r in data.get("relationships", [])],
            reports_to=data.get("reports_to"),
            direct_reports=data.get("direct_reports", []),
            interactions=data.get("interactions", []),
            total_interactions=data.get("total_interactions", 0),
            first_contact=first_contact,
            last_contact=last_contact,
            engagement_score=data.get("engagement_score", 0.5),
            responsiveness=data.get("responsiveness", "medium"),
            source_documents=data.get("source_documents", []),
            created_at=created_at,
            updated_at=updated_at,
            last_reviewed_by=data.get("last_reviewed_by", ""),
        )
