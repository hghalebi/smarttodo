"""
MCP (Model Context Protocol) integration for Google Tasks using FastMCP.
"""

from .server import gtasks_mcp
from .client import create_gtasks_client

__all__ = [
    'gtasks_mcp',
    'create_gtasks_client'
]
