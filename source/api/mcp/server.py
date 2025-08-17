"""
FastMCP server implementation for Google Tasks.
"""

import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import asdict

from fastmcp import FastMCP, Context
from ..services.gtasks_service import GoogleTasksService
from ..models.schemas import (
    TaskList, TaskListCreate, TaskListUpdate,
    Task, TaskCreate, TaskUpdate, TaskStatus
)

# Create FastMCP server instance
gtasks_mcp = FastMCP("Google Tasks MCP Server")

# Initialize the Google Tasks service
_gtasks_service = None

def get_gtasks_service() -> GoogleTasksService:
    """Get or create Google Tasks service instance."""
    global _gtasks_service
    if _gtasks_service is None:
        _gtasks_service = GoogleTasksService()
    return _gtasks_service

# =============================================================================
# TASK LIST TOOLS
# =============================================================================

@gtasks_mcp.tool
async def get_task_lists(ctx: Context) -> List[Dict[str, Any]]:
    """Get all Google Tasks task lists."""
    await ctx.info("Fetching all task lists...")
    
    service = get_gtasks_service()
    task_lists = await service.get_task_lists()
    
    result = [asdict(tl) for tl in task_lists]
    await ctx.info(f"Found {len(result)} task lists")
    
    return result

@gtasks_mcp.tool
async def get_task_list(task_list_id: str, ctx: Context) -> Optional[Dict[str, Any]]:
    """Get a specific task list by ID.
    
    Args:
        task_list_id: The ID of the task list to retrieve
    """
    await ctx.info(f"Fetching task list: {task_list_id}")
    
    service = get_gtasks_service()
    task_list = await service.get_task_list(task_list_id)
    
    if not task_list:
        await ctx.error(f"Task list '{task_list_id}' not found")
        return None
    
    await ctx.info(f"Retrieved task list: {task_list.title}")
    return asdict(task_list)

@gtasks_mcp.tool
async def create_task_list(title: str, ctx: Context) -> Dict[str, Any]:
    """Create a new task list.
    
    Args:
        title: The title of the new task list
    """
    await ctx.info(f"Creating task list: {title}")
    
    service = get_gtasks_service()
    task_list_data = TaskListCreate(title=title)
    task_list = await service.create_task_list(task_list_data)
    
    await ctx.info(f"Created task list: {task_list.title} (ID: {task_list.id})")
    return asdict(task_list)

@gtasks_mcp.tool
async def update_task_list(task_list_id: str, title: str, ctx: Context) -> Optional[Dict[str, Any]]:
    """Update an existing task list.
    
    Args:
        task_list_id: The ID of the task list to update
        title: The new title for the task list
    """
    await ctx.info(f"Updating task list {task_list_id} with title: {title}")
    
    service = get_gtasks_service()
    task_list_data = TaskListUpdate(title=title)
    task_list = await service.update_task_list(task_list_id, task_list_data)
    
    if not task_list:
        await ctx.error(f"Task list '{task_list_id}' not found")
        return None
    
    await ctx.info(f"Updated task list: {task_list.title}")
    return asdict(task_list)

@gtasks_mcp.tool
async def delete_task_list(task_list_id: str, ctx: Context) -> bool:
    """Delete a task list.
    
    Args:
        task_list_id: The ID of the task list to delete
    """
    await ctx.info(f"Deleting task list: {task_list_id}")
    
    service = get_gtasks_service()
    success = await service.delete_task_list(task_list_id)
    
    if success:
        await ctx.info(f"Task list '{task_list_id}' deleted successfully")
    else:
        await ctx.error(f"Task list '{task_list_id}' not found")
    
    return success

# =============================================================================
# TASK TOOLS
# =============================================================================

@gtasks_mcp.tool
async def get_tasks(task_list_id: str, completed: Optional[bool] = None, ctx: Context = None) -> List[Dict[str, Any]]:
    """Get all tasks in a task list.
    
    Args:
        task_list_id: The ID of the task list
        completed: Filter by completion status (optional)
    """
    if ctx:
        await ctx.info(f"Fetching tasks from list: {task_list_id}")
    
    service = get_gtasks_service()
    tasks = await service.get_tasks(task_list_id, completed=completed)
    
    result = [asdict(task) for task in tasks]
    if ctx:
        await ctx.info(f"Found {len(result)} tasks")
    
    return result

