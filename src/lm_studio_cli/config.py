"""
Configuration management for CLI-LM-Studio.

This module handles loading, saving, and managing configuration
for the CLI application. It supports both YAML files and environment
variables with sensible defaults.

TODO: Add configuration validation wizard
TODO: Support multiple configuration profiles
TODO: Add configuration inheritance/templates
TODO: Implement encrypted configuration for sensitive data
TODO: Add configuration migration for version updates
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field, validator
from rich.console import Console
from rich.table import Table

console = Console()


class ConfigurationError(Exception):
    """Raised when there's a configuration error."""
    pass


class Config(BaseModel):
    """
    Configuration model for CLI-LM-Studio.

    This class uses Pydantic for validation and type checking.
    All configuration values have sensible defaults.

    Attributes:
        api_url: LM Studio API base URL
        default_model: Default model to use for completions
        system_prompt: Default system prompt
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum tokens to generate
        history_enabled: Whether to save conversation history
        history_path: Path to history storage
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """

    # API Configuration
    api_url: str = Field(
        default="http://localhost:1234",
        description="LM Studio API base URL",
    )
    api_timeout: int = Field(
        default=30,
        ge=1,
        description="API request timeout in seconds",
    )

    # Model Configuration
    default_model: str = Field(
        default="local-model",
        description="Default model for completions",
    )
    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        description="Default system prompt",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature",
    )
    max_tokens: int = Field(
        default=2000,
        ge=1,
        description="Maximum tokens to generate",
    )
    top_p: float = Field(
        default=0.9,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling parameter",
    )

    # History Configuration
    history_enabled: bool = Field(
        default=True,
        description="Enable conversation history",
    )
    history_path: Path = Field(
        default_factory=lambda: Path.home() / ".lm_studio" / "history",
        description="Path to history storage",
    )
    history_max_entries: int = Field(
        default=1000,
        ge=1,
        description="Maximum history entries to keep",
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )
    log_file: Optional[Path] = Field(
        default=None,
        description="Optional log file path",
    )

    # Display Configuration
    color_enabled: bool = Field(
        default=True,
        description="Enable colored output",
    )
    markdown_enabled: bool = Field(
        default=True,
        description="Enable markdown rendering",
    )

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        arbitrary_types_allowed = True

    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v

    @validator("history_path", "log_file", pre=True)
    def convert_to_path(cls, v: Any) -> Optional[Path]:
        """Convert string paths to Path objects."""
        if v is None:
            return None
        return Path(v) if not isinstance(v, Path) else v

    @classmethod
    def get_config_path(cls, custom_path: Optional[Path] = None) -> Path:
        """
        Get the configuration file path.

        Args:
            custom_path: Optional custom path to config file

        Returns:
            Path to configuration file
        """
        if custom_path:
            return custom_path

        # Check environment variable
        env_path = os.getenv("LM_STUDIO_CONFIG")
        if env_path:
            return Path(env_path)

        # Default path
        return Path.home() / ".lm_studio" / "config.yaml"

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """
        Load configuration from file and environment variables.

        Environment variables take precedence over file configuration.
        Environment variable names are prefixed with LM_STUDIO_ and
        use uppercase with underscores (e.g., LM_STUDIO_API_URL).

        Args:
            config_path: Optional path to config file

        Returns:
            Loaded configuration object

        Raises:
            ConfigurationError: If configuration is invalid
        """
        config_file = cls.get_config_path(config_path)

        # Start with defaults
        config_data: Dict[str, Any] = {}

        # Load from file if it exists
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    file_data = yaml.safe_load(f)
                    if file_data:
                        config_data.update(file_data)
            except Exception as e:
                raise ConfigurationError(
                    f"Failed to load config from {config_file}: {e}"
                ) from e

        # Override with environment variables
        env_mapping = {
            "LM_STUDIO_API_URL": "api_url",
            "LM_STUDIO_API_TIMEOUT": "api_timeout",
            "LM_STUDIO_DEFAULT_MODEL": "default_model",
            "LM_STUDIO_SYSTEM_PROMPT": "system_prompt",
            "LM_STUDIO_TEMPERATURE": "temperature",
            "LM_STUDIO_MAX_TOKENS": "max_tokens",
            "LM_STUDIO_HISTORY_ENABLED": "history_enabled",
            "LM_STUDIO_HISTORY_PATH": "history_path",
            "LM_STUDIO_LOG_LEVEL": "log_level",
        }

        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert types as needed
                if config_key in ["api_timeout", "max_tokens", "history_max_entries"]:
                    value = int(value)
                elif config_key in ["temperature", "top_p"]:
                    value = float(value)
                elif config_key == "history_enabled":
                    value = value.lower() in ("true", "1", "yes")

                config_data[config_key] = value

        try:
            return cls(**config_data)
        except Exception as e:
            raise ConfigurationError(f"Invalid configuration: {e}") from e

    @classmethod
    def create_default(cls) -> "Config":
        """
        Create a default configuration.

        Returns:
            Default configuration object
        """
        return cls()

    def save(self, config_path: Optional[Path] = None) -> None:
        """
        Save configuration to file.

        Args:
            config_path: Optional path to save config file

        Raises:
            ConfigurationError: If saving fails
        """
        config_file = self.get_config_path(config_path)

        # Create directory if it doesn't exist
        config_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Convert to dictionary
            config_data = self.dict()

            # Convert Path objects to strings for YAML
            for key, value in config_data.items():
                if isinstance(value, Path):
                    config_data[key] = str(value)

            # Write to file
            with open(config_file, "w") as f:
                yaml.dump(
                    config_data,
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                )

        except Exception as e:
            raise ConfigurationError(
                f"Failed to save config to {config_file}: {e}"
            ) from e

    def display(self) -> None:
        """
        Display current configuration in a formatted table.
        """
        table = Table(title="CLI-LM-Studio Configuration", show_header=True)
        table.add_column("Setting", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Add rows
        table.add_row("API URL", self.api_url)
        table.add_row("API Timeout", f"{self.api_timeout}s")
        table.add_row("Default Model", self.default_model)
        table.add_row("Temperature", str(self.temperature))
        table.add_row("Max Tokens", str(self.max_tokens))
        table.add_row("Top P", str(self.top_p))
        table.add_row("History Enabled", "✓" if self.history_enabled else "✗")
        table.add_row("History Path", str(self.history_path))
        table.add_row("Log Level", self.log_level)

        console.print(table)

    def validate_connection(self) -> bool:
        """
        Validate that the API URL is accessible.

        Returns:
            True if connection is successful, False otherwise
        """
        from lm_studio_cli.client import LMStudioClient

        try:
            client = LMStudioClient(self)
            return client.health_check()
        except Exception:
            return False
