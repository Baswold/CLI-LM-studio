"""
Model management for CLI-LM-Studio.

This module provides functionality for listing, querying, and managing
language models available in LM Studio.
"""

from datetime import datetime
from typing import Any, Dict, List

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.json import JSON

from lm_studio_cli.client import LMStudioClient
from lm_studio_cli.exceptions import ModelNotFoundError

console = Console()


class ModelManager:
    """
    Manages language models in LM Studio.

    This class provides high-level operations for working with models,
    including listing, getting info, and displaying model details.

    Attributes:
        client: LM Studio API client
    """

    def __init__(self, client: LMStudioClient) -> None:
        """
        Initialize the model manager.

        Args:
            client: LM Studio API client
        """
        self.client = client

    def list_models(self, detailed: bool = False) -> None:
        """
        List all available models.

        Displays models in a formatted table with key information.

        Args:
            detailed: Whether to show detailed information
        """
        try:
            models = self.client.get_models()

            if not models:
                console.print("[yellow]No models found. Make sure LM Studio is running.[/yellow]")
                return

            if detailed:
                self._display_detailed_models(models)
            else:
                self._display_model_table(models)

        except Exception as e:
            console.print(f"[bold red]Error listing models:[/bold red] {e}")

    def _display_model_table(self, models: List[Dict[str, Any]]) -> None:
        """
        Display models in a simple table format.

        Args:
            models: List of model dictionaries
        """
        table = Table(
            title=f"Available Models ({len(models)} found)",
            show_header=True,
            header_style="bold cyan",
        )

        table.add_column("Model ID", style="green", no_wrap=True)
        table.add_column("Object Type", style="blue")
        table.add_column("Owned By", style="yellow")

        for model in models:
            table.add_row(
                model.get("id", "Unknown"),
                model.get("object", "Unknown"),
                model.get("owned_by", "Unknown"),
            )

        console.print(table)

        # Display usage hint
        console.print(
            "\n[dim]Tip: Use --detailed flag for more information[/dim]"
        )

    def _display_detailed_models(self, models: List[Dict[str, Any]]) -> None:
        """
        Display models with detailed information.

        Args:
            models: List of model dictionaries
        """
        console.print(f"\n[bold cyan]Found {len(models)} model(s):[/bold cyan]\n")

        for i, model in enumerate(models, 1):
            # Create a panel for each model
            model_info = []
            model_info.append(f"[bold]ID:[/bold] {model.get('id', 'Unknown')}")
            model_info.append(f"[bold]Type:[/bold] {model.get('object', 'Unknown')}")
            model_info.append(f"[bold]Owner:[/bold] {model.get('owned_by', 'Unknown')}")

            # Add creation time if available
            if "created" in model:
                created = datetime.fromtimestamp(model["created"])
                model_info.append(f"[bold]Created:[/bold] {created.strftime('%Y-%m-%d %H:%M:%S')}")

            # Add permissions if available
            if "permission" in model:
                model_info.append(f"[bold]Permissions:[/bold] Available")

            # Add root model if available
            if "root" in model:
                model_info.append(f"[bold]Root:[/bold] {model['root']}")

            # Add parent if available
            if "parent" in model:
                model_info.append(f"[bold]Parent:[/bold] {model['parent']}")

            console.print(
                Panel(
                    "\n".join(model_info),
                    title=f"[bold blue]Model {i}[/bold blue]",
                    border_style="blue",
                )
            )

    def show_model_info(self, model_name: str) -> None:
        """
        Show detailed information about a specific model.

        Args:
            model_name: Name of the model to query

        Raises:
            ModelNotFoundError: If model is not found
        """
        try:
            model = self.client.get_model_info(model_name)

            # Display as formatted JSON
            console.print(
                Panel(
                    JSON.from_data(model, indent=2),
                    title=f"[bold blue]Model Info: {model_name}[/bold blue]",
                    border_style="blue",
                )
            )

        except ModelNotFoundError:
            console.print(f"[bold red]Error:[/bold red] Model '{model_name}' not found")
            console.print("\n[dim]Available models:[/dim]")
            self.list_models(detailed=False)

        except Exception as e:
            console.print(f"[bold red]Error getting model info:[/bold red] {e}")

    def get_model_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about available models.

        Returns:
            Dictionary with model statistics
        """
        try:
            models = self.client.get_models()

            # Count models by owner
            owners: Dict[str, int] = {}
            for model in models:
                owner = model.get("owned_by", "Unknown")
                owners[owner] = owners.get(owner, 0) + 1

            return {
                "total_models": len(models),
                "models_by_owner": owners,
                "model_ids": [m.get("id") for m in models],
            }

        except Exception as e:
            console.print(f"[bold red]Error getting model statistics:[/bold red] {e}")
            return {
                "total_models": 0,
                "models_by_owner": {},
                "model_ids": [],
            }

    def validate_model(self, model_name: str) -> bool:
        """
        Check if a model exists and is available.

        Args:
            model_name: Name of the model to validate

        Returns:
            True if model exists, False otherwise
        """
        try:
            self.client.get_model_info(model_name)
            return True
        except ModelNotFoundError:
            return False
        except Exception:
            return False
