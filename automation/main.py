"""
Personal OS - Main Automation Runner
Coordinates all agents and runs scheduled workflows
"""

import schedule
import time
from datetime import datetime
from loguru import logger
from config import settings, validate_configuration
from agents.execution_agent import execution_agent
from agents.stakeholder_discovery_agent import stakeholder_discovery_agent

# Configure logging
logger.add(
    settings.log_file,
    rotation="1 week",
    retention="1 month",
    level=settings.log_level,
)


class PersonalOS:
    """Main coordinator for Personal OS automation"""

    def __init__(self):
        logger.info("Initializing Personal OS...")

        # Validate configuration
        if not validate_configuration():
            logger.error("Configuration validation failed. Please check your .env file.")
            raise ValueError("Invalid configuration")

        self.setup_schedules()
        logger.info("Personal OS initialized successfully")

    def setup_schedules(self):
        """Set up all scheduled jobs"""
        logger.info("Setting up schedules...")

        # Execution Agent Schedules
        if settings.enable_execution_agent:
            # Morning daily plan
            schedule.every().day.at(settings.execution_agent_morning_time).do(
                self.run_morning_daily_plan
            )
            logger.info(f"Scheduled morning daily plan at {settings.execution_agent_morning_time}")

            # Midday progress check
            schedule.every().day.at(settings.execution_agent_midday_time).do(
                self.run_midday_progress_check
            )
            logger.info(f"Scheduled midday check at {settings.execution_agent_midday_time}")

            # Evening summary
            schedule.every().day.at(settings.execution_agent_evening_time).do(
                self.run_evening_summary
            )
            logger.info(f"Scheduled evening summary at {settings.execution_agent_evening_time}")

        # Strategy Agent Schedules
        if settings.enable_strategy_agent:
            # Daily strategy check (same as morning plan)
            schedule.every().day.at(settings.strategy_agent_morning_time).do(
                self.run_strategy_check
            )
            logger.info(f"Scheduled strategy check at {settings.strategy_agent_morning_time}")

        # Stakeholder Agent Schedules
        if settings.enable_stakeholder_agent:
            # Weekly status update
            day, time_str = settings.stakeholder_agent_weekly_update_time.split()
            getattr(schedule.every(), day.lower()).at(time_str).do(
                self.run_weekly_stakeholder_discovery
            )
            logger.info(f"Scheduled weekly update at {settings.stakeholder_agent_weekly_update_time}")

        # Discovery Agent Schedules
        if settings.enable_discovery_agent:
            # Daily feedback digest
            schedule.every().day.at(settings.discovery_agent_daily_digest_time).do(
                self.run_feedback_digest
            )
            logger.info(f"Scheduled feedback digest at {settings.discovery_agent_daily_digest_time}")

    # ==================== Execution Agent Jobs ====================

    def run_morning_daily_plan(self):
        """Generate and send morning daily plan"""
        logger.info("Running morning daily plan workflow...")

        try:
            # Get calendar events from Google Calendar
            calendar_events = self._get_todays_calendar_events()
            open_tasks = self._get_open_tasks()

            # Generate the plan
            plan = execution_agent.generate_daily_plan(
                calendar_events=calendar_events,
                open_tasks=open_tasks,
            )

            # Log the plan (output via Google Docs or other method)
            logger.info(f"Daily Plan Generated:\n{plan}")

            logger.info("Morning daily plan completed successfully")

        except Exception as e:
            logger.error(f"Error in morning daily plan: {e}")

    def run_midday_progress_check(self):
        """Generate and send midday progress check"""
        logger.info("Running midday progress check workflow...")

        try:
            # TODO: Track actual progress during the day
            morning_plan = "Check your morning plan for context"
            completed = ["Completed task 1", "Completed task 2"]
            in_progress = ["Working on task 3"]
            pending = ["Task 4 pending", "Task 5 pending"]

            # Generate progress check
            progress = execution_agent.generate_progress_check(
                morning_plan=morning_plan,
                completed_tasks=completed,
                in_progress_tasks=in_progress,
                pending_tasks=pending,
            )

            logger.info(f"Progress Check:\n{progress}")
            logger.info("Midday progress check completed successfully")

        except Exception as e:
            logger.error(f"Error in midday progress check: {e}")

    def run_evening_summary(self):
        """Generate and send evening summary"""
        logger.info("Running evening summary workflow...")

        try:
            morning_plan = "Check morning plan for context"
            completed = ["Completed priority 1", "Completed priority 2"]
            incomplete = ["Priority 3 - partially done"]
            blockers = [
                {"task": "Feature X", "blocker": "Waiting on design review"}
            ]

            # Generate summary
            summary = execution_agent.generate_daily_summary(
                morning_plan=morning_plan,
                completed_tasks=completed,
                incomplete_tasks=incomplete,
                blockers=blockers,
            )

            logger.info(f"Daily Summary:\n{summary}")
            logger.info("Evening summary completed successfully")

        except Exception as e:
            logger.error(f"Error in evening summary: {e}")

    # ==================== Strategy Agent Jobs ====================

    def run_strategy_check(self):
        """Run daily strategy alignment check"""
        logger.info("Running strategy check workflow...")

        try:
            # TODO: Implement strategy agent
            logger.info("Strategy check placeholder - Coming soon!")
            logger.info("Strategy check completed")

        except Exception as e:
            logger.error(f"Error in strategy check: {e}")

    # ==================== Stakeholder Agent Jobs ====================

    def run_weekly_stakeholder_discovery(self):
        """Run weekly stakeholder discovery analysis"""
        logger.info("Running weekly stakeholder discovery workflow...")

        try:
            # Run discovery on recent notes
            report = stakeholder_discovery_agent.analyze_recent_notes(
                days=7,
                report_title=f"Weekly Stakeholder Discovery - {datetime.now().strftime('%Y-%m-%d')}",
            )

            logger.info(f"Stakeholder discovery completed")
            logger.info(f"Report: {report.google_doc_url or 'Not saved'}")
            logger.info(f"Stakeholders analyzed: {len(report.stakeholder_profiles)}")

        except Exception as e:
            logger.error(f"Error in stakeholder discovery: {e}")

    # ==================== Discovery Agent Jobs ====================

    def run_feedback_digest(self):
        """Generate and send feedback digest"""
        logger.info("Running feedback digest workflow...")

        try:
            # TODO: Implement discovery agent
            logger.info("Feedback digest placeholder - Coming soon!")
            logger.info("Feedback digest completed")

        except Exception as e:
            logger.error(f"Error in feedback digest: {e}")

    # ==================== Helper Methods ====================

    def _get_todays_calendar_events(self):
        """Fetch today's calendar events from Google Calendar"""
        try:
            from utils.google.calendar_client import calendar_client

            events = calendar_client.get_todays_events()
            formatted_events = []

            for event in events:
                start = event.get("start", {})
                start_time = start.get("dateTime", start.get("date", ""))

                formatted_events.append({
                    "time": start_time,
                    "title": event.get("summary", "No title"),
                    "duration": "See calendar",
                })

            return formatted_events

        except Exception as e:
            logger.warning(f"Could not fetch calendar events: {e}")
            # Return placeholder data
            return [
                {"time": "9:00 AM", "title": "Team Standup", "duration": "15 min"},
                {"time": "2:00 PM", "title": "Product Review", "duration": "1 hour"},
            ]

    def _get_open_tasks(self):
        """Fetch open tasks from Google Tasks"""
        try:
            from utils.google.tasks_client import tasks_client

            tasks = tasks_client.get_pending_tasks()
            formatted_tasks = []

            for task in tasks:
                formatted_tasks.append({
                    "title": task.get("title", "Untitled"),
                    "deadline": task.get("due", "No deadline"),
                    "priority": "Medium",
                    "estimate": "Unknown",
                })

            return formatted_tasks

        except Exception as e:
            logger.warning(f"Could not fetch tasks: {e}")
            # Return placeholder data
            return [
                {
                    "title": "Complete PRD for Feature X",
                    "deadline": "Friday",
                    "priority": "High",
                    "estimate": "4 hours"
                },
                {
                    "title": "Review design mockups",
                    "deadline": "Today",
                    "priority": "High",
                    "estimate": "1 hour"
                },
            ]

    def run(self):
        """Start the Personal OS automation loop"""
        logger.info("Personal OS is now running...")
        logger.info("Press Ctrl+C to stop")

        # Log startup
        startup_message = f"""
Personal OS Started

Enabled agents:
{'- Execution Agent' if settings.enable_execution_agent else ''}
{'- Strategy Agent' if settings.enable_strategy_agent else ''}
{'- Discovery Agent' if settings.enable_discovery_agent else ''}
{'- Stakeholder Agent' if settings.enable_stakeholder_agent else ''}

Next scheduled run: {schedule.next_run()}

{'DRY RUN MODE - No actual changes will be made' if settings.dry_run else ''}
"""
        logger.info(startup_message)

        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            logger.info("Personal OS stopped by user")

        except Exception as e:
            logger.error(f"Critical error in Personal OS: {e}")
            raise


def main():
    """Main entry point"""
    print("""
================================================================

              PERSONAL OS - AUTOMATION SYSTEM

   Automating your product management workflows
   Powered by Google Workspace + AI

================================================================
""")

    try:
        personal_os = PersonalOS()
        personal_os.run()

    except Exception as e:
        logger.error(f"Failed to start Personal OS: {e}")
        print(f"\nError: {e}")
        print("\nPlease check your configuration and try again.")
        exit(1)


if __name__ == "__main__":
    main()
