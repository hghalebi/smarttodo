"""
Google Tasks service layer for API operations.
"""

import os
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

from ..models.schemas import (
    TaskList, TaskListCreate, TaskListUpdate,
    Task, TaskCreate, TaskUpdate, TaskStatus
)


class GoogleTasksService:
    """Service class for Google Tasks operations."""
    
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    
    def __init__(self):
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Tasks service."""
        try:
            creds = self._get_credentials()
            self.service = build('tasks', 'v1', credentials=creds)
        except Exception as e:
            print(f"Failed to initialize Google Tasks service: {e}")
            raise e
    
    def _get_credentials(self) -> Credentials:
        """Get or refresh Google API credentials."""
        creds = None
        token_path = 'token.json'
        credentials_path = 'credentials.json'
        
        # Load existing credentials
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found: {credentials_path}. "
                        "Please download OAuth 2.0 credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def _run_async(self, func, *args, **kwargs):
        """Run synchronous Google API calls in async context."""
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, func, *args, **kwargs)
    
    def _convert_task_list(self, task_list_data: Dict[str, Any]) -> TaskList:
        """Convert Google API task list data to TaskList model."""
        return TaskList(
            id=task_list_data.get('id'),
            title=task_list_data.get('title', ''),
            updated=self._parse_datetime(task_list_data.get('updated')),
            self_link=task_list_data.get('selfLink'),
            kind=task_list_data.get('kind'),
            etag=task_list_data.get('etag')
        )
    
    def _convert_task(self, task_data: Dict[str, Any]) -> Task:
        """Convert Google API task data to Task model."""
        return Task(
            id=task_data.get('id'),
            title=task_data.get('title', ''),
            notes=task_data.get('notes'),
            status=TaskStatus(task_data.get('status', 'needsAction')),
            due=self._parse_datetime(task_data.get('due')),
            updated=self._parse_datetime(task_data.get('updated')),
            completed=self._parse_datetime(task_data.get('completed')),
            parent=task_data.get('parent'),
            position=task_data.get('position'),
            hidden=task_data.get('hidden'),
            deleted=task_data.get('deleted'),
            self_link=task_data.get('selfLink'),
            kind=task_data.get('kind'),
            etag=task_data.get('etag'),
            links=task_data.get('links')
        )
    
    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string from Google API."""
        if not date_str:
            return None
        try:
            # Handle RFC 3339 format
            if 'T' in date_str:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                # Handle date-only format
                return datetime.fromisoformat(date_str)
        except ValueError:
            return None
    
    def _format_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        """Format datetime for Google API."""
        if not dt:
            return None
        return dt.isoformat()
    
    # =============================================================================
    # TASK LIST OPERATIONS
    # =============================================================================
    
    async def get_task_lists(self) -> List[TaskList]:
        """Get all task lists."""
        def _get_task_lists():
            try:
                result = self.service.tasklists().list().execute()
                items = result.get('items', [])
                return [self._convert_task_list(item) for item in items]
            except HttpError as e:
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_get_task_lists)
    
    async def get_task_list(self, task_list_id: str) -> Optional[TaskList]:
        """Get a specific task list by ID."""
        def _get_task_list():
            try:
                result = self.service.tasklists().get(tasklist=task_list_id).execute()
                return self._convert_task_list(result)
            except HttpError as e:
                if e.resp.status == 404:
                    return None
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_get_task_list)
    
    async def create_task_list(self, task_list_data: TaskListCreate) -> TaskList:
        """Create a new task list."""
        def _create_task_list():
            try:
                body = {'title': task_list_data.title}
                result = self.service.tasklists().insert(body=body).execute()
                return self._convert_task_list(result)
            except HttpError as e:
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_create_task_list)
    
    async def update_task_list(self, task_list_id: str, task_list_data: TaskListUpdate) -> Optional[TaskList]:
        """Update a task list."""
        def _update_task_list():
            try:
                # First check if task list exists
                existing = self.service.tasklists().get(tasklist=task_list_id).execute()
                
                # Prepare update body
                body = {'id': task_list_id}
                if task_list_data.title is not None:
                    body['title'] = task_list_data.title
                
                result = self.service.tasklists().update(
                    tasklist=task_list_id, 
                    body=body
                ).execute()
                return self._convert_task_list(result)
            except HttpError as e:
                if e.resp.status == 404:
                    return None
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_update_task_list)
    
    async def delete_task_list(self, task_list_id: str) -> bool:
        """Delete a task list."""
        def _delete_task_list():
            try:
                self.service.tasklists().delete(tasklist=task_list_id).execute()
                return True
            except HttpError as e:
                if e.resp.status == 404:
                    return False
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_delete_task_list)
    
    # =============================================================================
    # TASK OPERATIONS
    # =============================================================================
    
    async def get_tasks(self, task_list_id: str, completed: Optional[bool] = None) -> List[Task]:
        """Get all tasks in a task list."""
        def _get_tasks():
            try:
                params = {'tasklist': task_list_id}
                if completed is not None:
                    if completed:
                        params['showCompleted'] = True
                    else:
                        params['showCompleted'] = False
                        params['showHidden'] = False
                
                result = self.service.tasks().list(**params).execute()
                items = result.get('items', [])
                return [self._convert_task(item) for item in items]
            except HttpError as e:
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_get_tasks)
    
    async def get_task(self, task_list_id: str, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        def _get_task():
            try:
                result = self.service.tasks().get(
                    tasklist=task_list_id, 
                    task=task_id
                ).execute()
                return self._convert_task(result)
            except HttpError as e:
                if e.resp.status == 404:
                    return None
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_get_task)
    
    async def create_task(self, task_list_id: str, task_data: TaskCreate) -> Task:
        """Create a new task."""
        def _create_task():
            try:
                body = {
                    'title': task_data.title,
                }
                
                if task_data.notes:
                    body['notes'] = task_data.notes
                if task_data.due:
                    body['due'] = self._format_datetime(task_data.due)
                
                params = {'tasklist': task_list_id, 'body': body}
                if task_data.parent:
                    params['parent'] = task_data.parent
                if task_data.previous:
                    params['previous'] = task_data.previous
                
                result = self.service.tasks().insert(**params).execute()
                return self._convert_task(result)
            except HttpError as e:
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_create_task)
    
    async def update_task(self, task_list_id: str, task_id: str, task_data: TaskUpdate) -> Optional[Task]:
        """Update a task."""
        def _update_task():
            try:
                # First get existing task
                existing = self.service.tasks().get(
                    tasklist=task_list_id, 
                    task=task_id
                ).execute()
                
                # Prepare update body
                body = {'id': task_id}
                
                if task_data.title is not None:
                    body['title'] = task_data.title
                if task_data.notes is not None:
                    body['notes'] = task_data.notes
                if task_data.due is not None:
                    body['due'] = self._format_datetime(task_data.due)
                if task_data.status is not None:
                    body['status'] = task_data.status.value
                
                params = {
                    'tasklist': task_list_id,
                    'task': task_id,
                    'body': body
                }
                
                result = self.service.tasks().update(**params).execute()
                return self._convert_task(result)
            except HttpError as e:
                if e.resp.status == 404:
                    return None
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_update_task)
    
    async def delete_task(self, task_list_id: str, task_id: str) -> bool:
        """Delete a task."""
        def _delete_task():
            try:
                self.service.tasks().delete(
                    tasklist=task_list_id, 
                    task=task_id
                ).execute()
                return True
            except HttpError as e:
                if e.resp.status == 404:
                    return False
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_delete_task)
    
    async def complete_task(self, task_list_id: str, task_id: str) -> Optional[Task]:
        """Mark a task as completed."""
        task_update = TaskUpdate(status=TaskStatus.COMPLETED)
        return await self.update_task(task_list_id, task_id, task_update)
    
    async def uncomplete_task(self, task_list_id: str, task_id: str) -> Optional[Task]:
        """Mark a task as not completed."""
        task_update = TaskUpdate(status=TaskStatus.NEEDS_ACTION)
        return await self.update_task(task_list_id, task_id, task_update)
    
    async def clear_completed_tasks(self, task_list_id: str) -> None:
        """Clear all completed tasks from a task list."""
        def _clear_completed():
            try:
                self.service.tasks().clear(tasklist=task_list_id).execute()
            except HttpError as e:
                raise Exception(f"Google API error: {e}")
        
        await self._run_async(_clear_completed)
    
    # =============================================================================
    # SEARCH OPERATIONS
    # =============================================================================
    
    async def search_tasks(self, query: str, task_list_id: Optional[str] = None) -> List[Task]:
        """Search for tasks by title or notes."""
        def _search_tasks():
            try:
                all_tasks = []
                
                if task_list_id:
                    # Search in specific task list
                    task_lists = [{'id': task_list_id}]
                else:
                    # Search in all task lists
                    result = self.service.tasklists().list().execute()
                    task_lists = result.get('items', [])
                
                query_lower = query.lower()
                
                for task_list in task_lists:
                    try:
                        result = self.service.tasks().list(
                            tasklist=task_list['id'],
                            showCompleted=True,
                            showHidden=True
                        ).execute()
                        
                        tasks = result.get('items', [])
                        
                        # Filter tasks by query
                        for task in tasks:
                            title = task.get('title', '').lower()
                            notes = task.get('notes', '').lower()
                            
                            if query_lower in title or query_lower in notes:
                                all_tasks.append(self._convert_task(task))
                                
                    except HttpError:
                        # Skip task lists that can't be accessed
                        continue
                
                return all_tasks
            except HttpError as e:
                raise Exception(f"Google API error: {e}")
        
        return await self._run_async(_search_tasks)
