"""
Task Creator Skill - Create tasks in Google Tasks
"""

from typing import List, Optional
from datetime import datetime, timedelta
from loguru import logger

from utils.google.tasks_client import tasks_client
from models.action import ActionItem
from models.enums import ActionStatus


class TaskCreator:
    """
    Skill for creating and managing tasks in Google Tasks.

    Capabilities:
    - Create tasks from action items
    - Create follow-up tasks for stakeholders
    - Batch create multiple tasks
    - Get pending follow-ups
    """

    def __init__(self):
        self.tasks = tasks_client

    def create_task(
        self,
        title: str,
        notes: Optional[str] = None,
        due_date: Optional[datetime] = None,
        task_list_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a new task.

        Args:
            title: Task title
            notes: Task notes/description
            due_date: Due date
            task_list_id: Task list ID

        Returns:
            Task ID or None
        """
        logger.info(f"Creating task: {title}")

        task_id = self.tasks.create_task(
            title=title,
            notes=notes,
            due_date=due_date,
            task_list_id=task_list_id,
        )

        if task_id:
            logger.info(f"Created task with ID: {task_id}")
        else:
            logger.warning(f"Failed to create task: {title}")

        return task_id

    def create_from_action_item(
        self,
        action_item: ActionItem,
        task_list_id: Optional[str] = None,
    ) -> ActionItem:
        """
        Create a Google Task from an ActionItem.

        Args:
            action_item: The action item to create
            task_list_id: Task list ID

        Returns:
            Updated ActionItem with google_task_id
        """
        logger.info(f"Creating task from action item: {action_item.title}")

        # Build notes
        notes_parts = []
        if action_item.description:
            notes_parts.append(action_item.description)
        if action_item.stakeholder:
            notes_parts.append(f"Stakeholder: {action_item.stakeholder}")
        if action_item.source_doc_id:
            notes_parts.append(f"Source: {action_item.source_doc_id}")

        notes = "\n".join(notes_parts) if notes_parts else None

        task_id = self.tasks.create_task(
            title=action_item.title,
            notes=notes,
            due_date=action_item.due_date,
            task_list_id=task_list_id,
        )

        if task_id:
            action_item.google_task_id = task_id
            logger.info(f"Linked action item to Google Task: {task_id}")

        return action_item

    def create_follow_up(
        self,
        stakeholder: str,
        topic: str,
        due_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        task_list_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a stakeholder follow-up task.

        Args:
            stakeholder: Stakeholder name
            topic: Follow-up topic
            due_date: Due date (defaults to 1 week from now)
            notes: Additional notes
            task_list_id: Task list ID

        Returns:
            Task ID or None
        """
        logger.info(f"Creating follow-up task for {stakeholder}: {topic}")

        # Default due date to 1 week from now
        if not due_date:
            due_date = datetime.utcnow() + timedelta(days=7)

        return self.tasks.create_follow_up_task(
            stakeholder=stakeholder,
            topic=topic,
            due_date=due_date,
            notes=notes,
            task_list_id=task_list_id,
        )

    def batch_create(
        self,
        action_items: List[ActionItem],
        task_list_id: Optional[str] = None,
    ) -> List[ActionItem]:
        """
        Create multiple tasks from action items.

        Args:
            action_items: List of action items
            task_list_id: Task list ID

        Returns:
            List of updated action items with google_task_ids
        """
        logger.info(f"Batch creating {len(action_items)} tasks")

        updated_items = []
        for item in action_items:
            updated = self.create_from_action_item(item, task_list_id)
            updated_items.append(updated)

        created_count = sum(1 for item in updated_items if item.google_task_id)
        logger.info(f"Successfully created {created_count}/{len(action_items)} tasks")

        return updated_items

    def get_pending_follow_ups(
        self,
        task_list_id: Optional[str] = None,
    ) -> List[dict]:
        """
        Get pending follow-up tasks.

        Args:
            task_list_id: Task list ID

        Returns:
            List of pending tasks
        """
        logger.info("Getting pending follow-up tasks")

        tasks = self.tasks.get_pending_tasks(task_list_id)

        # Filter for follow-up tasks
        follow_ups = [
            t for t in tasks
            if "follow up" in t.get("title", "").lower()
        ]

        logger.info(f"Found {len(follow_ups)} pending follow-ups")
        return follow_ups

    def complete_task(
        self,
        task_id: str,
        task_list_id: Optional[str] = None,
    ) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id: Task ID
            task_list_id: Task list ID

        Returns:
            True if successful
        """
        logger.info(f"Completing task: {task_id}")
        return self.tasks.complete_task(task_id, task_list_id)

    def sync_action_item_status(
        self,
        action_item: ActionItem,
        task_list_id: Optional[str] = None,
    ) -> ActionItem:
        """
        Sync action item status with Google Task.

        Args:
            action_item: Action item to sync
            task_list_id: Task list ID

        Returns:
            Updated action item
        """
        if not action_item.google_task_id:
            return action_item

        task = self.tasks.get_task(action_item.google_task_id, task_list_id)
        if task:
            status = task.get("status", "needsAction")
            if status == "completed":
                action_item.status = ActionStatus.COMPLETED
            else:
                action_item.status = ActionStatus.PENDING

        return action_item

    def create_task_list(self, title: str) -> Optional[str]:
        """
        Create a new task list.

        Args:
            title: Task list title

        Returns:
            Task list ID or None
        """
        logger.info(f"Creating task list: {title}")
        return self.tasks.create_task_list(title)

    def get_or_create_stakeholder_list(self) -> Optional[str]:
        """
        Get or create a task list for stakeholder follow-ups.

        Returns:
            Task list ID or None
        """
        # Check if list exists
        task_lists = self.tasks.list_task_lists()
        for tl in task_lists:
            if "stakeholder" in tl.get("title", "").lower():
                return tl.get("id")

        # Create if not exists
        return self.create_task_list("Stakeholder Follow-ups")


# Global instance
task_creator = TaskCreator()
