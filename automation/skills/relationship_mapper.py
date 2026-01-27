"""
Relationship Mapper Skill - Map relationships and influence between stakeholders
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from loguru import logger

from utils.ai_client import ai_client
from models.stakeholder import StakeholderProfile
from models.relationship import (
    Relationship,
    InfluenceRanking,
    StakeholderCluster,
    InfluenceMatrix,
)
from models.enums import Stance, RelationshipType


class RelationshipMapper:
    """
    Skill for mapping relationships and influence between stakeholders.

    Capabilities:
    - Build influence matrices
    - Identify power brokers and bridge builders
    - Cluster stakeholders by alignment
    - Find allies and blockers
    """

    CLUSTER_PROMPT = """You are an expert at stakeholder analysis and organizational dynamics.

Analyze the following stakeholders and identify clusters/groups of aligned stakeholders.

STAKEHOLDERS:
{stakeholders_info}

KNOWN RELATIONSHIPS:
{relationships_info}

Identify clusters of stakeholders who:
1. Share similar concerns or needs
2. Have similar stances
3. Work closely together
4. Have aligned interests

Return JSON:

```json
{{
    "clusters": [
        {{
            "name": "Cluster name (e.g., 'Engineering Leadership', 'Finance Skeptics')",
            "members": ["Name1", "Name2"],
            "common_concerns": ["Shared concern 1", "Shared concern 2"],
            "common_needs": ["Shared need 1"],
            "overall_stance": "champion|supporter|neutral|skeptic|blocker",
            "collective_influence": 0.0-1.0,
            "engagement_strategy": "Recommendation for engaging this group"
        }}
    ],
    "power_brokers": ["Names of highest-influence individuals"],
    "bridge_builders": ["Names of people who connect different groups"],
    "isolated_stakeholders": ["Names of stakeholders with few connections"]
}}
```

