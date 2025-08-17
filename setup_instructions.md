# Google Tasks Client Setup Instructions

This project provides two ways to interact with Google Tasks:
1. **Python Client** - Direct interaction with Google Tasks API
2. **MCP Server** - Model Context Protocol server for Google Tasks

## Prerequisites

### 1. Google Cloud Project Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Tasks API:
   - Go to "APIs & Services" > "Library"
   - Search for "Tasks API"
   - Click "Enable"

### 2. OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Desktop application"
4. Download the JSON file
5. Rename it to `credentials.json` and place it in the project root

## Option 1: Python Client

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Usage
```bash
# Show all task lists (default behavior)
python source/client/client.py

# Show all task lists explicitly
python source/client/client.py --lists

# Interactive mode (recommended)
python source/client/client.py --interactive

# Show tasks in a specific list (replace LIST_ID with actual ID)
python source/client/client.py --tasks LIST_ID
```

### First Run
- On first run, it will open a browser for Google OAuth authentication
- Grant permissions to access your Google Tasks
- A `token.json` file will be created for future authentications

## Option 2: MCP Server (Advanced)

### Build the MCP Server
```bash
cd source/mcp/gtasks-mcp
npm install
npm run build
```

### Authentication for MCP Server
```bash
# First, authenticate
node dist/index.js auth

# Then run the server
node dist/index.js
```

### Available MCP Tools
- `listTaskLists` - List all task lists
- `list` - List all tasks
- `search` - Search for tasks
- `create` - Create a new task
- `update` - Update a task
- `delete` - Delete a task
- `clear` - Clear completed tasks

## Quick Start (Recommended)

1. Set up Google Cloud credentials (see Prerequisites)
2. Place `credentials.json` in the project root
3. Run the Python client:
   ```bash
   pip install -r requirements.txt
   python source/client/client.py --interactive
   ```

## Features

### Python Client Features
- ✅ List all task lists with detailed information
- ✅ Show tasks within specific lists
- ✅ Interactive mode for easy navigation
- ✅ Beautiful emoji-enhanced output
- ✅ Automatic authentication with token refresh

### MCP Server Features
- ✅ Complete task management through MCP protocol
- ✅ Task list listing functionality
- ✅ Search and filter capabilities
- ✅ Full CRUD operations for tasks

## Troubleshooting

### Common Issues
1. **Authentication Error**: Make sure `credentials.json` is in the correct location
2. **Permission Denied**: Check that Google Tasks API is enabled in your project
3. **Module Not Found**: Run `pip install -r requirements.txt`

### Token Issues
- Delete `token.json` to re-authenticate
- Check that your OAuth 2.0 credentials are for "Desktop application"

## Example Output

When you run the client, you'll see something like:
```
🎯 Google Tasks - All Task Lists

📋 Found 3 task list(s):

============================================================
1. 📋 My Tasks
   ID: MTUzNjc4OTQ2MjM5MDY...
   Last Updated: 2024-01-15T10:30:00.000Z
   Self Link: https://www.googleapis.com/tasks/v1/users/@me/lists/MTUzNjc4OTQ2MjM5MDY...
----------------------------------------
2. 📋 Shopping List
   ID: MTUzNjc4OTQ2MjM5MDY...
   Last Updated: 2024-01-14T15:45:00.000Z
   Self Link: https://www.googleapis.com/tasks/v1/users/@me/lists/MTUzNjc4OTQ2MjM5MDY...
----------------------------------------
```
