"""
CLI-LM-Studio: A powerful command-line interface for LM Studio.

This package provides a comprehensive CLI tool for interacting with LM Studio,
including chat functionality, model management, and conversation history.
"""

__version__ = "0.1.0"
__author__ = "CLI-LM-Studio Contributors"
__license__ = "MIT"

from lm_studio_cli.client import LMStudioClient
from lm_studio_cli.config import Config

__all__ = ["LMStudioClient", "Config", "__version__"]
