import os
import pickle
from fastapi import FastAPI, Body
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
import json

# --- App and Configuration ---
app = FastAPI()
SCOPES = ['https://mail.google.com/'] # Only Gmail scope
CREDENTIALS_FILE = 'credentials.json'
TOKEN_PICKLE_FILE = 'token.pickle'

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# --- Gmail Authentication ---
def get_gmail_service():
    """Authenticates with Google and returns a Gmail service object."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)
            
    return build('gmail', 'v1', credentials=creds)

# --- MCP Tool Definition ---
@app.post("/send_email")
def send_email(data: dict = Body(...)):
    """
    Enhanced MCP tool to send an email to multiple recipients.
    Expects a JSON body with:
    - to: string or list of email addresses
    - subject: string
    - body: string
    - cc: optional list of email addresses
    - bcc: optional list of email addresses
    """
    service = get_gmail_service()
    
    # Create the email message
    message = MIMEMultipart()
    to_addresses = data.get("to")
    if isinstance(to_addresses, str):
        to_addresses = [to_addresses]
    
    message['to'] = ', '.join(to_addresses)
    message['subject'] = data.get("subject")
    
    # Add CC and BCC if provided
    if "cc" in data:
        message['cc'] = ', '.join(data.get("cc"))
    if "bcc" in data:
        message['bcc'] = ', '.join(data.get("bcc"))
    
    message.attach(MIMEText(data.get("body")))
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}
    
    # Call the Gmail API to send the email
    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    
    return {"message": "Email sent successfully!", "messageId": send_message['id']}

@app.post("/read_email")
def read_email(data: dict = Body(...)):
    """
    MCP tool to read a specific email by its ID.
    Expects a JSON body with 'messageId'.
    """
    service = get_gmail_service()
    message_id = data.get("messageId")
    
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    
    # Extract headers
    headers = message['payload']['headers']
    subject = next(h['value'] for h in headers if h['name'].lower() == 'subject')
    from_email = next(h['value'] for h in headers if h['name'].lower() == 'from')
    date = next(h['value'] for h in headers if h['name'].lower() == 'date')
    
    # Extract body
    if 'parts' in message['payload']:
        body = message['payload']['parts'][0]['body'].get('data', '')
    else:
        body = message['payload']['body'].get('data', '')
    
    if body:
        body = base64.urlsafe_b64decode(body).decode()
    
    return {
        "id": message_id,
        "subject": subject,
        "from": from_email,
        "date": date,
        "body": body
    }

@app.post("/search_emails")
def search_emails(data: dict = Body(...)):
    """
    Enhanced MCP tool to search emails with advanced filtering.
    Expects a JSON body with:
    - query: string (Gmail search query)
    - maxResults: int (optional)
    - includeContent: boolean (optional)
    """
    service = get_gmail_service()
    query = data.get("query", "")
    max_results = data.get("maxResults", 10)
    include_content = data.get("includeContent", False)
    
    result = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    messages = result.get('messages', [])
    
    if include_content:
        full_messages = []
        for msg in messages:
            full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            headers = full_msg['payload']['headers']
            subject = next(h['value'] for h in headers if h['name'].lower() == 'subject')
            from_email = next(h['value'] for h in headers if h['name'].lower() == 'from')
            
            full_messages.append({
                "id": msg['id'],
                "subject": subject,
                "from": from_email,
                "threadId": msg['threadId']
            })
        return {"messages": full_messages}
    
    return {"messages": messages}

    """
    MCP tool to create a calendar event and send invitations.
    Expects a JSON body with:
    - summary: string (meeting title)
    - description: string
    - start_time: string (ISO format)
    - duration_minutes: int
    - attendees: list of email addresses
    - location: string (optional)
    """
    # Build the calendar service
    service = build('calendar', 'v3', credentials=get_gmail_service().credentials)
    
    start_time = datetime.fromisoformat(data.get("start_time"))
    end_time = start_time + timedelta(minutes=data.get("duration_minutes", 60))
    
    event = {
        'summary': data.get("summary"),
        'location': data.get("location", ""),
        'description': data.get("description"),
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'UTC',
        },
        'attendees': [{'email': attendee} for attendee in data.get("attendees", [])],
        'reminders': {
            'useDefault': True
        },
    }

    event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
    return {"message": "Meeting created successfully!", "eventId": event['id'], "meetingLink": event.get('hangoutLink')}

# Add these new endpoints after the existing ones

@app.get("/unread_emails")
def get_unread_emails(max_results: int = 10):
    """Get unread emails with their details"""
    try:
        service = get_gmail_service()
        
        # Search for unread messages
        result = service.users().messages().list(
            userId='me',
            labelIds=['UNREAD'],
            maxResults=max_results
        ).execute()
        
        messages = result.get('messages', [])
        unread_emails = []
        
        if not messages:
            return {'unread_count': 0, 'messages': []}
            
        for msg in messages:
            # Get the full message details
            email = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            # Extract headers
            headers = email['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
            snippet = email.get('snippet', '')
            
            unread_emails.append({
                'id': msg['id'],
                'subject': subject,
                'from': sender,
                'date': date,
                'snippet': snippet,
                'labels': email.get('labelIds', [])
            })
        
        return {
            'unread_count': len(unread_emails),
            'messages': unread_emails
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'unread_count': 0,
            'messages': []
        }

@app.post("/filter_emails")
def filter_emails(data: dict = Body(...)):
    """
    Filter emails based on multiple criteria
    Expects a JSON body with any of these optional fields:
    - query: string (general search term across all fields)
    - from: sender email
    - subject: subject text to search
    - has_attachment: boolean
    - date_after: YYYY-MM-DD
    - date_before: YYYY-MM-DD
    - is_read: boolean
    - label: label name
    - max_results: int
    """
    service = get_gmail_service()
    query_parts = []
    
    # Add general search term if provided
    if 'query' in data and data['query']:
        # This will search in subject, body and from fields
        query_parts.append(data['query'])
    
    if 'from' in data and data['from']:
        query_parts.append(f'from:{data["from"]}')
    
    if 'subject' in data and data['subject']:
        query_parts.append(f'subject:{data["subject"]}')
    
    if 'has_attachment' in data and data['has_attachment']:
        query_parts.append('has:attachment')
    
    if 'date_after' in data and data['date_after']:
        query_parts.append(f'after:{data["date_after"]}')
    
    if 'date_before' in data and data['date_before']:
        query_parts.append(f'before:{data["date_before"]}')
    
    if 'is_read' in data:
        query_parts.append('is:read' if data['is_read'] else 'is:unread')
    
    if 'label' in data and data['label']:
        query_parts.append(f'label:{data["label"]}')
    
    query = ' '.join(query_parts)
    max_results = data.get('max_results', 10)
    
    result = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()
    
    messages = result.get('messages', [])
    filtered_emails = []
    
    for msg in messages:
        email = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()
        
        headers = email['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
        
        filtered_emails.append({
            'id': msg['id'],
            'subject': subject,
            'from': sender,
            'date': date,
            'labels': email['labelIds']
        })
    
    return {'count': len(filtered_emails), 'messages': filtered_emails}
