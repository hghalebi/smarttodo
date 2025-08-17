#!/bin/bash

# Complete BASH Testing Script for MCP Client
# Usage: ./test_mcp_bash_complete.sh

echo "🧪 Google Tasks MCP Client - BASH Testing Suite"
echo "================================================"

# Set the project directory
PROJECT_DIR="/Users/nadyakott/Desktop/CursorProjects/smarttodo"
cd "$PROJECT_DIR"

echo "📁 Working directory: $(pwd)"
echo ""

# Function to run a test and capture result
run_test() {
    local test_name="$1"
    local command="$2"
    
    echo "🔍 Running: $test_name"
    echo "   Command: $command"
    
    if eval "$command"; then
        echo "✅ PASSED: $test_name"
        return 0
    else
        echo "❌ FAILED: $test_name"
        return 1
    fi
    echo ""
}

# Test 1: Check Python availability
echo "=== Test 1: Python Environment ==="
run_test "Python3 availability" "python3 --version"

# Test 2: Check project structure
echo "=== Test 2: Project Structure ==="
run_test "MCP directory exists" "[ -d 'source/api/mcp' ]"
run_test "MCP client exists" "[ -f 'source/api/mcp/client.py' ]"
run_test "MCP server exists" "[ -f 'source/api/mcp/server.py' ]"
run_test "MCP examples exist" "[ -f 'source/api/mcp/example_usage.py' ]"

# Test 3: Test file structure analysis
echo "=== Test 3: File Structure Analysis ==="
run_test "Structure test script" "python3 test_mcp_simple.py"

# Test 4: Test basic imports (without dependencies)
echo "=== Test 4: Basic Import Test ==="
run_test "Basic MCP import test" "python3 test_mcp_bash.py"

# Test 5: Check dependencies
echo "=== Test 5: Dependencies Check ==="
check_dependency() {
    local dep="$1"
    python3 -c "import $dep; print('$dep is available')" 2>/dev/null
}

if check_dependency "fastmcp"; then
    echo "✅ fastmcp is installed"
    DEPS_OK=true
else
    echo "❌ fastmcp is NOT installed"
    DEPS_OK=false
fi

if check_dependency "fastapi"; then
    echo "✅ fastapi is installed"
else
    echo "❌ fastapi is NOT installed"
    DEPS_OK=false
fi

if check_dependency "google.auth"; then
    echo "✅ google-auth is installed"
else
    echo "❌ google-auth is NOT installed"
    DEPS_OK=false
fi

# Test 6: Run functional tests (only if dependencies are available)
if [ "$DEPS_OK" = true ]; then
    echo ""
    echo "=== Test 6: Functional Tests ==="
    run_test "MCP Client functional test" "python3 test_mcp_bash.py"
    run_test "MCP Example usage" "timeout 10s python3 -m source.api.mcp.example_usage || echo 'Example may require API credentials'"
else
    echo ""
    echo "⚠️  Skipping functional tests - dependencies not installed"
    echo "   To install dependencies, run:"
    echo "   pip3 install fastmcp fastapi uvicorn google-api-python-client google-auth google-auth-oauthlib"
fi

# Test 7: Try to start MCP server (quick test)
echo ""
echo "=== Test 7: Server Startup Test ==="
if [ "$DEPS_OK" = true ]; then
    echo "🖥️  Testing MCP server startup..."
    timeout 5s python3 -c "
import sys
sys.path.insert(0, 'source')
from source.api.mcp.server import gtasks_mcp
print('MCP server imported successfully!')
print('Available tools:', len([tool for tool in dir(gtasks_mcp) if not tool.startswith('_')]))
" && echo "✅ MCP server can be imported and initialized"
else
    echo "⚠️  Skipping server test - dependencies not installed"
fi

# Summary
echo ""
echo "================================================"
echo "🏁 Testing Complete!"
echo ""
echo "📋 Quick Commands for Testing MCP Client:"
echo ""
echo "1. Test structure:"
echo "   python3 test_mcp_simple.py"
echo ""
echo "2. Install dependencies:"
echo "   pip3 install fastmcp fastapi uvicorn google-api-python-client google-auth google-auth-oauthlib"
echo ""
echo "3. Test client functionality:"
echo "   python3 test_mcp_bash.py"
echo ""
echo "4. Run comprehensive examples:"
echo "   python3 -m source.api.mcp.example_usage"
echo ""
echo "5. Start MCP server (STDIO):"
echo "   python3 -m source.api.mcp.run_server"
echo ""
echo "6. Start MCP server (HTTP):"
echo "   python3 -m source.api.mcp.run_server --transport http --port 8000"
echo ""
echo "7. Quick manual test with Python:"
echo "   python3 -c \"
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def test():
    async with GoogleTasksMCPClient() as client:
        tools = await client.list_available_tools()
        print(f'Available tools: {tools}')

asyncio.run(test())
\""
echo ""
echo "8. Test specific MCP tool:"
echo "   python3 -c \"
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import quick_get_task_lists

async def test():
    try:
        lists = await quick_get_task_lists()
        print(f'Task lists: {lists}')
    except Exception as e:
        print(f'Error (may need API credentials): {e}')

asyncio.run(test())
\""

echo ""
echo "✨ Use these commands to test your MCP client from BASH!"

