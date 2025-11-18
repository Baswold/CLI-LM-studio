"""
Main CLI entry point for LM Studio CLI.

This module provides the primary command-line interface using Click.
It handles all user commands and orchestrates the various features.
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from lm_studio_cli import __version__
from lm_studio_cli.client import LMStudioClient
from lm_studio_cli.config import Config, ConfigurationError
from lm_studio_cli.chat import ChatSession
from lm_studio_cli.models import ModelManager
from lm_studio_cli.history import HistoryManager
from lm_studio_cli.utils import setup_logging, handle_error

# Rich console for beautiful output
console = Console()


@click.group(invoke_without_command=True)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--version", is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx: click.Context, config: Optional[Path], verbose: bool, version: bool) -> None:
    """
    CLI-LM-Studio: A powerful command-line interface for LM Studio.

    Interact with your local language models through an intuitive CLI.
    Chat, manage models, review history, and more!

    Examples:
        lms chat "Hello, how are you?"
        lms models list
        lms history show
    """
    # Show version if requested
    if version:
        console.print(f"[bold blue]CLI-LM-Studio[/bold blue] version {__version__}")
        sys.exit(0)

    # Setup logging
    setup_logging(verbose)

    # Load configuration
    try:
        ctx.obj = Config.load(config)
    except ConfigurationError as e:
        handle_error(f"Configuration error: {e}", exit_code=1)

    # If no command is provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument("message", required=False)
@click.option("--model", "-m", help="Model to use (overrides config)")
@click.option("--system", "-s", help="System prompt (overrides config)")
@click.option("--temperature", "-t", type=float, help="Temperature (0.0-2.0)")
@click.option("--max-tokens", type=int, help="Maximum tokens to generate")
@click.option("--interactive", "-i", is_flag=True, help="Start interactive chat mode")
@click.option("--stream/--no-stream", default=True, help="Stream responses (default: true)")
@click.pass_obj
def chat(
    config: Config,
    message: Optional[str],
    model: Optional[str],
    system: Optional[str],
    temperature: Optional[float],
    max_tokens: Optional[int],
    interactive: bool,
    stream: bool,
) -> None:
    """
    Chat with a language model.

    Supports both single-shot and interactive conversations.

    Examples:
        lms chat "What is Python?"
        lms chat -i  # Interactive mode
        lms chat -m "llama-2-7b" "Tell me a joke"
    """
    try:
        # Create client
        client = LMStudioClient(config)

        # Override config with CLI options
        if model:
            config.default_model = model
        if system:
            config.system_prompt = system
        if temperature is not None:
            config.temperature = temperature
        if max_tokens is not None:
            config.max_tokens = max_tokens

        # Create chat session
        session = ChatSession(client, config, stream=stream)

        if interactive or message is None:
            # Interactive mode
            session.start_interactive()
        else:
            # Single message mode
            response = session.send_message(message)
            console.print(Panel(Markdown(response), title="[bold blue]Response[/bold blue]"))

    except Exception as e:
        handle_error(f"Chat error: {e}", exit_code=1)


@cli.group()
def models() -> None:
    """
    Manage language models.

    List available models, get model information, and set defaults.
    """
    pass


@models.command("list")
@click.option("--detailed", "-d", is_flag=True, help="Show detailed information")
@click.pass_obj
def models_list(config: Config, detailed: bool) -> None:
    """
    List all available models.

    Examples:
        lms models list
        lms models list --detailed
    """
    try:
        client = LMStudioClient(config)
        manager = ModelManager(client)
        manager.list_models(detailed=detailed)
    except Exception as e:
        handle_error(f"Error listing models: {e}", exit_code=1)


@models.command("info")
@click.argument("model_name")
@click.pass_obj
def models_info(config: Config, model_name: str) -> None:
    """
    Get detailed information about a specific model.

    Examples:
        lms models info llama-2-7b
    """
    try:
        client = LMStudioClient(config)
        manager = ModelManager(client)
        manager.show_model_info(model_name)
    except Exception as e:
        handle_error(f"Error getting model info: {e}", exit_code=1)


@models.command("set-default")
@click.argument("model_name")
@click.pass_obj
def models_set_default(config: Config, model_name: str) -> None:
    """
    Set the default model for chat sessions.

    Examples:
        lms models set-default llama-2-7b
    """
    try:
        config.default_model = model_name
        config.save()
        console.print(f"[green]✓[/green] Default model set to: [bold]{model_name}[/bold]")
    except Exception as e:
        handle_error(f"Error setting default model: {e}", exit_code=1)


@cli.group()
def history() -> None:
    """
    Manage conversation history.

    View, search, and manage your chat history.
    """
    pass


@history.command("show")
@click.option("--limit", "-n", type=int, default=10, help="Number of entries to show")
@click.option("--all", "show_all", is_flag=True, help="Show all history")
@click.pass_obj
def history_show(config: Config, limit: int, show_all: bool) -> None:
    """
    Show recent conversation history.

    Examples:
        lms history show
        lms history show -n 20
        lms history show --all
    """
    try:
        manager = HistoryManager(config)
        manager.show_history(limit=None if show_all else limit)
    except Exception as e:
        handle_error(f"Error showing history: {e}", exit_code=1)


@history.command("search")
@click.argument("query")
@click.pass_obj
def history_search(config: Config, query: str) -> None:
    """
    Search conversation history.

    Examples:
        lms history search "python tutorial"
    """
    try:
        manager = HistoryManager(config)
        manager.search_history(query)
    except Exception as e:
        handle_error(f"Error searching history: {e}", exit_code=1)


@history.command("clear")
@click.option("--confirm", "-y", is_flag=True, help="Skip confirmation")
@click.pass_obj
def history_clear(config: Config, confirm: bool) -> None:
    """
    Clear all conversation history.

    Examples:
        lms history clear
        lms history clear -y  # Skip confirmation
    """
    if not confirm:
        if not click.confirm("Are you sure you want to clear all history?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    try:
        manager = HistoryManager(config)
        manager.clear_history()
        console.print("[green]✓[/green] History cleared")
    except Exception as e:
        handle_error(f"Error clearing history: {e}", exit_code=1)


@cli.command()
@click.pass_obj
def config_show(config: Config) -> None:
    """
    Show current configuration.

    Examples:
        lms config-show
    """
    config.display()


@cli.command()
@click.pass_obj
def init(config: Config) -> None:
    """
    Initialize CLI-LM-Studio configuration.

    Creates a default configuration file if none exists.

    Examples:
        lms init
    """
    try:
        config_path = Config.get_config_path()

        if config_path.exists():
            if not click.confirm(
                f"Configuration already exists at {config_path}. Overwrite?"
            ):
                console.print("[yellow]Cancelled[/yellow]")
                return

        # Create default config
        default_config = Config.create_default()
        default_config.save()

        console.print(
            Panel(
                f"[green]✓[/green] Configuration initialized at:\n"
                f"[cyan]{config_path}[/cyan]\n\n"
                f"Edit this file to customize your settings.",
                title="[bold blue]Configuration Initialized[/bold blue]",
            )
        )
    except Exception as e:
        handle_error(f"Error initializing configuration: {e}", exit_code=1)


if __name__ == "__main__":
    cli()
