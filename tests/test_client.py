"""
Tests for the LM Studio API client.

These tests verify the functionality of the client module,
including API communication, error handling, and streaming.
"""

import json
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from lm_studio_cli.client import LMStudioClient
from lm_studio_cli.config import Config
from lm_studio_cli.exceptions import (
    APIError,
    ConnectionError,
    ModelNotFoundError,
    TimeoutError,
)


@pytest.fixture
def mock_config():
    """Create a mock configuration for testing."""
    config = Config(
        api_url="http://localhost:1234",
        default_model="test-model",
        temperature=0.7,
        max_tokens=100,
    )
    return config


@pytest.fixture
def client(mock_config):
    """Create a client instance for testing."""
    return LMStudioClient(mock_config)


class TestClientInitialization:
    """Tests for client initialization."""

    def test_client_creation(self, mock_config):
        """Test that client can be created with config."""
        client = LMStudioClient(mock_config)
        assert client.base_url == "http://localhost:1234"
        assert client.timeout == 30

    def test_client_with_custom_timeout(self, mock_config):
        """Test client creation with custom timeout."""
        client = LMStudioClient(mock_config, timeout=60)
        assert client.timeout == 60


class TestHealthCheck:
    """Tests for health check functionality."""

    @patch('lm_studio_cli.client.LMStudioClient.get_models')
    def test_health_check_success(self, mock_get_models, client):
        """Test successful health check."""
        mock_get_models.return_value = [{"id": "test-model"}]
        assert client.health_check() is True

    @patch('lm_studio_cli.client.LMStudioClient.get_models')
    def test_health_check_failure(self, mock_get_models, client):
        """Test failed health check."""
        mock_get_models.side_effect = Exception("Connection failed")
        assert client.health_check() is False


class TestGetModels:
    """Tests for getting model list."""

    @patch('requests.Session.request')
    def test_get_models_success(self, mock_request, client):
        """Test successfully getting models."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {"id": "model-1", "object": "model"},
                {"id": "model-2", "object": "model"},
            ]
        }
        mock_request.return_value = mock_response

        models = client.get_models()
        assert len(models) == 2
        assert models[0]["id"] == "model-1"

    @patch('requests.Session.request')
    def test_get_models_empty(self, mock_request, client):
        """Test getting models when none exist."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        models = client.get_models()
        assert models == []

    @patch('requests.Session.request')
    def test_get_models_connection_error(self, mock_request, client):
        """Test connection error when getting models."""
        mock_request.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(ConnectionError):
            client.get_models()


class TestGetModelInfo:
    """Tests for getting model information."""

    @patch('lm_studio_cli.client.LMStudioClient.get_models')
    def test_get_model_info_success(self, mock_get_models, client):
        """Test successfully getting model info."""
        mock_get_models.return_value = [
            {"id": "test-model", "object": "model", "owned_by": "test"}
        ]

        info = client.get_model_info("test-model")
        assert info["id"] == "test-model"

    @patch('lm_studio_cli.client.LMStudioClient.get_models')
    def test_get_model_info_not_found(self, mock_get_models, client):
        """Test getting info for non-existent model."""
        mock_get_models.return_value = [
            {"id": "other-model", "object": "model"}
        ]

        with pytest.raises(ModelNotFoundError):
            client.get_model_info("test-model")


class TestChatCompletion:
    """Tests for chat completion functionality."""

    @patch('requests.Session.request')
    def test_chat_completion_non_streaming(self, mock_request, client):
        """Test non-streaming chat completion."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello, world!"
                    }
                }
            ]
        }
        mock_request.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]
        response = client.chat_completion(messages, stream=False)

        assert "choices" in response
        assert response["choices"][0]["message"]["content"] == "Hello, world!"

    @patch('requests.Session.request')
    def test_chat_completion_timeout(self, mock_request, client):
        """Test timeout during chat completion."""
        mock_request.side_effect = requests.exceptions.Timeout()

        messages = [{"role": "user", "content": "Hello"}]

        with pytest.raises(TimeoutError):
            client.chat_completion(messages, stream=False)


class TestContextManager:
    """Tests for context manager functionality."""

    def test_context_manager(self, mock_config):
        """Test using client as context manager."""
        with LMStudioClient(mock_config) as client:
            assert client is not None
        # Should close session after exiting context


class TestErrorHandling:
    """Tests for error handling."""

    @patch('requests.Session.request')
    def test_http_error(self, mock_request, client):
        """Test handling of HTTP errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=mock_response
        )
        mock_request.return_value = mock_response

        with pytest.raises(APIError):
            client.get_models()
