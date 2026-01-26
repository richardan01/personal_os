"""
Google Workspace Integration Clients

This module provides clients for interacting with Google Workspace APIs:
- Drive: File storage and management
- Docs: Document creation and editing
- Sheets: Spreadsheet operations
- Slides: Presentation management
- Calendar: Event and scheduling
- Tasks: Task management
"""

from utils.google.base_client import GoogleBaseClient
from utils.google.drive_client import DriveClient, drive_client
from utils.google.docs_client import DocsClient, docs_client
from utils.google.sheets_client import SheetsClient, sheets_client
from utils.google.slides_client import SlidesClient, slides_client
from utils.google.calendar_client import CalendarClient, calendar_client
from utils.google.tasks_client import TasksClient, tasks_client

__all__ = [
    "GoogleBaseClient",
    "DriveClient",
    "drive_client",
    "DocsClient",
    "docs_client",
    "SheetsClient",
    "sheets_client",
    "SlidesClient",
    "slides_client",
    "CalendarClient",
    "calendar_client",
    "TasksClient",
    "tasks_client",
]
