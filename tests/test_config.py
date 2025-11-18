"""
Tests for configuration management.

These tests verify configuration loading, saving, validation,
and environment variable handling.
"""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from lm_studio_cli.config import Config, ConfigurationError


class TestConfigDefaults:
    """Tests for default configuration values."""

    def test_default_config(self):
        """Test that default config has expected values."""
        config = Config()

        assert config.api_url == "http://localhost:1234"
        assert config.api_timeout == 30
        assert config.default_model == "local-model"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
        assert config.history_enabled is True

    def test_create_default(self):
        """Test creating default configuration."""
        config = Config.create_default()

        assert isinstance(config, Config)
        assert config.api_url == "http://localhost:1234"


class TestConfigValidation:
    """Tests for configuration validation."""

    def test_temperature_validation(self):
        """Test temperature value validation."""
        # Valid temperatures
        config = Config(temperature=0.0)
        assert config.temperature == 0.0

        config = Config(temperature=2.0)
        assert config.temperature == 2.0

        # Invalid temperatures should raise error
        with pytest.raises(Exception):  # Pydantic ValidationError
            Config(temperature=-0.1)

        with pytest.raises(Exception):
            Config(temperature=2.1)

    def test_api_timeout_validation(self):
        """Test API timeout validation."""
        # Valid timeout
        config = Config(api_timeout=60)
        assert config.api_timeout == 60

        # Invalid timeout
        with pytest.raises(Exception):
            Config(api_timeout=0)

    def test_log_level_validation(self):
        """Test log level validation."""
        # Valid log levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = Config(log_level=level)
            assert config.log_level == level

        # Case insensitive
        config = Config(log_level="debug")
        assert config.log_level == "DEBUG"

        # Invalid log level
        with pytest.raises(Exception):
            Config(log_level="INVALID")


class TestConfigLoading:
    """Tests for loading configuration from file."""

    def test_load_nonexistent_file(self, tmp_path):
        """Test loading when config file doesn't exist."""
        config_path = tmp_path / "nonexistent.yaml"
        config = Config.load(config_path)

        # Should return defaults
        assert config.api_url == "http://localhost:1234"

    def test_load_valid_file(self, tmp_path):
        """Test loading from valid config file."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("""
api_url: http://example.com:8080
default_model: test-model
temperature: 0.5
        """)

        config = Config.load(config_path)

        assert config.api_url == "http://example.com:8080"
        assert config.default_model == "test-model"
        assert config.temperature == 0.5

    def test_load_invalid_file(self, tmp_path):
        """Test loading from invalid config file."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("invalid: yaml: content:")

        # Should handle gracefully
        with pytest.raises(ConfigurationError):
            Config.load(config_path)


class TestEnvironmentVariables:
    """Tests for environment variable configuration."""

    def test_env_var_override(self, tmp_path):
        """Test that environment variables override file config."""
        config_path = tmp_path / "config.yaml"
        config_path.write_text("api_url: http://localhost:1234")

        with patch.dict(os.environ, {"LM_STUDIO_API_URL": "http://example.com"}):
            config = Config.load(config_path)
            assert config.api_url == "http://example.com"

    def test_env_var_temperature(self):
        """Test temperature from environment variable."""
        with patch.dict(os.environ, {"LM_STUDIO_TEMPERATURE": "0.9"}):
            config = Config.load()
            assert config.temperature == 0.9

    def test_env_var_boolean(self):
        """Test boolean environment variable."""
        with patch.dict(os.environ, {"LM_STUDIO_HISTORY_ENABLED": "false"}):
            config = Config.load()
            assert config.history_enabled is False

        with patch.dict(os.environ, {"LM_STUDIO_HISTORY_ENABLED": "true"}):
            config = Config.load()
            assert config.history_enabled is True


class TestConfigSaving:
    """Tests for saving configuration."""

    def test_save_config(self, tmp_path):
        """Test saving configuration to file."""
        config = Config(
            api_url="http://test.com",
            default_model="test-model",
            temperature=0.8,
        )

        config_path = tmp_path / "config.yaml"
        config.save(config_path)

        assert config_path.exists()

        # Load and verify
        loaded_config = Config.load(config_path)
        assert loaded_config.api_url == "http://test.com"
        assert loaded_config.default_model == "test-model"
        assert loaded_config.temperature == 0.8

    def test_save_creates_directory(self, tmp_path):
        """Test that save creates parent directories."""
        config = Config()
        config_path = tmp_path / "subdir" / "config.yaml"

        config.save(config_path)

        assert config_path.exists()
        assert config_path.parent.exists()


class TestConfigDisplay:
    """Tests for configuration display."""

    def test_display(self, capsys):
        """Test displaying configuration."""
        config = Config()

        # Should not raise exception
        config.display()


class TestConfigPaths:
    """Tests for configuration path handling."""

    def test_get_config_path_default(self):
        """Test getting default config path."""
        path = Config.get_config_path()

        assert isinstance(path, Path)
        assert path.name == "config.yaml"
        assert ".lm_studio" in str(path)

    def test_get_config_path_custom(self, tmp_path):
        """Test getting custom config path."""
        custom_path = tmp_path / "custom.yaml"
        path = Config.get_config_path(custom_path)

        assert path == custom_path

    def test_get_config_path_env_var(self, tmp_path):
        """Test getting config path from environment variable."""
        custom_path = tmp_path / "env.yaml"

        with patch.dict(os.environ, {"LM_STUDIO_CONFIG": str(custom_path)}):
            path = Config.get_config_path()
            assert path == custom_path
