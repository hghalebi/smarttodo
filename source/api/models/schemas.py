"""
Pydantic models for Google Tasks API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration."""
    NEEDS_ACTION = "needsAction"
    COMPLETED = "completed"


# =============================================================================
# TASK LIST MODELS
# =============================================================================

class TaskListBase(BaseModel):
    """Base task list model."""
    title: str = Field(..., description="Task list title", min_length=1, max_length=100)


class TaskListCreate(TaskListBase):
    """Task list creation model."""
    pass


class TaskListUpdate(BaseModel):
    """Task list update model."""
    title: Optional[str] = Field(None, description="Task list title", min_length=1, max_length=100)


class TaskList(TaskListBase):
    """Task list response model."""
    id: str = Field(..., description="Task list ID")
    updated: Optional[datetime] = Field(None, description="Last updated timestamp")
    self_link: Optional[str] = Field(None, description="Self link URL")
    kind: Optional[str] = Field(None, description="Resource kind")
    etag: Optional[str] = Field(None, description="ETag")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


# =============================================================================
# TASK MODELS
# =============================================================================

class TaskBase(BaseModel):
    """Base task model."""
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    notes: Optional[str] = Field(None, description="Task notes", max_length=8192)
    due: Optional[datetime] = Field(None, description="Due date")


class TaskCreate(TaskBase):
    """Task creation model."""
    parent: Optional[str] = Field(None, description="Parent task ID")
    previous: Optional[str] = Field(None, description="Previous sibling task ID")


class TaskUpdate(BaseModel):
    """Task update model."""
    title: Optional[str] = Field(None, description="Task title", min_length=1, max_length=200)
    notes: Optional[str] = Field(None, description="Task notes", max_length=8192)
    due: Optional[datetime] = Field(None, description="Due date")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    parent: Optional[str] = Field(None, description="Parent task ID")
    previous: Optional[str] = Field(None, description="Previous sibling task ID")


class Task(TaskBase):
    """Task response model."""
    id: str = Field(..., description="Task ID")
    status: TaskStatus = Field(default=TaskStatus.NEEDS_ACTION, description="Task status")
    updated: Optional[datetime] = Field(None, description="Last updated timestamp")
    completed: Optional[datetime] = Field(None, description="Completion timestamp")
    parent: Optional[str] = Field(None, description="Parent task ID")
    position: Optional[str] = Field(None, description="Task position")
    hidden: Optional[bool] = Field(None, description="Whether task is hidden")
    deleted: Optional[bool] = Field(None, description="Whether task is deleted")
    self_link: Optional[str] = Field(None, description="Self link URL")
    kind: Optional[str] = Field(None, description="Resource kind")
    etag: Optional[str] = Field(None, description="ETag")
    links: Optional[List[dict]] = Field(None, description="Related links")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


# =============================================================================
# RESPONSE MODELS
# =============================================================================

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    detail: Optional[str] = Field(None, description="Additional error details")


class SuccessResponse(BaseModel):
    """Generic success response model."""
    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Additional data")


class PaginatedResponse(BaseModel):
    """Paginated response model."""
    items: List[dict] = Field(..., description="Items in current page")
    page_token: Optional[str] = Field(None, description="Next page token")
    total_count: Optional[int] = Field(None, description="Total item count")


# =============================================================================
# SEARCH MODELS
# =============================================================================

class SearchQuery(BaseModel):
    """Search query model."""
    query: str = Field(..., description="Search query", min_length=1)
    task_list_id: Optional[str] = Field(None, description="Specific task list to search in")
    include_completed: bool = Field(default=True, description="Include completed tasks")
    limit: int = Field(default=50, description="Maximum results to return", ge=1, le=100)


class SearchResult(BaseModel):
    """Search result model."""
    tasks: List[Task] = Field(..., description="Matching tasks")
    total_count: int = Field(..., description="Total matching tasks")
    query: str = Field(..., description="Original search query")


# =============================================================================
# FILTER MODELS
# =============================================================================

class TaskFilter(BaseModel):
    """Task filtering options."""
    status: Optional[TaskStatus] = Field(None, description="Filter by status")
    completed_min: Optional[datetime] = Field(None, description="Minimum completion date")
    completed_max: Optional[datetime] = Field(None, description="Maximum completion date")
    due_min: Optional[datetime] = Field(None, description="Minimum due date")
    due_max: Optional[datetime] = Field(None, description="Maximum due date")
    updated_min: Optional[datetime] = Field(None, description="Minimum update date")
    show_completed: bool = Field(default=True, description="Include completed tasks")
    show_hidden: bool = Field(default=False, description="Include hidden tasks")
    show_deleted: bool = Field(default=False, description="Include deleted tasks")


# =============================================================================
# BATCH OPERATION MODELS
# =============================================================================

class BatchTaskUpdate(BaseModel):
    """Batch task update model."""
    task_ids: List[str] = Field(..., description="List of task IDs to update")
    updates: TaskUpdate = Field(..., description="Updates to apply")


class BatchTaskOperation(BaseModel):
    """Batch task operation result."""
    success_count: int = Field(..., description="Number of successful operations")
    failure_count: int = Field(..., description="Number of failed operations")
    errors: List[str] = Field(default=[], description="Error messages for failed operations")


# =============================================================================
# STATISTICS MODELS
# =============================================================================

class TaskListStats(BaseModel):
    """Task list statistics."""
    task_list_id: str = Field(..., description="Task list ID")
    total_tasks: int = Field(..., description="Total number of tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    pending_tasks: int = Field(..., description="Number of pending tasks")
    overdue_tasks: int = Field(..., description="Number of overdue tasks")
    completion_rate: float = Field(..., description="Completion rate percentage")


class OverallStats(BaseModel):
    """Overall statistics across all task lists."""
    total_task_lists: int = Field(..., description="Total number of task lists")
    total_tasks: int = Field(..., description="Total number of tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    pending_tasks: int = Field(..., description="Number of pending tasks")
    overdue_tasks: int = Field(..., description="Number of overdue tasks")
    overall_completion_rate: float = Field(..., description="Overall completion rate percentage")
    task_list_stats: List[TaskListStats] = Field(..., description="Per-list statistics")
