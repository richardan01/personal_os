"""
Enumerations for Personal OS Data Models
"""

from enum import Enum


class DocType(Enum):
    """Type of Google Workspace document"""
    DOCS = "docs"
    SHEETS = "sheets"
    SLIDES = "slides"
    PDF = "pdf"
    OTHER = "other"


class Sentiment(Enum):
    """Sentiment analysis result"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class Severity(Enum):
    """Severity or importance level"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Priority(Enum):
    """Priority level for needs and requirements"""
    MUST_HAVE = "must_have"
    SHOULD_HAVE = "should_have"
    NICE_TO_HAVE = "nice_to_have"


class InfluenceLevel(Enum):
    """Stakeholder influence level in decision making"""
    DECISION_MAKER = "decision_maker"      # Has final say, can approve/reject
    KEY_INFLUENCER = "key_influencer"      # Strongly influences decision makers
    CONTRIBUTOR = "contributor"            # Provides input, but limited influence
    INFORMED = "informed"                  # Needs to know, but doesn't influence


class Stance(Enum):
    """Stakeholder stance toward an initiative"""
    CHAMPION = "champion"      # Actively advocates for the initiative
    SUPPORTER = "supporter"    # Generally positive, will support if asked
    NEUTRAL = "neutral"        # No strong opinion either way
    SKEPTIC = "skeptic"        # Has doubts, needs convincing
    BLOCKER = "blocker"        # Actively opposed, may try to stop progress


class RelationshipType(Enum):
    """Type of relationship between stakeholders"""
    REPORTS_TO = "reports_to"          # Direct reporting relationship
    MANAGES = "manages"                # Manages the other person
    COLLABORATES = "collaborates"      # Works together frequently
    INFLUENCES = "influences"          # Has influence over them
    CONFLICTS_WITH = "conflicts_with"  # Known friction/conflict
    ALLIES_WITH = "allies_with"        # Strong alliance/partnership


class RelationshipStrength(Enum):
    """Strength of relationship between stakeholders"""
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


class ActionStatus(Enum):
    """Status of an action item"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ConcernCategory(Enum):
    """Category of stakeholder concern"""
    BUDGET = "budget"                          # Cost/funding concerns
    TIMELINE = "timeline"                      # Schedule/deadline worries
    RESOURCE = "resource"                      # Headcount/capacity issues
    TECHNICAL = "technical"                    # Technical feasibility doubts
    POLITICAL = "political"                    # Org politics, turf wars
    CHANGE_MANAGEMENT = "change_management"    # Adoption/transition fears
    RISK = "risk"                              # Business/operational risks
    OTHER = "other"                            # Anything else


class NeedCategory(Enum):
    """Category of stakeholder need"""
    FUNCTIONAL = "functional"          # Feature/capability needs
    INFORMATION = "information"        # Reporting/visibility needs
    PROCESS = "process"                # Workflow/procedure needs
    COMMUNICATION = "communication"    # Updates/alignment needs
    SUPPORT = "support"                # Training/help needs
    RECOGNITION = "recognition"        # Credit/visibility needs
