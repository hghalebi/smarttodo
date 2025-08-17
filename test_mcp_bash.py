#!/usr/bin/env python3
"""
Simple BASH-friendly test for the MCP client.
This script tests the MCP client functionality in a minimal way.
"""

import sys
import os
import asyncio

# Add the source directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

def test_imports():
    """Test that we can import the MCP components."""
    print("🔍 Testing MCP Imports...")
    
    try:
        from source.api.mcp.client import GoogleTasksMCPClient
        print("✅ Successfully imported GoogleTasksMCPClient")
        
        from source.api.mcp.client import quick_get_task_lists, quick_create_task
        print("✅ Successfully imported quick functions")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_client_creation():
    """Test that we can create a client instance."""
    print("\n🔧 Testing Client Creation...")
    
    try:
        from source.api.mcp.client import GoogleTasksMCPClient
        
        client = GoogleTasksMCPClient()
        print("✅ Successfully created GoogleTasksMCPClient instance")
        
        # Test that client has expected methods
        expected_methods = [
            'get_task_lists', 'create_task', 'update_task', 
            'delete_task', 'search_tasks', 'complete_task'
        ]
        
        for method in expected_methods:
            if hasattr(client, method):
                print(f"✅ Method '{method}' exists")
            else:
                print(f"❌ Method '{method}' missing")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Client creation error: {e}")
        return False

async def test_client_tools():
    """Test listing available tools."""
    print("\n🛠️  Testing Tool Discovery...")
    
    try:
        from source.api.mcp.client import GoogleTasksMCPClient
        
        async with GoogleTasksMCPClient() as client:
            tools = await client.list_available_tools()
            print(f"✅ Found {len(tools)} available tools:")
            for tool in tools:
                print(f"   - {tool}")
            return True
            
    except Exception as e:
        print(f"❌ Tool discovery error: {e}")
        print("   This might be expected if Google Tasks API is not configured")
        return False

def test_server_import():
    """Test that we can import the server."""
    print("\n🖥️  Testing Server Import...")
    
    try:
        from source.api.mcp.server import gtasks_mcp
        print("✅ Successfully imported MCP server")
        
        # Check if the server has the expected structure
        if hasattr(gtasks_mcp, 'run'):
            print("✅ Server has 'run' method")
        else:
            print("❌ Server missing 'run' method")
            return False
            
        return True
    except ImportError as e:
        print(f"❌ Server import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 MCP Client BASH Testing Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports()),
        ("Client Creation", test_client_creation()),
        ("Server Import", test_server_import()),
        ("Tool Discovery", await test_client_tools())
    ]
    
    passed = sum(1 for name, result in tests if result)
    total = len(tests)
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP client is ready for use.")
        print("\n🚀 Next steps:")
        print("1. Configure Google Tasks API credentials")
        print("2. Run: python3 -m source.api.mcp.example_usage")
        print("3. Or start server: python3 -m source.api.mcp.run_server")
    else:
        print("❌ Some tests failed. Check the error messages above.")
        
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

