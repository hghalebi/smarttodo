# MCP Client Testing - BASH Commands

## Quick BASH Commands for Testing MCP Client

### 1. **Basic Structure Test**
```bash
cd /Users/nadyakott/Desktop/CursorProjects/smarttodo
python3 test_mcp_simple.py
```

### 2. **Install Dependencies** 
```bash
pip3 install fastmcp fastapi uvicorn google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

### 3. **Test Client Import**
```bash
python3 -c "
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient
print('✅ MCP Client imported successfully!')
print('Available methods:', [m for m in dir(GoogleTasksMCPClient) if not m.startswith('_')][:10])
"
```

### 4. **Test Server Import**
```bash
python3 -c "
import sys
sys.path.insert(0, 'source')
from source.api.mcp.server import gtasks_mcp
print('✅ MCP Server imported successfully!')
"
```

### 5. **List Available Tools**
```bash
python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def test():
    try:
        async with GoogleTasksMCPClient() as client:
            tools = await client.list_available_tools()
            print(f'✅ Available MCP tools: {tools}')
    except Exception as e:
        print(f'⚠️  Error (may need API credentials): {e}')

asyncio.run(test())
"
```

### 6. **Test Quick Functions**
```bash
python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import quick_get_task_lists

async def test():
    try:
        lists = await quick_get_task_lists()
        print(f'✅ Task lists retrieved: {len(lists)} lists')
    except Exception as e:
        print(f'⚠️  Error (may need API credentials): {e}')

asyncio.run(test())
"
```

### 7. **Run Example Usage**
```bash
python3 -m source.api.mcp.example_usage
```

### 8. **Start MCP Server (STDIO)**
```bash
python3 -m source.api.mcp.run_server
```

### 9. **Start MCP Server (HTTP)**
```bash
python3 -m source.api.mcp.run_server --transport http --port 8000
```

### 10. **Test Custom Client Session**
```bash
python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def test():
    print('🔧 Testing MCP Client session...')
    client = GoogleTasksMCPClient()
    await client.connect()
    print('✅ Client connected successfully!')
    await client.disconnect()
    print('✅ Client disconnected successfully!')

asyncio.run(test())
"
```

### 11. **Full Integration Test**
```bash
python3 test_mcp_bash.py
```

### 12. **Comprehensive Test Suite**
```bash
./test_mcp_bash_complete.sh
```

## One-Liner BASH Test Commands

### Test Everything Quickly:
```bash
cd /Users/nadyakott/Desktop/CursorProjects/smarttodo && python3 test_mcp_simple.py && echo "=== Testing Client ===" && python3 -c "import sys; sys.path.insert(0, 'source'); from source.api.mcp.client import GoogleTasksMCPClient; print('✅ MCP Client ready!')"
```

### Install + Test:
```bash
pip3 install fastmcp fastapi && python3 -c "import sys; sys.path.insert(0, 'source'); from source.api.mcp.client import GoogleTasksMCPClient; from source.api.mcp.server import gtasks_mcp; print('✅ MCP components ready!')"
```

### Quick Tool Check:
```bash
python3 -c "import asyncio, sys; sys.path.insert(0, 'source'); from source.api.mcp.client import GoogleTasksMCPClient; asyncio.run((lambda: GoogleTasksMCPClient().list_available_tools())())"
```

## File-based Testing

### Run Test Scripts:
```bash
# Structure test
python3 test_mcp_simple.py

# Functional test  
python3 test_mcp_bash.py

# Complete test suite
chmod +x test_mcp_bash_complete.sh && ./test_mcp_bash_complete.sh
```

## Debugging Commands

### Check Dependencies:
```bash
python3 -c "
deps = ['fastmcp', 'fastapi', 'google.auth', 'google.api_core']
for dep in deps:
    try:
        __import__(dep)
        print(f'✅ {dep}')
    except:
        print(f'❌ {dep} (missing)')
"
```

### Check MCP Files:
```bash
find source/api/mcp -name "*.py" -exec echo "File: {}" \; -exec head -5 {} \; -exec echo "" \;
```

### Validate Python Path:
```bash
python3 -c "import sys; print('Python path:'); [print(f'  {p}') for p in sys.path]"
```

---

Copy and paste any of these commands to test your MCP client from BASH! 🚀

