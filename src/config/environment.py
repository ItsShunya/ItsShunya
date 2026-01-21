# The Python Standard Library.
from typing import Optional, Dict, Literal

# External project dependencies.
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


EnvType = Literal["development", "production"]


class EnvConfig(BaseSettings):
    """
    Environment configuration handler using pydantic-settings.

    Configuration values are loaded automatically from:
    - Environment variables
    - `.env` file (if present)

    Validation is performed at initialization time.
    """

    ACCESS_TOKEN: str = Field(..., description="Authentication token for API access")
    USER_NAME: str = Field(..., description="GitHub username or application identifier")
    OUTPUT_PATH: Optional[str] = Field(
        default=None,
        description="Path where application output will be stored",
    )
    ENV: EnvType = Field(
        default="production",
        description="Runtime environment",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def from_env(cls) -> "EnvConfig":
        """
        Create an EnvConfig instance from environment variables.

        This is the preferred constructor for application code.

        Returns:
            EnvConfig: Initialized and validated configuration instance.

        Raises:
            ValidationError: If required configuration values are missing or invalid.
        """
        return cls()

    def to_dict(self) -> Dict[str, Optional[str]]:
        """
        Convert the configuration to a dictionary.

        Returns:
            Dict[str, Optional[str]]: Dictionary representation of the configuration.
        """
        return self.model_dump()
