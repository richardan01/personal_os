"""
Google Calendar Client - Event and scheduling management
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from loguru import logger

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.google.base_client import google_base_client
from config import settings


class CalendarClient:
    """Client for Google Calendar operations"""

    def __init__(self):
        self._service = None

    @property
    def service(self):
        """Lazy initialization of Calendar service"""
        if self._service is None and google_base_client.is_authenticated():
            self._service = build(
                "calendar", "v3", credentials=google_base_client.credentials
            )
        return self._service

    def list_calendars(self) -> List[Dict[str, Any]]:
        """
        List all calendars accessible to the user.

        Returns:
            List of calendar metadata dicts
        """
        if not self.service:
            logger.warning("Calendar service not initialized")
            return []

        try:
            calendars = []
            page_token = None

            while True:
                response = self.service.calendarList().list(
                    pageToken=page_token
                ).execute()

                calendars.extend(response.get("items", []))
                page_token = response.get("nextPageToken")

                if not page_token:
                    break

            logger.info(f"Listed {len(calendars)} calendars")
            return calendars

        except HttpError as e:
            logger.error(f"Failed to list calendars: {e}")
            return []

    def get_events(
        self,
        calendar_id: Optional[str] = None,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        max_results: int = 100,
        single_events: bool = True,
        order_by: str = "startTime",
    ) -> List[Dict[str, Any]]:
        """
        Get events from a calendar.

        Args:
            calendar_id: Calendar ID (defaults to primary)
            time_min: Start of time range (defaults to now)
            time_max: End of time range
            max_results: Maximum number of events
            single_events: Expand recurring events
            order_by: Sort order (startTime or updated)

        Returns:
            List of event dicts
        """
        if not self.service:
            return []

        try:
            cal_id = calendar_id or settings.google_calendar_id or "primary"

            # Default time range
            if time_min is None:
                time_min = datetime.utcnow()

            params = {
                "calendarId": cal_id,
                "timeMin": time_min.isoformat() + "Z",
                "maxResults": max_results,
                "singleEvents": single_events,
                "orderBy": order_by,
            }

            if time_max:
                params["timeMax"] = time_max.isoformat() + "Z"

            events = []
            page_token = None

            while True:
                if page_token:
                    params["pageToken"] = page_token

                response = self.service.events().list(**params).execute()
                events.extend(response.get("items", []))
                page_token = response.get("nextPageToken")

                if not page_token or len(events) >= max_results:
                    break

            logger.info(f"Retrieved {len(events)} events from calendar")
            return events[:max_results]

        except HttpError as e:
            logger.error(f"Failed to get events: {e}")
            return []

    def get_todays_events(self, calendar_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get today's events.

        Args:
            calendar_id: Calendar ID

        Returns:
            List of today's events
        """
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        return self.get_events(
            calendar_id=calendar_id,
            time_min=start_of_day,
            time_max=end_of_day,
        )

    def get_upcoming_events(
        self,
        calendar_id: Optional[str] = None,
        days: int = 7,
    ) -> List[Dict[str, Any]]:
        """
        Get upcoming events for the next N days.

        Args:
            calendar_id: Calendar ID
            days: Number of days to look ahead

        Returns:
            List of upcoming events
        """
        now = datetime.utcnow()
        end_date = now + timedelta(days=days)

        return self.get_events(
            calendar_id=calendar_id,
            time_min=now,
            time_max=end_date,
        )

    def get_event(
        self,
        event_id: str,
        calendar_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific event by ID.

        Args:
            event_id: The event ID
            calendar_id: Calendar ID

        Returns:
            Event dict or None
        """
        if not self.service:
            return None

        try:
            cal_id = calendar_id or settings.google_calendar_id or "primary"

            event = self.service.events().get(
                calendarId=cal_id,
                eventId=event_id,
            ).execute()

            return event

        except HttpError as e:
            logger.error(f"Failed to get event {event_id}: {e}")
            return None

    def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
        calendar_id: Optional[str] = None,
        reminders: Optional[Dict] = None,
    ) -> Optional[str]:
        """
        Create a new calendar event.

        Args:
            summary: Event title
            start_time: Start datetime
            end_time: End datetime
            description: Event description
            location: Event location
            attendees: List of attendee emails
            calendar_id: Calendar ID
            reminders: Custom reminders config

        Returns:
            Event ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would create event: {summary}")
            return "dry_run_event_id"

        if not self.service:
            return None

        try:
            cal_id = calendar_id or settings.google_calendar_id or "primary"

            event_body = {
                "summary": summary,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": settings.timezone,
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": settings.timezone,
                },
            }

            if description:
                event_body["description"] = description
            if location:
                event_body["location"] = location
            if attendees:
                event_body["attendees"] = [{"email": email} for email in attendees]
            if reminders:
                event_body["reminders"] = reminders

            event = self.service.events().insert(
                calendarId=cal_id,
                body=event_body,
            ).execute()

            event_id = event.get("id")
            logger.info(f"Created event '{summary}' with ID: {event_id}")
            return event_id

        except HttpError as e:
            logger.error(f"Failed to create event: {e}")
            return None

    def update_event(
        self,
        event_id: str,
        calendar_id: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """
        Update an existing event.

        Args:
            event_id: The event ID
            calendar_id: Calendar ID
            **kwargs: Fields to update (summary, description, start, end, etc.)

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would update event {event_id}")
            return True

        if not self.service:
            return False

        try:
            cal_id = calendar_id or settings.google_calendar_id or "primary"

            # Get existing event
            event = self.get_event(event_id, cal_id)
            if not event:
                return False

            # Update fields
            for key, value in kwargs.items():
                if key in ["start_time", "end_time"]:
                    field = "start" if key == "start_time" else "end"
                    event[field] = {
                        "dateTime": value.isoformat(),
                        "timeZone": settings.timezone,
                    }
                else:
                    event[key] = value

            self.service.events().update(
                calendarId=cal_id,
                eventId=event_id,
                body=event,
            ).execute()

            logger.info(f"Updated event {event_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to update event: {e}")
            return False

    def delete_event(
        self,
        event_id: str,
        calendar_id: Optional[str] = None,
    ) -> bool:
        """
        Delete an event.

        Args:
            event_id: The event ID
            calendar_id: Calendar ID

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would delete event {event_id}")
            return True

        if not self.service:
            return False

        try:
            cal_id = calendar_id or settings.google_calendar_id or "primary"

            self.service.events().delete(
                calendarId=cal_id,
                eventId=event_id,
            ).execute()

            logger.info(f"Deleted event {event_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to delete event: {e}")
            return False

    def find_free_time(
        self,
        duration_minutes: int,
        time_min: Optional[datetime] = None,
        time_max: Optional[datetime] = None,
        calendar_id: Optional[str] = None,
        working_hours: tuple = (9, 17),
    ) -> List[Dict[str, datetime]]:
        """
        Find free time slots.

        Args:
            duration_minutes: Required duration in minutes
            time_min: Start of search range
            time_max: End of search range
            calendar_id: Calendar ID
            working_hours: Tuple of (start_hour, end_hour)

        Returns:
            List of {start, end} dicts for free slots
        """
        if not self.service:
            return []

        try:
            if time_min is None:
                time_min = datetime.utcnow()
            if time_max is None:
                time_max = time_min + timedelta(days=7)

            events = self.get_events(
                calendar_id=calendar_id,
                time_min=time_min,
                time_max=time_max,
            )

            # Build busy periods
            busy = []
            for event in events:
                start = event.get("start", {})
                end = event.get("end", {})

                start_dt = start.get("dateTime") or start.get("date")
                end_dt = end.get("dateTime") or end.get("date")

                if start_dt and end_dt:
                    busy.append({
                        "start": datetime.fromisoformat(start_dt.replace("Z", "+00:00")),
                        "end": datetime.fromisoformat(end_dt.replace("Z", "+00:00")),
                    })

            # Sort by start time
            busy.sort(key=lambda x: x["start"])

            # Find gaps
            free_slots = []
            current = time_min

            for period in busy:
                # Check if there's a gap before this event
                if period["start"] > current:
                    gap_duration = (period["start"] - current).total_seconds() / 60
                    if gap_duration >= duration_minutes:
                        free_slots.append({
                            "start": current,
                            "end": period["start"],
                        })
                current = max(current, period["end"])

            # Check remaining time
            if time_max > current:
                gap_duration = (time_max - current).total_seconds() / 60
                if gap_duration >= duration_minutes:
                    free_slots.append({
                        "start": current,
                        "end": time_max,
                    })

            return free_slots

        except Exception as e:
            logger.error(f"Failed to find free time: {e}")
            return []


# Global Calendar client instance
calendar_client = CalendarClient()


if __name__ == "__main__":
    print("Testing Google Calendar Client...")
    print("=" * 50)

    if calendar_client.service:
        print("Calendar service initialized successfully")

        # Get today's events
        events = calendar_client.get_todays_events()
        print(f"\nToday's events ({len(events)}):")
        for event in events:
            start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
            print(f"  - {event.get('summary', 'No title')} at {start}")
    else:
        print("Calendar service not initialized - check credentials")

    print("\n" + "=" * 50)
