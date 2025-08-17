"""
MCP Server exposing Google Calendar tools (read/write) using the Model Context Protocol.

Tools:
- gcal_list_events: List upcoming events.
- gcal_create_event: Create a calendar event.

Environment variables (optional):
- GCAL_CREDENTIALS_FILE: path to OAuth client secrets JSON (default: ./mcp_calendar.json)
- GCAL_TOKEN_FILE: path to token cache JSON (default: ./token.json)
- GCAL_CALENDAR_ID: calendar id to target (default: primary)

Run:
  python mcp_gcal_server.py

This starts a stdio MCP server. Connect with an MCP-compatible client.
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import Any, Dict, List

from fastmcp import FastMCP

from google_calendar_client import (
    list_events as g_list_events,
    create_event as g_create_event,
    local_iso,
)

# Configure defaults via env
CALENDAR_ID = os.getenv("GCAL_CALENDAR_ID", "primary")


mcp = FastMCP(
    "google-calendar-mcp",
    instructions=(
        "Tools to read/write Google Calendar events. Times must be RFC3339 dateTime strings "
        "with timezone offset (e.g., 2025-08-17T20:00:00+03:00)."
    ),
)


@mcp.tool()
def gcal_list_events(max_results: int = 10) -> List[Dict[str, Any]]:
    """List upcoming events from the configured calendar, ordered by start time."""
    return g_list_events(calendar_id=CALENDAR_ID, max_results=max_results)


@mcp.tool()
def gcal_create_event(
    summary: str,
    start_time: str,
    end_time: str,
    description: str | None = None,
    location: str | None = None,
    attendees: List[str] | None = None,
) -> Dict[str, Any]:
    """Create an event in the configured calendar.

    Args:
      summary: Title of the event.
      start_time: RFC3339 string with timezone (e.g., 2025-08-17T20:00:00+03:00)
      end_time: RFC3339 string with timezone
      description: Optional description
      location: Optional location
      attendees: Optional list of attendee emails
    Returns: The created event object.
    """
    return g_create_event(
        calendar_id=CALENDAR_ID,
        summary=summary,
        description=description,
        location=location,
        start_time=start_time,
        end_time=end_time,
        attendees=attendees,
    )


async def main() -> None:
    await mcp.run()


if __name__ == "__main__":
    asyncio.run(main())
