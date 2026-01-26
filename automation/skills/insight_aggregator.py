"""
Insight Aggregator Skill - Aggregate insights across stakeholders to find patterns
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from collections import Counter
import json
from loguru import logger

from utils.ai_client import ai_client
from models.stakeholder import StakeholderProfile, StakeholderInsight
from models.insight import Quote, Theme, Conflict, Concern, Need
from models.action import ActionItem
from models.report import InsightSummary
from models.enums import Stance, Severity


class InsightAggregator:
    """
    Skill for aggregating insights across multiple stakeholders to find patterns.

    Capabilities:
    - Find common themes across stakeholders
    - Identify conflicts between groups
    - Prioritize concerns and needs
    - Generate summary insights
    """

    THEME_ANALYSIS_PROMPT = """You are an expert at synthesizing stakeholder research for product management.

Analyze the following aggregated stakeholder data and identify key themes, patterns, and conflicts.

STAKEHOLDER CONCERNS (aggregated):
{concerns}

STAKEHOLDER NEEDS (aggregated):
{needs}

KEY QUOTES:
{quotes}

STAKEHOLDER STANCES:
{stances}

Identify:
1. Common themes across stakeholders
2. Conflicts or tensions between different groups
3. Strategic risks and opportunities
4. Recommended actions

Return JSON:

```json
{{
    "themes": [
        {{
            "name": "Theme name",
            "description": "Detailed description",
            "category": "concern|need|opportunity|risk",
            "frequency": <number of stakeholders>,
            "stakeholders": ["Names who share this theme"],
            "severity": "high|medium|low",
            "urgency": "immediate|short-term|long-term",
            "recommended_actions": ["Action 1", "Action 2"]
        }}
    ],
    "conflicts": [
        {{
            "description": "What the conflict is about",
            "parties": ["Group/Person 1", "Group/Person 2"],
            "conflict_type": "priority|resource|approach|political",
            "severity": "high|medium|low",
            "evidence": ["Quote or observation"],
            "impact_on_initiative": "How this affects the project",
            "resolution_approach": "Recommended approach"
        }}
    ],
    "key_risks": ["Risk 1", "Risk 2"],
    "key_opportunities": ["Opportunity 1", "Opportunity 2"],
    "strategic_recommendations": ["Recommendation 1", "Recommendation 2"]
}}
```

