#!/usr/bin/env python3
"""
FastMCP server for Google Tasks CRUD operations.
"""

from fastmcp import FastMCP
from typing import List, Optional, Dict, Any
import json

from .services.gtasks_service import GoogleTasksService
from .models.schemas import (
    TaskList, TaskListCreate, TaskListUpdate,
    Task, TaskCreate, TaskUpdate, TaskStatus
)

# Initialize FastMCP server
mcp = FastMCP("Google Tasks MCP Server 🚀")

# Global service instance
gtasks_service = None

def get_gtasks_service() -> GoogleTasksService:
    """Get Google Tasks service instance."""
    global gtasks_service
    if gtasks_service is None:
        gtasks_service = GoogleTasksService()
    return gtasks_service


# =============================================================================
# TASK LISTS TOOLS
# =============================================================================

@mcp.tool
async def get_task_lists() -> List[Dict[str, Any]]:
    """Get all task lists from Google Tasks."""
    try:
        gtasks = get_gtasks_service()
        task_lists = await gtasks.get_task_lists()
        return [task_list.model_dump() for task_list in task_lists]
    except Exception as e:
        raise Exception(f"Failed to fetch task lists: {str(e)}")


@mcp.tool
async def get_task_list(task_list_id: str) -> Dict[str, Any]:
    """Get a specific task list by ID."""
    try:
        gtasks = get_gtasks_service()
        task_list = await gtasks.get_task_list(task_list_id)
        if not task_list:
            raise Exception(f"Task list with ID {task_list_id} not found")
        return task_list.model_dump()
    except Exception as e:
        raise Exception(f"Failed to fetch task list: {str(e)}")


@mcp.tool
async def create_task_list(title: str) -> Dict[str, Any]:
    """Create a new task list."""
    try:
        gtasks = get_gtasks_service()
        task_list_data = TaskListCreate(title=title)
        task_list = await gtasks.create_task_list(task_list_data)
        return task_list.model_dump()
    except Exception as e:
        raise Exception(f"Failed to create task list: {str(e)}")


@mcp.tool
async def update_task_list(task_list_id: str, title: str) -> Dict[str, Any]:
    """Update a task list."""
    try:
        gtasks = get_gtasks_service()
        task_list_data = TaskListUpdate(title=title)
        task_list = await gtasks.update_task_list(task_list_id, task_list_data)
        if not task_list:
            raise Exception(f"Task list with ID {task_list_id} not found")
        return task_list.model_dump()
    except Exception as e:
        raise Exception(f"Failed to update task list: {str(e)}")


@mcp.tool
async def delete_task_list(task_list_id: str) -> Dict[str, str]:
    """Delete a task list."""
    try:
        gtasks = get_gtasks_service()
        success = await gtasks.delete_task_list(task_list_id)
        if not success:
            raise Exception(f"Task list with ID {task_list_id} not found")
        return {"message": f"Task list {task_list_id} deleted successfully"}
    except Exception as e:
        raise Exception(f"Failed to delete task list: {str(e)}")


# =============================================================================
# TASKS TOOLS
# =============================================================================

