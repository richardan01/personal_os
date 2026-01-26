"""
Google Tasks Client - Task management
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.google.base_client import google_base_client
from config import settings


class TasksClient:
    """Client for Google Tasks operations"""

    def __init__(self):
        self._service = None

    @property
    def service(self):
        """Lazy initialization of Tasks service"""
        if self._service is None and google_base_client.is_authenticated():
            self._service = build(
                "tasks", "v1", credentials=google_base_client.credentials
            )
        return self._service

    def list_task_lists(self) -> List[Dict[str, Any]]:
        """
        List all task lists.

        Returns:
            List of task list metadata dicts
        """
        if not self.service:
            logger.warning("Tasks service not initialized")
            return []

        try:
            task_lists = []
            page_token = None

            while True:
                response = self.service.tasklists().list(
                    pageToken=page_token
                ).execute()

                task_lists.extend(response.get("items", []))
                page_token = response.get("nextPageToken")

                if not page_token:
                    break

            logger.info(f"Listed {len(task_lists)} task lists")
            return task_lists

        except HttpError as e:
            logger.error(f"Failed to list task lists: {e}")
            return []

    def get_default_task_list(self) -> Optional[str]:
        """
        Get the default task list ID.

        Returns:
            Task list ID or None
        """
        task_lists = self.list_task_lists()
        if task_lists:
            return task_lists[0].get("id")
        return None

    def create_task_list(self, title: str) -> Optional[str]:
        """
        Create a new task list.

        Args:
            title: Task list title

        Returns:
            Task list ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would create task list: {title}")
            return "dry_run_tasklist_id"

        if not self.service:
            return None

        try:
            task_list = self.service.tasklists().insert(
                body={"title": title}
            ).execute()

            list_id = task_list.get("id")
            logger.info(f"Created task list '{title}' with ID: {list_id}")
            return list_id

        except HttpError as e:
            logger.error(f"Failed to create task list: {e}")
            return None

    def get_tasks(
        self,
        task_list_id: Optional[str] = None,
        show_completed: bool = False,
        show_hidden: bool = False,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get tasks from a task list.

        Args:
            task_list_id: Task list ID (defaults to primary)
            show_completed: Include completed tasks
            show_hidden: Include hidden tasks
            max_results: Maximum number of tasks

        Returns:
            List of task dicts
        """
        if not self.service:
            return []

        try:
            list_id = task_list_id or self.get_default_task_list() or "@default"

            tasks = []
            page_token = None

            while True:
                response = self.service.tasks().list(
                    tasklist=list_id,
                    showCompleted=show_completed,
                    showHidden=show_hidden,
                    maxResults=min(max_results - len(tasks), 100),
                    pageToken=page_token,
                ).execute()

                tasks.extend(response.get("items", []))
                page_token = response.get("nextPageToken")

                if not page_token or len(tasks) >= max_results:
                    break

            logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks[:max_results]

        except HttpError as e:
            logger.error(f"Failed to get tasks: {e}")
            return []

    def get_pending_tasks(
        self,
        task_list_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get pending (incomplete) tasks.

        Args:
            task_list_id: Task list ID

        Returns:
            List of pending tasks
        """
        tasks = self.get_tasks(task_list_id, show_completed=False)
        return [t for t in tasks if t.get("status") != "completed"]

    def get_task(
        self,
        task_id: str,
        task_list_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific task by ID.

        Args:
            task_id: The task ID
            task_list_id: Task list ID

        Returns:
            Task dict or None
        """
        if not self.service:
            return None

        try:
            list_id = task_list_id or self.get_default_task_list() or "@default"

            task = self.service.tasks().get(
                tasklist=list_id,
                task=task_id,
            ).execute()

            return task

        except HttpError as e:
            logger.error(f"Failed to get task {task_id}: {e}")
            return None

    def create_task(
        self,
        title: str,
        notes: Optional[str] = None,
        due_date: Optional[datetime] = None,
        task_list_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a new task.

        Args:
            title: Task title
            notes: Task notes/description
            due_date: Due date
            task_list_id: Task list ID
            parent_task_id: Parent task ID (for subtasks)

        Returns:
            Task ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would create task: {title}")
            return "dry_run_task_id"

        if not self.service:
            return None

        try:
            list_id = task_list_id or self.get_default_task_list() or "@default"

            task_body = {"title": title}

            if notes:
                task_body["notes"] = notes
            if due_date:
                # Google Tasks expects RFC 3339 format with date only
                task_body["due"] = due_date.strftime("%Y-%m-%dT00:00:00.000Z")

            params = {"tasklist": list_id, "body": task_body}
            if parent_task_id:
                params["parent"] = parent_task_id

            task = self.service.tasks().insert(**params).execute()

            task_id = task.get("id")
            logger.info(f"Created task '{title}' with ID: {task_id}")
            return task_id

        except HttpError as e:
            logger.error(f"Failed to create task: {e}")
            return None

    def update_task(
        self,
        task_id: str,
        task_list_id: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """
        Update an existing task.

        Args:
            task_id: The task ID
            task_list_id: Task list ID
            **kwargs: Fields to update (title, notes, due, status)

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would update task {task_id}")
            return True

        if not self.service:
            return False

        try:
            list_id = task_list_id or self.get_default_task_list() or "@default"

            # Get existing task
            task = self.get_task(task_id, list_id)
            if not task:
                return False

            # Update fields
            for key, value in kwargs.items():
                if key == "due_date" and value:
                    task["due"] = value.strftime("%Y-%m-%dT00:00:00.000Z")
                else:
                    task[key] = value

            self.service.tasks().update(
                tasklist=list_id,
                task=task_id,
                body=task,
            ).execute()

            logger.info(f"Updated task {task_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to update task: {e}")
            return False

    def complete_task(
        self,
        task_id: str,
        task_list_id: Optional[str] = None,
    ) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id: The task ID
            task_list_id: Task list ID

        Returns:
            True if successful
        """
        return self.update_task(task_id, task_list_id, status="completed")

    def uncomplete_task(
        self,
        task_id: str,
        task_list_id: Optional[str] = None,
    ) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id: The task ID
            task_list_id: Task list ID

        Returns:
            True if successful
        """
        return self.update_task(task_id, task_list_id, status="needsAction")

    def delete_task(
        self,
        task_id: str,
        task_list_id: Optional[str] = None,
    ) -> bool:
        """
        Delete a task.

        Args:
            task_id: The task ID
            task_list_id: Task list ID

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would delete task {task_id}")
            return True

        if not self.service:
            return False

        try:
            list_id = task_list_id or self.get_default_task_list() or "@default"

            self.service.tasks().delete(
                tasklist=list_id,
                task=task_id,
            ).execute()

            logger.info(f"Deleted task {task_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to delete task: {e}")
            return False

    def move_task(
        self,
        task_id: str,
        task_list_id: Optional[str] = None,
        parent_task_id: Optional[str] = None,
        previous_task_id: Optional[str] = None,
    ) -> bool:
        """
        Move a task (reorder or change parent).

        Args:
            task_id: The task ID
            task_list_id: Task list ID
            parent_task_id: New parent task ID (None for top level)
            previous_task_id: Task to position after

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would move task {task_id}")
            return True

        if not self.service:
            return False

        try:
            list_id = task_list_id or self.get_default_task_list() or "@default"

            params = {
                "tasklist": list_id,
                "task": task_id,
            }
            if parent_task_id:
                params["parent"] = parent_task_id
            if previous_task_id:
                params["previous"] = previous_task_id

            self.service.tasks().move(**params).execute()

            logger.info(f"Moved task {task_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to move task: {e}")
            return False

    def create_follow_up_task(
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
            due_date: Due date
            notes: Additional notes
            task_list_id: Task list ID

        Returns:
            Task ID or None
        """
        title = f"Follow up with {stakeholder}: {topic}"
        return self.create_task(
            title=title,
            notes=notes,
            due_date=due_date,
            task_list_id=task_list_id,
        )


# Global Tasks client instance
tasks_client = TasksClient()


if __name__ == "__main__":
    print("Testing Google Tasks Client...")
    print("=" * 50)

    if tasks_client.service:
        print("Tasks service initialized successfully")

        # List task lists
        task_lists = tasks_client.list_task_lists()
        print(f"\nTask lists ({len(task_lists)}):")
        for tl in task_lists:
            print(f"  - {tl.get('title', 'Untitled')}")

        # Get pending tasks from default list
        tasks = tasks_client.get_pending_tasks()
        print(f"\nPending tasks ({len(tasks)}):")
        for task in tasks[:5]:
            print(f"  - {task.get('title', 'Untitled')}")
    else:
        print("Tasks service not initialized - check credentials")

    print("\n" + "=" * 50)
