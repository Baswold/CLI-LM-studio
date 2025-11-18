"""
Utility functions for CLI-LM-Studio.

This module provides various helper functions used throughout
the application, including logging setup, error handling,
formatting, and validation.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.logging import RichHandler

console = Console()


def setup_logging(verbose: bool = False, log_file: Optional[Path] = None) -> None:
    """
    Configure logging for the application.

    Sets up both console and file logging with appropriate formats
    and levels. Uses Rich for beautiful console logging.

    Args:
        verbose: If True, set log level to DEBUG, otherwise INFO
        log_file: Optional path to log file
    """
    # Determine log level
    log_level = logging.DEBUG if verbose else logging.INFO

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers.clear()

    # Add Rich console handler
    console_handler = RichHandler(
        console=console,
        show_time=True,
        show_path=verbose,
        markup=True,
        rich_tracebacks=True,
        tracebacks_show_locals=verbose,
    )
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        "%(message)s",
        datefmt="[%X]",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)  # Always DEBUG for file
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        except Exception as e:
            console.print(f"[yellow]Warning: Could not set up file logging: {e}[/yellow]")

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def handle_error(message: str, exit_code: int = 1) -> None:
    """
    Handle an error by displaying it and exiting.

    Args:
        message: Error message to display
        exit_code: Exit code (default: 1)
    """
    console.print(f"[bold red]Error:[/bold red] {message}")
    sys.exit(exit_code)


def format_timestamp(timestamp: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a timestamp as a string.

    Args:
        timestamp: Datetime object to format
        format_str: strftime format string

    Returns:
        Formatted timestamp string
    """
    return timestamp.strftime(format_str)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated (default: "...")

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    # Account for suffix length
    truncate_at = max_length - len(suffix)
    return text[:truncate_at] + suffix


def validate_temperature(temperature: float) -> float:
    """
    Validate and clamp temperature value.

    Args:
        temperature: Temperature value to validate

    Returns:
        Validated temperature (clamped to 0.0-2.0)
    """
    if temperature < 0.0:
        console.print("[yellow]Warning: Temperature < 0.0, using 0.0[/yellow]")
        return 0.0
    elif temperature > 2.0:
        console.print("[yellow]Warning: Temperature > 2.0, using 2.0[/yellow]")
        return 2.0
    return temperature


def validate_max_tokens(max_tokens: int) -> int:
    """
    Validate max_tokens value.

    Args:
        max_tokens: Maximum tokens value to validate

    Returns:
        Validated max_tokens

    Raises:
        ValueError: If max_tokens is less than 1
    """
    if max_tokens < 1:
        raise ValueError("max_tokens must be at least 1")
    return max_tokens


def estimate_tokens(text: str) -> int:
    """
    Roughly estimate the number of tokens in text.

    This is a simple approximation using word count.
    Real tokenization depends on the specific model.

    Args:
        text: Text to estimate tokens for

    Returns:
        Estimated token count
    """
    # Rough approximation: 1 token ≈ 0.75 words
    words = len(text.split())
    return int(words * 1.33)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists

    Raises:
        OSError: If directory cannot be created
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Failed to create directory {path}: {e}") from e


def read_file_safe(file_path: Path) -> Optional[str]:
    """
    Safely read a file, returning None on error.

    Args:
        file_path: Path to file to read

    Returns:
        File contents or None if reading failed
    """
    try:
        return file_path.read_text()
    except Exception as e:
        console.print(f"[yellow]Warning: Could not read {file_path}: {e}[/yellow]")
        return None


def write_file_safe(file_path: Path, content: str) -> bool:
    """
    Safely write to a file.

    Args:
        file_path: Path to file to write
        content: Content to write

    Returns:
        True if successful, False otherwise
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return True
    except Exception as e:
        console.print(f"[yellow]Warning: Could not write {file_path}: {e}[/yellow]")
        return False


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Ask user to confirm an action.

    Args:
        message: Confirmation message
        default: Default response if user just presses Enter

    Returns:
        True if user confirms, False otherwise
    """
    from rich.prompt import Confirm
    return Confirm.ask(message, default=default)


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "2m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {remaining_seconds}s"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    return f"{hours}h {remaining_minutes}m"


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.

    Args:
        filename: Original filename
        replacement: Character to replace invalid chars with

    Returns:
        Sanitized filename
    """
    # Characters that are invalid in filenames
    invalid_chars = '<>:"/\\|?*'

    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, replacement)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")

    # Ensure filename is not empty
    if not sanitized:
        sanitized = "unnamed"

    return sanitized


def get_terminal_width() -> int:
    """
    Get the width of the terminal.

    Returns:
        Terminal width in characters
    """
    return console.width


class Timer:
    """
    Simple context manager for timing operations.

    Example:
        with Timer() as timer:
            # Do some work
            pass
        print(f"Operation took {timer.elapsed:.2f} seconds")
    """

    def __init__(self) -> None:
        """Initialize the timer."""
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self) -> "Timer":
        """Start the timer."""
        import time
        self.start_time = time.time()
        return self

    def __exit__(self, *args: Any) -> None:
        """Stop the timer."""
        import time
        self.end_time = time.time()

    @property
    def elapsed(self) -> float:
        """
        Get elapsed time in seconds.

        Returns:
            Elapsed time in seconds
        """
        if self.start_time is None:
            return 0.0

        if self.end_time is None:
            import time
            return time.time() - self.start_time

        return self.end_time - self.start_time
