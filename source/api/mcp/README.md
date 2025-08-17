# Google Tasks MCP Integration

This directory contains a complete MCP (Model Context Protocol) implementation for Google Tasks using the [FastMCP library](https://github.com/jlowin/fastmcp). It provides both server and client components for interacting with Google Tasks through the MCP protocol.

## Features

- **Complete Google Tasks API Coverage**: All CRUD operations for task lists and tasks
- **FastMCP Integration**: Built using the modern FastMCP library for optimal performance
- **Search Capabilities**: Search across tasks by title and notes
- **Batch Operations**: Create multiple tasks efficiently
- **Error Handling**: Comprehensive error handling and validation
- **Context Logging**: Built-in logging through MCP context
- **Async Support**: Full async/await support throughout

## Quick Start

### 1. Install Dependencies

The FastMCP library is already included in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Run the MCP Server

Start the MCP server directly:

```bash
python -m source.api.mcp.server
```

Or import and use in your code:

```python
from source.api.mcp.server import gtasks_mcp

# Run with stdio transport (default)
gtasks_mcp.run()

# Or run with HTTP transport
gtasks_mcp.run(transport="http", port=8000)
```

### 3. Use the MCP Client

```python
import asyncio
from source.api.mcp.client import GoogleTasksMCPClient

async def main():
    async with GoogleTasksMCPClient() as client:
        # Get all task lists
        task_lists = await client.get_task_lists()
        print(f"Found {len(task_lists)} task lists")
        
        # Create a new task
        if task_lists:
            task = await client.create_task(
                task_lists[0]["id"],
                "My new task",
                notes="Created via MCP"
            )
            print(f"Created task: {task['title']}")

asyncio.run(main())
```

## Available Tools

The MCP server exposes the following tools:

### Task List Management
- `get_task_lists()` - Get all task lists
- `get_task_list(task_list_id)` - Get specific task list
- `create_task_list(title)` - Create new task list
- `update_task_list(task_list_id, title)` - Update task list
- `delete_task_list(task_list_id)` - Delete task list

### Task Management
- `get_tasks(task_list_id, completed?)` - Get tasks from list
- `get_task(task_list_id, task_id)` - Get specific task
- `create_task(task_list_id, title, notes?, due?, parent?, previous?)` - Create task
- `update_task(task_list_id, task_id, title?, notes?, due?, status?)` - Update task
- `delete_task(task_list_id, task_id)` - Delete task
- `complete_task(task_list_id, task_id)` - Mark task complete
- `uncomplete_task(task_list_id, task_id)` - Mark task incomplete
- `clear_completed_tasks(task_list_id)` - Clear completed tasks

### Search & Batch Operations
- `search_tasks(query, task_list_id?)` - Search tasks by title/notes
- `create_multiple_tasks(task_list_id, tasks)` - Create multiple tasks

## Client Usage Examples

### Basic Operations

```python
from source.api.mcp.client import GoogleTasksMCPClient

async def demo():
    async with GoogleTasksMCPClient() as client:
        # Create a task list
        task_list = await client.create_task_list("My Project")
        list_id = task_list["id"]
        
        # Create tasks
        task1 = await client.create_task(list_id, "Design mockups")
        task2 = await client.create_task(
            list_id, 
            "Review code",
            notes="Check the new API implementation",
            due="2024-12-31T09:00:00Z"
        )
        
        # Complete a task
        await client.complete_task(list_id, task1["id"])
        
        # Search tasks
        results = await client.search_tasks("review")
        print(f"Found {len(results)} tasks containing 'review'")
```

### Batch Operations

```python
# Create multiple tasks at once
tasks_to_create = [
    {"title": "Task 1", "notes": "First task"},
    {"title": "Task 2", "due": "2024-12-25T10:00:00Z"},
    {"title": "Task 3", "notes": "Third task"}
]

result = await client.create_multiple_tasks(list_id, tasks_to_create)
print(f"Created {result['created_count']} tasks")
```

### Quick Functions

For simple operations, use the convenience functions:

```python
from source.api.mcp.client import quick_get_task_lists, quick_create_task, quick_search_tasks

# Quick operations without managing client lifecycle
task_lists = await quick_get_task_lists()
new_task = await quick_create_task(list_id, "Quick task")
search_results = await quick_search_tasks("urgent")
```

## Running Examples

Run the comprehensive demo:

```bash
python -m source.api.mcp.example_usage
```

This will demonstrate:
- Basic CRUD operations
- Batch task creation
- Search functionality
- Error handling
- Quick convenience functions

## Integration with Existing API

The MCP implementation works seamlessly with your existing FastAPI application:

```python
from fastapi import FastAPI
from source.api.mcp.client import GoogleTasksMCPClient

app = FastAPI()

@app.get("/mcp/tasks")
async def get_tasks_via_mcp(list_id: str):
    async with GoogleTasksMCPClient() as client:
        return await client.get_tasks(list_id)

@app.post("/mcp/tasks")
async def create_task_via_mcp(list_id: str, title: str, notes: str = None):
    async with GoogleTasksMCPClient() as client:
        return await client.create_task(list_id, title, notes=notes)
```

## Configuration

The MCP server can be configured for different transports:

```python
from source.api.mcp.server import gtasks_mcp

# STDIO transport (default) - for command-line tools
gtasks_mcp.run(transport="stdio")

# HTTP transport - for web deployments
gtasks_mcp.run(transport="http", host="0.0.0.0", port=8000)

# SSE transport - for real-time applications
gtasks_mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

## Error Handling

The implementation includes comprehensive error handling:

```python
try:
    task = await client.create_task(
        "invalid-list-id", 
        "Test task",
        due="invalid-date-format"
    )
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Operation failed: {e}")
```

## Logging

All operations include context-aware logging through the MCP Context:

```python
# Logs are automatically generated for each operation:
# "Creating task 'My Task' in list abc123..."
# "Created task: My Task (ID: xyz789)"
# "Task completed: My Task"
```

## Dependencies

This implementation requires:
- `fastmcp>=2.11.0` - The FastMCP library
- `google-api-python-client` - Google APIs client
- `google-auth-*` packages - Authentication
- Your existing project dependencies

## Architecture

```
mcp/
├── __init__.py          # Module exports
├── server.py            # FastMCP server with @tool decorators
├── client.py            # High-level client wrapper
├── example_usage.py     # Comprehensive examples
└── README.md           # This documentation
```

The implementation follows FastMCP best practices:
- Uses `@mcp.tool` decorators for clean tool definitions
- Leverages `Context` for logging and error handling
- Supports both direct server usage and client connections
- Provides both high-level and convenience interfaces

## Next Steps

1. **Run the examples** to see the MCP integration in action
2. **Integrate with your app** using the client or direct tool calls
3. **Customize the tools** by modifying the server implementation
4. **Deploy the server** using your preferred transport method
5. **Build AI agents** that can manipulate Google Tasks through MCP

For more information about FastMCP, visit the [official documentation](https://github.com/jlowin/fastmcp).
