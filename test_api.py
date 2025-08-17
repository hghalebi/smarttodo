#!/usr/bin/env python3
"""
Test script for Google Tasks FastAPI.
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the Google Tasks API endpoints."""
    
    print("🧪 Testing Google Tasks FastAPI")
    print("=" * 50)
    
    # Health check
    print("\n1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("   ❌ API server is not running. Please start it with: python source/api/run.py")
        return
    
    # Get all task lists
    print("\n2. Get All Task Lists")
    try:
        response = requests.get(f"{BASE_URL}/task-lists")
        if response.status_code == 200:
            task_lists = response.json()
            print(f"   ✅ Found {len(task_lists)} task list(s)")
            for i, tl in enumerate(task_lists[:3], 1):  # Show first 3
                print(f"   {i}. {tl['title']} (ID: {tl['id']})")
            
            if task_lists:
                # Test with first task list
                test_task_list_id = task_lists[0]['id']
                test_tasks_operations(test_task_list_id)
                
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test creating a new task list
    print("\n3. Create New Task List")
    try:
        new_list_data = {
            "title": f"Test API List {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        response = requests.post(f"{BASE_URL}/task-lists", json=new_list_data)
        if response.status_code == 201:
            new_list = response.json()
            print(f"   ✅ Created: {new_list['title']} (ID: {new_list['id']})")
            
            # Test tasks in new list
            test_tasks_operations(new_list['id'])
            
            # Clean up - delete the test list
            print(f"\n   🧹 Cleaning up test list...")
            delete_response = requests.delete(f"{BASE_URL}/task-lists/{new_list['id']}")
            if delete_response.status_code == 204:
                print("   ✅ Test list deleted successfully")
            else:
                print(f"   ⚠️  Failed to delete test list: {delete_response.status_code}")
                
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def test_tasks_operations(task_list_id):
    """Test task operations on a specific task list."""
    
    print(f"\n   📝 Testing Tasks in List: {task_list_id[:20]}...")
    
    # Get existing tasks
    print("   • Getting existing tasks...")
    try:
        response = requests.get(f"{BASE_URL}/task-lists/{task_list_id}/tasks")
        if response.status_code == 200:
            existing_tasks = response.json()
            print(f"     Found {len(existing_tasks)} existing task(s)")
        else:
            print(f"     ❌ Error getting tasks: {response.status_code}")
            return
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return
    
    # Create a new task
    print("   • Creating new task...")
    try:
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        new_task_data = {
            "title": f"Test Task {datetime.now().strftime('%H:%M:%S')}",
            "notes": "This is a test task created by the API test script",
            "due": due_date
        }
        response = requests.post(f"{BASE_URL}/task-lists/{task_list_id}/tasks", json=new_task_data)
        if response.status_code == 201:
            new_task = response.json()
            print(f"     ✅ Created: {new_task['title']} (ID: {new_task['id'][:10]}...)")
            
            # Test updating the task
            print("   • Updating task...")
            update_data = {
                "title": f"Updated: {new_task['title']}",
                "notes": "Updated notes from API test"
            }
            update_response = requests.put(
                f"{BASE_URL}/task-lists/{task_list_id}/tasks/{new_task['id']}", 
                json=update_data
            )
            if update_response.status_code == 200:
                updated_task = update_response.json()
                print(f"     ✅ Updated: {updated_task['title']}")
            else:
                print(f"     ❌ Update failed: {update_response.status_code}")
            
            # Test completing the task
            print("   • Completing task...")
            complete_response = requests.patch(
                f"{BASE_URL}/task-lists/{task_list_id}/tasks/{new_task['id']}/complete"
            )
            if complete_response.status_code == 200:
                completed_task = complete_response.json()
                print(f"     ✅ Task completed: {completed_task['status']}")
            else:
                print(f"     ❌ Complete failed: {complete_response.status_code}")
            
            # Test search
            print("   • Testing search...")
            search_response = requests.get(f"{BASE_URL}/search/tasks?query=Test")
            if search_response.status_code == 200:
                search_results = search_response.json()
                print(f"     ✅ Search found {len(search_results)} result(s)")
            else:
                print(f"     ❌ Search failed: {search_response.status_code}")
            
            # Clean up - delete the test task
            print("   • Cleaning up test task...")
            delete_response = requests.delete(f"{BASE_URL}/task-lists/{task_list_id}/tasks/{new_task['id']}")
            if delete_response.status_code == 204:
                print("     ✅ Test task deleted")
            else:
                print(f"     ⚠️  Failed to delete test task: {delete_response.status_code}")
                
        else:
            print(f"     ❌ Error creating task: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"     ❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 Make sure the API server is running:")
    print("   python source/api/run.py")
    print("\n⏳ Starting API tests in 3 seconds...")
    
    import time
    time.sleep(3)
    
    test_api()
    
    print("\n✨ API testing completed!")
    print("📚 Visit http://localhost:8000/docs for interactive API documentation")

