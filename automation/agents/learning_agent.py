"""
Learning Agent - Continuous improvement and skill development

Handles industry trend curation, best practice recommendations,
skill gap identification, and retrospective facilitation.
"""

from typing import Dict, List, Any, Optional
from loguru import logger
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from utils.messaging_client import messaging_client


class LearningAgent(BaseAgent):
    """
    Learning Agent for continuous improvement.

    Capabilities:
    - Industry trend curation
    - Best practice recommendations
    - Skill gap identification
    - Learning resource curation
    - Retrospective facilitation
    """

    def __init__(self):
        super().__init__("Learning Agent", "📖")

    def run_workflow(self, **kwargs) -> str:
        """
        Main workflow for learning agent.

        Args:
            workflow_type: Type of learning workflow to run
            **kwargs: Additional parameters for the workflow

        Returns:
            Learning content or report
        """
        workflow_type = kwargs.get("workflow_type", "digest")

        if workflow_type == "digest":
            return self.generate_learning_digest(**kwargs)
        elif workflow_type == "retrospective":
            return self.facilitate_retrospective(**kwargs)
        elif workflow_type == "skill_assessment":
            return self.assess_skills(**kwargs)
        elif workflow_type == "reading_list":
            return self.curate_reading_list(**kwargs)
        else:
            return self._general_learning_content(**kwargs)

    def generate_learning_digest(
        self,
        timeframe: str = "weekly",
        topics: Optional[List[str]] = None
    ) -> str:
        """
        Generate a curated learning digest.

        Args:
            timeframe: Time period (daily, weekly, monthly)
            topics: Specific topics to focus on

        Returns:
            Formatted learning digest
        """
        logger.info(f"{self.name}: Generating {timeframe} learning digest")

        topics = topics or ["product management", "technology trends", "leadership"]

        system_prompt = f"""
You are a learning curator helping a product manager stay current.

User: {self.user_name}
Role: {self.user_role}
Company: {self.company_name}

Current OKRs:
{self.format_list(self.okrs)}

Strategic Priorities:
{self.format_list(self.strategic_priorities)}

Curate relevant learning content that:
1. Aligns with current priorities and OKRs
2. Addresses skill gaps
3. Highlights emerging trends
4. Provides actionable insights
5. Is digestible in 5-10 minutes
"""

        prompt = f"""
Create a {timeframe} learning digest focused on: {', '.join(topics)}

Include:
- Industry trends and news
- Best practices and frameworks
- Recommended articles/resources
- Actionable takeaways
- Application to current work

Keep it concise and actionable.
"""

        try:
            digest_content = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.7
            )

            # Format the digest
            digest = f"""# {timeframe.title()} Learning Digest
**{self.emoji} Generated for {self.user_name}**

**Date:** {self.current_date}
**Focus Areas:** {', '.join(topics)}

---

{digest_content}

---

**Reading Time:** ~5-10 minutes
**Next Digest:** {self._next_digest_date(timeframe)}
"""
            return digest

        except Exception as e:
            logger.error(f"Error generating learning digest: {e}")
            return f"Error generating learning digest: {str(e)}"

    def facilitate_retrospective(
        self,
        period: str = "sprint",
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Facilitate a retrospective discussion.

        Args:
            period: Time period (sprint, quarter, etc.)
            context: Context including wins, challenges, data

        Returns:
            Structured retrospective
        """
        logger.info(f"{self.name}: Facilitating {period} retrospective")

        context = context or {}

        system_prompt = f"""
You are facilitating a retrospective for a product manager.

User: {self.user_name}
Role: {self.user_role}

Structure the retrospective with:
1. What went well (celebrate wins)
2. What could be improved (identify challenges)
3. Key learnings (extract insights)
4. Action items (commit to improvements)
5. Experiments to try (test hypotheses)

Focus on growth mindset and actionable outcomes.
"""

        wins = context.get("wins", [])
        challenges = context.get("challenges", [])
        data = context.get("data", {})

        prompt = f"""
Facilitate a {period} retrospective.

{f"Wins: {', '.join(wins)}" if wins else ''}
{f"Challenges: {', '.join(challenges)}" if challenges else ''}
{f"Data: {data}" if data else ''}

Create a structured retrospective that extracts learnings and identifies improvements.
"""

        try:
            retro_content = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2500,
                temperature=0.7
            )

            # Format retrospective
            retrospective = f"""# {period.title()} Retrospective
**{self.emoji} Facilitated by {self.name}**

**Date:** {self.current_date}
**Period:** {period}
**Participants:** {self.user_name}

---

{retro_content}

---

**Follow-up:** Review action items in next retrospective
**Next Retro:** {self._next_retro_date(period)}
"""
            return retrospective

        except Exception as e:
            logger.error(f"Error facilitating retrospective: {e}")
            return f"Error facilitating retrospective: {str(e)}"

    def assess_skills(
        self,
        current_skills: Optional[List[str]] = None,
        target_role: Optional[str] = None
    ) -> str:
        """
        Assess skill gaps and create learning paths.

        Args:
            current_skills: List of current skills
            target_role: Target role or career goal

        Returns:
            Skill assessment and learning plan
        """
        logger.info(f"{self.name}: Assessing skills")

        current_skills = current_skills or []
        target_role = target_role or f"Senior {self.user_role}"

        system_prompt = f"""
You are a career development advisor assessing skills.

Current Role: {self.user_role}
Target Role: {target_role}

Provide:
1. Current skill assessment
2. Gap analysis
3. Priority skills to develop
4. Recommended learning path
5. Resources (books, courses, practices)
"""

        prompt = f"""
Current Skills: {', '.join(current_skills) if current_skills else 'To be identified'}
Target Role: {target_role}

Current OKRs:
{self.format_list(self.okrs)}

Assess skill gaps and create a learning plan aligned with career goals and current priorities.
"""

        try:
            assessment = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2500,
                temperature=0.7
            )

            # Format assessment
            skill_report = f"""# Skill Assessment & Learning Plan
**{self.emoji} For {self.user_name}**

**Date:** {self.current_date}
**Current Role:** {self.user_role}
**Target Role:** {target_role}

---

{assessment}

---

**Next Review:** Quarterly (in 3 months)
"""
            return skill_report

        except Exception as e:
            logger.error(f"Error assessing skills: {e}")
            return f"Error assessing skills: {str(e)}"

    def curate_reading_list(
        self,
        topics: Optional[List[str]] = None,
        timeframe: str = "week"
    ) -> str:
        """
        Curate a reading list based on current priorities.

        Args:
            topics: Topics to focus on
            timeframe: Time to complete (week, month)

        Returns:
            Curated reading list
        """
        logger.info(f"{self.name}: Curating reading list")

        topics = topics or ["product management", "data analysis", "team leadership"]

        system_prompt = f"""
You are curating learning resources for a product manager.

User Role: {self.user_role}
Strategic Priorities: {', '.join(self.strategic_priorities)}

Recommend:
1. Must-read articles (2-3)
2. Books (1-2)
3. Podcasts/videos (optional)
4. Practice exercises

Focus on actionable, high-signal content aligned with current work.
"""

        prompt = f"""
Create a {timeframe} reading list for: {', '.join(topics)}

Prioritize:
- Relevance to current OKRs
- Practical application
- Trusted sources
- Realistic time commitment

Include brief descriptions and estimated reading time.
"""

        try:
            reading_list = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.7
            )

            # Format reading list
            formatted_list = f"""# {timeframe.title()} Reading List
**{self.emoji} Curated for {self.user_name}**

**Date:** {self.current_date}
**Topics:** {', '.join(topics)}
**Time Commitment:** {self._estimate_reading_time(timeframe)}

---

{reading_list}

---

**Track Progress:** Mark items as completed
**Next List:** {self._next_reading_list_date(timeframe)}
"""
            return formatted_list

        except Exception as e:
            logger.error(f"Error curating reading list: {e}")
            return f"Error curating reading list: {str(e)}"

    def _general_learning_content(self, **kwargs) -> str:
        """
        Generate general learning content.

        Returns:
            Learning content
        """
        topic = kwargs.get("topic", "continuous improvement")
        logger.info(f"{self.name}: Generating learning content for {topic}")

        system_prompt = f"""
You are a learning advisor providing insights on {topic}.

User: {self.user_name}
Role: {self.user_role}

Provide actionable learning content that can be applied immediately.
"""

        prompt = f"Provide learning insights and recommendations for: {topic}"

        try:
            content = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.7
            )

            return f"""# Learning: {topic.title()}
**Date:** {self.current_date}

{content}
"""

        except Exception as e:
            logger.error(f"Error generating learning content: {e}")
            return f"Error generating learning content: {str(e)}"

    def _next_digest_date(self, timeframe: str) -> str:
        """Calculate next digest date based on timeframe."""
        days_map = {"daily": 1, "weekly": 7, "monthly": 30}
        days = days_map.get(timeframe, 7)
        next_date = datetime.now() + timedelta(days=days)
        return next_date.strftime("%Y-%m-%d")

    def _next_retro_date(self, period: str) -> str:
        """Calculate next retrospective date."""
        days_map = {"sprint": 14, "monthly": 30, "quarterly": 90}
        days = days_map.get(period, 14)
        next_date = datetime.now() + timedelta(days=days)
        return next_date.strftime("%Y-%m-%d")

    def _next_reading_list_date(self, timeframe: str) -> str:
        """Calculate next reading list date."""
        days_map = {"week": 7, "month": 30}
        days = days_map.get(timeframe, 7)
        next_date = datetime.now() + timedelta(days=days)
        return next_date.strftime("%Y-%m-%d")

    def _estimate_reading_time(self, timeframe: str) -> str:
        """Estimate reading time based on timeframe."""
        time_map = {"week": "2-3 hours", "month": "5-8 hours"}
        return time_map.get(timeframe, "2-3 hours")

    def send_learning_digest(self, digest: str) -> None:
        """
        Send learning digest via messaging.

        Args:
            digest: Digest content
        """
        message = f"""**Weekly Learning Digest**

{digest[:500]}...

[View full digest]
"""
        self.send_to_messaging(message, title="Learning Digest")


# Global singleton instance
learning_agent = LearningAgent()


if __name__ == "__main__":
    # Test the agent
    print("Testing Learning Agent...")

    # Test learning digest
    digest = learning_agent.generate_learning_digest(
        timeframe="weekly",
        topics=["product management", "AI trends"]
    )
    print("\nGenerated Learning Digest:")
    print(digest[:500])

    # Test retrospective
    retro = learning_agent.facilitate_retrospective(
        period="sprint",
        context={
            "wins": ["Shipped feature X", "Improved team velocity"],
            "challenges": ["Unclear requirements", "Technical debt"]
        }
    )
    print("\nGenerated Retrospective:")
    print(retro[:500])
