import os
import pickle
from fastapi import FastAPI, Body
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timedelta
from fastmcp import FastMCP
from typing import List, Optional, Union
import base64

# Initialize FastMCP
mcp = FastMCP("Gmail MCP 📧")

# Create ASGI app from MCP server with specific path
mcp_app = mcp.http_app(path='/mcp')

# Create FastAPI app with MCP lifespan
app = FastAPI(title="Gmail MCP API", lifespan=mcp_app.lifespan)

# --- App and Configuration ---
SCOPES = ['https://mail.google.com/']
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

# --- MCP Tools Definition ---
@mcp.tool
def send_email(
    to: Union[str, List[str]],
    subject: str,
    body: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
) -> dict:
    """
    Send an email to one or multiple recipients.
    
    Args:
        to: Email address or list of email addresses
        subject: Email subject
        body: Email content
        cc: Optional list of CC recipients
        bcc: Optional list of BCC recipients
    
    Returns:
        dict: Message ID and status
    """
    # Normalize the 'to' field to always be a list
    if isinstance(to, str):
        to = [to]
    elif not isinstance(to, (list, tuple)):
        raise ValueError("'to' must be a string or list of strings")

    data = {
        "to": to,
        "subject": subject or "",
        "body": body or "",
        "cc": cc if isinstance(cc, (list, type(None))) else [cc],
        "bcc": bcc if isinstance(bcc, (list, type(None))) else [bcc]
    }
    return send_email_endpoint(data)

@mcp.tool
def read_email(message_id: str) -> dict:
    """
    Read a specific email by its ID.
    
    Args:
        message_id: The ID of the email to read
    
    Returns:
        dict: Email content including subject, sender, date, and body
    """
    return read_email_endpoint({"messageId": message_id})

@mcp.tool
def search_emails(
    query: str,
    max_results: int = 10,
    include_content: bool = False
) -> dict:
    """
    Search emails using Gmail query syntax.
    
    Args:
        query: Gmail search query
        max_results: Maximum number of results to return
        include_content: Whether to include email content in results
    
    Returns:
        dict: List of matching emails
    """
    data = {
        "query": query,
        "maxResults": max_results,
        "includeContent": include_content
    }
    return search_emails_endpoint(data)

@mcp.tool
def filter_emails(
    query: Optional[str] = None,
    from_email: Optional[str] = None,
    subject: Optional[str] = None,
    has_attachment: Optional[bool] = None,
    date_after: Optional[str] = None,
    date_before: Optional[str] = None,
    is_read: Optional[bool] = None,
    label: Optional[str] = None,
    max_results: int = 10
) -> dict:
    """
    Filter emails using multiple criteria.
    
    Args:
        query: General search term
        from_email: Sender's email address
        subject: Subject text to search
        has_attachment: Filter by attachment presence
        date_after: Filter emails after date (YYYY-MM-DD)
        date_before: Filter emails before date (YYYY-MM-DD)
        is_read: Filter by read status
        label: Filter by label
        max_results: Maximum number of results
    
    Returns:
        dict: Filtered email list with count
    """
    data = {
        "query": query,
        "from": from_email,
        "subject": subject,
        "has_attachment": has_attachment,
        "date_after": date_after,
        "date_before": date_before,
        "is_read": is_read,
        "label": label,
        "max_results": max_results
    }
    return filter_emails_endpoint(data)

@mcp.tool
def get_unread_emails(max_results: int = 10) -> dict:
    """
    Get unread emails.
    
    Args:
        max_results: Maximum number of unread emails to retrieve
    
    Returns:
        dict: List of unread emails with count
    """
    return get_unread_emails_endpoint(max_results=max_results)

# --- Original FastAPI endpoints (renamed to avoid conflicts) ---
@app.post("/send_email")
def send_email_endpoint(data: dict = Body(...)):
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

    # Handle 'to' field
    to_addresses = data.get("to")
    if not to_addresses:
        raise ValueError("'to' field is required")
    
    if isinstance(to_addresses, str):
        to_addresses = [to_addresses]
    elif isinstance(to_addresses, (list, tuple)):
        if not all(isinstance(addr, str) for addr in to_addresses):
            raise ValueError("All email addresses must be strings")
    else:
        raise ValueError("'to' must be a string or list of strings")

    message['to'] = ', '.join(str(addr) for addr in to_addresses)
    message['subject'] = str(data.get("subject", ""))
    
    # Handle CC
    cc_addresses = data.get("cc", [])
    if cc_addresses:
        if isinstance(cc_addresses, str):
            cc_addresses = [cc_addresses]
        message['cc'] = ', '.join(str(addr) for addr in cc_addresses)

    # Handle BCC
    bcc_addresses = data.get("bcc", [])
    if bcc_addresses:
        if isinstance(bcc_addresses, str):
            bcc_addresses = [bcc_addresses]
        message['bcc'] = ', '.join(str(addr) for addr in bcc_addresses)
    
    message.attach(MIMEText(data.get("body")))
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}
    
    # Call the Gmail API to send the email
    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    
    return {"message": "Email sent successfully!", "messageId": send_message['id']}

@app.post("/read_email")
def read_email_endpoint(data: dict = Body(...)):
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
def search_emails_endpoint(data: dict = Body(...)):
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

@app.post("/filter_emails")
def filter_emails_endpoint(data: dict = Body(...)):
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

@app.get("/unread_emails")
def get_unread_emails_endpoint(max_results: int = 10):
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

# Mount the MCP server
app.mount("/api", mcp_app)
