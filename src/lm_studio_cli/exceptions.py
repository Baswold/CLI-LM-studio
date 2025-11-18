"""
Custom exceptions for CLI-LM-Studio.

This module defines all custom exceptions used throughout the application.
Each exception includes detailed documentation about when it's raised and
how it should be handled.
"""


class LMStudioError(Exception):
    """
    Base exception for all CLI-LM-Studio errors.

    All custom exceptions in this application inherit from this base class,
    making it easy to catch all application-specific errors.
    """
    pass


class ConnectionError(LMStudioError):
    """
    Raised when unable to connect to the LM Studio server.

    This typically indicates that:
    - LM Studio is not running
    - The API URL is incorrect
    - Network connectivity issues

    Suggested resolution: Start LM Studio and ensure the server is running.
    """
    pass


class TimeoutError(LMStudioError):
    """
    Raised when an API request times out.

    This can occur when:
    - The model is taking too long to generate a response
    - Network latency is high
    - The server is overloaded

    Suggested resolution: Increase the timeout value or use a smaller model.
    """
    pass


class APIError(LMStudioError):
    """
    Raised when the API returns an error response.

    This is a general error for any API-level issues including:
    - Invalid request format
    - Server-side errors
    - Rate limiting

    The exception message will contain details from the API response.
    """
    pass


class ModelNotFoundError(LMStudioError):
    """
    Raised when a requested model is not found.

    This occurs when:
    - The model name is incorrect
    - The model is not loaded in LM Studio
    - The model has been removed

    Suggested resolution: Check available models with 'lms models list'.
    """
    pass


class ConfigurationError(LMStudioError):
    """
    Raised when there's a configuration error.

    This can happen when:
    - Config file is malformed
    - Required settings are missing
    - Settings have invalid values

    Suggested resolution: Run 'lms init' to create a valid configuration.
    """
    pass


class HistoryError(LMStudioError):
    """
    Raised when there's an error with conversation history.

    This can occur when:
    - Unable to read/write history files
    - History storage is corrupted
    - Insufficient permissions

    Suggested resolution: Check file permissions and storage availability.
    """
    pass


class ValidationError(LMStudioError):
    """
    Raised when input validation fails.

    This occurs when:
    - User input is invalid
    - Parameters are out of acceptable ranges
    - Required fields are missing

    The exception message will describe what validation failed.
    """
    pass
