# cl_llm/cli.py
"""
Main CLI entry point for CLLM application.
"""

import typer
from typing import Optional
from rich import print as rprint
from rich.panel import Panel
from rich.columns import Columns
from cl_llm.theme import ICONS, console, create_header, create_system_message, create_divider
from cl_llm.commands import ask, chat

app = typer.Typer(
    help="✨ CLLM - An elegant CLI for interacting with Gemini LLM ✨",
    add_completion=False,
    rich_markup_mode="rich"
)

@app.callback()
def callback():
    """
    ✨ CLLM - Interact with Gemini LLM through your command line! ✨
    
    A beautiful CLI for conversing with Google's Gemini LLM.
    """
    # Show a welcome banner when no command is provided
    if typer.Context.invoke == callback:
        console.print(create_header("Welcome to CLLM", "Your terminal gateway to Gemini LLM"))
        console.print(create_system_message("Type 'cllm help' to see available commands"))
        console.print(create_divider())

# Register commands
app.command("ask", help="Ask a question to Gemini LLM")(ask.main)
app.command("chat", help="Start a conversation with Gemini LLM")(chat.main)

@app.command("help")
def help_cmd():
    """Show help information with command examples"""
    console.print(create_header("CLLM Help", "Available commands and examples"))
    console.print(create_divider())
    
    commands = [
        Panel(
            f"[bold]ask [cyan]<your question or prompt>[/cyan][/]\n"
            f"Ask a question or provide a prompt to Gemini LLM\n"
            f"[dim]Example: cllm ask \"What is machine learning?\"[/]\n"
            f"[dim]Example: cllm ask Write a haiku about coding[/]",
            title=f"{ICONS['ask']} Ask Command",
            border_style="panel.border",
            title_align="left"
        ),
        Panel(
            f"[bold]chat [cyan][--id SESSION_ID][/cyan] [cyan]<optional initial prompt>[/cyan][/]\n"
            f"Start an interactive conversation with Gemini LLM\n"
            f"[dim]Example: cllm chat[/]\n"
            f"[dim]Example: cllm chat --id project1 \"Let's discuss a Python project\"[/]",
            title=f"{ICONS['ask']} Chat Command",
            border_style="cyan"
        ),
    ]
    
    console.print(*commands)
    
if __name__ == "__main__":
    app()