Return ONLY the JSON."""

    def __init__(self):
        self.ai = ai_client

    def build_influence_matrix(
        self,
        profiles: List[StakeholderProfile],
    ) -> InfluenceMatrix:
        """
        Build an influence matrix from stakeholder profiles.

        Args:
            profiles: List of stakeholder profiles

        Returns:
            InfluenceMatrix object
        """
        logger.info(f"Building influence matrix for {len(profiles)} stakeholders")

        if not profiles:
            return InfluenceMatrix()

        # Get stakeholder names
        stakeholders = [p.name for p in profiles]

        # Build influence scores matrix
        # influence_scores[i][j] = how much stakeholder i influences stakeholder j
        n = len(profiles)
        influence_scores = [[0.0] * n for _ in range(n)]

        # Map name to index
        name_to_idx = {p.name: i for i, p in enumerate(profiles)}

        # Fill in influence based on relationships
        for i, profile in enumerate(profiles):
            for rel in profile.relationships:
                target_idx = name_to_idx.get(rel.target_stakeholder_name)
                if target_idx is not None:
                    # Base influence weight
                    weight = rel.influence_weight

                    # Adjust based on relationship type
                    if rel.relationship_type == RelationshipType.MANAGES:
                        weight = max(weight, 0.7)
                    elif rel.relationship_type == RelationshipType.REPORTS_TO:
                        # They are influenced BY the target
                        influence_scores[target_idx][i] = max(
                            influence_scores[target_idx][i], 0.7
                        )
                        continue
                    elif rel.relationship_type == RelationshipType.INFLUENCES:
                        weight = max(weight, 0.6)
                    elif rel.relationship_type == RelationshipType.ALLIES_WITH:
                        weight = max(weight, 0.5)

                    influence_scores[i][target_idx] = max(
                        influence_scores[i][target_idx], weight
                    )

        # Calculate influence rankings
        rankings = []
        for i, profile in enumerate(profiles):
            outbound = sum(influence_scores[i])
            inbound = sum(influence_scores[j][i] for j in range(n))

            ranking = InfluenceRanking(
                stakeholder_id=profile.id,
                stakeholder_name=profile.name,
                outbound_influence=outbound * 100 / max(n - 1, 1),
                inbound_influence=inbound * 100 / max(n - 1, 1),
                net_influence=(outbound - inbound) * 100 / max(n - 1, 1),
                total_connections=len(profile.relationships),
            )
            rankings.append(ranking)

        # Sort and assign ranks
        rankings.sort(key=lambda r: r.outbound_influence, reverse=True)
        for i, ranking in enumerate(rankings):
            ranking.rank = i + 1

        # Identify key players
        power_brokers = [r.stakeholder_name for r in rankings[:3] if r.outbound_influence > 30]

        bridge_builders = []
        for profile in profiles:
            # Bridge builders have connections to multiple clusters/groups
            departments = set()
            for rel in profile.relationships:
                target = next((p for p in profiles if p.name == rel.target_stakeholder_name), None)
                if target:
                    departments.add(target.department)
            if len(departments) >= 2:
                bridge_builders.append(profile.name)

        isolated = [r.stakeholder_name for r in rankings if r.total_connections == 0]

        return InfluenceMatrix(
            stakeholders=stakeholders,
            influence_scores=influence_scores,
            influence_rankings=rankings,
            power_brokers=power_brokers,
            bridge_builders=bridge_builders,
            isolated_stakeholders=isolated,
            generated_at=datetime.utcnow(),
            based_on_profiles=len(profiles),
        )

    def identify_clusters(
        self,
        profiles: List[StakeholderProfile],
    ) -> List[StakeholderCluster]:
        """
        Identify clusters of aligned stakeholders using AI.

        Args:
            profiles: List of stakeholder profiles

        Returns:
            List of StakeholderCluster objects
        """
        logger.info(f"Identifying clusters among {len(profiles)} stakeholders")

        if len(profiles) < 2:
            return []

        # Format stakeholder info
        stakeholders_info = []
        for p in profiles:
            concerns = ", ".join([c.description for c in p.top_concerns[:3]]) or "None"
            needs = ", ".join([n.description for n in p.top_needs[:3]]) or "None"

            stakeholders_info.append(
                f"- {p.name} ({p.role}, {p.department})\n"
                f"  Stance: {p.stance.value}\n"
                f"  Concerns: {concerns}\n"
                f"  Needs: {needs}"
            )

        # Format relationships
        relationships_info = []
        for p in profiles:
            for rel in p.relationships:
                relationships_info.append(
                    f"- {p.name} {rel.relationship_type.value} {rel.target_stakeholder_name}"
                )

        prompt = self.CLUSTER_PROMPT.format(
            stakeholders_info="\n".join(stakeholders_info),
            relationships_info="\n".join(relationships_info) or "No explicit relationships",
        )

        response = self.ai.generate(
            prompt=prompt,
            system_prompt="You are an organizational dynamics expert. Analyze stakeholder groups objectively.",
            max_tokens=2000,
            temperature=0.3,
        )

        # Parse response
        try:
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            clusters = []
            for c in data.get("clusters", []):
                try:
                    cluster = StakeholderCluster(
                        name=c.get("name", ""),
                        members=c.get("members", []),
                        common_concerns=c.get("common_concerns", []),
                        common_needs=c.get("common_needs", []),
                        overall_stance=Stance(c.get("overall_stance", "neutral")),
                        collective_influence=c.get("collective_influence", 0.5),
                        engagement_strategy=c.get("engagement_strategy", ""),
                    )
                    clusters.append(cluster)
                except Exception as e:
                    logger.warning(f"Error parsing cluster: {e}")

            return clusters

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            return []

    def find_allies(
        self,
        target_stakeholder: StakeholderProfile,
        all_profiles: List[StakeholderProfile],
    ) -> List[StakeholderProfile]:
        """
        Find allies for a specific stakeholder.

        Args:
            target_stakeholder: The stakeholder to find allies for
            all_profiles: All stakeholder profiles

        Returns:
            List of allied stakeholders
        """
        allies = []

        for profile in all_profiles:
            if profile.id == target_stakeholder.id:
                continue

            # Check for explicit ally relationship
            for rel in profile.relationships:
                if rel.target_stakeholder_id == target_stakeholder.id:
                    if rel.relationship_type == RelationshipType.ALLIES_WITH:
                        allies.append(profile)
                        break

            # Check for similar stance (both champions or supporters)
            if target_stakeholder.stance in [Stance.CHAMPION, Stance.SUPPORTER]:
                if profile.stance in [Stance.CHAMPION, Stance.SUPPORTER]:
                    if profile not in allies:
                        allies.append(profile)

        return allies

    def find_blockers(
        self,
        target_stakeholder: StakeholderProfile,
        all_profiles: List[StakeholderProfile],
    ) -> List[StakeholderProfile]:
        """
        Find potential blockers for a stakeholder.

        Args:
            target_stakeholder: The stakeholder
            all_profiles: All stakeholder profiles

        Returns:
            List of potential blockers
        """
        blockers = []

        for profile in all_profiles:
            if profile.id == target_stakeholder.id:
                continue

            # Check for explicit conflict
            for rel in profile.relationships:
                if rel.target_stakeholder_id == target_stakeholder.id:
                    if rel.relationship_type == RelationshipType.CONFLICTS_WITH:
                        blockers.append(profile)
                        break

            # Check stance
            if profile.stance == Stance.BLOCKER:
                if profile not in blockers:
                    blockers.append(profile)

        return blockers

    def get_decision_chain(
        self,
        profiles: List[StakeholderProfile],
    ) -> List[StakeholderProfile]:
        """
        Get the decision-making chain (ordered by influence).

        Args:
            profiles: All stakeholder profiles

        Returns:
            List of profiles ordered by decision-making power
        """
        from models.enums import InfluenceLevel

        # Sort by influence level
        influence_order = {
            InfluenceLevel.DECISION_MAKER: 0,
            InfluenceLevel.KEY_INFLUENCER: 1,
            InfluenceLevel.CONTRIBUTOR: 2,
            InfluenceLevel.INFORMED: 3,
        }

        sorted_profiles = sorted(
            profiles,
            key=lambda p: influence_order.get(p.influence_level, 4)
        )

        return sorted_profiles

    def analyze_influence_path(
        self,
        source: StakeholderProfile,
        target: StakeholderProfile,
        all_profiles: List[StakeholderProfile],
    ) -> List[str]:
        """
        Find the influence path between two stakeholders.

        Args:
            source: Starting stakeholder
            target: Target stakeholder
            all_profiles: All profiles

        Returns:
            List of names representing the path
        """
        # Build adjacency list
        name_to_profile = {p.name: p for p in all_profiles}
        graph: Dict[str, List[str]] = {p.name: [] for p in all_profiles}

        for profile in all_profiles:
            for rel in profile.relationships:
                if rel.target_stakeholder_name in graph:
                    graph[profile.name].append(rel.target_stakeholder_name)

        # BFS to find shortest path
        from collections import deque

        queue = deque([(source.name, [source.name])])
        visited = {source.name}

        while queue:
            current, path = queue.popleft()

            if current == target.name:
                return path

            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []  # No path found


# Global instance
relationship_mapper = RelationshipMapper()