@mcp.tool
async def get_tasks(task_list_id: str, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Get all tasks in a task list."""
    try:
        gtasks = get_gtasks_service()
        tasks = await gtasks.get_tasks(task_list_id, completed=completed)
        return [task.model_dump() for task in tasks]
    except Exception as e:
        raise Exception(f"Failed to fetch tasks: {str(e)}")


@mcp.tool
async def get_task(task_list_id: str, task_id: str) -> Dict[str, Any]:
    """Get a specific task by ID."""
    try:
        gtasks = get_gtasks_service()
        task = await gtasks.get_task(task_list_id, task_id)
        if not task:
            raise Exception(f"Task with ID {task_id} not found")
        return task.model_dump()
    except Exception as e:
        raise Exception(f"Failed to fetch task: {str(e)}")


@mcp.tool
async def create_task(
    task_list_id: str, 
    title: str, 
    notes: Optional[str] = None,
    due: Optional[str] = None,
    parent: Optional[str] = None,
    previous: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new task in a task list."""
    try:
        gtasks = get_gtasks_service()
        
        # Parse due date if provided
        due_date = None
        if due:
            from datetime import datetime
            due_date = datetime.fromisoformat(due.replace('Z', '+00:00'))
        
        task_data = TaskCreate(
            title=title,
            notes=notes,
            due=due_date,
            parent=parent,
            previous=previous
        )
        task = await gtasks.create_task(task_list_id, task_data)
        return task.model_dump()
    except Exception as e:
        raise Exception(f"Failed to create task: {str(e)}")


@mcp.tool
async def update_task(
    task_list_id: str, 
    task_id: str,
    title: Optional[str] = None,
    notes: Optional[str] = None,
    due: Optional[str] = None,
    status: Optional[str] = None,
    parent: Optional[str] = None,
    previous: Optional[str] = None
) -> Dict[str, Any]:
    """Update a task."""
    try:
        gtasks = get_gtasks_service()
        
        # Parse due date if provided
        due_date = None
        if due:
            from datetime import datetime
            due_date = datetime.fromisoformat(due.replace('Z', '+00:00'))
        
        # Parse status if provided
        task_status = None
        if status:
            task_status = TaskStatus(status)
        
        task_data = TaskUpdate(
            title=title,
            notes=notes,
            due=due_date,
            status=task_status,
            parent=parent,
            previous=previous
        )
        task = await gtasks.update_task(task_list_id, task_id, task_data)
        if not task:
            raise Exception(f"Task with ID {task_id} not found")
        return task.model_dump()
    except Exception as e:
        raise Exception(f"Failed to update task: {str(e)}")


@mcp.tool
async def delete_task(task_list_id: str, task_id: str) -> Dict[str, str]:
    """Delete a task."""
    try:
        gtasks = get_gtasks_service()
        success = await gtasks.delete_task(task_list_id, task_id)
        if not success:
            raise Exception(f"Task with ID {task_id} not found")
        return {"message": f"Task {task_id} deleted successfully"}
    except Exception as e:
        raise Exception(f"Failed to delete task: {str(e)}")


@mcp.tool
async def complete_task(task_list_id: str, task_id: str) -> Dict[str, Any]:
    """Mark a task as completed."""
    try:
        gtasks = get_gtasks_service()
        task = await gtasks.complete_task(task_list_id, task_id)
        if not task:
            raise Exception(f"Task with ID {task_id} not found")
        return task.model_dump()
    except Exception as e:
        raise Exception(f"Failed to complete task: {str(e)}")


@mcp.tool
async def uncomplete_task(task_list_id: str, task_id: str) -> Dict[str, Any]:
    """Mark a task as not completed."""
    try:
        gtasks = get_gtasks_service()
        task = await gtasks.uncomplete_task(task_list_id, task_id)
        if not task:
            raise Exception(f"Task with ID {task_id} not found")
        return task.model_dump()
    except Exception as e:
        raise Exception(f"Failed to uncomplete task: {str(e)}")


@mcp.tool
async def clear_completed_tasks(task_list_id: str) -> Dict[str, str]:
    """Clear all completed tasks from a task list."""
    try:
        gtasks = get_gtasks_service()
        await gtasks.clear_completed_tasks(task_list_id)
        return {"message": f"Cleared completed tasks from task list {task_list_id}"}
    except Exception as e:
        raise Exception(f"Failed to clear completed tasks: {str(e)}")


# =============================================================================
# SEARCH TOOLS
# =============================================================================

@mcp.tool
async def search_tasks(query: str, task_list_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for tasks across all task lists or within a specific task list."""
    try:
        gtasks = get_gtasks_service()
        tasks = await gtasks.search_tasks(query, task_list_id)
        return [task.model_dump() for task in tasks]
    except Exception as e:
        raise Exception(f"Failed to search tasks: {str(e)}")


# =============================================================================
# UTILITY TOOLS
# =============================================================================

@mcp.tool
async def get_server_info() -> Dict[str, str]:
    """Get information about the Google Tasks MCP server."""
    return {
        "name": "Google Tasks MCP Server",
        "version": "1.0.0",
        "description": "FastMCP server for Google Tasks CRUD operations",
        "status": "active"
    }


# =============================================================================
# SERVER STARTUP
# =============================================================================

if __name__ == "__main__":
    print("🚀 Starting Google Tasks MCP Server...")
    mcp.run()
