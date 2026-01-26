"""
Stakeholder Profiler Skill - Build and update stakeholder profiles
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from loguru import logger

from utils.ai_client import ai_client
from models.stakeholder import StakeholderProfile, StakeholderInsight
from models.insight import Concern, Need, Quote
from models.relationship import Relationship
from models.enums import (
    InfluenceLevel,
    Stance,
    RelationshipType,
    RelationshipStrength,
)


class StakeholderProfiler:
    """
    Skill for building and maintaining stakeholder profiles.

    Capabilities:
    - Create new profiles from insights
    - Update existing profiles with new data
    - Determine influence level and stance
    - Track relationships
    """

    ANALYSIS_PROMPT = """You are an expert stakeholder analyst for product management.

Based on the following stakeholder information, analyze and determine:
1. Their influence level in decision-making
2. Their stance toward the initiative
3. Their communication and decision-making preferences

STAKEHOLDER INFORMATION:
Name: {name}
Role: {role}
Department: {department}

CONCERNS:
{concerns}

NEEDS:
{needs}

GOALS:
{goals}

KEY QUOTES:
{quotes}

TOTAL INTERACTIONS: {interaction_count}

Analyze this stakeholder and return JSON:

```json
{{
    "influence_level": "decision_maker|key_influencer|contributor|informed",
    "influence_scope": "What areas/decisions do they influence?",
    "stance": "champion|supporter|neutral|skeptic|blocker",
    "stance_confidence": 0.0-1.0,
    "stance_reasoning": "Why you assessed this stance",
    "communication_preference": "detailed|executive_summary|visual",
    "decision_style": "data-driven|consensus|gut_feel",
    "engagement_recommendations": ["List of recommendations for engaging this stakeholder"],
    "risk_factors": ["Potential risks or blockers related to this stakeholder"]
}}
```

Guidelines:
- influence_level: Based on their role and scope
  - decision_maker: Can approve/reject initiatives
  - key_influencer: Strongly shapes decisions
  - contributor: Provides input but limited influence
  - informed: Needs to know but doesn't influence
- stance: Based on their expressed concerns, needs, and quotes
  - champion: Actively advocates
  - supporter: Generally positive
  - neutral: No strong opinion
  - skeptic: Has doubts
  - blocker: Actively opposed
- Be objective and base assessments on evidence