@gtasks_mcp.tool
async def get_task(task_list_id: str, task_id: str, ctx: Context) -> Optional[Dict[str, Any]]:
    """Get a specific task by ID.
    
    Args:
        task_list_id: The ID of the task list
        task_id: The ID of the task to retrieve
    """
    await ctx.info(f"Fetching task {task_id} from list {task_list_id}")
    
    service = get_gtasks_service()
    task = await service.get_task(task_list_id, task_id)
    
    if not task:
        await ctx.error(f"Task '{task_id}' not found")
        return None
    
    await ctx.info(f"Retrieved task: {task.title}")
    return asdict(task)

@gtasks_mcp.tool
async def create_task(
    task_list_id: str, 
    title: str, 
    notes: Optional[str] = None,
    due: Optional[str] = None,
    parent: Optional[str] = None,
    previous: Optional[str] = None,
    ctx: Context = None
) -> Dict[str, Any]:
    """Create a new task in a task list.
    
    Args:
        task_list_id: The ID of the task list
        title: The title of the new task
        notes: Optional notes for the task
        due: Optional due date (ISO 8601 format)
        parent: Optional parent task ID for subtasks
        previous: Optional previous sibling task ID for ordering
    """
    if ctx:
        await ctx.info(f"Creating task '{title}' in list {task_list_id}")
    
    due_date = None
    if due:
        try:
            due_date = datetime.fromisoformat(due.replace('Z', '+00:00'))
        except ValueError:
            if ctx:
                await ctx.error(f"Invalid due date format: {due}")
            raise ValueError(f"Invalid due date format: {due}")
    
    service = get_gtasks_service()
    task_data = TaskCreate(
        title=title,
        notes=notes,
        due=due_date,
        parent=parent,
        previous=previous
    )
    task = await service.create_task(task_list_id, task_data)
    
    if ctx:
        await ctx.info(f"Created task: {task.title} (ID: {task.id})")
    
    return asdict(task)

@gtasks_mcp.tool
async def update_task(
    task_list_id: str,
    task_id: str,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    due: Optional[str] = None,
    status: Optional[str] = None,
    ctx: Context = None
) -> Optional[Dict[str, Any]]:
    """Update an existing task.
    
    Args:
        task_list_id: The ID of the task list
        task_id: The ID of the task to update
        title: New title for the task
        notes: New notes for the task
        due: New due date (ISO 8601 format)
        status: New status ('needsAction' or 'completed')
    """
    if ctx:
        await ctx.info(f"Updating task {task_id} in list {task_list_id}")
    
    due_date = None
    if due:
        try:
            due_date = datetime.fromisoformat(due.replace('Z', '+00:00'))
        except ValueError:
            if ctx:
                await ctx.error(f"Invalid due date format: {due}")
            raise ValueError(f"Invalid due date format: {due}")
    
    task_status = None
    if status:
        try:
            task_status = TaskStatus(status)
        except ValueError:
            if ctx:
                await ctx.error(f"Invalid status: {status}")
            raise ValueError(f"Invalid status: {status}")
    
    service = get_gtasks_service()
    task_data = TaskUpdate(
        title=title,
        notes=notes,
        due=due_date,
        status=task_status
    )
    task = await service.update_task(task_list_id, task_id, task_data)
    
    if not task:
        if ctx:
            await ctx.error(f"Task '{task_id}' not found")
        return None
    
    if ctx:
        await ctx.info(f"Updated task: {task.title}")
    
    return asdict(task)

@gtasks_mcp.tool
async def delete_task(task_list_id: str, task_id: str, ctx: Context) -> bool:
    """Delete a task.
    
    Args:
        task_list_id: The ID of the task list
        task_id: The ID of the task to delete
    """
    await ctx.info(f"Deleting task {task_id} from list {task_list_id}")
    
    service = get_gtasks_service()
    success = await service.delete_task(task_list_id, task_id)
    
    if success:
        await ctx.info(f"Task '{task_id}' deleted successfully")
    else:
        await ctx.error(f"Task '{task_id}' not found")
    
    return success

