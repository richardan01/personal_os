"""
Stakeholder Agent - Communication and alignment
Handles status updates, meeting prep, and stakeholder management
"""

from typing import Dict, List, Any, Optional
from loguru import logger

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.base_agent import BaseAgent
from utils.messaging_client import messaging_client


class StakeholderAgent(BaseAgent):
    """Handles stakeholder communication and alignment"""

    def __init__(self):
        super().__init__("Stakeholder Agent", "📢")

    def run_workflow(self, **kwargs) -> str:
        """Run the stakeholder workflow"""
        workflow_type = kwargs.get("workflow_type", "weekly_update")

        if workflow_type == "weekly_update":
            return self.generate_weekly_update(
                accomplishments=kwargs.get("accomplishments", []),
                challenges=kwargs.get("challenges", []),
                next_week=kwargs.get("next_week", [])
            )
        elif workflow_type == "executive_update":
            return self.generate_executive_update(
                metrics=kwargs.get("metrics", {}),
                highlights=kwargs.get("highlights", []),
                risks=kwargs.get("risks", [])
            )
        elif workflow_type == "meeting_agenda":
            return self.generate_meeting_agenda(
                meeting_type=kwargs.get("meeting_type", "General"),
                attendees=kwargs.get("attendees", []),
                topics=kwargs.get("topics", [])
            )
        else:
            return self.generate_weekly_update()

    def generate_weekly_update(
        self,
        accomplishments: Optional[List[str]] = None,
        challenges: Optional[List[Dict[str, str]]] = None,
        next_week: Optional[List[str]] = None
    ) -> str:
        """
        Generate weekly status update

        Args:
            accomplishments: List of accomplishments this week
            challenges: List of challenges encountered
            next_week: Priorities for next week

        Returns:
            Weekly status update
        """
        logger.info("Generating weekly update...")

        accomplishments_text = self.format_list(accomplishments or ["No accomplishments logged"])
        challenges_text = ""
        if challenges:
            for c in challenges:
                challenges_text += f"- {c.get('issue', 'Unknown')}: {c.get('mitigation', 'TBD')}\n"
        else:
            challenges_text = "- No significant challenges"
        next_week_text = self.format_list(next_week or ["To be determined"])

        prompt = f"""
ROLE: Executive Communication Specialist
CONTEXT: Creating weekly status update for {self.user_name}, {self.user_role}

WEEK ENDING: {self.current_date}

ACCOMPLISHMENTS:
{accomplishments_text}

CHALLENGES:
{challenges_text}

NEXT WEEK PRIORITIES:
{next_week_text}

OKRS:
{self.format_list(self.okrs)}

TASK:
Create a professional weekly status update:

## Weekly Status Update - Week of {self.current_date}

### TL;DR
2-3 sentence executive summary.

### Highlights
- [Accomplishment with impact]

### Progress on OKRs
| OKR | Progress | Status |
Brief update on each OKR.

### Challenges & Mitigations
| Challenge | Impact | Mitigation |

### Next Week
1. [Priority 1] - Expected outcome
2. [Priority 2] - Expected outcome
3. [Priority 3] - Expected outcome

### Help Needed
Any asks or decisions needed from stakeholders.

### Team Recognition
Shoutouts and acknowledgments.

Be concise but comprehensive. Lead with impact.
"""

        system_prompt = f"""You are an expert at executive communication, helping
{self.user_name} create clear, impactful status updates."""

        try:
            update = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.6
            )
            logger.info("Weekly update generated successfully")
            return update

        except Exception as e:
            logger.error(f"Error generating weekly update: {e}")
            raise

    def generate_executive_update(
        self,
        metrics: Optional[Dict[str, Any]] = None,
        highlights: Optional[List[str]] = None,
        risks: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate executive-level update

        Args:
            metrics: Key metrics data
            highlights: Major highlights
            risks: Current risks

        Returns:
            Executive update
        """
        logger.info("Generating executive update...")

        metrics_text = ""
        if metrics:
            for key, value in metrics.items():
                metrics_text += f"- {key}: {value}\n"
        else:
            metrics_text = "No metrics data available"

        prompt = f"""
ROLE: Executive Communication Expert
CONTEXT: Creating executive update for {self.user_name}

KEY METRICS:
{metrics_text}

HIGHLIGHTS:
{self.format_list(highlights or ['No highlights provided'])}

RISKS:
{self.format_list([r.get('risk', 'Unknown') for r in (risks or [])])}

TASK:
Create a concise executive update:

## Executive Update - {self.current_date}

### Bottom Line
One sentence on overall status.

### Key Metrics
| Metric | Current | Target | Trend |

### Highlights
- [Win with business impact]

### Risks & Asks
| Risk | Impact | Mitigation | Decision Needed |

### 30-Day Outlook
What to expect in the next month.

Keep it brief. Executives need the "so what" quickly.
"""

        system_prompt = """You are an expert at C-level communication. Be concise,
lead with impact, and make asks clear."""

        try:
            update = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1200,
                temperature=0.5
            )
            logger.info("Executive update generated successfully")
            return update

        except Exception as e:
            logger.error(f"Error generating executive update: {e}")
            raise

    def generate_meeting_agenda(
        self,
        meeting_type: str,
        attendees: List[str],
        topics: List[str],
        duration: int = 60
    ) -> str:
        """
        Generate meeting agenda

        Args:
            meeting_type: Type of meeting
            attendees: List of attendees
            topics: Topics to cover
            duration: Meeting duration in minutes

        Returns:
            Meeting agenda
        """
        logger.info(f"Generating agenda for {meeting_type}...")

        prompt = f"""
ROLE: Meeting Facilitator
CONTEXT: Creating agenda for {self.user_name}

MEETING TYPE: {meeting_type}
DURATION: {duration} minutes
ATTENDEES: {', '.join(attendees) if attendees else 'TBD'}

TOPICS TO COVER:
{self.format_list(topics or ['General discussion'])}

TASK:
Create a structured meeting agenda:

## {meeting_type}
**Date**: {self.current_date} | **Duration**: {duration} min

### Objective
What we need to accomplish in this meeting.

### Attendees
{', '.join(attendees) if attendees else 'TBD'}

### Agenda
| Time | Topic | Owner | Type |
Allocate time appropriately for {duration} minutes.
Type: Inform / Discuss / Decide

### Pre-read
Documents or context attendees should review.

### Success Criteria
Meeting is successful if:
1. [Outcome]
2. [Outcome]

### Parking Lot
Space for topics to defer.

Leave buffer time. Don't overschedule.
"""

        system_prompt = """You are an expert meeting facilitator. Create
focused, outcome-oriented agendas."""

        try:
            agenda = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1000,
                temperature=0.5
            )
            logger.info("Meeting agenda generated successfully")
            return agenda

        except Exception as e:
            logger.error(f"Error generating meeting agenda: {e}")
            raise

    def send_weekly_update_to_messaging(self, update: str) -> None:
        """Send weekly update to messaging"""
        messaging_client.send_status_update(f"📊 *Weekly Status Update*\n\n{update}")

    def send_executive_update_to_messaging(self, update: str) -> None:
        """Send executive update to messaging"""
        self.send_to_messaging(update, title="Executive Update")


# Global instance
stakeholder_agent = StakeholderAgent()


if __name__ == "__main__":
    print("Testing Stakeholder Agent...")
    print("=" * 50)

    try:
        update = stakeholder_agent.generate_weekly_update(
            accomplishments=[
                "Shipped new onboarding flow",
                "Completed user research for Feature X",
                "Reduced bug backlog by 30%"
            ],
            challenges=[
                {"issue": "API latency issues", "mitigation": "Working with backend team"},
            ],
            next_week=[
                "Launch A/B test for checkout",
                "Sprint planning for Q2"
            ]
        )
        print("\nGenerated Weekly Update:")
        print("-" * 50)
        print(update)
        print("\n" + "=" * 50)
        print("✅ Stakeholder Agent test successful")

    except Exception as e:
        print(f"❌ Test failed: {e}")
