"""
Commands module for Todoist CLI
Implements the command pattern for CLI operations
"""

import sys
import argparse
from typing import List, Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table

from todoist_cli.api import TodoistManager


console = Console()


class Command:
    """Base command class"""
    
    def __init__(self, todoist: TodoistManager):
        """
        Initialize with TodoistManager
        
        Args:
            todoist: TodoistManager instance
        """
        self.todoist = todoist
        
    def execute(self, args: List[str]) -> None:
        """
        Execute the command
        
        Args:
            args: Command arguments
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    @staticmethod
    def get_description() -> str:
        """Get command description for help text"""
        return "Command description"


class ListTasksCommand(Command):
    """Command to list tasks"""
    
    def execute(self, args: List[str]) -> None:
        """List tasks with filtering options"""
        parser = argparse.ArgumentParser(description="List Todoist tasks")
        parser.add_argument("--project", "-p", help="Filter by project name")
        parser.add_argument("--label", "-l", help="Filter by label name")
        parser.add_argument("--priority", "-P", type=int, choices=[1, 2, 3, 4], 
                           help="Filter by priority (1=lowest, 4=highest)")
        parser.add_argument("--due", "-d", help="Filter by due date (today, tomorrow, overdue)")
        parser.add_argument("--completed", "-c", action="store_true", help="Show completed tasks")
        
        try:
            parsed_args = parser.parse_args(args)
            
            # Build filter dict
            filters = {}
            
            # Get tasks with filters
            tasks = self.todoist.get_tasks(**filters)
            
            # Apply client-side filtering (for things the API doesn't support directly)
            if parsed_args.project:
                # We'd need to get projects first and match by name
                # This is simplified here
                pass
                
            if parsed_args.label:
                # We'd need to get labels first and match by name
                # This is simplified here
                pass
                
            if parsed_args.priority:
                # API priority is 1-4, where 4 is highest
                tasks = [t for t in tasks if t.priority == parsed_args.priority]
                
            # Apply due date filtering
            if parsed_args.due:
                # This would require more complex logic with the API
                pass
            
            self._display_tasks(tasks)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    def _display_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Display tasks in a formatted table"""
        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return
            
        table = Table(show_header=True)
        table.add_column("ID", style="dim")
        table.add_column("Task", style="bold")
        table.add_column("Due Date", style="blue")
        table.add_column("Priority", style="red")
        table.add_column("Project", style="green")
        
        priority_map = {1: "Low", 2: "Medium", 3: "High", 4: "Urgent"}
        
        for task in tasks:
            priority = priority_map.get(task.priority, "None")
            due_date = task.due.date if task.due else "No due date"
            project = task.project_id or "Inbox"  # Would need to resolve project name
            
            table.add_row(
                task.id,
                task.content,
                due_date,
                priority,
                str(project)
            )
        
        console.print(table)
    
    @staticmethod
    def get_description() -> str:
        return "List and filter your Todoist tasks"


class CreateTaskCommand(Command):
    """Command to create a task"""
    
    def execute(self, args: List[str]) -> None:
        """Create a new task with optional attributes"""
        parser = argparse.ArgumentParser(description="Create a new Todoist task")
        parser.add_argument("content", help="Task content/description")
        parser.add_argument("--project", "-p", help="Project name")
        parser.add_argument("--priority", "-P", type=int, choices=[1, 2, 3, 4], 
                           help="Priority (1=lowest, 4=highest)")
        parser.add_argument("--due", "-d", help="Due date (today, tomorrow, or YYYY-MM-DD)")
        parser.add_argument("--label", "-l", action="append", help="Add a label (can use multiple times)")
        parser.add_argument("--subtask", "-s", action="append", help="Add a subtask (can use multiple times)")
        
        try:
            parsed_args = parser.parse_args(args)
            
            kwargs = {}
            
            # Handle priority
            if parsed_args.priority:
                kwargs["priority"] = parsed_args.priority
                
            # Handle due date
            if parsed_args.due:
                due_dict = self.todoist.parse_due_date(parsed_args.due)
                kwargs["due_string"] = parsed_args.due
                
            # Handle project - would need to look up by name first
            if parsed_args.project:
                # This is simplified here
                pass
                
            # Handle labels - would need to look up by name first
            if parsed_args.label:
                # This is simplified here
                pass
            
            # Create the task with subtasks if provided
            if parsed_args.subtask:
                task = self.todoist.create_task_with_subtasks(
                    content=parsed_args.content,
                    subtasks=parsed_args.subtask,
                    **kwargs
                )
            else:
                task = self.todoist.add_task(
                    content=parsed_args.content,
                    **kwargs
                )
                
            console.print(f"[green]Task created:[/green] {task.content}")
            if parsed_args.subtask:
                console.print(f"[green]With {len(parsed_args.subtask)} subtasks[/green]")
                
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    @staticmethod
    def get_description() -> str:
        return "Create a new task with optional attributes"


