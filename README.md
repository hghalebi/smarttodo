# SmartTodo Gmail Integration

This project implements a Model Context Protocol (MCP) server that provides a RESTful API interface for Gmail integration. The server is built using FastAPI and offers comprehensive email management capabilities.

## Main Features

- **Email Management**
  - Send emails with support for CC and BCC
  - Read specific emails by ID
  - Search emails with advanced filtering
  - Get unread emails
  - Filter emails based on multiple criteria

## API Endpoints

### Core Endpoints
- `POST /send_email` - Send emails to multiple recipients
- `POST /read_email` - Read a specific email by ID
- `POST /search_emails` - Search emails with advanced filtering
- `GET /unread_emails` - Get a list of unread emails
- `POST /filter_emails` - Filter emails based on multiple criteria

### Authentication
The application uses Gmail OAuth2 authentication. It automatically handles:
- Token management
- Credential refresh
- Local server authentication flow

## Setup Requirements

1. Create a Google Cloud Project and enable Gmail API
2. Download `credentials.json` from Google Cloud Console
3. Install required Python packages (see requirements.txt)
