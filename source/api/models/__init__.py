"""
Models package for Google Tasks API.
"""

from .schemas import (
    # Task List models
    TaskList,
    TaskListCreate,
    TaskListUpdate,
    TaskListBase,
    
    # Task models
    Task,
    TaskCreate,
    TaskUpdate,
    TaskBase,
    TaskStatus,
    
    # Response models
    ErrorResponse,
    SuccessResponse,
    PaginatedResponse,
    
    # Search models
    SearchQuery,
    SearchResult,
    
    # Filter models
    TaskFilter,
    
    # Batch operation models
    BatchTaskUpdate,
    BatchTaskOperation,
    
    # Statistics models
    TaskListStats,
    OverallStats,
)

__all__ = [
    # Task List models
    "TaskList",
    "TaskListCreate", 
    "TaskListUpdate",
    "TaskListBase",
    
    # Task models
    "Task",
    "TaskCreate",
    "TaskUpdate", 
    "TaskBase",
    "TaskStatus",
    
    # Response models
    "ErrorResponse",
    "SuccessResponse",
    "PaginatedResponse",
    
    # Search models
    "SearchQuery",
    "SearchResult",
    
    # Filter models
    "TaskFilter",
    
    # Batch operation models
    "BatchTaskUpdate",
    "BatchTaskOperation",
    
    # Statistics models
    "TaskListStats",
    "OverallStats",
]
