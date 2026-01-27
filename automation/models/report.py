"""
Report Models - Discovery reports and summaries
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Tuple, Optional

from models.enums import Stance
from models.insight import Quote, Theme, Conflict
from models.stakeholder import StakeholderProfile
from models.relationship import InfluenceMatrix
from models.action import ActionItem
from models.document import DocumentContent


@dataclass
class InsightSummary:
    """Aggregated summary of all stakeholder insights"""

    # Overview
    total_stakeholders: int = 0
    total_interactions: int = 0
    date_range: Tuple[Optional[datetime], Optional[datetime]] = (None, None)

    # Stance distribution
    stance_breakdown: Dict[str, int] = field(default_factory=dict)

    # Top themes
    top_concerns: List[Theme] = field(default_factory=list)
    top_needs: List[Theme] = field(default_factory=list)

    # Risks & opportunities
    key_risks: List[str] = field(default_factory=list)
    key_opportunities: List[str] = field(default_factory=list)

    # Conflicts
    active_conflicts: List[Conflict] = field(default_factory=list)

    # Recommendations
    strategic_recommendations: List[str] = field(default_factory=list)
    immediate_actions: List[ActionItem] = field(default_factory=list)

    # Key quotes (executive highlights)
    highlight_quotes: List[Quote] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_stakeholders": self.total_stakeholders,
            "total_interactions": self.total_interactions,
            "date_range": (
                self.date_range[0].isoformat() if self.date_range[0] else None,
                self.date_range[1].isoformat() if self.date_range[1] else None,
            ),
            "stance_breakdown": self.stance_breakdown,
            "top_concerns": [t.to_dict() for t in self.top_concerns],
            "top_needs": [t.to_dict() for t in self.top_needs],
            "key_risks": self.key_risks,
            "key_opportunities": self.key_opportunities,
            "active_conflicts": [c.to_dict() for c in self.active_conflicts],
            "strategic_recommendations": self.strategic_recommendations,
            "immediate_actions": [a.to_dict() for a in self.immediate_actions],
            "highlight_quotes": [q.to_dict() for q in self.highlight_quotes],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "InsightSummary":
        date_range = (None, None)
        if data.get("date_range"):
            start = data["date_range"][0]
            end = data["date_range"][1]
            date_range = (
                datetime.fromisoformat(start) if start else None,
                datetime.fromisoformat(end) if end else None,
            )

        return cls(
            total_stakeholders=data.get("total_stakeholders", 0),
            total_interactions=data.get("total_interactions", 0),
            date_range=date_range,
            stance_breakdown=data.get("stance_breakdown", {}),
            top_concerns=[Theme.from_dict(t) for t in data.get("top_concerns", [])],
            top_needs=[Theme.from_dict(t) for t in data.get("top_needs", [])],
            key_risks=data.get("key_risks", []),
            key_opportunities=data.get("key_opportunities", []),
            active_conflicts=[Conflict.from_dict(c) for c in data.get("active_conflicts", [])],
            strategic_recommendations=data.get("strategic_recommendations", []),
            immediate_actions=[ActionItem.from_dict(a) for a in data.get("immediate_actions", [])],
            highlight_quotes=[Quote.from_dict(q) for q in data.get("highlight_quotes", [])],
        )


@dataclass
class DiscoveryReport:
    """Complete stakeholder discovery report"""

    # Metadata
    id: str = ""
    title: str = ""
    generated_at: Optional[datetime] = None
    generated_by: str = "StakeholderDiscoveryAgent"

    # Google Doc reference
    google_doc_id: str = ""
    google_doc_url: str = ""

    # Content sections
    executive_summary: str = ""
    insight_summary: Optional[InsightSummary] = None
    stakeholder_profiles: List[StakeholderProfile] = field(default_factory=list)
    influence_matrix: Optional[InfluenceMatrix] = None
    themes_and_patterns: List[Theme] = field(default_factory=list)
    conflicts_and_risks: List[Conflict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    action_plan: List[ActionItem] = field(default_factory=list)

    # Appendix
    source_documents: List[DocumentContent] = field(default_factory=list)
    all_quotes: List[Quote] = field(default_factory=list)

    def __post_init__(self):
        """Set defaults"""
        if not self.id:
            self.id = f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        if not self.generated_at:
            self.generated_at = datetime.utcnow()

    def generate_executive_summary(self) -> str:
        """Generate executive summary from content"""
        if not self.insight_summary:
            return ""

        summary_parts = [
            f"# Stakeholder Discovery Report: {self.title}",
            f"\nGenerated: {self.generated_at.strftime('%B %d, %Y') if self.generated_at else 'N/A'}",
            f"\n## Overview",
            f"- **Total Stakeholders Analyzed:** {self.insight_summary.total_stakeholders}",
            f"- **Total Interactions:** {self.insight_summary.total_interactions}",
        ]

        # Stance breakdown
        if self.insight_summary.stance_breakdown:
            summary_parts.append("\n## Stakeholder Sentiment")
            for stance, count in self.insight_summary.stance_breakdown.items():
                summary_parts.append(f"- {stance.title()}: {count}")

        # Key concerns
        if self.insight_summary.top_concerns:
            summary_parts.append("\n## Top Concerns")
            for concern in self.insight_summary.top_concerns[:3]:
                summary_parts.append(f"- **{concern.name}**: {concern.description}")

        # Key needs
        if self.insight_summary.top_needs:
            summary_parts.append("\n## Top Needs")
            for need in self.insight_summary.top_needs[:3]:
                summary_parts.append(f"- **{need.name}**: {need.description}")

        # Recommendations
        if self.insight_summary.strategic_recommendations:
            summary_parts.append("\n## Strategic Recommendations")
            for rec in self.insight_summary.strategic_recommendations[:5]:
                summary_parts.append(f"- {rec}")

        return "\n".join(summary_parts)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "generated_by": self.generated_by,
            "google_doc_id": self.google_doc_id,
            "google_doc_url": self.google_doc_url,
            "executive_summary": self.executive_summary,
            "insight_summary": self.insight_summary.to_dict() if self.insight_summary else None,
            "stakeholder_profiles": [p.to_dict() for p in self.stakeholder_profiles],
            "influence_matrix": self.influence_matrix.to_dict() if self.influence_matrix else None,
            "themes_and_patterns": [t.to_dict() for t in self.themes_and_patterns],
            "conflicts_and_risks": [c.to_dict() for c in self.conflicts_and_risks],
            "recommendations": self.recommendations,
            "action_plan": [a.to_dict() for a in self.action_plan],
            "source_documents": [d.to_dict() for d in self.source_documents],
            "all_quotes": [q.to_dict() for q in self.all_quotes],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DiscoveryReport":
        generated_at = None
        if data.get("generated_at"):
            generated_at = datetime.fromisoformat(data["generated_at"])

        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            generated_at=generated_at,
            generated_by=data.get("generated_by", "StakeholderDiscoveryAgent"),
            google_doc_id=data.get("google_doc_id", ""),
            google_doc_url=data.get("google_doc_url", ""),
            executive_summary=data.get("executive_summary", ""),
            insight_summary=InsightSummary.from_dict(data["insight_summary"]) if data.get("insight_summary") else None,
            stakeholder_profiles=[StakeholderProfile.from_dict(p) for p in data.get("stakeholder_profiles", [])],
            influence_matrix=InfluenceMatrix.from_dict(data["influence_matrix"]) if data.get("influence_matrix") else None,
            themes_and_patterns=[Theme.from_dict(t) for t in data.get("themes_and_patterns", [])],
            conflicts_and_risks=[Conflict.from_dict(c) for c in data.get("conflicts_and_risks", [])],
            recommendations=data.get("recommendations", []),
            action_plan=[ActionItem.from_dict(a) for a in data.get("action_plan", [])],
            source_documents=[DocumentContent.from_dict(d) for d in data.get("source_documents", [])],
            all_quotes=[Quote.from_dict(q) for q in data.get("all_quotes", [])],
        )
