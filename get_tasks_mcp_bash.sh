#!/bin/bash

# MCP Get Tasks - BASH Prompts and Examples
# Usage: ./get_tasks_mcp_bash.sh

echo "📋 Getting Tasks using MCP - BASH Commands"
echo "=========================================="

PROJECT_DIR="/Users/nadyakott/Desktop/CursorProjects/smarttodo"
cd "$PROJECT_DIR"

echo "📁 Working in: $(pwd)"
echo ""

# Function to show usage
show_usage() {
    echo "🔧 Available MCP Get Tasks Commands:"
    echo ""
    echo "1. Get all tasks from a task list:"
    echo "   get_all_tasks <task_list_id>"
    echo ""
    echo "2. Get completed tasks only:"
    echo "   get_completed_tasks <task_list_id>"
    echo ""
    echo "3. Get pending (incomplete) tasks only:"
    echo "   get_pending_tasks <task_list_id>"
    echo ""
    echo "4. Get a specific task:"
    echo "   get_task <task_list_id> <task_id>"
    echo ""
    echo "5. Search tasks:"
    echo "   search_tasks <query> [task_list_id]"
    echo ""
    echo "6. Get task lists first (to get task_list_id):"
    echo "   get_task_lists"
    echo ""
}

# Function to get all task lists
get_task_lists() {
    echo "📁 Getting all task lists..."
    python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_lists():
    try:
        async with GoogleTasksMCPClient() as client:
            task_lists = await client.get_task_lists()
            print(f'\\n✅ Found {len(task_lists)} task lists:')
            for i, tlist in enumerate(task_lists):
                print(f'  {i+1}. {tlist[\"title\"]} (ID: {tlist[\"id\"]})')
            return task_lists
    except Exception as e:
        print(f'❌ Error: {e}')
        return []

asyncio.run(get_lists())
"
}

# Function to get all tasks from a task list
get_all_tasks() {
    local task_list_id="$1"
    
    if [ -z "$task_list_id" ]; then
        echo "❌ Error: Please provide task_list_id"
        echo "Usage: get_all_tasks <task_list_id>"
        return 1
    fi
    
    echo "📋 Getting all tasks from list: $task_list_id"
    python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_tasks():
    try:
        async with GoogleTasksMCPClient() as client:
            tasks = await client.get_tasks('$task_list_id')
            print(f'\\n✅ Found {len(tasks)} tasks:')
            for i, task in enumerate(tasks):
                status = '✅' if task.get('status') == 'completed' else '⭕'
                due = f' (Due: {task[\"due\"]})' if task.get('due') else ''
                notes = f' - {task[\"notes\"][:50]}...' if task.get('notes') else ''
                print(f'  {i+1}. {status} {task[\"title\"]}{due}{notes}')
                print(f'     ID: {task[\"id\"]}')
            return tasks
    except Exception as e:
        print(f'❌ Error: {e}')
        return []

asyncio.run(get_tasks())
"
}

# Function to get completed tasks only
get_completed_tasks() {
    local task_list_id="$1"
    
    if [ -z "$task_list_id" ]; then
        echo "❌ Error: Please provide task_list_id"
        echo "Usage: get_completed_tasks <task_list_id>"
        return 1
    fi
    
    echo "✅ Getting completed tasks from list: $task_list_id"
    python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_completed():
    try:
        async with GoogleTasksMCPClient() as client:
            tasks = await client.get_tasks('$task_list_id', completed=True)
            print(f'\\n✅ Found {len(tasks)} completed tasks:')
            for i, task in enumerate(tasks):
                due = f' (Due: {task[\"due\"]})' if task.get('due') else ''
                print(f'  {i+1}. ✅ {task[\"title\"]}{due}')
                print(f'     ID: {task[\"id\"]}')
            return tasks
    except Exception as e:
        print(f'❌ Error: {e}')
        return []

asyncio.run(get_completed())
"
}

