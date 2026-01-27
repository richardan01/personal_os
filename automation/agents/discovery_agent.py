"""
Discovery Agent - User research and feedback synthesis
Handles interview analysis, feedback processing, and persona development
"""

from typing import Dict, List, Any, Optional
from loguru import logger

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.base_agent import BaseAgent
from utils.messaging_client import messaging_client


class DiscoveryAgent(BaseAgent):
    """Handles user research and feedback analysis"""

    def __init__(self):
        super().__init__("Discovery Agent", "🔍")

    def run_workflow(self, **kwargs) -> str:
        """Run the discovery workflow"""
        workflow_type = kwargs.get("workflow_type", "feedback_digest")

        if workflow_type == "feedback_digest":
            return self.generate_feedback_digest(
                feedback_items=kwargs.get("feedback_items", [])
            )
        elif workflow_type == "interview_synthesis":
            return self.synthesize_interview(
                interview_notes=kwargs.get("interview_notes", "")
            )
        else:
            return self.generate_feedback_digest()

    def generate_feedback_digest(
        self,
        feedback_items: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Generate a digest of recent customer feedback

        Args:
            feedback_items: List of feedback items with source, content, type

        Returns:
            Synthesized feedback digest
        """
        logger.info("Generating feedback digest...")

        if feedback_items:
            feedback_text = ""
            for item in feedback_items:
                feedback_text += f"- [{item.get('type', 'General')}] {item.get('content', '')} (Source: {item.get('source', 'Unknown')})\n"
        else:
            feedback_text = "No new feedback to process"

        prompt = f"""
ROLE: User Research Analyst
CONTEXT: Processing customer feedback for {self.user_name}, {self.user_role}

TODAY: {self.current_date}

STRATEGIC PRIORITIES:
{self.format_list(self.strategic_priorities)}

RECENT FEEDBACK:
{feedback_text}

TASK:
Create a feedback digest following this format:

## Feedback Digest - {self.current_date}

### Summary
2-3 sentence overview of today's feedback themes.

### Feedback by Category
| Type | Count | Key Theme |
Categorize as: Bug, Feature Request, UX Issue, Praise, Question

### High-Priority Items
Items that need immediate attention:
- [Item] - Why urgent: [Reason]

### Patterns Emerging
Recurring themes across feedback.

### Notable Quotes
Direct quotes worth preserving.

### Recommended Actions
1. Quick Win: [Something actionable now]
2. Investigate: [Something needing research]
3. Backlog: [Add to product backlog]

### Connection to Priorities
How does this feedback relate to strategic priorities?

Be specific and actionable. Preserve user voice where impactful.
"""

        system_prompt = f"""You are a user research analyst helping {self.user_name}
understand customer needs and feedback patterns. Focus on actionable insights."""

        try:
            digest = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.6
            )
            logger.info("Feedback digest generated successfully")
            return digest

        except Exception as e:
            logger.error(f"Error generating feedback digest: {e}")
            raise

    def synthesize_interview(
        self,
        interview_notes: str,
        interviewee_type: Optional[str] = None
    ) -> str:
        """
        Synthesize user interview notes into structured insights

        Args:
            interview_notes: Raw interview notes
            interviewee_type: Type of user interviewed

        Returns:
            Synthesized interview insights
        """
        logger.info("Synthesizing interview notes...")

        prompt = f"""
ROLE: User Research Synthesizer
CONTEXT: Analyzing interview notes for {self.user_name}

INTERVIEW NOTES:
{interview_notes}

INTERVIEWEE TYPE: {interviewee_type or "Not specified"}

TASK:
Synthesize these interview notes:

## Interview Synthesis

### Key Insights
1. [Major insight with supporting evidence]
2. [Major insight with supporting evidence]

### Pain Points Identified
| Pain Point | Severity | Quote/Evidence |

### Jobs-to-be-Done
What job is the user trying to accomplish?
- Main job: [Job description]
- Related jobs: [Supporting jobs]

### Feature Requests (with underlying needs)
| What They Said | What They Need | Priority |

### Notable Quotes
> "[Direct quote]" - Context: [When/why they said it]

### Surprises or Unexpected Findings
Things that challenged assumptions.

### Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]

### Follow-up Questions
Questions to explore in future interviews.

Focus on the "why" behind what users say.
"""

        system_prompt = """You are an expert user researcher skilled at extracting
deep insights from interview notes. Look for underlying needs, not just stated wants."""

        try:
            synthesis = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.6
            )
            logger.info("Interview synthesis generated successfully")
            return synthesis

        except Exception as e:
            logger.error(f"Error synthesizing interview: {e}")
            raise

    def send_feedback_digest_to_messaging(self, digest: str) -> None:
        """Send feedback digest to messaging"""
        self.send_to_messaging(digest, title="Daily Feedback Digest")

    def send_interview_synthesis_to_messaging(self, synthesis: str) -> None:
        """Send interview synthesis to messaging"""
        self.send_to_messaging(synthesis, title="Interview Synthesis")


# Global instance
discovery_agent = DiscoveryAgent()


if __name__ == "__main__":
    print("Testing Discovery Agent...")
    print("=" * 50)

    try:
        # Test feedback digest
        digest = discovery_agent.generate_feedback_digest(
            feedback_items=[
                {"type": "Feature Request", "content": "Need dark mode", "source": "Support ticket"},
                {"type": "Bug", "content": "App crashes on login", "source": "App Store review"},
                {"type": "Praise", "content": "Love the new dashboard!", "source": "Email"},
            ]
        )
        print("\nGenerated Feedback Digest:")
        print("-" * 50)
        print(digest)
        print("\n" + "=" * 50)
        print("✅ Discovery Agent test successful")

    except Exception as e:
        print(f"❌ Test failed: {e}")
