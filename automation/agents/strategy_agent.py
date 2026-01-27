"""
Strategy Agent - High-level planning and strategic alignment
Handles OKR tracking, competitive analysis, and strategic decision making
"""

from typing import Dict, List, Any, Optional
from loguru import logger

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.base_agent import BaseAgent
from utils.messaging_client import messaging_client


class StrategyAgent(BaseAgent):
    """Handles strategic planning and alignment"""

    def __init__(self):
        super().__init__("Strategy Agent", "🎯")

    def run_workflow(self, **kwargs) -> str:
        """Run the strategy alignment workflow"""
        workflow_type = kwargs.get("workflow_type", "alignment_check")

        if workflow_type == "alignment_check":
            return self.generate_alignment_check(
                current_activities=kwargs.get("current_activities", []),
                recent_decisions=kwargs.get("recent_decisions", [])
            )
        elif workflow_type == "okr_review":
            return self.generate_okr_review(
                okr_progress=kwargs.get("okr_progress", {})
            )
        else:
            return self.generate_alignment_check()

    def generate_alignment_check(
        self,
        current_activities: Optional[List[str]] = None,
        recent_decisions: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate a strategic alignment check

        Args:
            current_activities: List of current work items
            recent_decisions: List of recent decisions made

        Returns:
            Strategic alignment assessment
        """
        logger.info("Generating strategic alignment check...")

        activities_text = self.format_list(current_activities or ["No activities provided"])
        decisions_text = self.format_list(
            [f"{d.get('decision', 'Unknown')}" for d in (recent_decisions or [])]
        ) if recent_decisions else "- No recent decisions"

        prompt = f"""
ROLE: Strategic Advisor and Chief of Staff
CONTEXT: Reviewing strategic alignment for {self.user_name}, {self.user_role} at {self.company_name}

TODAY: {self.current_date} ({self.day_of_week})

CURRENT OKRs:
{self.format_list(self.okrs)}

STRATEGIC PRIORITIES:
{self.format_list(self.strategic_priorities)}

CURRENT ACTIVITIES:
{activities_text}

RECENT DECISIONS:
{decisions_text}

TASK:
Perform a strategic alignment check following this format:

## Strategic Alignment Check - {self.current_date}

### OKR Progress Snapshot
For each OKR, assess current progress status.

### Alignment Assessment
Score: [X/10]
Analyze how well current activities align with strategic priorities.

### Well-Aligned Activities
List activities that strongly support OKRs.

### Potential Misalignment
Flag activities that may not serve strategic goals.

### Strategic Opportunities
Based on priorities, what high-impact opportunities should be considered?

### Recommended Focus
What should be the top strategic focus this week?

### Questions to Consider
Strategic questions that need answering.

Be direct and actionable. Challenge misalignment respectfully.
"""

        system_prompt = f"""You are a strategic advisor helping {self.user_name} ensure
their daily work aligns with long-term strategic goals. Be direct, insightful, and
challenge assumptions when needed."""

        try:
            alignment_check = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.7
            )
            logger.info("Strategic alignment check generated successfully")
            return alignment_check

        except Exception as e:
            logger.error(f"Error generating alignment check: {e}")
            raise

    def generate_okr_review(
        self,
        okr_progress: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate an OKR progress review

        Args:
            okr_progress: Dictionary of OKR progress data

        Returns:
            OKR review assessment
        """
        logger.info("Generating OKR review...")

        progress_text = ""
        if okr_progress:
            for okr, data in okr_progress.items():
                progress_text += f"- {okr}: {data.get('progress', 'Unknown')}% - {data.get('status', 'Unknown')}\n"
        else:
            progress_text = "No progress data available"

        prompt = f"""
ROLE: OKR Coach and Strategic Advisor
CONTEXT: Reviewing OKR progress for {self.user_name}

CURRENT OKRs:
{self.format_list(self.okrs)}

PROGRESS DATA:
{progress_text}

TASK:
Create an OKR progress review:

## OKR Review - {self.current_date}

### Progress Summary
| OKR | Progress | Status | Confidence |
Assess each OKR's progress.

### On Track
OKRs making good progress.

### At Risk
OKRs that need attention.

### Recommendations
Specific actions to improve OKR progress.

### Key Focus for Next Week
What moves the needle most?
"""

        system_prompt = "You are an OKR coach helping track and improve goal progress."

        try:
            review = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1200,
                temperature=0.6
            )
            logger.info("OKR review generated successfully")
            return review

        except Exception as e:
            logger.error(f"Error generating OKR review: {e}")
            raise

    def send_alignment_check_to_messaging(self, alignment_check: str) -> None:
        """Send strategic alignment check to messaging"""
        self.send_to_messaging(alignment_check, title="Strategic Alignment Check")

    def send_okr_review_to_messaging(self, review: str) -> None:
        """Send OKR review to messaging"""
        self.send_to_messaging(review, title="OKR Progress Review")


# Global instance
strategy_agent = StrategyAgent()


if __name__ == "__main__":
    print("Testing Strategy Agent...")
    print("=" * 50)

    try:
        check = strategy_agent.generate_alignment_check(
            current_activities=[
                "Working on Feature X PRD",
                "User interview analysis",
                "Sprint planning meeting"
            ]
        )
        print("\nGenerated Alignment Check:")
        print("-" * 50)
        print(check)
        print("\n" + "=" * 50)
        print("✅ Strategy Agent test successful")

    except Exception as e:
        print(f"❌ Test failed: {e}")
