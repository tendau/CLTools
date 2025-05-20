import typer
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from cl_tasks.storage import get_store
from cl_tasks.theme import ICONS

def main(
    title: str = typer.Argument(..., help="Title of the task to add"),
    position: int = typer.Option(None, "--position", "-p", help="Position to insert task at (1-based)")
):
    """Add a new task to your list.
    
    Args:
        title: The title of the task to add
        position: Optional position to insert the task at (1-based)
    """
    console = Console()
    store = get_store()
    
    # Validate position if provided
    if position is not None and position < 1:
        console.print("[bold red]Position must be 1 or greater.[/]")
        raise typer.Exit(1)
    
    position_msg = f" at position {position}" if position else ""
    with console.status(f"[bold green]Adding task{position_msg}...[/]"):
        task = store.add_task(title, position)
    
    # Create a nicely formatted success message
    task_id_text = Text(f"#{task['id']}", style="bold cyan")
    title_text = Text(f" {task['title']}", style="bold white")
    message = Text.assemble(
        "✅ Added task: ", 
        task_id_text,
        title_text
    )
    
    # Display in a nice panel
    panel = Panel(
        message,
        title="[bold green]Task Added[/]",
        border_style="green"
    )
    console.print(panel)
