"""
FastMCP client for Google Tasks operations.
"""

import asyncio
from typing import List, Dict, Any, Optional
from fastmcp import Client
from .server import gtasks_mcp


async def create_gtasks_client():
    """Create a FastMCP client connected to the Google Tasks server.
    
    Returns:
        Client: Connected FastMCP client instance
    """
    # Use in-memory transport for direct connection to the server
    return Client(gtasks_mcp)


class GoogleTasksMCPClient:
    """High-level client for Google Tasks MCP operations."""
    
    def __init__(self):
        self.client = None
    
    def _extract_result(self, result) -> Any:
        """Extract the actual result from MCP tool call response."""
        if not result:
            return None
        
        # FastMCP tools return data directly
        if hasattr(result, 'content') and result.content:
            content = result.content[0]
            if hasattr(content, 'text'):
                return content.text
            else:
                return content
        
        # Fallback to the result itself
        return result
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.client = await create_gtasks_client()
        await self.client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.__aexit__(exc_type, exc_val, exc_tb)
    
    async def connect(self):
        """Connect to the MCP server."""
        if not self.client:
            self.client = await create_gtasks_client()
            await self.client.__aenter__()
    
    async def disconnect(self):
        """Disconnect from the MCP server."""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None
    
    # =============================================================================
    # TASK LIST OPERATIONS
    # =============================================================================
    
    async def get_task_lists(self) -> List[Dict[str, Any]]:
        """Get all task lists."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("get_task_lists")
        return self._extract_result(result) or []
    
    async def get_task_list(self, task_list_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task list by ID."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("get_task_list", {"task_list_id": task_list_id})
        return self._extract_result(result)
    
    async def create_task_list(self, title: str) -> Dict[str, Any]:
        """Create a new task list."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("create_task_list", {"title": title})
        return self._extract_result(result) or {}
    
    async def update_task_list(self, task_list_id: str, title: str) -> Optional[Dict[str, Any]]:
        """Update a task list."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("update_task_list", {
            "task_list_id": task_list_id,
            "title": title
        })
        return self._extract_result(result)
    
    async def delete_task_list(self, task_list_id: str) -> bool:
        """Delete a task list."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("delete_task_list", {"task_list_id": task_list_id})
        return self._extract_result(result) or False
    
    # =============================================================================
    # TASK OPERATIONS
    # =============================================================================
    
    async def get_tasks(self, task_list_id: str, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get all tasks in a task list."""
        if not self.client:
            await self.connect()
        
        params = {"task_list_id": task_list_id}
        if completed is not None:
            params["completed"] = completed
        
        result = await self.client.call_tool("get_tasks", params)
        return self._extract_result(result) or []
    
    async def get_task(self, task_list_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("get_task", {
            "task_list_id": task_list_id,
            "task_id": task_id
        })
        return self._extract_result(result)
    
    async def create_task(
        self,
        task_list_id: str,
        title: str,
        notes: Optional[str] = None,
        due: Optional[str] = None,
        parent: Optional[str] = None,
        previous: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new task."""
        if not self.client:
            await self.connect()
        
        params = {
            "task_list_id": task_list_id,
            "title": title
        }
        
        if notes:
            params["notes"] = notes
        if due:
            params["due"] = due
        if parent:
            params["parent"] = parent
        if previous:
            params["previous"] = previous
        
        result = await self.client.call_tool("create_task", params)
        return self._extract_result(result) or {}
    
    async def update_task(
        self,
        task_list_id: str,
        task_id: str,
        title: Optional[str] = None,
        notes: Optional[str] = None,
        due: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Update a task."""
        if not self.client:
            await self.connect()
        
        params = {
            "task_list_id": task_list_id,
            "task_id": task_id
        }
        
        if title:
            params["title"] = title
        if notes:
            params["notes"] = notes
        if due:
            params["due"] = due
        if status:
            params["status"] = status
        
        result = await self.client.call_tool("update_task", params)
        return self._extract_result(result)
    
    async def delete_task(self, task_list_id: str, task_id: str) -> bool:
        """Delete a task."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("delete_task", {
            "task_list_id": task_list_id,
            "task_id": task_id
        })
        return self._extract_result(result) or False
    
    async def complete_task(self, task_list_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """Mark a task as completed."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("complete_task", {
            "task_list_id": task_list_id,
            "task_id": task_id
        })
        return self._extract_result(result)
    
    async def uncomplete_task(self, task_list_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """Mark a task as not completed."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("uncomplete_task", {
            "task_list_id": task_list_id,
            "task_id": task_id
        })
        return self._extract_result(result)
    
    async def clear_completed_tasks(self, task_list_id: str) -> str:
        """Clear all completed tasks from a task list."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("clear_completed_tasks", {"task_list_id": task_list_id})
        return self._extract_result(result) or ""
    
    # =============================================================================
    # SEARCH OPERATIONS
    # =============================================================================
    
    async def search_tasks(self, query: str, task_list_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for tasks by title or notes."""
        if not self.client:
            await self.connect()
        
        params = {"query": query}
        if task_list_id:
            params["task_list_id"] = task_list_id
        
        result = await self.client.call_tool("search_tasks", params)
        return self._extract_result(result) or []
    
    # =============================================================================
    # BATCH OPERATIONS
    # =============================================================================
    
    async def create_multiple_tasks(
        self,
        task_list_id: str,
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create multiple tasks at once."""
        if not self.client:
            await self.connect()
        
        result = await self.client.call_tool("create_multiple_tasks", {
            "task_list_id": task_list_id,
            "tasks": tasks
        })
        return self._extract_result(result) or {}
    
    # =============================================================================
    # UTILITY METHODS
    # =============================================================================
    
    async def list_available_tools(self) -> List[str]:
        """List all available MCP tools."""
        if not self.client:
            await self.connect()
        
        tools = await self.client.list_tools()
        # Handle different possible return formats from FastMCP
        if hasattr(tools, 'tools'):
            return [tool.name for tool in tools.tools]
        elif isinstance(tools, list):
            return [tool.name if hasattr(tool, 'name') else str(tool) for tool in tools]
        else:
            # Fallback - return empty list if structure is unexpected
            return []
    
    async def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """Get information about a specific tool."""
        if not self.client:
            await self.connect()
        
        tools = await self.client.list_tools()
        # Handle different possible return formats from FastMCP
        tool_list = []
        if hasattr(tools, 'tools'):
            tool_list = tools.tools
        elif isinstance(tools, list):
            tool_list = tools
        
        for tool in tool_list:
            if hasattr(tool, 'name') and tool.name == tool_name:
                return {
                    "name": tool.name,
                    "description": getattr(tool, 'description', ''),
                    "input_schema": getattr(tool, 'inputSchema', {})
                }
        return {}


# Convenience functions for quick usage

async def quick_get_task_lists() -> List[Dict[str, Any]]:
    """Quick function to get all task lists."""
    async with GoogleTasksMCPClient() as client:
        return await client.get_task_lists()

async def quick_create_task(task_list_id: str, title: str, **kwargs) -> Dict[str, Any]:
    """Quick function to create a task."""
    async with GoogleTasksMCPClient() as client:
        return await client.create_task(task_list_id, title, **kwargs)

async def quick_search_tasks(query: str, task_list_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Quick function to search tasks."""
    async with GoogleTasksMCPClient() as client:
        return await client.search_tasks(query, task_list_id)
