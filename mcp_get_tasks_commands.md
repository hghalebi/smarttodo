# MCP Get Tasks - BASH Commands Reference

## 🚀 Quick BASH Commands to Get Tasks using MCP

### **Prerequisites**
```bash
cd /Users/nadyakott/Desktop/CursorProjects/smarttodo
# Ensure dependencies are installed:
# pip3 install fastmcp fastapi google-api-python-client google-auth
```

---

## **1. Get All Task Lists (First Step)**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_lists():
    async with GoogleTasksMCPClient() as client:
        lists = await client.get_task_lists()
        print(f'Found {len(lists)} task lists:')
        for i, tlist in enumerate(lists):
            print(f'  {i+1}. {tlist[\"title\"]} (ID: {tlist[\"id\"]})')

asyncio.run(get_lists())
"
```

---

## **2. Get All Tasks from a Task List**
```bash
# Replace YOUR_TASK_LIST_ID with actual ID from step 1
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_all():
    async with GoogleTasksMCPClient() as client:
        tasks = await client.get_tasks('YOUR_TASK_LIST_ID')
        print(f'Found {len(tasks)} tasks:')
        for i, task in enumerate(tasks):
            status = '✅' if task.get('status') == 'completed' else '⭕'
            print(f'  {i+1}. {status} {task[\"title\"]} (ID: {task[\"id\"]})')

asyncio.run(get_all())
"
```

---

## **3. Get Only Completed Tasks**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_completed():
    async with GoogleTasksMCPClient() as client:
        tasks = await client.get_tasks('YOUR_TASK_LIST_ID', completed=True)
        print(f'Found {len(tasks)} completed tasks:')
        for task in tasks:
            print(f'  ✅ {task[\"title\"]}')

asyncio.run(get_completed())
"
```

---

## **4. Get Only Pending (Incomplete) Tasks**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_pending():
    async with GoogleTasksMCPClient() as client:
        tasks = await client.get_tasks('YOUR_TASK_LIST_ID', completed=False)
        print(f'Found {len(tasks)} pending tasks:')
        for task in tasks:
            due = f' (Due: {task[\"due\"]})' if task.get('due') else ''
            print(f'  ⭕ {task[\"title\"]}{due}')

asyncio.run(get_pending())
"
```

---

## **5. Get a Specific Task by ID**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_one():
    async with GoogleTasksMCPClient() as client:
        task = await client.get_task('YOUR_TASK_LIST_ID', 'YOUR_TASK_ID')
        if task:
            print(f'Task: {task[\"title\"]}')
            print(f'Status: {task.get(\"status\")}')
            print(f'Due: {task.get(\"due\", \"No due date\")}')
            print(f'Notes: {task.get(\"notes\", \"No notes\")}')
        else:
            print('Task not found')

asyncio.run(get_one())
"
```

---

## **6. Search Tasks by Query**
```bash
# Search in all task lists
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def search():
    async with GoogleTasksMCPClient() as client:
        tasks = await client.search_tasks('YOUR_SEARCH_QUERY')
        print(f'Found {len(tasks)} matching tasks:')
        for task in tasks:
            status = '✅' if task.get('status') == 'completed' else '⭕'
            print(f'  {status} {task[\"title\"]}')

asyncio.run(search())
"
```

---

## **7. Search Tasks in Specific List**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def search_in_list():
    async with GoogleTasksMCPClient() as client:
        tasks = await client.search_tasks('YOUR_SEARCH_QUERY', 'YOUR_TASK_LIST_ID')
        print(f'Found {len(tasks)} matching tasks:')
        for task in tasks:
            print(f'  - {task[\"title\"]}')

asyncio.run(search_in_list())
"
```

---

## **🛠️ Advanced Examples**

### **Get Tasks with Detailed Information**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def detailed_tasks():
    async with GoogleTasksMCPClient() as client:
        tasks = await client.get_tasks('YOUR_TASK_LIST_ID')
        for task in tasks:
            print(f'\\n📋 {task[\"title\"]}')
            print(f'   ID: {task[\"id\"]}')
            print(f'   Status: {task.get(\"status\", \"Unknown\")}')
            print(f'   Due: {task.get(\"due\", \"No due date\")}')
            print(f'   Updated: {task.get(\"updated\", \"Unknown\")}')
            if task.get('notes'):
                print(f'   Notes: {task[\"notes\"]}')

asyncio.run(detailed_tasks())
"
```

### **Get Tasks with Count Summary**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def task_summary():
    async with GoogleTasksMCPClient() as client:
        all_tasks = await client.get_tasks('YOUR_TASK_LIST_ID')
        completed = await client.get_tasks('YOUR_TASK_LIST_ID', completed=True)
        pending = await client.get_tasks('YOUR_TASK_LIST_ID', completed=False)
        
        print(f'📊 Task Summary:')
        print(f'   Total: {len(all_tasks)}')
        print(f'   Completed: {len(completed)}')
        print(f'   Pending: {len(pending)}')

asyncio.run(task_summary())
"
```

---

## **💡 Using Quick Functions**

### **Quick Get Tasks (Alternative Method)**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import quick_get_task_lists

async def quick_lists():
    lists = await quick_get_task_lists()
    for tlist in lists:
        print(f'{tlist[\"title\"]}: {tlist[\"id\"]}')

asyncio.run(quick_lists())
"
```

---

## **🔧 Interactive BASH Script Usage**

Make the script executable and use it:
```bash
chmod +x get_tasks_mcp_bash.sh

# Get help
./get_tasks_mcp_bash.sh help

# Get task lists
./get_tasks_mcp_bash.sh get_task_lists

# Get all tasks
./get_tasks_mcp_bash.sh get_all_tasks "YOUR_TASK_LIST_ID"

# Get completed tasks only
./get_tasks_mcp_bash.sh get_completed_tasks "YOUR_TASK_LIST_ID"

# Get pending tasks only
./get_tasks_mcp_bash.sh get_pending_tasks "YOUR_TASK_LIST_ID"

# Get specific task
./get_tasks_mcp_bash.sh get_task "YOUR_TASK_LIST_ID" "YOUR_TASK_ID"

# Search tasks
./get_tasks_mcp_bash.sh search_tasks "important"
./get_tasks_mcp_bash.sh search_tasks "meeting" "YOUR_TASK_LIST_ID"
```

---

## **🚨 Error Handling Examples**

### **Safe Get Tasks with Error Handling**
```bash
python3 -c "
import asyncio, sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def safe_get_tasks():
    try:
        async with GoogleTasksMCPClient() as client:
            tasks = await client.get_tasks('YOUR_TASK_LIST_ID')
            if tasks:
                print(f'✅ Successfully retrieved {len(tasks)} tasks')
                for task in tasks[:5]:  # Show first 5
                    print(f'  - {task[\"title\"]}')
            else:
                print('⚠️  No tasks found')
    except Exception as e:
        print(f'❌ Error: {e}')

asyncio.run(safe_get_tasks())
"
```

---

## **📝 Notes**
- Replace `YOUR_TASK_LIST_ID` and `YOUR_TASK_ID` with actual IDs
- Replace `YOUR_SEARCH_QUERY` with your search terms
- Ensure Google Tasks API credentials are configured
- All commands return JSON-formatted task data
- Use the interactive script for easier task management

🎯 **Copy and paste any of these commands to get tasks using MCP!**