class CompleteTaskCommand(Command):
    """Command to complete a task"""
    
    def execute(self, args: List[str]) -> None:
        """Mark a task as complete"""
        parser = argparse.ArgumentParser(description="Complete a Todoist task")
        parser.add_argument("task_id", help="ID of the task to complete")
        
        try:
            parsed_args = parser.parse_args(args)
            self.todoist.complete_task(parsed_args.task_id)
            console.print(f"[green]Task {parsed_args.task_id} marked as complete![/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    @staticmethod
    def get_description() -> str:
        return "Mark a task as complete"


class DeleteTaskCommand(Command):
    """Command to delete a task"""
    
    def execute(self, args: List[str]) -> None:
        """Delete a task"""
        parser = argparse.ArgumentParser(description="Delete a Todoist task")
        parser.add_argument("task_id", help="ID of the task to delete")
        parser.add_argument("--force", "-f", action="store_true", help="Skip confirmation")
        
        try:
            parsed_args = parser.parse_args(args)
            
            # Confirm deletion unless --force is used
            if not parsed_args.force:
                confirmation = input(f"Are you sure you want to delete task {parsed_args.task_id}? (y/n): ")
                if confirmation.lower() != 'y':
                    console.print("[yellow]Deletion cancelled.[/yellow]")
                    return
            
            self.todoist.delete_task(parsed_args.task_id)
            console.print(f"[green]Task {parsed_args.task_id} deleted![/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    @staticmethod
    def get_description() -> str:
        return "Delete a task"


class CreateResetTaskCommand(Command):
    """Command to create a Task Reset workflow"""
    
    def execute(self, args: List[str]) -> None:
        """Create a Task Reset with predefined subtasks"""
        try:
            reset_task = self.todoist.create_task_with_subtasks(
                "⚡ Task Reset",
                subtasks=[
                    "Capture all tasks",
                    "Prioritise captured tasks",
                    "Take action on highest priority tasks"
                ]
            )
            console.print("[green]Task Reset created successfully![/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    @staticmethod
    def get_description() -> str:
        return "Create a Task Reset workflow with predefined subtasks"


class ListProjectsCommand(Command):
    """Command to list projects"""
    
    def execute(self, args: List[str]) -> None:
        """List all projects"""
        try:
            projects = self.todoist.get_projects()
            
            if not projects:
                console.print("[yellow]No projects found.[/yellow]")
                return
                
            table = Table(show_header=True)
            table.add_column("ID", style="dim")
            table.add_column("Name", style="bold green")
            table.add_column("Order", style="blue")
            
            for project in projects:
                table.add_row(
                    project.id,
                    project.name,
                    str(project.order)
                )
            
            console.print(table)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    @staticmethod
    def get_description() -> str:
        return "List all your Todoist projects"


class ListLabelsCommand(Command):
    """Command to list labels"""
    
    def execute(self, args: List[str]) -> None:
        """List all labels"""
        try:
            labels = self.todoist.get_labels()
            
            if not labels:
                console.print("[yellow]No labels found.[/yellow]")
                return
                
            table = Table(show_header=True)
            table.add_column("ID", style="dim")
            table.add_column("Name", style="bold magenta")
            
            for label in labels:
                table.add_row(
                    label.id,
                    label.name
                )
            
            console.print(table)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    @staticmethod
    def get_description() -> str:
        return "List all your Todoist labels"


class CommandRegistry:
    """Registry of available commands"""
    
    def __init__(self, todoist_manager: TodoistManager):
        """
        Initialize with TodoistManager
        
        Args:
            todoist_manager: TodoistManager instance
        """
        self.todoist = todoist_manager
        self.commands = {}
        self._register_commands()
        
    def _register_commands(self) -> None:
        """Register all available commands"""
        self.register_command("list", ListTasksCommand)
        self.register_command("add", CreateTaskCommand)
        self.register_command("complete", CompleteTaskCommand)
        self.register_command("delete", DeleteTaskCommand)
        self.register_command("reset", CreateResetTaskCommand)
        self.register_command("projects", ListProjectsCommand)
        self.register_command("labels", ListLabelsCommand)
        
        # For backward compatibility
        self.register_command("create", CreateTaskCommand)
        self.register_command("create_reset_task", CreateResetTaskCommand)
        
    def register_command(self, name: str, command_class) -> None:
        """
        Register a command
        
        Args:
            name: Command name
            command_class: Command class
        """
        self.commands[name] = command_class(self.todoist)
        
    def execute_command(self, command_name: str, args: List[str]) -> None:
        """
        Execute a command by name
        
        Args:
            command_name: Name of the command to execute
            args: Command arguments
        """
        if command_name in self.commands:
            self.commands[command_name].execute(args)
        else:
            self._show_help()
            
    def _show_help(self) -> None:
        """Show help information"""
        console.print("[bold]Todoist CLI - Available commands:[/bold]")
        
        table = Table(show_header=True)
        table.add_column("Command", style="green")
        table.add_column("Description", style="yellow")
        
        for name, command in sorted(self.commands.items()):
            # Skip duplicate commands (for backwards compatibility)
            if name in ["create", "create_reset_task"]:
                continue
                
            table.add_row(name, command.get_description())
        
        console.print(table)
        console.print("\n[bold]Example usage:[/bold]")
        console.print("  python main.py list             - List all tasks")
        console.print("  python main.py add \"New task\"   - Create a task")
        console.print("  python main.py reset            - Create Task Reset workflow")