Return ONLY the JSON."""

    def __init__(self):
        self.ai = ai_client
        self._profiles: Dict[str, StakeholderProfile] = {}

    def create_profile(
        self,
        name: str,
        role: str = "",
        department: str = "",
        email: str = "",
    ) -> StakeholderProfile:
        """
        Create a new stakeholder profile.

        Args:
            name: Stakeholder name
            role: Job title
            department: Department/team
            email: Email address

        Returns:
            New StakeholderProfile
        """
        logger.info(f"Creating profile for: {name}")

        profile = StakeholderProfile(
            name=name,
            role=role,
            department=department,
            email=email,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self._profiles[profile.id] = profile
        return profile

    def update_from_insight(
        self,
        profile: StakeholderProfile,
        insight: StakeholderInsight,
    ) -> StakeholderProfile:
        """
        Update a profile with new insight data.

        Args:
            profile: Existing profile
            insight: New insight to incorporate

        Returns:
            Updated profile
        """
        logger.info(f"Updating profile for {profile.name} with new insight")

        # Update basic info if not already set
        if not profile.role and insight.stakeholder_role:
            profile.role = insight.stakeholder_role
        if not profile.department and insight.stakeholder_department:
            profile.department = insight.stakeholder_department
        if not profile.email and insight.stakeholder_email:
            profile.email = insight.stakeholder_email

        # Add insight data
        profile.add_insight(insight)

        # Update in storage
        self._profiles[profile.id] = profile

        return profile

    def analyze_profile(self, profile: StakeholderProfile) -> StakeholderProfile:
        """
        Analyze a profile using AI to determine influence and stance.

        Args:
            profile: Profile to analyze

        Returns:
            Updated profile with analysis
        """
        logger.info(f"Analyzing profile for: {profile.name}")

        # Format data for prompt
        concerns_text = "\n".join([
            f"- {c.description} (severity: {c.severity.value})"
            for c in profile.top_concerns
        ]) or "No concerns recorded"

        needs_text = "\n".join([
            f"- {n.description} (priority: {n.priority.value})"
            for n in profile.top_needs
        ]) or "No needs recorded"

        goals_text = "\n".join([f"- {g}" for g in profile.goals]) or "No goals recorded"

        quotes_text = "\n".join([
            f'- "{q.text}" (sentiment: {q.sentiment.value})'
            for q in profile.highlight_quotes[:5]
        ]) or "No quotes recorded"

        prompt = self.ANALYSIS_PROMPT.format(
            name=profile.name,
            role=profile.role,
            department=profile.department,
            concerns=concerns_text,
            needs=needs_text,
            goals=goals_text,
            quotes=quotes_text,
            interaction_count=profile.total_interactions,
        )

        # Call AI
        response = self.ai.generate(
            prompt=prompt,
            system_prompt="You are a stakeholder analyst. Provide objective assessments based on evidence.",
            max_tokens=1500,
            temperature=0.2,
        )

        # Parse response
        try:
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            # Update profile with analysis
            try:
                profile.influence_level = InfluenceLevel(data.get("influence_level", "contributor"))
            except ValueError:
                profile.influence_level = InfluenceLevel.CONTRIBUTOR

            profile.influence_scope = data.get("influence_scope", "")

            try:
                profile.stance = Stance(data.get("stance", "neutral"))
            except ValueError:
                profile.stance = Stance.NEUTRAL

            profile.stance_confidence = data.get("stance_confidence", 0.5)
            profile.communication_preference = data.get("communication_preference", "detailed")
            profile.decision_style = data.get("decision_style", "data-driven")

            profile.updated_at = datetime.utcnow()
            self._profiles[profile.id] = profile

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")

        return profile

    def get_profile(self, stakeholder_id: str) -> Optional[StakeholderProfile]:
        """
        Get a profile by ID.

        Args:
            stakeholder_id: Profile ID

        Returns:
            StakeholderProfile or None
        """
        return self._profiles.get(stakeholder_id)

    def get_profile_by_name(self, name: str) -> Optional[StakeholderProfile]:
        """
        Get a profile by name.

        Args:
            name: Stakeholder name

        Returns:
            StakeholderProfile or None
        """
        name_lower = name.lower()
        for profile in self._profiles.values():
            if profile.name.lower() == name_lower:
                return profile
        return None

    def get_or_create_profile(
        self,
        name: str,
        role: str = "",
        department: str = "",
    ) -> StakeholderProfile:
        """
        Get existing profile or create new one.

        Args:
            name: Stakeholder name
            role: Job title
            department: Department

        Returns:
            StakeholderProfile
        """
        profile = self.get_profile_by_name(name)
        if profile:
            return profile
        return self.create_profile(name, role, department)

    def list_all_profiles(self) -> List[StakeholderProfile]:
        """
        List all stakeholder profiles.

        Returns:
            List of all profiles
        """
        return list(self._profiles.values())

    def get_profiles_by_stance(self, stance: Stance) -> List[StakeholderProfile]:
        """
        Get profiles filtered by stance.

        Args:
            stance: Stance to filter by

        Returns:
            List of matching profiles
        """
        return [p for p in self._profiles.values() if p.stance == stance]

    def get_profiles_by_influence(self, influence: InfluenceLevel) -> List[StakeholderProfile]:
        """
        Get profiles filtered by influence level.

        Args:
            influence: Influence level to filter by

        Returns:
            List of matching profiles
        """
        return [p for p in self._profiles.values() if p.influence_level == influence]

    def add_relationship(
        self,
        profile: StakeholderProfile,
        target_name: str,
        relationship_type: RelationshipType,
        strength: RelationshipStrength = RelationshipStrength.MODERATE,
        context: str = "",
    ) -> StakeholderProfile:
        """
        Add a relationship to a profile.

        Args:
            profile: Profile to update
            target_name: Name of related stakeholder
            relationship_type: Type of relationship
            strength: Relationship strength
            context: Additional context

        Returns:
            Updated profile
        """
        # Find or create target profile
        target = self.get_or_create_profile(target_name)

        # Create relationship
        relationship = Relationship(
            target_stakeholder_id=target.id,
            target_stakeholder_name=target_name,
            relationship_type=relationship_type,
            strength=strength,
            context=context,
        )

        # Add to profile (avoid duplicates)
        existing = [r for r in profile.relationships if r.target_stakeholder_id == target.id]
        if not existing:
            profile.relationships.append(relationship)
            profile.updated_at = datetime.utcnow()
            self._profiles[profile.id] = profile

        return profile

    def build_profiles_from_insights(
        self,
        insights: List[StakeholderInsight],
        analyze: bool = True,
    ) -> List[StakeholderProfile]:
        """
        Build profiles from a list of insights.

        Args:
            insights: List of insights
            analyze: Whether to run AI analysis on profiles

        Returns:
            List of created/updated profiles
        """
        logger.info(f"Building profiles from {len(insights)} insights")

        for insight in insights:
            if not insight.stakeholder_name:
                continue

            # Get or create profile
            profile = self.get_or_create_profile(
                name=insight.stakeholder_name,
                role=insight.stakeholder_role,
                department=insight.stakeholder_department,
            )

            # Update with insight
            self.update_from_insight(profile, insight)

            # Add mentioned stakeholders as relationships
            for mentioned in insight.mentioned_stakeholders:
                if mentioned.name:
                    self.add_relationship(
                        profile=profile,
                        target_name=mentioned.name,
                        relationship_type=RelationshipType.COLLABORATES,
                        context=mentioned.context,
                    )

        # Run analysis on profiles
        if analyze:
            for profile in self._profiles.values():
                if profile.total_interactions > 0:
                    self.analyze_profile(profile)

        return self.list_all_profiles()

    def export_profiles(self) -> List[Dict[str, Any]]:
        """
        Export all profiles as dictionaries.

        Returns:
            List of profile dicts
        """
        return [p.to_dict() for p in self._profiles.values()]

    def import_profiles(self, data: List[Dict[str, Any]]) -> int:
        """
        Import profiles from dictionaries.

        Args:
            data: List of profile dicts

        Returns:
            Number of profiles imported
        """
        count = 0
        for item in data:
            try:
                profile = StakeholderProfile.from_dict(item)
                self._profiles[profile.id] = profile
                count += 1
            except Exception as e:
                logger.error(f"Error importing profile: {e}")
        return count


# Global instance
stakeholder_profiler = StakeholderProfiler()
