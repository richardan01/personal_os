"""
Execution Agent - Daily Planning and Task Management
Automates daily plan generation, progress tracking, and summaries
"""

from datetime import datetime, date
from typing import Dict, List, Any, Optional
from loguru import logger
from config import settings
from utils.ai_client import ai_client
from utils.messaging_client import messaging_client


class ExecutionAgent:
    """Handles daily execution planning and tracking"""

    def __init__(self):
        self.name = "Execution Agent"
        logger.info(f"Initialized {self.name}")

    def generate_daily_plan(
        self,
        calendar_events: List[Dict[str, Any]],
        open_tasks: List[Dict[str, Any]],
        strategic_priorities: Optional[List[str]] = None,
    ) -> str:
        """
        Generate a daily execution plan

        Args:
            calendar_events: List of today's meetings/events
            open_tasks: List of open tasks with deadlines
            strategic_priorities: Optional list of strategic priorities

        Returns:
            Generated daily plan as formatted string
        """
        logger.info("Generating daily plan...")

        # Prepare context
        current_date = date.today().strftime("%Y-%m-%d")
        day_of_week = date.today().strftime("%A")

        # Format calendar events
        calendar_text = self._format_calendar_events(calendar_events)

        # Format tasks
        tasks_text = self._format_tasks(open_tasks)

        # Get strategic priorities
        priorities = strategic_priorities or settings.priorities_list

        # Build the prompt
        prompt = f"""
ROLE: Personal Chief of Staff
CONTEXT: Planning optimal workday for maximum impact

TODAY'S DATE: {current_date} ({day_of_week})

CALENDAR EVENTS:
{calendar_text}

OPEN TASKS:
{tasks_text}

STRATEGIC PRIORITIES:
{chr(10).join(f'- {p}' for p in priorities)}

TASK:
Create a detailed daily execution plan following this format:

## Daily Execution Plan - {current_date}

### Day Overview
- Available Focus Time: [Calculate based on meetings]
- Meetings: [Count and total time]
- Energy Forecast: [How demanding is this day?]

### Top 3 Priorities
List the 3 most important tasks to complete today, considering:
- Deadlines and urgency
- Strategic alignment
- Available time blocks

For each priority:
1. **[Task Name]** - [Why it matters] - [Time needed]
   - Links to: [Strategic goal if applicable]
   - Deadline: [Date]

### Time-Blocked Schedule
Create hour-by-hour schedule with:
- Focus blocks for priorities
- Meeting times with prep/follow-up
- Buffer time
- Breaks

### Meeting Preparation
For each meeting, note:
- What prep is needed
- Objective for the meeting

### Success Criteria
List 3 specific outcomes that would make today successful.

### Potential Risks
Flag any scheduling conflicts or overcommitment.

Be realistic about time. Better to under-promise and over-deliver.
"""

        system_prompt = f"""You are an expert productivity advisor helping {settings.user_name},
a {settings.user_role} at {settings.company_name}, plan their day for maximum effectiveness."""

        try:
            plan = ai_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.7
            )

            logger.info("Daily plan generated successfully")
            return plan

        except Exception as e:
            logger.error(f"Error generating daily plan: {e}")
            raise

    def generate_progress_check(
        self,
        morning_plan: str,
        completed_tasks: List[str],
        in_progress_tasks: List[str],
        pending_tasks: List[str],
    ) -> str:
        """
        Generate mid-day progress check and adjustments

        Args:
            morning_plan: The plan generated this morning
            completed_tasks: Tasks completed so far
            in_progress_tasks: Tasks currently being worked on
            pending_tasks: Tasks not yet started

        Returns:
            Progress check with recommendations
        """
        logger.info("Generating progress check...")

        current_time = datetime.now().strftime("%I:%M %p")

        prompt = f"""
ROLE: Project Delivery Monitor
CONTEXT: Mid-day check-in to ensure on track

CURRENT TIME: {current_time}

MORNING PLAN:
{morning_plan}

PROGRESS SO FAR:
Completed:
{chr(10).join(f'- {task}' for task in completed_tasks) if completed_tasks else '- None yet'}

In Progress:
{chr(10).join(f'- {task}' for task in in_progress_tasks) if in_progress_tasks else '- None'}

Not Started:
{chr(10).join(f'- {task}' for task in pending_tasks) if pending_tasks else '- None'}

TASK:
Assess progress and provide course corrections if needed.

## Mid-Day Progress Check - {current_time}

### Progress Score: [X/10]
Rate overall progress and explain.

### ✅ Completed Today
List what's been accomplished with impact level.

### Status Assessment
Are we: Ahead of schedule / On track / Behind / Significantly behind
Explain why.

### Recommended Adjustments
If behind, what should we:
- Defer to tomorrow?
- Timebox?
- Get help with?

If on track:
- Any opportunities to tackle stretch goals?

### Afternoon Plan (Revised)
Based on current progress, what's the best use of remaining time?

### Energy & Motivation Check
Quick morale boost or recommendation for managing energy.
"""

        system_prompt = "You are a supportive productivity coach helping assess progress and adjust plans."

        try:
            progress = ai_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.7
            )

            logger.info("Progress check generated successfully")
            return progress

        except Exception as e:
            logger.error(f"Error generating progress check: {e}")
            raise

    def generate_daily_summary(
        self,
        morning_plan: str,
        completed_tasks: List[str],
        incomplete_tasks: List[str],
        blockers: List[Dict[str, str]],
        time_spent: Optional[Dict[str, int]] = None,
    ) -> str:
        """
        Generate end-of-day summary and tomorrow prep

        Args:
            morning_plan: Original plan for today
            completed_tasks: Tasks completed
            incomplete_tasks: Tasks not completed
            blockers: List of blockers encountered
            time_spent: Optional dict of time allocation

        Returns:
            Daily summary with tomorrow's prep
        """
        logger.info("Generating daily summary...")

        current_date = date.today().strftime("%Y-%m-%d")

        prompt = f"""
ROLE: End-of-Day Analyst
CONTEXT: Reviewing today's execution and setting up tomorrow

TODAY: {current_date}

ORIGINAL PLAN:
{morning_plan}

COMPLETED TASKS:
{chr(10).join(f'- {task}' for task in completed_tasks)}

INCOMPLETE TASKS:
{chr(10).join(f'- {task}' for task in incomplete_tasks)}

BLOCKERS:
{chr(10).join(f'- {b.get("task", "Unknown")}: {b.get("blocker", "")}' for b in blockers) if blockers else '- None'}

TASK:
Create a comprehensive end-of-day summary.

## Daily Execution Summary - {current_date}

### Achievement Score: [X/10]
Overall rating for the day.

### ✅ Completed
List completed tasks with outcomes.

**Completion Rate**: [X/Y tasks] = [Z%]

### ⏭️ Rolled to Tomorrow
Tasks not completed and why.

### 🚧 Blockers Encountered
List blockers with:
- Impact level
- Who can resolve
- Next action

### What Went Well ✨
Celebrate wins, even small ones.

### What Could Be Better 🔄
Honest assessment of challenges.

### Key Learnings
Insights about work patterns or productivity.

### Tomorrow's Priorities (Draft)
Based on rollovers and upcoming deadlines, suggest top 3 for tomorrow.

### Gratitude & Motivation 💪
End on a positive note with encouragement.
"""

        system_prompt = "You are a reflective coach helping process the day and prepare for tomorrow."

        try:
            summary = ai_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.7
            )

            logger.info("Daily summary generated successfully")
            return summary

        except Exception as e:
            logger.error(f"Error generating daily summary: {e}")
            raise

    def send_daily_plan_to_messaging(self, plan: str) -> None:
        """Send the daily plan to configured messaging platforms"""
        logger.info("Sending daily plan to messaging platforms...")

        try:
            messaging_client.send_daily_plan(plan)
            logger.info("Daily plan sent successfully")
        except Exception as e:
            logger.error(f"Error sending daily plan: {e}")

    def send_progress_check_to_messaging(self, progress: str) -> None:
        """Send progress check to messaging platforms"""
        logger.info("Sending progress check to messaging platforms...")

        try:
            messaging_client.send_dm(f"📊 *Mid-Day Progress Check*\n\n{progress}")
            logger.info("Progress check sent successfully")
        except Exception as e:
            logger.error(f"Error sending progress check: {e}")

    def send_daily_summary_to_messaging(self, summary: str) -> None:
        """Send daily summary to messaging platforms"""
        logger.info("Sending daily summary to messaging platforms...")

        try:
            messaging_client.send_dm(f"🌟 *Daily Summary*\n\n{summary}")
            logger.info("Daily summary sent successfully")
        except Exception as e:
            logger.error(f"Error sending daily summary to Slack: {e}")

    # Helper methods
    def _format_calendar_events(self, events: List[Dict[str, Any]]) -> str:
        """Format calendar events for the prompt"""
        if not events:
            return "- No meetings scheduled"

        formatted = []
        for event in events:
            time = event.get("time", "TBD")
            title = event.get("title", "Untitled")
            duration = event.get("duration", "")
            formatted.append(f"- {time}: {title} ({duration})")

        return "\n".join(formatted)

    def _format_tasks(self, tasks: List[Dict[str, Any]]) -> str:
        """Format tasks for the prompt"""
        if not tasks:
            return "- No open tasks"

        formatted = []
        for task in tasks:
            title = task.get("title", "Untitled")
            deadline = task.get("deadline", "No deadline")
            priority = task.get("priority", "Medium")
            estimate = task.get("estimate", "Unknown")
            formatted.append(f"- [{priority}] {title} - Due: {deadline} - Est: {estimate}")

        return "\n".join(formatted)


# Global execution agent instance
execution_agent = ExecutionAgent()


if __name__ == "__main__":
    # Test the execution agent
    print("Testing Execution Agent...")
    print("=" * 50)

    # Sample data
    sample_events = [
        {"time": "9:30 AM", "title": "Team Standup", "duration": "15 min"},
        {"time": "2:00 PM", "title": "Product Review", "duration": "1 hour"},
    ]

    sample_tasks = [
        {
            "title": "Finish PRD for Feature X",
            "deadline": "Friday",
            "priority": "High",
            "estimate": "4 hours"
        },
        {
            "title": "Review design mocks",
            "deadline": "Today",
            "priority": "High",
            "estimate": "1 hour"
        },
        {
            "title": "Respond to customer feedback",
            "deadline": "This week",
            "priority": "Medium",
            "estimate": "30 min"
        },
    ]

    try:
        plan = execution_agent.generate_daily_plan(
            calendar_events=sample_events,
            open_tasks=sample_tasks,
        )

        print("\nGenerated Daily Plan:")
        print("-" * 50)
        print(plan)
        print("\n" + "=" * 50)
        print("✅ Execution Agent test successful")

    except Exception as e:
        print(f"❌ Test failed: {e}")
