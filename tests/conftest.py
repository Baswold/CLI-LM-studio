"""
Pytest configuration and shared fixtures.

This module provides common fixtures and configuration
for all tests in the test suite.
"""

import tempfile
from pathlib import Path

import pytest

from lm_studio_cli.config import Config


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config(temp_dir):
    """Create a mock configuration for testing."""
    config = Config(
        api_url="http://localhost:1234",
        default_model="test-model",
        temperature=0.7,
        max_tokens=100,
        history_enabled=True,
        history_path=temp_dir / "history",
    )
    return config


@pytest.fixture
def sample_messages():
    """Sample message list for testing."""
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]


@pytest.fixture
def sample_api_response():
    """Sample API response for testing."""
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "test-model",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a test response.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
    }


@pytest.fixture
def sample_models_response():
    """Sample models list response for testing."""
    return {
        "data": [
            {
                "id": "model-1",
                "object": "model",
                "created": 1677652288,
                "owned_by": "test",
            },
            {
                "id": "model-2",
                "object": "model",
                "created": 1677652289,
                "owned_by": "test",
            },
        ]
    }
