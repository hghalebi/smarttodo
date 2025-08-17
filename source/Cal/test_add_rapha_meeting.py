"""
Test script: add a 30-minute meeting today at 8:00 PM with Rapha.
Uses OAuth secrets from ./mcp_calendar.json and stores tokens in ./token.json.
"""
from __future__ import annotations

from datetime import datetime, timedelta
import json

from tzlocal import get_localzone

from google_calendar_client import create_event, local_iso


if __name__ == "__main__":
    tz = get_localzone()
    today = datetime.now(tz)
    start = today.replace(hour=20, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=30)

    event = create_event(
        calendar_id="primary",
        summary="Meet Rapha",
        description="To-do app sync with Rapha",
        start_time=local_iso(start),
        end_time=local_iso(end),
        attendees=["pimvic@gmail.com"],
    )
    print(json.dumps({
        "created_event_id": event.get("id"),
        "htmlLink": event.get("htmlLink"),
        "summary": event.get("summary"),
        "start": event.get("start"),
        "end": event.get("end"),
    }, indent=2))
