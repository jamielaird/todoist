#!/usr/bin/env python3
"""
Todoist CLI - A command-line interface for interacting with Todoist tasks.
"""

import sys
import argparse
import logging
from typing import Optional, List

from todoist_cli.auth import AuthManager
from todoist_cli.api import TodoistManager
from todoist_cli.commands import CommandRegistry
from todoist_cli.utils import setup_logging, load_config


def parse_global_args() -> argparse.Namespace:
    """
    Parse global command line arguments
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Todoist CLI - A command-line interface for Todoist",
        add_help=False  # We'll handle help manually to show command-specific help
    )
    
    # Global options
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--token-path", help="Path to Todoist API token in 1Password")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--help", "-h", action="store_true", help="Show help message and exit")
    
    # Parse just the known args, as command-specific args will be parsed later
    args, _ = parser.parse_known_args()
    
    return args


def main() -> int:
    """
    Main entry point
    
    Returns:
        Exit code
    """
    # Parse global arguments
    args = parse_global_args()
    
    # Setup logging
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config = load_config(config_path=args.config)
    
    # Override config with command line arguments
    if args.token_path:
        config["token_path"] = args.token_path
    if args.verbose:
        config["verbose"] = True
        
    # Initialize authentication
    auth_manager = AuthManager(token_path=config.get("token_path"))
    api_token = auth_manager.get_api_token()
    
    if not api_token:
        print("Could not retrieve API token. Exiting.")
        print("Make sure 1Password CLI is installed and you're signed in,")
        print("or set the TODOIST_API_TOKEN environment variable.")
        return 1
    
    # Initialize API client
    todoist_manager = TodoistManager(api_token)
    
    # Initialize command registry
    command_registry = CommandRegistry(todoist_manager)
    
    # Get the command and its arguments
    command_args = sys.argv[1:]
    
    # If no arguments or --help, show help
    if not command_args or args.help:
        if len(command_args) > 0 and command_args[0] in command_registry.commands and not args.help:
            # If a valid command is provided without --help, execute it
            command = command_args[0]
            command_registry.execute_command(command, command_args[1:])
        else:
            # Show help
            command_registry._show_help()
        return 0
    
    # Execute the command
    command = command_args[0]
    command_registry.execute_command(command, command_args[1:])
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        logging.exception("Unhandled exception")
        sys.exit(1)
