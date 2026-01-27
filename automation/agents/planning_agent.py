"""
Planning Agent - Backlog and sprint management
Handles prioritization, sprint planning, and capacity management
"""

from typing import Dict, List, Any, Optional
from loguru import logger

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.base_agent import BaseAgent
from utils.messaging_client import messaging_client


class PlanningAgent(BaseAgent):
    """Handles backlog management and sprint planning"""

    def __init__(self):
        super().__init__("Planning Agent", "📋")

    def run_workflow(self, **kwargs) -> str:
        """Run the planning workflow"""
        workflow_type = kwargs.get("workflow_type", "sprint_plan")

        if workflow_type == "sprint_plan":
            return self.generate_sprint_plan(
                backlog_items=kwargs.get("backlog_items", []),
                team_capacity=kwargs.get("team_capacity", {}),
                sprint_length=kwargs.get("sprint_length", 14)
            )
        elif workflow_type == "prioritization":
            return self.prioritize_backlog(
                items=kwargs.get("items", []),
                method=kwargs.get("method", "RICE")
            )
        else:
            return self.generate_sprint_plan()

    def generate_sprint_plan(
        self,
        backlog_items: Optional[List[Dict[str, Any]]] = None,
        team_capacity: Optional[Dict[str, Any]] = None,
        sprint_length: int = 14
    ) -> str:
        """
        Generate a sprint plan

        Args:
            backlog_items: List of backlog items to consider
            team_capacity: Team capacity information
            sprint_length: Sprint length in days

        Returns:
            Sprint plan
        """
        logger.info("Generating sprint plan...")

        if backlog_items:
            items_text = ""
            for item in backlog_items:
                items_text += f"- [{item.get('priority', 'Medium')}] {item.get('title', 'Untitled')} - {item.get('estimate', 'Unknown')} points\n"
        else:
            items_text = "No backlog items provided"

        capacity_text = ""
        if team_capacity:
            capacity_text = f"""
Team Size: {team_capacity.get('team_size', 'Unknown')}
Velocity: {team_capacity.get('velocity', 'Unknown')} points/sprint
Availability: {team_capacity.get('availability', '100')}%
"""
        else:
            capacity_text = "No capacity data - using estimates"

        prompt = f"""
ROLE: Agile Coach and Sprint Planner
CONTEXT: Planning sprint for {self.user_name}, {self.user_role}

SPRINT LENGTH: {sprint_length} days

TEAM CAPACITY:
{capacity_text}

BACKLOG ITEMS:
{items_text}

STRATEGIC PRIORITIES:
{self.format_list(self.strategic_priorities)}

TASK:
Create a sprint plan:

## Sprint Plan

### Sprint Goal
One clear, measurable objective for this sprint.

### Capacity Analysis
- Gross Capacity: [X points]
- Buffer (20%): [X points]
- Net Capacity: [X points]

### Committed Items

#### P0 - Must Complete
| Item | Points | Owner | Dependencies |

#### P1 - Should Complete
| Item | Points | Owner | Dependencies |

#### P2 - Stretch Goals
| Item | Points | Owner | Dependencies |

### Total Committed: [X points] / [Y capacity]

### Dependencies & Risks
| Dependency | Status | Risk | Mitigation |

### Sprint Schedule
- Day 1-2: [Focus]
- Day 3-7: [Focus]
- Day 8-12: [Focus]
- Day 13-14: [Testing/Polish]

### Success Criteria
Sprint is successful if:
1. [Measurable outcome]
2. [Measurable outcome]

### Not This Sprint
Items explicitly deferred with reason.

Be realistic about capacity. Leave room for unknowns.
"""

        system_prompt = f"""You are an agile coach helping {self.user_name} plan
an effective sprint. Focus on realistic commitments and clear priorities."""

        try:
            plan = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1800,
                temperature=0.6
            )
            logger.info("Sprint plan generated successfully")
            return plan

        except Exception as e:
            logger.error(f"Error generating sprint plan: {e}")
            raise

    def prioritize_backlog(
        self,
        items: List[Dict[str, Any]],
        method: str = "RICE"
    ) -> str:
        """
        Prioritize backlog items using specified method

        Args:
            items: List of items to prioritize
            method: Prioritization method (RICE, MoSCoW, Value/Effort)

        Returns:
            Prioritized list with scores
        """
        logger.info(f"Prioritizing backlog using {method}...")

        items_text = ""
        for item in items:
            items_text += f"- {item.get('title', 'Untitled')}: {item.get('description', 'No description')}\n"

        prompt = f"""
ROLE: Product Prioritization Expert
CONTEXT: Prioritizing backlog for {self.user_name}

METHOD: {method}

ITEMS TO PRIORITIZE:
{items_text}

STRATEGIC PRIORITIES:
{self.format_list(self.strategic_priorities)}

TASK:
Prioritize these items using {method}:

## Prioritization Analysis - {method}

### Scoring Criteria
Explain how {method} scoring works.

### Scored Items
| Rank | Item | Score | Breakdown |

### Recommendations
1. **Do First**: [Item] - Why
2. **Do Next**: [Item] - Why
3. **Consider Later**: [Item] - Why
4. **Don't Do**: [Item] - Why

### Trade-offs to Consider
Key decisions that affect prioritization.

### Alignment Check
How does this ranking align with strategic priorities?

Be objective and data-driven in scoring.
"""

        system_prompt = """You are a prioritization expert. Apply the framework
rigorously and explain your reasoning."""

        try:
            prioritization = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.5
            )
            logger.info("Prioritization complete")
            return prioritization

        except Exception as e:
            logger.error(f"Error prioritizing backlog: {e}")
            raise

    def send_sprint_plan_to_messaging(self, plan: str) -> None:
        """Send sprint plan to messaging"""
        self.send_to_messaging(plan, title="Sprint Plan")

    def send_prioritization_to_messaging(self, prioritization: str) -> None:
        """Send prioritization to messaging"""
        self.send_to_messaging(prioritization, title="Backlog Prioritization")


# Global instance
planning_agent = PlanningAgent()


if __name__ == "__main__":
    print("Testing Planning Agent...")
    print("=" * 50)

    try:
        plan = planning_agent.generate_sprint_plan(
            backlog_items=[
                {"title": "User authentication", "priority": "High", "estimate": 8},
                {"title": "Dashboard redesign", "priority": "Medium", "estimate": 5},
                {"title": "Bug fixes", "priority": "High", "estimate": 3},
            ],
            team_capacity={"team_size": 3, "velocity": 20, "availability": 80}
        )
        print("\nGenerated Sprint Plan:")
        print("-" * 50)
        print(plan)
        print("\n" + "=" * 50)
        print("✅ Planning Agent test successful")

    except Exception as e:
        print(f"❌ Test failed: {e}")
