"""
Example usage of the Google Tasks MCP client.
"""

import asyncio
from datetime import datetime, timedelta
from .client import GoogleTasksMCPClient, quick_get_task_lists, quick_create_task, quick_search_tasks


async def demo_basic_operations():
    """Demonstrate basic MCP operations."""
    print("🚀 Starting Google Tasks MCP Demo")
    
    async with GoogleTasksMCPClient() as client:
        print("\n📋 Available MCP Tools:")
        tools = await client.list_available_tools()
        for tool in tools:
            print(f"  - {tool}")
        
        print("\n📁 Getting all task lists...")
        task_lists = await client.get_task_lists()
        print(f"Found {len(task_lists)} task lists")
        
        if not task_lists:
            print("📋 Creating a demo task list...")
            demo_list = await client.create_task_list("MCP Demo List")
            print(f"Created: {demo_list}")
            task_lists = [demo_list]
        
        # Use the first task list for demo
        demo_list_id = task_lists[0]["id"]
        print(f"\n🎯 Using task list: {task_lists[0]['title']} (ID: {demo_list_id})")
        
        print("\n📝 Creating demo tasks...")
        
        # Create a simple task
        task1 = await client.create_task(
            task_list_id=demo_list_id,
            title="Review MCP integration",
            notes="Check the FastMCP implementation and test all tools"
        )
        print(f"Created task: {task1['title']}")
        
        # Create a task with due date
        tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
        task2 = await client.create_task(
            task_list_id=demo_list_id,
            title="Prepare demo presentation",
            notes="Create slides showing MCP capabilities",
            due=tomorrow
        )
        print(f"Created task with due date: {task2['title']}")
        
        # Create multiple tasks at once
        batch_tasks = [
            {"title": "Test task automation", "notes": "Verify batch operations"},
            {"title": "Update documentation", "notes": "Add MCP integration docs"},
            {"title": "Schedule team review", "due": tomorrow}
        ]
        
        print(f"\n📦 Creating {len(batch_tasks)} tasks in batch...")
        batch_result = await client.create_multiple_tasks(demo_list_id, batch_tasks)
        print(f"Batch creation result: {batch_result['created_count']} tasks created")
        
        print("\n📋 Getting all tasks...")
        all_tasks = await client.get_tasks(demo_list_id)
        print(f"Total tasks in list: {len(all_tasks)}")
        
        for task in all_tasks:
            status = "✅" if task["status"] == "completed" else "⭕"
            due_info = f" (Due: {task['due']})" if task.get('due') else ""
            print(f"  {status} {task['title']}{due_info}")
        
        # Complete a task
        if all_tasks:
            task_to_complete = all_tasks[0]
            print(f"\n✅ Completing task: {task_to_complete['title']}")
            completed_task = await client.complete_task(demo_list_id, task_to_complete["id"])
            print(f"Task completed: {completed_task['title']}")
        
        # Search for tasks
        print("\n🔍 Searching for tasks containing 'demo'...")
        search_results = await client.search_tasks("demo", demo_list_id)
        print(f"Found {len(search_results)} matching tasks:")
        for task in search_results:
            print(f"  - {task['title']}")
        
        print("\n🧹 Clearing completed tasks...")
        clear_result = await client.clear_completed_tasks(demo_list_id)
        print(f"Clear result: {clear_result}")
        
        print("\n📊 Final task count...")
        final_tasks = await client.get_tasks(demo_list_id)
        print(f"Remaining tasks: {len(final_tasks)}")


async def demo_quick_functions():
    """Demonstrate quick convenience functions."""
    print("\n🚀 Quick Functions Demo")
    
    # Quick task list retrieval
    print("📁 Quick get task lists...")
    task_lists = await quick_get_task_lists()
    print(f"Found {len(task_lists)} task lists")
    
    if task_lists:
        demo_list_id = task_lists[0]["id"]
        
        # Quick task creation
        print(f"📝 Quick create task in {task_lists[0]['title']}...")
        new_task = await quick_create_task(
            demo_list_id,
            "Quick task creation test",
            notes="Created using the quick function"
        )
        print(f"Created: {new_task['title']}")
        
        # Quick search
        print("🔍 Quick search for 'test'...")
        search_results = await quick_search_tasks("test", demo_list_id)
        print(f"Found {len(search_results)} matching tasks")


async def demo_error_handling():
    """Demonstrate error handling."""
    print("\n🚨 Error Handling Demo")
    
    async with GoogleTasksMCPClient() as client:
        try:
            # Try to get a non-existent task list
            print("Testing with invalid task list ID...")
            result = await client.get_task_list("invalid-id")
            print(f"Result: {result}")
        except Exception as e:
            print(f"Handled error: {e}")
        
        try:
            # Try to create a task with invalid due date
            print("Testing with invalid due date...")
            await client.create_task(
                "some-list-id",
                "Test task",
                due="invalid-date"
            )
        except ValueError as e:
            print(f"Handled date error: {e}")


async def main():
    """Run all demos."""
    try:
        await demo_basic_operations()
        await demo_quick_functions()
        await demo_error_handling()
        print("\n✨ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