@gtasks_mcp.tool
async def complete_task(task_list_id: str, task_id: str, ctx: Context) -> Optional[Dict[str, Any]]:
    """Mark a task as completed.
    
    Args:
        task_list_id: The ID of the task list
        task_id: The ID of the task to complete
    """
    await ctx.info(f"Completing task {task_id} in list {task_list_id}")
    
    service = get_gtasks_service()
    task = await service.complete_task(task_list_id, task_id)
    
    if not task:
        await ctx.error(f"Task '{task_id}' not found")
        return None
    
    await ctx.info(f"Task completed: {task.title}")
    return asdict(task)

@gtasks_mcp.tool
async def uncomplete_task(task_list_id: str, task_id: str, ctx: Context) -> Optional[Dict[str, Any]]:
    """Mark a task as not completed.
    
    Args:
        task_list_id: The ID of the task list
        task_id: The ID of the task to mark as incomplete
    """
    await ctx.info(f"Marking task {task_id} as incomplete in list {task_list_id}")
    
    service = get_gtasks_service()
    task = await service.uncomplete_task(task_list_id, task_id)
    
    if not task:
        await ctx.error(f"Task '{task_id}' not found")
        return None
    
    await ctx.info(f"Task marked incomplete: {task.title}")
    return asdict(task)

@gtasks_mcp.tool
async def clear_completed_tasks(task_list_id: str, ctx: Context) -> str:
    """Clear all completed tasks from a task list.
    
    Args:
        task_list_id: The ID of the task list
    """
    await ctx.info(f"Clearing completed tasks from list {task_list_id}")
    
    service = get_gtasks_service()
    await service.clear_completed_tasks(task_list_id)
    
    await ctx.info(f"Cleared completed tasks from list '{task_list_id}'")
    return f"Cleared completed tasks from list '{task_list_id}'"

# =============================================================================
# SEARCH TOOLS
# =============================================================================

@gtasks_mcp.tool
async def search_tasks(query: str, task_list_id: Optional[str] = None, ctx: Context = None) -> List[Dict[str, Any]]:
    """Search for tasks by title or notes.
    
    Args:
        query: Search query to match against task titles and notes
        task_list_id: Optional task list ID to limit search scope
    """
    if ctx:
        await ctx.info(f"Searching tasks for: {query}")
    
    service = get_gtasks_service()
    tasks = await service.search_tasks(query, task_list_id)
    
    result = [asdict(task) for task in tasks]
    if ctx:
        await ctx.info(f"Found {len(result)} matching tasks")
    
    return result

# =============================================================================
# BATCH OPERATIONS
# =============================================================================

@gtasks_mcp.tool
async def create_multiple_tasks(
    task_list_id: str,
    tasks: List[Dict[str, Any]],
    ctx: Context
) -> Dict[str, Any]:
    """Create multiple tasks at once.
    
    Args:
        task_list_id: The ID of the task list
        tasks: Array of task objects with 'title' and optional 'notes', 'due'
    """
    await ctx.info(f"Creating {len(tasks)} tasks in list {task_list_id}")
    
    service = get_gtasks_service()
    created_tasks = []
    errors = []
    
    for i, task_data in enumerate(tasks):
        try:
            title = task_data.get("title")
            if not title:
                errors.append(f"Task {i+1}: Missing title")
                continue
            
            notes = task_data.get("notes")
            due_str = task_data.get("due")
            
            due_date = None
            if due_str:
                try:
                    due_date = datetime.fromisoformat(due_str.replace('Z', '+00:00'))
                except ValueError:
                    errors.append(f"Task {i+1}: Invalid due date format: {due_str}")
                    continue
            
            task_create = TaskCreate(title=title, notes=notes, due=due_date)
            task = await service.create_task(task_list_id, task_create)
            created_tasks.append(asdict(task))
            
        except Exception as e:
            errors.append(f"Task {i+1}: {str(e)}")
    
    await ctx.info(f"Created {len(created_tasks)} tasks, {len(errors)} errors")
    
    return {
        "created_tasks": created_tasks,
        "created_count": len(created_tasks),
        "errors": errors,
        "success": len(errors) == 0
    }

# =============================================================================
# SERVER ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Run the FastMCP server
    gtasks_mcp.run()