# Function to get pending (incomplete) tasks only
get_pending_tasks() {
    local task_list_id="$1"
    
    if [ -z "$task_list_id" ]; then
        echo "❌ Error: Please provide task_list_id"
        echo "Usage: get_pending_tasks <task_list_id>"
        return 1
    fi
    
    echo "⭕ Getting pending tasks from list: $task_list_id"
    python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_pending():
    try:
        async with GoogleTasksMCPClient() as client:
            tasks = await client.get_tasks('$task_list_id', completed=False)
            print(f'\\n⭕ Found {len(tasks)} pending tasks:')
            for i, task in enumerate(tasks):
                due = f' (Due: {task[\"due\"]})' if task.get('due') else ''
                priority = '🔥' if 'urgent' in task.get('notes', '').lower() else ''
                print(f'  {i+1}. ⭕ {priority} {task[\"title\"]}{due}')
                print(f'     ID: {task[\"id\"]}')
                if task.get('notes'):
                    print(f'     Notes: {task[\"notes\"][:100]}...')
            return tasks
    except Exception as e:
        print(f'❌ Error: {e}')
        return []

asyncio.run(get_pending())
"
}

# Function to get a specific task
get_task() {
    local task_list_id="$1"
    local task_id="$2"
    
    if [ -z "$task_list_id" ] || [ -z "$task_id" ]; then
        echo "❌ Error: Please provide both task_list_id and task_id"
        echo "Usage: get_task <task_list_id> <task_id>"
        return 1
    fi
    
    echo "🔍 Getting specific task: $task_id from list: $task_list_id"
    python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def get_single_task():
    try:
        async with GoogleTasksMCPClient() as client:
            task = await client.get_task('$task_list_id', '$task_id')
            if task:
                print(f'\\n✅ Task found:')
                print(f'  Title: {task[\"title\"]}')
                print(f'  ID: {task[\"id\"]}')
                print(f'  Status: {task.get(\"status\", \"Unknown\")}')
                print(f'  Due: {task.get(\"due\", \"No due date\")}')
                print(f'  Notes: {task.get(\"notes\", \"No notes\")}')
                print(f'  Updated: {task.get(\"updated\", \"Unknown\")}')
            else:
                print(f'❌ Task not found')
            return task
    except Exception as e:
        print(f'❌ Error: {e}')
        return None

asyncio.run(get_single_task())
"
}

# Function to search tasks
search_tasks() {
    local query="$1"
    local task_list_id="$2"
    
    if [ -z "$query" ]; then
        echo "❌ Error: Please provide search query"
        echo "Usage: search_tasks <query> [task_list_id]"
        return 1
    fi
    
    echo "🔍 Searching for tasks with query: '$query'"
    if [ -n "$task_list_id" ]; then
        echo "   In task list: $task_list_id"
    else
        echo "   In all task lists"
    fi
    
    python3 -c "
import asyncio
import sys
sys.path.insert(0, 'source')
from source.api.mcp.client import GoogleTasksMCPClient

async def search():
    try:
        async with GoogleTasksMCPClient() as client:
            task_list_id = '$task_list_id' if '$task_list_id' else None
            tasks = await client.search_tasks('$query', task_list_id)
            print(f'\\n🔍 Found {len(tasks)} matching tasks:')
            for i, task in enumerate(tasks):
                status = '✅' if task.get('status') == 'completed' else '⭕'
                due = f' (Due: {task[\"due\"]})' if task.get('due') else ''
                print(f'  {i+1}. {status} {task[\"title\"]}{due}')
                print(f'     ID: {task[\"id\"]}')
                if task.get('notes'):
                    print(f'     Notes: {task[\"notes\"][:80]}...')
            return tasks
    except Exception as e:
        print(f'❌ Error: {e}')
        return []

asyncio.run(search())
"
}

# Main script logic
case "$1" in
    "get_task_lists")
        get_task_lists
        ;;
    "get_all_tasks")
        get_all_tasks "$2"
        ;;
    "get_completed_tasks")
        get_completed_tasks "$2"
        ;;
    "get_pending_tasks")
        get_pending_tasks "$2"
        ;;
    "get_task")
        get_task "$2" "$3"
        ;;
    "search_tasks")
        search_tasks "$2" "$3"
        ;;
    "help"|"--help"|"-h"|"")
        show_usage
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_usage
        exit 1
        ;;
esac

