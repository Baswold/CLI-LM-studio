"""
Conversation history management for CLI-LM-Studio.

This module handles saving, loading, searching, and managing
conversation history. History is stored as JSON for easy querying.

TODO: Implement full-text search with indexing
TODO: Add tagging/categorization for conversations
TODO: Support exporting history to various formats
TODO: Implement conversation analytics and insights
TODO: Add conversation sharing/collaboration features
TODO: Optimize storage format for large histories
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from lm_studio_cli.config import Config
from lm_studio_cli.exceptions import HistoryError

console = Console()


class HistoryEntry:
    """
    Represents a single conversation history entry.

    Attributes:
        timestamp: When the conversation occurred
        user_message: The user's message
        assistant_message: The assistant's response
        model: Which model was used
        metadata: Additional metadata about the conversation
    """

    def __init__(
        self,
        user_message: str,
        assistant_message: str,
        model: str,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize a history entry.

        Args:
            user_message: User's message
            assistant_message: Assistant's response
            model: Model used
            timestamp: When the conversation occurred (default: now)
            metadata: Additional metadata
        """
        self.timestamp = timestamp or datetime.now()
        self.user_message = user_message
        self.assistant_message = assistant_message
        self.model = model
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert entry to dictionary.

        Returns:
            Dictionary representation of the entry
        """
        return {
            "timestamp": self.timestamp.isoformat(),
            "user_message": self.user_message,
            "assistant_message": self.assistant_message,
            "model": self.model,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistoryEntry":
        """
        Create entry from dictionary.

        Args:
            data: Dictionary with entry data

        Returns:
            HistoryEntry instance
        """
        return cls(
            user_message=data["user_message"],
            assistant_message=data["assistant_message"],
            model=data["model"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )


class HistoryManager:
    """
    Manages conversation history.

    This class handles all operations related to conversation history,
    including saving, loading, searching, and cleanup.

    Attributes:
        config: Configuration object
        history_file: Path to the history JSON file
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the history manager.

        Args:
            config: Configuration object
        """
        self.config = config
        self.history_file = config.history_path / "conversations.json"

        # Ensure history directory exists
        self._ensure_history_dir()

    def _ensure_history_dir(self) -> None:
        """Create history directory if it doesn't exist."""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise HistoryError(f"Failed to create history directory: {e}") from e

    def add_entry(
        self,
        user_message: str,
        assistant_message: str,
        model: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add a new entry to the history.

        Args:
            user_message: User's message
            assistant_message: Assistant's response
            model: Model used
            metadata: Additional metadata
        """
        entry = HistoryEntry(
            user_message=user_message,
            assistant_message=assistant_message,
            model=model,
            metadata=metadata,
        )

        try:
            # Load existing history
            history = self._load_history()

            # Add new entry
            history.append(entry.to_dict())

            # Enforce max entries limit
            if len(history) > self.config.history_max_entries:
                # Keep only the most recent entries
                history = history[-self.config.history_max_entries:]

            # Save back to file
            self._save_history(history)

        except Exception as e:
            # Don't raise - history failure shouldn't break the app
            console.print(f"[yellow]Warning: Failed to save history: {e}[/yellow]")

    def _load_history(self) -> List[Dict[str, Any]]:
        """
        Load history from file.

        Returns:
            List of history entry dictionaries
        """
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # File is corrupted, start fresh
            console.print("[yellow]Warning: History file corrupted, starting fresh[/yellow]")
            return []
        except Exception as e:
            raise HistoryError(f"Failed to load history: {e}") from e

    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """
        Save history to file.

        Args:
            history: List of history entries
        """
        try:
            with open(self.history_file, "w") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {e}") from e

    def show_history(self, limit: Optional[int] = None) -> None:
        """
        Display conversation history.

        Args:
            limit: Maximum number of entries to show (None for all)
        """
        try:
            history = self._load_history()

            if not history:
                console.print("[yellow]No history found[/yellow]")
                return

            # Apply limit
            if limit:
                history = history[-limit:]

            # Create table
            table = Table(
                title=f"Conversation History ({len(history)} entries)",
                show_header=True,
                header_style="bold cyan",
            )

            table.add_column("Time", style="cyan", no_wrap=True)
            table.add_column("Model", style="green")
            table.add_column("User Message", style="yellow", max_width=40)
            table.add_column("Assistant Response", style="blue", max_width=40)

            for entry_data in history:
                entry = HistoryEntry.from_dict(entry_data)

                # Format timestamp
                time_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")

                # Truncate messages for display
                user_msg = self._truncate(entry.user_message, 37)
                assistant_msg = self._truncate(entry.assistant_message, 37)

                table.add_row(
                    time_str,
                    entry.model,
                    user_msg,
                    assistant_msg,
                )

            console.print(table)

        except Exception as e:
            console.print(f"[bold red]Error showing history:[/bold red] {e}")

    def search_history(self, query: str) -> None:
        """
        Search history for entries matching a query.

        Args:
            query: Search query string
        """
        try:
            history = self._load_history()

            if not history:
                console.print("[yellow]No history found[/yellow]")
                return

            # Search for matches
            matches = []
            query_lower = query.lower()

            for entry_data in history:
                entry = HistoryEntry.from_dict(entry_data)

                # Check if query appears in either message
                if (query_lower in entry.user_message.lower() or
                    query_lower in entry.assistant_message.lower()):
                    matches.append(entry)

            if not matches:
                console.print(f"[yellow]No results found for '{query}'[/yellow]")
                return

            # Display results
            console.print(f"\n[bold cyan]Found {len(matches)} result(s) for '{query}':[/bold cyan]\n")

            for i, entry in enumerate(matches, 1):
                time_str = entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")

                panel_content = (
                    f"[bold]Time:[/bold] {time_str}\n"
                    f"[bold]Model:[/bold] {entry.model}\n\n"
                    f"[bold cyan]User:[/bold cyan]\n{entry.user_message}\n\n"
                    f"[bold blue]Assistant:[/bold blue]\n{entry.assistant_message}"
                )

                console.print(
                    Panel(
                        panel_content,
                        title=f"[bold]Result {i}[/bold]",
                        border_style="green",
                    )
                )

        except Exception as e:
            console.print(f"[bold red]Error searching history:[/bold red] {e}")

    def clear_history(self) -> None:
        """
        Clear all history.
        """
        try:
            self._save_history([])
            console.print("[green]✓[/green] History cleared")
        except Exception as e:
            console.print(f"[bold red]Error clearing history:[/bold red] {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the conversation history.

        Returns:
            Dictionary with history statistics
        """
        try:
            history = self._load_history()

            # Count conversations by model
            models: Dict[str, int] = {}
            for entry_data in history:
                model = entry_data.get("model", "Unknown")
                models[model] = models.get(model, 0) + 1

            # Get date range
            timestamps = [
                datetime.fromisoformat(e["timestamp"])
                for e in history
            ]

            return {
                "total_conversations": len(history),
                "models_used": models,
                "oldest_entry": min(timestamps).isoformat() if timestamps else None,
                "newest_entry": max(timestamps).isoformat() if timestamps else None,
            }

        except Exception:
            return {
                "total_conversations": 0,
                "models_used": {},
                "oldest_entry": None,
                "newest_entry": None,
            }

    @staticmethod
    def _truncate(text: str, max_length: int) -> str:
        """
        Truncate text to a maximum length.

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text with ellipsis if needed
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
