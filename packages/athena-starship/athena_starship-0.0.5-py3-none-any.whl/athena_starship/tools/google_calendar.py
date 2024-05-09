from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
from swarms.tools import tool


@tool
def calendar(
    action: str,
    event_id: str = None,
    summary: str = None,
    start_time: str = None,
    duration: int = 1,
    description: str = None,
):
    """
    Manage a Google Calendar event based on the specified action.

    Args:
        action (str): The action to perform on the event. Possible values are "create" or "update".
        event_id (str, optional): The ID of the event to update. Required if action is "update".
        summary (str, optional): The summary or title of the event.
        start_time (str, optional): The start time of the event in ISO 8601 format.
        duration (int, optional): The duration of the event in hours. Default is 1 hour.
        description (str, optional): The description of the event.

    Returns:
        str: The ID of the created or updated event.

    Raises:
        ValueError: If the action is not valid or required arguments are missing.

    """
    # Load credentials from the file
    creds = Credentials.from_authorized_user_file(
        os.getenv("GOOGLE_CREDENTIALS_FILE"),
        scopes=["https://www.googleapis.com/auth/calendar"],
    )

    # Build the service
    service = build("calendar", "v3", credentials=creds)

    # Prepare event data
    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "America/New_York",
        },
        "end": {
            "dateTime": (
                datetime.fromisoformat(start_time)
                + timedelta(hours=duration)
            ).isoformat(),
            "timeZone": "America/New_York",
        },
    }

    if action == "create":
        # Call the Calendar API to create an event
        created_event = (
            service.events()
            .insert(calendarId="primary", body=event)
            .execute()
        )
        print(f'Event created: {created_event.get("htmlLink")}')
        return created_event.get("id")

    elif action == "update":
        # Call the Calendar API to update an existing event
        updated_event = (
            service.events()
            .update(
                calendarId="primary", eventId=event_id, body=event
            )
            .execute()
        )
        print(f'Event updated: {updated_event.get("htmlLink")}')
        return updated_event.get("id")


# Usage example:
# To create an event:
# event_id = calendar('create', 'credentials.json', summary='Meeting with Bob', start_time='2024-05-10T15:00:00', description='Discuss project updates')

# To update an existing event:
# calendar('update', 'credentials.json', event_id=event_id, summary='Updated Meeting with Bob', start_time='2024-05-10T16:00:00', description='Discuss all updates')
