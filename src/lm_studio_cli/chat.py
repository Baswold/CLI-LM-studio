"""
Chat session management for CLI-LM-Studio.

This module handles interactive and single-shot chat sessions,
managing conversation state, streaming responses, and user interaction.

TODO: Add conversation branching/checkpoints
TODO: Implement conversation templates
TODO: Add support for file attachments (when LM Studio supports it)
TODO: Add conversation export in multiple formats (MD, JSON, HTML)
TODO: Implement pause/resume for streaming responses
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner

from lm_studio_cli.client import LMStudioClient
from lm_studio_cli.config import Config
from lm_studio_cli.history import HistoryManager
from lm_studio_cli.exceptions import APIError, ValidationError

console = Console()


class ChatSession:
    """
    Manages a chat session with LM Studio.

    This class handles the conversation state, sends messages to the API,
    and manages the display of responses. Supports both streaming and
    non-streaming modes.

    Attributes:
        client: LM Studio API client
        config: Configuration object
        messages: Current conversation messages
        stream: Whether to stream responses
        history_manager: Manager for conversation history
    """

    def __init__(
        self,
        client: LMStudioClient,
        config: Config,
        stream: bool = True,
    ) -> None:
        """
        Initialize a chat session.

        Args:
            client: LM Studio API client
            config: Configuration object
            stream: Whether to stream responses (default: True)
        """
        self.client = client
        self.config = config
        self.stream = stream
        self.messages: List[Dict[str, str]] = []

        # Initialize history manager
        self.history_manager = HistoryManager(config) if config.history_enabled else None

        # Add system prompt if configured
        if config.system_prompt:
            self.messages.append({
                "role": "system",
                "content": config.system_prompt,
            })

    def send_message(self, content: str) -> str:
        """
        Send a message and get a response.

        Args:
            content: User message content

        Returns:
            Assistant's response

        Raises:
            ValidationError: If message is empty
            APIError: If API request fails
        """
        # Validate input
        if not content.strip():
            raise ValidationError("Message cannot be empty")

        # Add user message to conversation
        self.messages.append({
            "role": "user",
            "content": content,
        })

        try:
            if self.stream:
                response = self._send_streaming()
            else:
                response = self._send_non_streaming()

            # Add assistant response to conversation
            self.messages.append({
                "role": "assistant",
                "content": response,
            })

            # Save to history
            if self.history_manager:
                self.history_manager.add_entry(
                    user_message=content,
                    assistant_message=response,
                    model=self.config.default_model,
                )

            return response

        except Exception as e:
            # Remove user message if request failed
            self.messages.pop()
            raise APIError(f"Failed to get response: {e}") from e

    def _send_streaming(self) -> str:
        """
        Send message with streaming response.

        Returns:
            Complete response text
        """
        response_text = ""

        console.print(Panel("", title="[bold blue]Response[/bold blue]", border_style="blue"))

        # Use Live display for streaming updates
        with Live(Spinner("dots", text="Thinking..."), console=console, refresh_per_second=10) as live:
            try:
                for chunk in self.client.chat_completion(
                    messages=self.messages,
                    stream=True,
                ):
                    # Extract content from chunk
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")

                    if content:
                        response_text += content

                        # Update display with accumulated response
                        if self.config.markdown_enabled:
                            live.update(Markdown(response_text))
                        else:
                            live.update(response_text)

            except KeyboardInterrupt:
                console.print("\n[yellow]Response interrupted[/yellow]")
                raise

        console.print()  # Add newline after response
        return response_text

    def _send_non_streaming(self) -> str:
        """
        Send message without streaming.

        Returns:
            Complete response text
        """
        with console.status("[bold blue]Thinking...", spinner="dots"):
            response = self.client.chat_completion(
                messages=self.messages,
                stream=False,
            )

        # Extract response text
        response_text = response["choices"][0]["message"]["content"]
        return response_text

    def start_interactive(self) -> None:
        """
        Start an interactive chat session.

        This method runs a loop accepting user input and displaying
        responses until the user exits.
        """
        console.print(
            Panel(
                "[bold blue]Interactive Chat Mode[/bold blue]\n\n"
                "Type your messages and press Enter.\n"
                "Commands:\n"
                "  /exit, /quit - Exit the chat\n"
                "  /clear - Clear conversation history\n"
                "  /save - Save conversation\n"
                "  /help - Show this help message",
                border_style="blue",
            )
        )

        try:
            while True:
                # Get user input
                try:
                    user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                except KeyboardInterrupt:
                    console.print("\n[yellow]Exiting...[/yellow]")
                    break

                # Handle commands
                if user_input.lower() in ["/exit", "/quit"]:
                    console.print("[yellow]Goodbye![/yellow]")
                    break

                elif user_input.lower() == "/clear":
                    self._clear_conversation()
                    continue

                elif user_input.lower() == "/save":
                    self._save_conversation()
                    continue

                elif user_input.lower() == "/help":
                    self._show_help()
                    continue

                # Skip empty messages
                if not user_input.strip():
                    continue

                # Send message and get response
                try:
                    self.send_message(user_input)

                except Exception as e:
                    console.print(f"[bold red]Error:[/bold red] {e}")

        except Exception as e:
            console.print(f"[bold red]Fatal error:[/bold red] {e}")
            sys.exit(1)

    def _clear_conversation(self) -> None:
        """Clear the current conversation history."""
        # Keep system prompt if it exists
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        self.messages = system_messages
        console.print("[green]✓[/green] Conversation cleared")

    def _save_conversation(self) -> None:
        """Save the current conversation to a file."""
        if not self.history_manager:
            console.print("[yellow]History is disabled in configuration[/yellow]")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.txt"

        try:
            # Create conversation text
            conversation_text = []
            for msg in self.messages:
                if msg["role"] == "system":
                    continue
                role = "You" if msg["role"] == "user" else "Assistant"
                conversation_text.append(f"{role}: {msg['content']}\n")

            # Save to file
            filepath = self.config.history_path / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w") as f:
                f.write("\n".join(conversation_text))

            console.print(f"[green]✓[/green] Conversation saved to: {filepath}")

        except Exception as e:
            console.print(f"[bold red]Error saving conversation:[/bold red] {e}")

    def _show_help(self) -> None:
        """Show help message."""
        console.print(
            Panel(
                "[bold]Available Commands:[/bold]\n\n"
                "  /exit, /quit - Exit the chat\n"
                "  /clear - Clear conversation history\n"
                "  /save - Save conversation to file\n"
                "  /help - Show this help message\n\n"
                "[bold]Tips:[/bold]\n"
                "  - Press Ctrl+C to interrupt a response\n"
                "  - Responses are rendered in Markdown format\n"
                f"  - Current model: {self.config.default_model}\n"
                f"  - Temperature: {self.config.temperature}",
                title="[bold blue]Help[/bold blue]",
                border_style="blue",
            )
        )

    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current conversation.

        Returns:
            Dictionary with conversation statistics
        """
        user_messages = [msg for msg in self.messages if msg["role"] == "user"]
        assistant_messages = [msg for msg in self.messages if msg["role"] == "assistant"]

        total_tokens = sum(
            len(msg["content"].split()) for msg in self.messages
        )

        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "estimated_tokens": total_tokens,
            "model": self.config.default_model,
        }
