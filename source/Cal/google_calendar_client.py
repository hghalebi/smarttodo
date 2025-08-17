"""
Simple Google Calendar client using OAuth client secrets in mcp_calendar.json.
On first run it will open a browser for consent and save tokens into token.json.

Functions provided:
- get_service()
- list_events(calendar_id="primary", max_results=10)
- create_event(calendar_id="primary", **event_fields)
- update_event(calendar_id="primary", event_id=..., **event_fields)
- delete_event(calendar_id="primary", event_id=...)

The file paths default to the current working directory:
- credentials (client secret): ./mcp_calendar.json
- token storage: ./token.json
"""
from __future__ import annotations

from datetime import datetime, timedelta
import json
import os
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tzlocal import get_localzone

# If modifying these scopes, delete token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar",  # read/write
]

CREDENTIALS_FILE = os.getenv("GCAL_CREDENTIALS_FILE", "mcp_calendar.json")
TOKEN_FILE = os.getenv("GCAL_TOKEN_FILE", "token.json")


def _load_credentials() -> Credentials:
    """Load OAuth credentials, refreshing or performing local installed-app flow as needed."""
    creds: Optional[Credentials] = None

    # Load existing tokens if present
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Google OAuth client secret file not found at '{CREDENTIALS_FILE}'. "
                    "Place your downloaded OAuth client (installed app) JSON here or set GCAL_CREDENTIALS_FILE."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            # Use local server flow to simplify callback. This will open a browser once.
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return creds


def get_service():
    """Build and return a Google Calendar API service client."""
    creds = _load_credentials()
    return build("calendar", "v3", credentials=creds)


# ---------- Convenience helpers ----------

def local_iso(dt: datetime) -> str:
    """Convert a naive or aware datetime to RFC3339 in the local timezone with offset.
    Returns a string like: 2025-08-17T20:00:00+03:00
    """
    tz = get_localzone()
    if dt.tzinfo is None:
        # tzlocal returns a zoneinfo.ZoneInfo on modern Python; attach tz directly
        dt = dt.replace(tzinfo=tz)
    else:
        dt = dt.astimezone(tz)
    # RFC3339 format
    return dt.isoformat(timespec="seconds")


# ---------- Calendar operations ----------

def list_events(calendar_id: str = "primary", max_results: int = 10) -> List[Dict[str, Any]]:
    """List upcoming events sorted by start time."""
    service = get_service()
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])


def create_event(
    calendar_id: str = "primary",
    summary: str = "",
    description: Optional[str] = None,
    location: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    timezone: Optional[str] = None,
    reminders_overrides: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Create an event with flexible fields.

    Pass RFC3339 strings (e.g., from local_iso) for start_time and end_time.
    If timezone is None, Google will infer from the timestamps.
    """
    service = get_service()

    event: Dict[str, Any] = {
        "summary": summary,
        "start": {"dateTime": start_time, **({"timeZone": timezone} if timezone else {})},
        "end": {"dateTime": end_time, **({"timeZone": timezone} if timezone else {})},
    }
    if description:
        event["description"] = description
    if location:
        event["location"] = location
    if attendees:
        event["attendees"] = [{"email": a} for a in attendees]
    if reminders_overrides is not None:
        event["reminders"] = {"useDefault": False, "overrides": reminders_overrides}

    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created


def update_event(
    calendar_id: str,
    event_id: str,
    **fields: Any,
) -> Dict[str, Any]:
    """Update an existing event with partial fields.

    Example fields: summary, description, start={...}, end={...}
    """
    service = get_service()
    # Get existing event
    ev = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    # Merge changes
    ev.update(fields)
    updated = service.events().update(calendarId=calendar_id, eventId=event_id, body=ev).execute()
    return updated


def delete_event(calendar_id: str, event_id: str) -> None:
    """Delete an event by ID."""
    service = get_service()
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


# ---------- Quick self-test utility ----------
if __name__ == "__main__":
    # Example: create a 30-minute event today at 8:00 PM local time
    tz = get_localzone()
    today = datetime.now(tz)
    start = today.replace(hour=20, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=30)

    created = create_event(
        calendar_id="primary",
        summary="Meet Rapha",
        description="Quick sync",
        start_time=local_iso(start),
        end_time=local_iso(end),
        attendees=["pimvic@gmail.com"],
    )
    print(json.dumps({"created_event_id": created.get("id")}, indent=2))
