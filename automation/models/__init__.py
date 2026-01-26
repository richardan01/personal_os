"""
Data Models for Personal OS

This module provides data models used throughout the system:
- Enums: Status types, categories, severity levels
- Document: Content extracted from Google Workspace docs
- Stakeholder: Stakeholder profiles and insights
- Insight: Concerns, needs, quotes, themes
- Relationship: Stakeholder relationships and influence mapping
- Action: Action items and interaction summaries
- Report: Discovery reports and summaries
"""

from models.enums import (
    DocType,
    Sentiment,
    Severity,
    Priority,
    InfluenceLevel,
    Stance,
    RelationshipType,
    RelationshipStrength,
    ActionStatus,
    ConcernCategory,
    NeedCategory,
)

from models.document import (
    TableData,
    DocumentContent,
)

from models.insight import (
    Concern,
    Need,
    Quote,
    Theme,
    Conflict,
    MentionedStakeholder,
)

from models.stakeholder import (
    StakeholderInsight,
    StakeholderProfile,
)

from models.relationship import (
    Relationship,
    InfluenceRanking,
    StakeholderCluster,
    InfluenceMatrix,
)

from models.action import (
    ActionItem,
    InteractionSummary,
)

from models.report import (
    InsightSummary,
    DiscoveryReport,
)

__all__ = [
    # Enums
    "DocType",
    "Sentiment",
    "Severity",
    "Priority",
    "InfluenceLevel",
    "Stance",
    "RelationshipType",
    "RelationshipStrength",
    "ActionStatus",
    "ConcernCategory",
    "NeedCategory",
    # Document
    "TableData",
    "DocumentContent",
    # Insight
    "Concern",
    "Need",
    "Quote",
    "Theme",
    "Conflict",
    "MentionedStakeholder",
    # Stakeholder
    "StakeholderInsight",
    "StakeholderProfile",
    # Relationship
    "Relationship",
    "InfluenceRanking",
    "StakeholderCluster",
    "InfluenceMatrix",
    # Action
    "ActionItem",
    "InteractionSummary",
    # Report
    "InsightSummary",
    "DiscoveryReport",
]
