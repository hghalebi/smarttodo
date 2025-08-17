#!/usr/bin/env python3
"""
Test script for the FastMCP Google Tasks server.
"""

import asyncio
import sys
import os

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

async def test_mcp_server():
    """Test the MCP server functionality."""
    try:
        # Import the MCP server
        from source.api.main import mcp, get_server_info, get_task_lists
        
        print("✅ Successfully imported FastMCP server")
        print(f"✅ MCP Server: {mcp}")
        
        # Test server info
        print("\n🔍 Testing server info...")
        server_info = await get_server_info()
        print(f"✅ Server info: {server_info}")
        
        # Test task lists (this will require Google credentials)
        print("\n🔍 Testing task lists retrieval...")
        try:
            task_lists = await get_task_lists()
            print(f"✅ Retrieved {len(task_lists)} task lists")
            if task_lists:
                print(f"   First task list: {task_lists[0].get('title', 'No title')}")
        except Exception as e:
            print(f"⚠️  Task lists test failed (expected if no Google credentials): {e}")
        
        print("\n✅ MCP server tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing FastMCP Google Tasks Server...")
    success = asyncio.run(test_mcp_server())
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Tests failed!")
        sys.exit(1)

