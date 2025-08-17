# Google Tasks FastAPI

A comprehensive FastAPI application providing CRUD operations for Google Tasks.

## 🚀 Features

### Task Lists Management
- ✅ **GET** `/task-lists` - List all task lists
- ✅ **GET** `/task-lists/{id}` - Get specific task list
- ✅ **POST** `/task-lists` - Create new task list
- ✅ **PUT** `/task-lists/{id}` - Update task list
- ✅ **DELETE** `/task-lists/{id}` - Delete task list

### Tasks Management
- ✅ **GET** `/task-lists/{list_id}/tasks` - List tasks in a task list
- ✅ **GET** `/task-lists/{list_id}/tasks/{task_id}` - Get specific task
- ✅ **POST** `/task-lists/{list_id}/tasks` - Create new task
- ✅ **PUT** `/task-lists/{list_id}/tasks/{task_id}` - Update task
- ✅ **DELETE** `/task-lists/{list_id}/tasks/{task_id}` - Delete task

### Task Operations
- ✅ **PATCH** `/task-lists/{list_id}/tasks/{task_id}/complete` - Mark task as completed
- ✅ **PATCH** `/task-lists/{list_id}/tasks/{task_id}/uncomplete` - Mark task as not completed
- ✅ **DELETE** `/task-lists/{list_id}/tasks/completed` - Clear all completed tasks

### Search & Utilities
- ✅ **GET** `/search/tasks?query=...` - Search tasks across all lists
- ✅ **GET** `/health` - Health check endpoint

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Google Cloud Setup
1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Google Tasks API
3. Create OAuth 2.0 credentials (Desktop application)
4. Download credentials as `credentials.json` and place in project root

### 3. Run the API
```bash
# From the source directory
python api/run.py

# Or using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. First Time Authentication
- On first API call, you'll be redirected to authenticate with Google
- A `token.json` file will be created for future requests

## 📚 API Documentation

### Interactive Documentation
Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Base URL
```
http://localhost:8000
```

## 🔧 Usage Examples

### Get All Task Lists
```bash
curl -X GET "http://localhost:8000/task-lists"
```

### Create a New Task List
```bash
curl -X POST "http://localhost:8000/task-lists" \
  -H "Content-Type: application/json" \
  -d '{"title": "My New Task List"}'
```

### Create a New Task
```bash
curl -X POST "http://localhost:8000/task-lists/{list_id}/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "notes": "Milk, bread, eggs",
    "due": "2024-01-20T10:00:00Z"
  }'
```

### Mark Task as Completed
```bash
curl -X PATCH "http://localhost:8000/task-lists/{list_id}/tasks/{task_id}/complete"
```

### Search Tasks
```bash
curl -X GET "http://localhost:8000/search/tasks?query=groceries"
```

## 📊 Response Formats

### Task List Response
```json
{
  "id": "MTUzNjc4OTQ2MjM5MDY...",
  "title": "My Tasks",
  "updated": "2024-01-15T10:30:00Z",
  "self_link": "https://www.googleapis.com/tasks/v1/users/@me/lists/...",
  "kind": "tasks#taskList",
  "etag": "\"LTEzNjc4OTQ2MjM5MDY...\""
}
```

### Task Response
```json
{
  "id": "MTUzNjc4OTQ2MjM5MDY...",
  "title": "Buy groceries",
  "notes": "Milk, bread, eggs",
  "status": "needsAction",
  "due": "2024-01-20T10:00:00Z",
  "updated": "2024-01-15T10:30:00Z",
  "completed": null,
  "parent": null,
  "position": "00000000001000000000",
  "hidden": false,
  "deleted": false,
  "self_link": "https://www.googleapis.com/tasks/v1/users/@me/lists/.../tasks/...",
  "kind": "tasks#task",
  "etag": "\"LTEzNjc4OTQ2MjM5MDY...\"",
  "links": null
}
```

### Error Response
```json
{
  "error": "Task not found",
  "status_code": 404,
  "detail": "Task with ID xyz not found"
}
```

## 🔐 Authentication

The API uses Google OAuth 2.0 for authentication:
1. First request triggers OAuth flow
2. User grants permissions in browser
3. Credentials are cached in `token.json`
4. Subsequent requests use cached credentials
5. Tokens are automatically refreshed when needed

## 🏗️ Architecture

```
source/api/
├── main.py              # FastAPI application and routes
├── run.py               # Startup script
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic models
├── services/
│   ├── __init__.py
│   └── gtasks_service.py # Google Tasks service layer
└── README.md            # This file
```

## 🔍 Development

### Running in Development Mode
```bash
python api/run.py
```

### Testing the API
```bash
# Health check
curl http://localhost:8000/health

# Get task lists
curl http://localhost:8000/task-lists
```

### Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google credentials (optional)
- `PORT` - Server port (default: 8000)

## 🐛 Troubleshooting

### Common Issues

1. **Credentials Error**
   - Ensure `credentials.json` is in the project root
   - Verify Google Tasks API is enabled
   - Check OAuth 2.0 setup in Google Cloud Console

2. **Permission Denied**
   - Delete `token.json` to re-authenticate
   - Ensure correct OAuth scopes

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python path in `run.py`

### Debug Mode
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## 📝 License

This project is licensed under the MIT License.
