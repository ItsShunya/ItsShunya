import os
from typing import Optional
from dataclasses import dataclass
from dataclass_wizard import EnvWizard
from dotenv import load_dotenv

@dataclass
class EnvConfig(EnvWizard):
    """
    Manages environment variables for the application using EnvWizard.

    Automatically handles loading from .env files and system environment variables.
    """
    ACCESS_TOKEN: Optional[str] = None
    USER_NAME: Optional[str] = None
    OUTPUT_PATH: Optional[str] = None
    ENV: str = "production"  # Default to production

    def __post_init__(self):
        """
        Post-initialization method to perform additional validations and setup.
        """
        # Automatically load .env file if in development mode
        if self.ENV.lower() == "development":
            self._load_env_vars()

    def _load_env_vars(self):
        """
        Load environment variables from .env file and override system variables.
        """
        load_dotenv()
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', self.ACCESS_TOKEN)
        self.USER_NAME = os.getenv('USER_NAME', self.USER_NAME)
        self.OUTPUT_PATH = os.getenv('OUTPUT_PATH', self.OUTPUT_PATH)
        #self.BIRTHDAY = os.getenv('BIRTHDAY', self.BIRTHDAY)
        #self.ENV = os.getenv('ENV', self.ENV)

    def to_dict(self):
        """
        Convert the configuration to a dictionary.
        """
        return self.__dict__
