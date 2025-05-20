# cl_llm/cli.py
"""
Main CLI entry point for CLLM application.
"""

import typer
from typing import Optional
from rich import print as rprint
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from cl_llm.theme import ICONS, console, create_header, create_system_message, create_divider, create_chat_header
from cl_llm.commands import ask, chat

app = typer.Typer(
    help=f"{ICONS['gem']} CLLM - An elegant CLI for interacting with Gemini LLM {ICONS['gem']}",
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
        console.print(create_header(f"Welcome to CLLM {ICONS['star']}", "Your elegant terminal gateway to Gemini LLM"))
        
        # Create a beautiful command table
        table = Table(show_header=True, header_style="bold gradient.1", border_style="gradient.3")
        table.add_column("Command", style="gradient.2")
        table.add_column("Description", style="gradient.3")
        table.add_column("Example", style="gradient.4")
        
        table.add_row(
            f"{ICONS['ask']} ask", 
            "Ask a one-time question", 
            "cllm ask \"What is quantum computing?\""
        )
        table.add_row(
            f"{ICONS['chat']} chat", 
            "Start an interactive conversation", 
            "cllm chat --id myproject"
        )
        table.add_row(
            f"{ICONS['help']} help", 
            "Show detailed help information", 
            "cllm help"
        )
        
        console.print(Panel(table, border_style="gradient.2", padding=(1, 2)))
        console.print(create_divider())

# Register commands
app.command("ask", help=f"{ICONS['ask']} Ask a question to Gemini LLM")(ask.main)
app.command("chat", help=f"{ICONS['chat']} Start a conversation with Gemini LLM")(chat.main)

@app.command("help")
def help_cmd():
    """Show help information with command examples"""
    console.print(create_header(f"CLLM Help {ICONS['help']}", "Available commands and examples"))
    console.print(create_divider())
    
    # Create a beautiful, more detailed command table
    table = Table(show_header=True, header_style="bold gradient.1", border_style="gradient.3", width=100)
    table.add_column("Command", style="gradient.2", width=20)
    table.add_column("Description", style="gradient.3")
    table.add_column("Example", style="gradient.4")
    
    table.add_row(
        f"{ICONS['ask']} ask <prompt>", 
        "Ask a one-time question or provide a prompt to get a single response from Gemini.", 
        "cllm ask \"What are the benefits of quantum computing?\""
    )
    table.add_row(
        f"{ICONS['chat']} chat [--id SESSION_ID]", 
        "Start an interactive conversation with Gemini. Optionally specify a session ID to continue a previous conversation.", 
        "cllm chat --id project1 \"Let's discuss a Python project\""
    )
    table.add_row(
        f"{ICONS['help']} help", 
        "Display this help information with detailed command examples.", 
        "cllm help"
    )
    
    console.print(Panel(table, border_style="gradient.2", padding=(1, 2)))    console.print(create_system_message(
        f"CLLM is an elegant terminal interface for Google's Gemini LLM.\n"
        f"To get started, try a simple question with: cllm ask \"What is machine learning?\"\n"
        f"Or start a conversation with: cllm chat"
    ))
    console.print(create_divider())


if __name__ == "__main__":
    app()
            border_style="cyan"
        ),
    ]
    
    console.print(*commands)
    
if __name__ == "__main__":
    app()
