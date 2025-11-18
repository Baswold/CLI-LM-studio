"""
LM Studio API Client.

This module provides a robust client for interacting with the LM Studio API.
It handles connection management, error handling, and provides a clean
interface for making requests.

TODO: Add response caching for repeated queries
TODO: Implement async/await support for better performance
TODO: Add request batching for multiple queries
TODO: Support websocket connections for real-time streaming
"""

import logging
from typing import Any, Dict, Iterator, List, Optional, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from lm_studio_cli.config import Config
from lm_studio_cli.exceptions import (
    APIError,
    ConnectionError as LMConnectionError,
    ModelNotFoundError,
    TimeoutError,
)

logger = logging.getLogger(__name__)


class LMStudioClient:
    """
    Client for interacting with LM Studio's local API.

    This client handles all communication with the LM Studio server,
    including chat completions, model queries, and health checks.

    Attributes:
        base_url: The base URL of the LM Studio server
        timeout: Request timeout in seconds
        session: Configured requests session with retry logic
    """

    def __init__(
        self,
        config: Config,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        """
        Initialize the LM Studio client.

        Args:
            config: Configuration object containing server details
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries for failed requests (default: 3)
        """
        self.base_url = config.api_url
        self.timeout = timeout
        self.config = config

        # Configure session with retry logic
        self.session = self._create_session(max_retries)

        logger.info(f"Initialized LM Studio client for {self.base_url}")

    def _create_session(self, max_retries: int) -> requests.Session:
        """
        Create a requests session with automatic retry logic.

        Args:
            max_retries: Maximum number of retries

        Returns:
            Configured requests session
        """
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Make an HTTP request to the LM Studio API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object

        Raises:
            LMConnectionError: If connection to server fails
            TimeoutError: If request times out
            APIError: If API returns an error
        """
        url = urljoin(self.base_url, endpoint)

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise LMConnectionError(
                f"Could not connect to LM Studio at {self.base_url}. "
                "Is LM Studio running?"
            ) from e

        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error: {e}")
            raise TimeoutError(
                f"Request timed out after {self.timeout} seconds"
            ) from e

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise APIError(
                f"API error: {e.response.status_code} - {e.response.text}"
            ) from e

    def health_check(self) -> bool:
        """
        Check if the LM Studio server is healthy and responsive.

        Returns:
            True if server is healthy, False otherwise
        """
        try:
            # Try to get models as a health check
            self.get_models()
            return True
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False

    def get_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from LM Studio.

        Returns:
            List of model dictionaries with metadata

        Raises:
            APIError: If the API request fails
        """
        try:
            response = self._make_request("GET", "/v1/models")
            data = response.json()

            # LM Studio returns models in OpenAI-compatible format
            if "data" in data:
                return data["data"]
            return []

        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            raise APIError(f"Failed to fetch models: {e}") from e

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific model.

        Args:
            model_name: Name of the model

        Returns:
            Dictionary with model information

        Raises:
            ModelNotFoundError: If model is not found
            APIError: If the API request fails
        """
        models = self.get_models()

        for model in models:
            if model.get("id") == model_name:
                return model

        raise ModelNotFoundError(f"Model '{model_name}' not found")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Create a chat completion.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to config default)
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters for the API

        Returns:
            Response dictionary or iterator of response chunks (if streaming)

        Raises:
            APIError: If the API request fails
        """
        # Use config defaults if not specified
        model = model or self.config.default_model
        temperature = temperature if temperature is not None else self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            **kwargs,
        }

        logger.debug(f"Chat completion request: {payload}")

        if stream:
            return self._stream_completion(payload)
        else:
            response = self._make_request("POST", "/v1/chat/completions", json=payload)
            return response.json()

    def _stream_completion(
        self, payload: Dict[str, Any]
    ) -> Iterator[Dict[str, Any]]:
        """
        Stream a chat completion response.

        Args:
            payload: Request payload

        Yields:
            Response chunks as they arrive
        """
        url = urljoin(self.base_url, "/v1/chat/completions")

        try:
            with self.session.post(
                url,
                json=payload,
                timeout=self.timeout,
                stream=True,
            ) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if not line:
                        continue

                    # SSE format: "data: {json}"
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]

                        # Check for stream end
                        if data_str.strip() == "[DONE]":
                            break

                        try:
                            import json
                            yield json.loads(data_str)
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse chunk: {data_str}")

        except Exception as e:
            logger.error(f"Error streaming completion: {e}")
            raise APIError(f"Failed to stream completion: {e}") from e

    def close(self) -> None:
        """
        Close the client session and cleanup resources.
        """
        self.session.close()
        logger.info("LM Studio client closed")

    def __enter__(self) -> "LMStudioClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
