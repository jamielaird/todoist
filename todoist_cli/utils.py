"""
Utilities module for Todoist CLI
Contains helper functions and utilities
"""

import os
import logging
from typing import Optional, Dict, Any
import json


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration
    
    Args:
        verbose: Whether to enable verbose logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Configure the root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set up console handler with a higher level
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)  # Only show warnings and errors in console
    
    # Add the console handler to the root logger
    logging.getLogger('').addHandler(console)
    
    # Create logger
    logger = logging.getLogger('todoist_cli')
    logger.setLevel(log_level)


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a JSON file
    
    Args:
        config_path: Path to the config file, or None to use default
        
    Returns:
        Dict containing configuration values
    """
    if not config_path:
        # Use default config path
        config_path = os.path.expanduser("~/.todoist-cli.json")
    
    # Default configuration
    default_config = {
        "token_path": "op://Private/Todoist/token",
        "default_project": None,
        "default_priority": 1,
        "use_colors": True,
        "verbose": False
    }
    
    # Try to load from file
    config = default_config.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                loaded_config = json.load(f)
                config.update(loaded_config)
        except json.JSONDecodeError:
            logging.warning(f"Could not parse config file {config_path}, using defaults")
        except Exception as e:
            logging.warning(f"Error loading config file: {e}, using defaults")
    
    return config


def save_config(config: Dict[str, Any], config_path: Optional[str] = None) -> bool:
    """
    Save configuration to a JSON file
    
    Args:
        config: Configuration dictionary
        config_path: Path to save the config, or None to use default
        
    Returns:
        True if successful, False otherwise
    """
    if not config_path:
        # Use default config path
        config_path = os.path.expanduser("~/.todoist-cli.json")
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving config file: {e}")
        return False


def format_project_for_display(project_id: str, projects_map: Dict[str, Any]) -> str:
    """
    Format a project ID for display, resolving to name if available
    
    Args:
        project_id: Project ID to format
        projects_map: Dictionary mapping project IDs to project objects
        
    Returns:
        Formatted project string
    """
    if project_id in projects_map:
        return projects_map[project_id].name
    return project_id or "Inbox"


def format_labels_for_display(label_ids: list, labels_map: Dict[str, Any]) -> str:
    """
    Format a list of label IDs for display, resolving to names if available
    
    Args:
        label_ids: List of label IDs to format
        labels_map: Dictionary mapping label IDs to label objects
        
    Returns:
        Formatted labels string
    """
    if not label_ids:
        return ""
        
    label_names = []
    for label_id in label_ids:
        if label_id in labels_map:
            label_names.append(labels_map[label_id].name)
        else:
            label_names.append(label_id)
            
    return ", ".join(label_names)


def build_cache_for_display(todoist_manager) -> Dict[str, Dict[str, Any]]:
    """
    Build a cache of projects and labels for efficient display
    
    Args:
        todoist_manager: TodoistManager instance
        
    Returns:
        Dictionary containing projects_map and labels_map
    """
    cache = {
        "projects_map": {},
        "labels_map": {}
    }
    
    # Build projects map
    try:
        projects = todoist_manager.get_projects()
        for project in projects:
            cache["projects_map"][project.id] = project
    except Exception as e:
        logging.error(f"Error building projects cache: {e}")
    
    # Build labels map
    try:
        labels = todoist_manager.get_labels()
        for label in labels:
            cache["labels_map"][label.id] = label
    except Exception as e:
        logging.error(f"Error building labels cache: {e}")
    
    return cache
