"""
Relationship Models - Stakeholder relationships and influence mapping
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

from models.enums import (
    RelationshipType,
    RelationshipStrength,
    Stance,
)


@dataclass
class Relationship:
    """Relationship between two stakeholders"""

    target_stakeholder_id: str                             # Who this relationship is with
    target_stakeholder_name: str = ""                      # Name for easy reference

    relationship_type: RelationshipType = RelationshipType.COLLABORATES
    strength: RelationshipStrength = RelationshipStrength.MODERATE

    context: str = ""                                      # Additional context

    # For influence mapping
    influence_direction: str = "bidirectional"             # "outbound", "inbound", "bidirectional"
    influence_weight: float = 0.5                          # 0.0-1.0 how much influence

    def to_dict(self) -> dict:
        return {
            "target_stakeholder_id": self.target_stakeholder_id,
            "target_stakeholder_name": self.target_stakeholder_name,
            "relationship_type": self.relationship_type.value,
            "strength": self.strength.value,
            "context": self.context,
            "influence_direction": self.influence_direction,
            "influence_weight": self.influence_weight,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Relationship":
        return cls(
            target_stakeholder_id=data["target_stakeholder_id"],
            target_stakeholder_name=data.get("target_stakeholder_name", ""),
            relationship_type=RelationshipType(data.get("relationship_type", "collaborates")),
            strength=RelationshipStrength(data.get("strength", "moderate")),
            context=data.get("context", ""),
            influence_direction=data.get("influence_direction", "bidirectional"),
            influence_weight=data.get("influence_weight", 0.5),
        )


@dataclass
class InfluenceRanking:
    """Influence ranking for a stakeholder"""

    stakeholder_id: str
    stakeholder_name: str = ""

    # Scores
    outbound_influence: float = 0.0          # How much they influence others (0-100)
    inbound_influence: float = 0.0           # How much others influence them (0-100)
    net_influence: float = 0.0               # outbound - inbound
    total_connections: int = 0               # Number of relationships

    # Ranking
    rank: int = 0                            # Overall influence rank

    def to_dict(self) -> dict:
        return {
            "stakeholder_id": self.stakeholder_id,
            "stakeholder_name": self.stakeholder_name,
            "outbound_influence": self.outbound_influence,
            "inbound_influence": self.inbound_influence,
            "net_influence": self.net_influence,
            "total_connections": self.total_connections,
            "rank": self.rank,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "InfluenceRanking":
        return cls(
            stakeholder_id=data["stakeholder_id"],
            stakeholder_name=data.get("stakeholder_name", ""),
            outbound_influence=data.get("outbound_influence", 0.0),
            inbound_influence=data.get("inbound_influence", 0.0),
            net_influence=data.get("net_influence", 0.0),
            total_connections=data.get("total_connections", 0),
            rank=data.get("rank", 0),
        )


@dataclass
class StakeholderCluster:
    """A group of aligned stakeholders"""

    name: str                                              # Cluster name
    members: List[str] = field(default_factory=list)       # Stakeholder names

    # Shared characteristics
    common_concerns: List[str] = field(default_factory=list)
    common_needs: List[str] = field(default_factory=list)
    overall_stance: Stance = Stance.NEUTRAL

    # Influence
    collective_influence: float = 0.0                      # Combined influence score

    # Strategy notes
    engagement_strategy: str = ""                          # How to engage this group

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "members": self.members,
            "common_concerns": self.common_concerns,
            "common_needs": self.common_needs,
            "overall_stance": self.overall_stance.value,
            "collective_influence": self.collective_influence,
            "engagement_strategy": self.engagement_strategy,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StakeholderCluster":
        return cls(
            name=data["name"],
            members=data.get("members", []),
            common_concerns=data.get("common_concerns", []),
            common_needs=data.get("common_needs", []),
            overall_stance=Stance(data.get("overall_stance", "neutral")),
            collective_influence=data.get("collective_influence", 0.0),
            engagement_strategy=data.get("engagement_strategy", ""),
        )


@dataclass
class InfluenceMatrix:
    """Influence mapping across all stakeholders"""

    stakeholders: List[str] = field(default_factory=list)  # All stakeholder names

    # Matrix: stakeholders[i] influence on stakeholders[j]
    influence_scores: List[List[float]] = field(default_factory=list)

    # Computed metrics
    influence_rankings: List[InfluenceRanking] = field(default_factory=list)

    # Cluster analysis
    clusters: List[StakeholderCluster] = field(default_factory=list)

    # Key findings
    power_brokers: List[str] = field(default_factory=list)      # Highest influence
    bridge_builders: List[str] = field(default_factory=list)    # Connect different groups
    isolated_stakeholders: List[str] = field(default_factory=list)  # Low connectivity

    # Metadata
    generated_at: Optional[datetime] = None
    based_on_profiles: int = 0

    def get_stakeholder_influence(self, stakeholder_name: str) -> Optional[InfluenceRanking]:
        """Get influence ranking for a specific stakeholder"""
        for ranking in self.influence_rankings:
            if ranking.stakeholder_name == stakeholder_name:
                return ranking
        return None

    def get_cluster_for_stakeholder(self, stakeholder_name: str) -> Optional[StakeholderCluster]:
        """Get cluster that contains a specific stakeholder"""
        for cluster in self.clusters:
            if stakeholder_name in cluster.members:
                return cluster
        return None

    def to_dict(self) -> dict:
        return {
            "stakeholders": self.stakeholders,
            "influence_scores": self.influence_scores,
            "influence_rankings": [r.to_dict() for r in self.influence_rankings],
            "clusters": [c.to_dict() for c in self.clusters],
            "power_brokers": self.power_brokers,
            "bridge_builders": self.bridge_builders,
            "isolated_stakeholders": self.isolated_stakeholders,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "based_on_profiles": self.based_on_profiles,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "InfluenceMatrix":
        generated_at = None
        if data.get("generated_at"):
            generated_at = datetime.fromisoformat(data["generated_at"])

        return cls(
            stakeholders=data.get("stakeholders", []),
            influence_scores=data.get("influence_scores", []),
            influence_rankings=[
                InfluenceRanking.from_dict(r) for r in data.get("influence_rankings", [])
            ],
            clusters=[
                StakeholderCluster.from_dict(c) for c in data.get("clusters", [])
            ],
            power_brokers=data.get("power_brokers", []),
            bridge_builders=data.get("bridge_builders", []),
            isolated_stakeholders=data.get("isolated_stakeholders", []),
            generated_at=generated_at,
            based_on_profiles=data.get("based_on_profiles", 0),
        )
