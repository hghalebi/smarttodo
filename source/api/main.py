#!/usr/bin/env python3
"""
FastAPI application for Google Tasks CRUD operations.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional

from .services.gtasks_service import GoogleTasksService
from .models.schemas import (
    TaskList, TaskListCreate, TaskListUpdate,
    Task, TaskCreate, TaskUpdate,
    ErrorResponse
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 Starting Google Tasks API...")
    yield
    # Shutdown
    print("🛑 Shutting down Google Tasks API...")


app = FastAPI(
    title="Google Tasks API",
    description="FastAPI layer for Google Tasks CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get Google Tasks service
def get_gtasks_service() -> GoogleTasksService:
    """Get Google Tasks service instance."""
    return GoogleTasksService()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Google Tasks API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Google Tasks API"}


# =============================================================================
# TASK LISTS ENDPOINTS
# =============================================================================

@app.get("/task-lists", response_model=List[TaskList])
async def get_task_lists(
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Get all task lists."""
    try:
        task_lists = await gtasks.get_task_lists()
        return task_lists
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch task lists: {str(e)}"
        )


@app.get("/task-lists/{task_list_id}", response_model=TaskList)
async def get_task_list(
    task_list_id: str,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Get a specific task list by ID."""
    try:
        task_list = await gtasks.get_task_list(task_list_id)
        if not task_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task list with ID {task_list_id} not found"
            )
        return task_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch task list: {str(e)}"
        )


@app.post("/task-lists", response_model=TaskList, status_code=status.HTTP_201_CREATED)
async def create_task_list(
    task_list_data: TaskListCreate,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Create a new task list."""
    try:
        task_list = await gtasks.create_task_list(task_list_data)
        return task_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task list: {str(e)}"
        )


@app.put("/task-lists/{task_list_id}", response_model=TaskList)
async def update_task_list(
    task_list_id: str,
    task_list_data: TaskListUpdate,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Update a task list."""
    try:
        task_list = await gtasks.update_task_list(task_list_id, task_list_data)
        if not task_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task list with ID {task_list_id} not found"
            )
        return task_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task list: {str(e)}"
        )


@app.delete("/task-lists/{task_list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_list(
    task_list_id: str,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Delete a task list."""
    try:
        success = await gtasks.delete_task_list(task_list_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task list with ID {task_list_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task list: {str(e)}"
        )


# =============================================================================
# TASKS ENDPOINTS
# =============================================================================

@app.get("/task-lists/{task_list_id}/tasks", response_model=List[Task])
async def get_tasks(
    task_list_id: str,
    completed: Optional[bool] = None,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Get all tasks in a task list."""
    try:
        tasks = await gtasks.get_tasks(task_list_id, completed=completed)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tasks: {str(e)}"
        )


@app.get("/task-lists/{task_list_id}/tasks/{task_id}", response_model=Task)
async def get_task(
    task_list_id: str,
    task_id: str,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Get a specific task by ID."""
    try:
        task = await gtasks.get_task(task_list_id, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch task: {str(e)}"
        )


@app.post("/task-lists/{task_list_id}/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_list_id: str,
    task_data: TaskCreate,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Create a new task in a task list."""
    try:
        task = await gtasks.create_task(task_list_id, task_data)
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@app.put("/task-lists/{task_list_id}/tasks/{task_id}", response_model=Task)
async def update_task(
    task_list_id: str,
    task_id: str,
    task_data: TaskUpdate,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Update a task."""
    try:
        task = await gtasks.update_task(task_list_id, task_id, task_data)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@app.delete("/task-lists/{task_list_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_list_id: str,
    task_id: str,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Delete a task."""
    try:
        success = await gtasks.delete_task(task_list_id, task_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )


@app.patch("/task-lists/{task_list_id}/tasks/{task_id}/complete", response_model=Task)
async def complete_task(
    task_list_id: str,
    task_id: str,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Mark a task as completed."""
    try:
        task = await gtasks.complete_task(task_list_id, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete task: {str(e)}"
        )


@app.patch("/task-lists/{task_list_id}/tasks/{task_id}/uncomplete", response_model=Task)
async def uncomplete_task(
    task_list_id: str,
    task_id: str,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Mark a task as not completed."""
    try:
        task = await gtasks.uncomplete_task(task_list_id, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to uncomplete task: {str(e)}"
        )


@app.delete("/task-lists/{task_list_id}/tasks/completed", status_code=status.HTTP_204_NO_CONTENT)
async def clear_completed_tasks(
    task_list_id: str,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Clear all completed tasks from a task list."""
    try:
        await gtasks.clear_completed_tasks(task_list_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear completed tasks: {str(e)}"
        )


# =============================================================================
# SEARCH ENDPOINTS
# =============================================================================

@app.get("/search/tasks", response_model=List[Task])
async def search_tasks(
    query: str,
    task_list_id: Optional[str] = None,
    gtasks: GoogleTasksService = Depends(get_gtasks_service)
):
    """Search for tasks across all task lists or within a specific task list."""
    try:
        tasks = await gtasks.search_tasks(query, task_list_id)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search tasks: {str(e)}"
        )


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
