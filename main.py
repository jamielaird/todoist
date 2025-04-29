import subprocess
import json
import sys
from todoist_api_python.api import TodoistAPI

# Get the API token from 1Password using the CLI
def get_api_token():
    try:
        # Run the 1Password CLI command to get the token
        result = subprocess.run(
            ["op", "read", "op://Private/Todoist/token"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving API token from 1Password: {e}")
        print(f"Make sure 1Password CLI is installed and you're signed in.")
        return None

# Get the API token
api_token = get_api_token()

if not api_token:
    print("Could not retrieve API token. Exiting.")
    exit(1)

# Initialize the Todoist API with the token
api = TodoistAPI(api_token)

def get_tasks():
    """Retrieve and display all tasks from Todoist"""
    try:
        # Get all tasks
        tasks = api.get_tasks()
        
        # Print tasks in a more readable format
        if tasks:
            print(f"Retrieved {len(tasks)} tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.content} (Due: {task.due.date if task.due else 'No due date'})")
        else:
            print("No tasks found.")
        
        return tasks
    except Exception as error:
        print(f"Error accessing Todoist API: {error}")
        return None

def create_task(content, subtasks=None, **kwargs):
    """
    Create a new task in Todoist with optional subtasks.
    
    Args:
        content (str): The task content/name
        subtasks (list): Optional list of subtask names
        **kwargs: Additional task attributes (due_date, priority, etc.)
    
    Returns:
        dict: The created task data
    """
    try:
        # Create main task
        task = api.add_task(content=content, **kwargs)
        print(f"Created task: {task.content}")
        
        # Create subtasks if provided
        if subtasks and task:
            for subtask_content in subtasks:
                subtask = api.add_task(
                    content=subtask_content,
                    parent_id=task.id
                )
                print(f"  - Added subtask: {subtask.content}")
        
        return task
    except Exception as error:
        print(f"Error creating task: {error}")
        return None

# Main execution
if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        # Create the Task Reset task with subtasks
        if command == "create_reset_task":
            reset_task = create_task(
                "⚡ Task Reset",
                subtasks=[
                    "Capture all tasks",
                    "Prioritise captured tasks",
                    "Take action on highest priority tasks"
                ]
            )
            if reset_task:
                print("Task Reset created successfully!")
        
        # Generic task creation command
        elif command == "create":
            if len(sys.argv) < 3:
                print("Error: Task content required")
                print("Usage: python main.py create \"Task name\" [\"Subtask 1\" \"Subtask 2\" ...]")
                sys.exit(1)
            
            # Get task content and optional subtasks
            task_content = sys.argv[2]
            subtasks = sys.argv[3:] if len(sys.argv) > 3 else None
            
            # Create the task
            task = create_task(task_content, subtasks)
            if task:
                print(f"Task '{task_content}' created successfully!")
        
        # Show usage information
        elif command == "help":
            print("\nTodoist CLI - Available commands:")
            print("  python main.py                     - List all tasks")
            print("  python main.py create_reset_task   - Create Task Reset with predefined subtasks")
            print("  python main.py create \"Task name\" [\"Subtask 1\" \"Subtask 2\" ...] - Create custom task with optional subtasks")
            print("  python main.py help                - Show this help message\n")
        else:
            print(f"Unknown command: {command}")
            print("Use 'python main.py help' to see available commands")
    else:
        # Default behavior: get tasks
        get_tasks()