Return ONLY the JSON."""

    def __init__(self):
        self.ai = ai_client

    def find_common_themes(
        self,
        profiles: List[StakeholderProfile],
    ) -> List[Theme]:
        """
        Find common themes across stakeholder profiles using AI.

        Args:
            profiles: List of stakeholder profiles

        Returns:
            List of Theme objects
        """
        logger.info(f"Finding common themes across {len(profiles)} stakeholders")

        if not profiles:
            return []

        # Aggregate concerns
        all_concerns = []
        for p in profiles:
            for c in p.all_concerns:
                all_concerns.append(f"[{p.name}] {c.description} (severity: {c.severity.value})")

        # Aggregate needs
        all_needs = []
        for p in profiles:
            for n in p.all_needs:
                all_needs.append(f"[{p.name}] {n.description} (priority: {n.priority.value})")

        # Aggregate quotes
        all_quotes = []
        for p in profiles:
            for q in p.highlight_quotes[:3]:
                all_quotes.append(f'[{p.name}] "{q.text}"')

        # Aggregate stances
        stance_info = []
        for p in profiles:
            stance_info.append(f"- {p.name}: {p.stance.value}")

        prompt = self.THEME_ANALYSIS_PROMPT.format(
            concerns="\n".join(all_concerns[:30]) or "No concerns recorded",
            needs="\n".join(all_needs[:30]) or "No needs recorded",
            quotes="\n".join(all_quotes[:20]) or "No quotes recorded",
            stances="\n".join(stance_info) or "No stance data",
        )

        response = self.ai.generate(
            prompt=prompt,
            system_prompt="You are a stakeholder research analyst. Identify patterns objectively.",
            max_tokens=3000,
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

            themes = []
            for t in data.get("themes", []):
                try:
                    theme = Theme(
                        name=t.get("name", ""),
                        description=t.get("description", ""),
                        category=t.get("category", ""),
                        frequency=t.get("frequency", 0),
                        stakeholders=t.get("stakeholders", []),
                        severity=Severity(t.get("severity", "medium")),
                        urgency=t.get("urgency", "short-term"),
                        recommended_actions=t.get("recommended_actions", []),
                    )
                    themes.append(theme)
                except Exception as e:
                    logger.warning(f"Error parsing theme: {e}")

            return themes

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            return []

    def find_conflicts(
        self,
        profiles: List[StakeholderProfile],
    ) -> List[Conflict]:
        """
        Find conflicts between stakeholders.

        Args:
            profiles: List of stakeholder profiles

        Returns:
            List of Conflict objects
        """
        # Use the same analysis that finds themes
        # (The AI identifies conflicts in the same call)
        logger.info(f"Finding conflicts among {len(profiles)} stakeholders")

        if len(profiles) < 2:
            return []

        # Aggregate data for analysis
        all_concerns = []
        for p in profiles:
            for c in p.all_concerns:
                all_concerns.append(f"[{p.name}] {c.description}")

        all_needs = []
        for p in profiles:
            for n in p.all_needs:
                all_needs.append(f"[{p.name}] {n.description}")

        all_quotes = []
        for p in profiles:
            for q in p.highlight_quotes[:3]:
                all_quotes.append(f'[{p.name}] "{q.text}"')

        stance_info = [f"- {p.name}: {p.stance.value}" for p in profiles]

        prompt = self.THEME_ANALYSIS_PROMPT.format(
            concerns="\n".join(all_concerns[:30]) or "None",
            needs="\n".join(all_needs[:30]) or "None",
            quotes="\n".join(all_quotes[:20]) or "None",
            stances="\n".join(stance_info) or "None",
        )

        response = self.ai.generate(
            prompt=prompt,
            system_prompt="You are a stakeholder research analyst.",
            max_tokens=3000,
            temperature=0.2,
        )

        try:
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            conflicts = []
            for c in data.get("conflicts", []):
                try:
                    conflict = Conflict(
                        description=c.get("description", ""),
                        parties=c.get("parties", []),
                        conflict_type=c.get("conflict_type", "priority"),
                        severity=Severity(c.get("severity", "medium")),
                        evidence=c.get("evidence", []),
                        impact_on_initiative=c.get("impact_on_initiative", ""),
                        resolution_approach=c.get("resolution_approach", ""),
                    )
                    conflicts.append(conflict)
                except Exception as e:
                    logger.warning(f"Error parsing conflict: {e}")

            return conflicts

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            return []

    def prioritize_concerns(
        self,
        profiles: List[StakeholderProfile],
    ) -> List[Dict[str, Any]]:
        """
        Prioritize concerns by frequency and severity.

        Args:
            profiles: List of stakeholder profiles

        Returns:
            List of prioritized concerns with metadata
        """
        # Count concerns by description
        concern_data: Dict[str, Dict] = {}

        for p in profiles:
            for c in p.all_concerns:
                key = c.description.lower().strip()
                if key not in concern_data:
                    concern_data[key] = {
                        "description": c.description,
                        "category": c.category.value,
                        "count": 0,
                        "stakeholders": [],
                        "max_severity": "low",
                        "quotes": [],
                    }

                concern_data[key]["count"] += 1
                concern_data[key]["stakeholders"].append(p.name)

                # Track max severity
                severity_order = {"high": 3, "medium": 2, "low": 1}
                if severity_order.get(c.severity.value, 0) > severity_order.get(
                    concern_data[key]["max_severity"], 0
                ):
                    concern_data[key]["max_severity"] = c.severity.value

                if c.quote:
                    concern_data[key]["quotes"].append(c.quote)

        # Sort by count and severity
        severity_weight = {"high": 3, "medium": 2, "low": 1}
        sorted_concerns = sorted(
            concern_data.values(),
            key=lambda x: (x["count"], severity_weight.get(x["max_severity"], 0)),
            reverse=True,
        )

        return sorted_concerns

    def prioritize_needs(
        self,
        profiles: List[StakeholderProfile],
    ) -> List[Dict[str, Any]]:
        """
        Prioritize needs by frequency and priority.

        Args:
            profiles: List of stakeholder profiles

        Returns:
            List of prioritized needs with metadata
        """
        need_data: Dict[str, Dict] = {}

        for p in profiles:
            for n in p.all_needs:
                key = n.description.lower().strip()
                if key not in need_data:
                    need_data[key] = {
                        "description": n.description,
                        "category": n.category.value,
                        "count": 0,
                        "stakeholders": [],
                        "max_priority": "nice_to_have",
                        "quotes": [],
                    }

                need_data[key]["count"] += 1
                need_data[key]["stakeholders"].append(p.name)

                priority_order = {"must_have": 3, "should_have": 2, "nice_to_have": 1}
                if priority_order.get(n.priority.value, 0) > priority_order.get(
                    need_data[key]["max_priority"], 0
                ):
                    need_data[key]["max_priority"] = n.priority.value

                if n.quote:
                    need_data[key]["quotes"].append(n.quote)

        priority_weight = {"must_have": 3, "should_have": 2, "nice_to_have": 1}
        sorted_needs = sorted(
            need_data.values(),
            key=lambda x: (x["count"], priority_weight.get(x["max_priority"], 0)),
            reverse=True,
        )

        return sorted_needs

    def generate_summary(
        self,
        profiles: List[StakeholderProfile],
        insights: Optional[List[StakeholderInsight]] = None,
    ) -> InsightSummary:
        """
        Generate a comprehensive insight summary.

        Args:
            profiles: List of stakeholder profiles
            insights: Optional list of raw insights

        Returns:
            InsightSummary object
        """
        logger.info(f"Generating summary for {len(profiles)} stakeholders")

        # Calculate stance breakdown
        stance_breakdown = Counter(p.stance.value for p in profiles)

        # Get date range
        all_dates = []
        for p in profiles:
            if p.first_contact:
                all_dates.append(p.first_contact)
            if p.last_contact:
                all_dates.append(p.last_contact)

        date_range = (
            min(all_dates) if all_dates else None,
            max(all_dates) if all_dates else None,
        )

        # Get themes
        themes = self.find_common_themes(profiles)
        top_concerns = [t for t in themes if t.category == "concern"][:5]
        top_needs = [t for t in themes if t.category == "need"][:5]

        # Get conflicts
        conflicts = self.find_conflicts(profiles)

        # Collect highlight quotes
        highlight_quotes = []
        for p in profiles:
            highlight_quotes.extend([q for q in p.highlight_quotes if q.is_highlight][:2])

        # Generate recommendations
        strategic_recommendations = []
        for theme in themes[:3]:
            strategic_recommendations.extend(theme.recommended_actions[:2])

        # Identify risks and opportunities
        key_risks = [t.description for t in themes if t.category == "risk"][:5]
        key_opportunities = [t.description for t in themes if t.category == "opportunity"][:5]

        # Gather immediate actions
        immediate_actions = []
        for p in profiles:
            for interaction in p.interactions:
                if isinstance(interaction, dict) and "follow_ups" in interaction:
                    for follow_up in interaction["follow_ups"]:
                        if isinstance(follow_up, str):
                            immediate_actions.append(ActionItem(title=follow_up, stakeholder=p.name))

        return InsightSummary(
            total_stakeholders=len(profiles),
            total_interactions=sum(p.total_interactions for p in profiles),
            date_range=date_range,
            stance_breakdown=dict(stance_breakdown),
            top_concerns=top_concerns,
            top_needs=top_needs,
            key_risks=key_risks,
            key_opportunities=key_opportunities,
            active_conflicts=[c for c in conflicts if c.resolution_status == "unresolved"],
            strategic_recommendations=strategic_recommendations[:10],
            immediate_actions=immediate_actions[:10],
            highlight_quotes=highlight_quotes[:10],
        )


# Global instance
insight_aggregator = InsightAggregator()
