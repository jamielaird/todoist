"""
API module for Todoist CLI
Handles all interactions with the Todoist API
"""

import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from todoist_api_python.api import TodoistAPI

logger = logging.getLogger(__name__)


class TodoistManager:
    """Manages interactions with the Todoist API"""
    
    def __init__(self, api_token: str):
        """
        Initialize with the Todoist API token
        
        Args:
            api_token: The API token for Todoist
        """
        self.api = TodoistAPI(api_token)
        
    # Task Management Methods
    
    def get_tasks(self, **filters) -> List[Dict[str, Any]]:
        """
        Retrieve tasks from Todoist with optional filtering
        
        Args:
            **filters: Optional filters (project_id, label_id, filter, etc.)
            
        Returns:
            List of task objects
        """
        try:
            tasks = self.api.get_tasks(**filters)
            logger.info(f"Retrieved {len(tasks)} tasks")
            return tasks
        except Exception as error:
            logger.error(f"Error retrieving tasks: {error}")
            raise

    def add_task(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        Create a new task in Todoist
        
        Args:
            content: The task content/name
            **kwargs: Additional task attributes (due_date, priority, etc.)
            
        Returns:
            The created task object
        """
        try:
            task = self.api.add_task(content=content, **kwargs)
            logger.info(f"Created task: {task.content}")
            return task
        except Exception as error:
            logger.error(f"Error creating task: {error}")
            raise
    
    def create_task_with_subtasks(self, content: str, subtasks: Optional[List[str]] = None, **kwargs) -> Dict[str, Any]:
        """
        Create a task with optional subtasks
        
        Args:
            content: The parent task content
            subtasks: List of subtask names to create
            **kwargs: Additional task attributes
            
        Returns:
            The parent task object
        """
        # Create main task
        task = self.add_task(content=content, **kwargs)
        
        # Create subtasks if provided
        if subtasks and task:
            for subtask_content in subtasks:
                self.add_task(
                    content=subtask_content,
                    parent_id=task.id
                )
        
        return task
    
    def update_task(self, task_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing task
        
        Args:
            task_id: The ID of the task to update
            **kwargs: Attributes to update (content, due_date, priority, etc.)
            
        Returns:
            The updated task object
        """
        try:
            task = self.api.update_task(task_id=task_id, **kwargs)
            logger.info(f"Updated task {task_id}")
            return task
        except Exception as error:
            logger.error(f"Error updating task: {error}")
            raise
    
    def complete_task(self, task_id: str) -> bool:
        """
        Mark a task as complete
        
        Args:
            task_id: The ID of the task to complete
            
        Returns:
            True if successful
        """
        try:
            self.api.close_task(task_id=task_id)
            logger.info(f"Completed task {task_id}")
            return True
        except Exception as error:
            logger.error(f"Error completing task: {error}")
            raise
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if successful
        """
        try:
            self.api.delete_task(task_id=task_id)
            logger.info(f"Deleted task {task_id}")
            return True
        except Exception as error:
            logger.error(f"Error deleting task: {error}")
            raise
    
    # Project Management Methods
    
    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Retrieve all projects
        
        Returns:
            List of project objects
        """
        try:
            projects = self.api.get_projects()
            logger.info(f"Retrieved {len(projects)} projects")
            return projects
        except Exception as error:
            logger.error(f"Error retrieving projects: {error}")
            raise
    
    # Label Management Methods
    
    def get_labels(self) -> List[Dict[str, Any]]:
        """
        Retrieve all labels
        
        Returns:
            List of label objects
        """
        try:
            labels = self.api.get_labels()
            logger.info(f"Retrieved {len(labels)} labels")
            return labels
        except Exception as error:
            logger.error(f"Error retrieving labels: {error}")
            raise

    # Helper Methods
    
    @staticmethod
    def parse_due_date(due_string: str) -> Dict[str, Any]:
        """
        Parse a human-readable due date string
        
        Args:
            due_string: A due date string like "today", "tomorrow", "next monday", etc.
            
        Returns:
            A dictionary with due date information
        """
        today = datetime.now().date()
        
        if due_string.lower() == "today":
            return {"date": today.isoformat()}
        elif due_string.lower() == "tomorrow":
            tomorrow = today + timedelta(days=1)
            return {"date": tomorrow.isoformat()}
        
        # For more complex parsing, you could add a date parsing library
        
        # Default to the provided string
        return {"date": due_string}
