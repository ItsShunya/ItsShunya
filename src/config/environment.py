import os
from datetime import datetime
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

class EnvironmentConfig:
    """
    Manages environment variables for the application.
    
    Provides methods to set and retrieve required environment variables with proper validation.
    """
    
    def __init__(self):
        self._access_token: Optional[str] = None
        self._user_name: Optional[str] = None
        self._output_path: Optional[str] = None
        self._birthday: Optional[datetime] = None
        self._env: str = 'production'  # Default to production
        
    @property
    def env(self) -> str:
        """Get the current environment mode."""
        return self._env
        
    @env.setter
    def env(self, value: str) -> None:
        """
        Set the environment mode (development or production).
        
        Args:
            value: The environment mode to set. Must be either "development" or "production".
            
        Raises:
            ValueError: If invalid environment mode is provided
        """
        if value not in ["development", "production"]:
            raise ValueError("Invalid environment mode. Must be 'development' or 'production'.")
        
        self._env = value
        
    @staticmethod
    def __determine_environment() -> str:
        """
        Determines the environment based on the presence of a .env file.
        
        Checks the current directory and the parent directory for a .env file.
        Returns "development" if found, otherwise "production".
        
        Returns:
            str: "development" or "production"
        """
        current_dir = Path(".")
        parent_dir = Path("..")
        
        if current_dir.joinpath(".env").exists() or parent_dir.joinpath(".env").exists():
            return "development"
        
        return "production"
        
    def load_env_vars(self) -> None:
        """
        Loads environment variables from either .env file (development) or system (production).
        """
        # Set environment mode
        self.env = self.__determine_environment()
        
        # Load variables from .env file if in development
        if self.env == "development":
            load_dotenv()
            
        # Load variables
        self._access_token = os.getenv('ACCESS_TOKEN')
        self._user_name = os.getenv('USER_NAME')
        self._output_path = os.getenv('OUTPUT_PATH')
        
        # Parse birthday string into datetime object
        birthday_str = os.getenv('BIRTHDAY')
        if birthday_str:
            try:
                self._birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
            except ValueError:
                self._birthday = None
                
    @property
    def ACCESS_TOKEN(self) -> Optional[str]:
        """Get the access token value."""
        return self._access_token
        
    @ACCESS_TOKEN.setter
    def ACCESS_TOKEN(self, value: str) -> None:
        """Set the access token value."""
        self._access_token = value
        
    @property
    def USER_NAME(self) -> Optional[str]:
        """Get the user name value."""
        return self._user_name
        
    @USER_NAME.setter
    def USER_NAME(self, value: str) -> None:
        """Set the user name value."""
        self._user_name = value
        
    @property
    def OUTPUT_PATH(self) -> Optional[str]:
        """Get the output path value."""
        return self._output_path
        
    @OUTPUT_PATH.setter
    def OUTPUT_PATH(self, value: str) -> None:
        """Set the output path value."""
        self._output_path = value
        
    @property
    def BIRTHDAY(self) -> Optional[datetime]:
        """Get the birthday value as a datetime object."""
        return self._birthday
        
    @BIRTHDAY.setter
    def BIRTHDAY(self, value: str) -> None:
        """
        Set the birthday value from a string in format 'YYYY-MM-DD'.
        
        Args:
            value: Birthday string to parse
            
        Raises:
            ValueError: If invalid date format
        """
        try:
            self._birthday = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format for BIRTHDAY. Expected 'YYYY-MM-DD'.")
            
    def __repr__(self) -> str:
        return f"EnvironmentConfig(env={self.env}, access_token={'*' * len(self.ACCESS_TOKEN) if self.ACCESS_TOKEN else None}, " \
               f"user_name={self.USER_NAME}, output_path={self.OUTPUT_PATH}, " \
               f"birthday={self.BIRTHDAY.strftime('%Y-%m-%d') if self.BIRTHDAY else None})"