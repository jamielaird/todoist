"""
Authentication module for Todoist CLI
Handles API token retrieval and management
"""

import os
import subprocess
from typing import Optional


class AuthManager:
    """Manages authentication for Todoist API access"""

    def __init__(self, token_path: str = "op://Private/Todoist/token"):
        """
        Initialize the auth manager
        
        Args:
            token_path: Path to the token in 1Password or None to use env var
        """
        self.token_path = token_path
        self.env_var_name = "TODOIST_API_TOKEN"

    def get_api_token(self) -> Optional[str]:
        """
        Get the Todoist API token using available methods
        
        Returns:
            str: The API token if found, None otherwise
        """
        # First try environment variable
        token = self._get_token_from_env()
        if token:
            return token
            
        # Then try 1Password if configured
        if self.token_path:
            token = self._get_token_from_1password()
            if token:
                return token
                
        return None
    
    def _get_token_from_env(self) -> Optional[str]:
        """Get API token from environment variable"""
        token = os.environ.get(self.env_var_name)
        if token:
            print(f"Using API token from environment variable {self.env_var_name}")
            return token
        return None
    
    def _get_token_from_1password(self) -> Optional[str]:
        """Get API token from 1Password using CLI"""
        try:
            # Run the 1Password CLI command to get the token
            result = subprocess.run(
                ["op", "read", self.token_path],
                capture_output=True,
                text=True,
                check=True
            )
            token = result.stdout.strip()
            print("Retrieved API token from 1Password")
            return token
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving API token from 1Password: {e}")
            print("Make sure 1Password CLI is installed and you're signed in.")
            return None
        except Exception as e:
            print(f"Unexpected error accessing 1Password: {e}")
            return None
