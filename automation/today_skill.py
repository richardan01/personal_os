"""
Today Skill - Quick daily overview
Fetches calendar events and displays priorities
"""

import sys
import io
from datetime import datetime
from pathlib import Path

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add automation directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.google.calendar_client import calendar_client
from loguru import logger

# Suppress logger output to console for cleaner display
logger.remove()
logger.add(sys.stderr, level="ERROR")


def format_time(event_time_str):
    """Format event time to readable format"""
    try:
        # Parse ISO format datetime
        dt = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
        # Convert to local time and format
        return dt.strftime("%I:%M %p")
    except:
        return event_time_str


def get_event_link(event):
    """Extract meeting link from event"""
    # Check for Google Meet link
    if 'hangoutLink' in event:
        return event['hangoutLink']

    # Check for Zoom link in description
    description = event.get('description', '')
    if 'zoom.us' in description.lower():
        import re
        zoom_match = re.search(r'https://[^\s]*zoom\.us/[^\s]*', description)
        if zoom_match:
            return zoom_match.group(0)

    # Check location for links
    location = event.get('location', '')
    if location.startswith('http'):
        return location

    return event.get('htmlLink', 'Calendar')


def execute_today_skill():
    """Execute the /today skill"""
    print("\n" + "=" * 60)
    print(f"## Today - {datetime.now().strftime('%A, %B %d, %Y')}")
    print("=" * 60)

    # Fetch calendar events
    print("\n### Calendar\n")
    events = calendar_client.get_todays_events()

    if events:
        print("| Time      | Event                           | Location           |")
        print("|-----------|----------------------------------|-------------------|")

        for event in events:
            # Get event details
            summary = event.get('summary', 'No title')
            start = event.get('start', {})
            start_time_str = start.get('dateTime', start.get('date', ''))

            # Format time
            if 'dateTime' in start:
                time_str = format_time(start_time_str)
            else:
                time_str = "All day"

            # Get link or location
            link = get_event_link(event)

            # Sanitize strings to remove problematic characters
            summary_clean = summary.encode('ascii', 'replace').decode('ascii').replace('?', '')
            link_clean = link.encode('ascii', 'replace').decode('ascii').replace('?', '')

            # Truncate long strings for table format
            summary_display = summary_clean[:32] if len(summary_clean) > 32 else summary_clean
            link_display = link_clean[:17] if len(link_clean) > 17 else link_clean

            print(f"| {time_str:9} | {summary_display:32} | {link_display:17} |")
    else:
        print("No events scheduled for today")

    # Display priorities from context
    print("\n### Current Focus\n")
    print("- Primary: Data quality improvements")
    print("- Secondary: Quality and bug fixes")
    print("- Stretch: Tech debt reduction")

    # Display strategic priorities
    print("\n### Strategic Priorities\n")
    print("1. Data quality - Ensuring accurate, reliable customer data")
    print("2. Product quality - Reliability and polish")
    print("3. Team efficiency - Sustainable velocity")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        execute_today_skill()
    except Exception as e:
        logger.error(f"Error executing /today skill: {e}")
        print(f"\nError: {e}")
        print("\nMake sure Google Calendar is authenticated.")
        sys.exit(1)
