# cl_tasks/commands/complete.py

import typer
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from cl_tasks.storage import get_store

def main(task_id: int):
    """Mark a task as complete.
    
    Args:
        task_id: The ID of the task to mark as complete
    """
    console = Console()
    store = get_store()
    
    with console.status(f"[bold blue]Marking task #{task_id} as complete...[/]"):
        success = store.complete_task(task_id)

    if success:
        # Create a nicely formatted success message
        message = Text.assemble(
            "🎉 Task ", 
            Text(f"#{task_id}", style="bold cyan"),
            " marked as ",
            Text("complete", style="bold green"),
            "!"
        )
        
        # Display in a nice panel
        panel = Panel(
            message,
            title="[bold green]Task Completed[/]",
            border_style="green"
        )
        console.print(panel)
    else:
        # Error message in a different colored panel
        message = Text(f"⚠️ Task with ID #{task_id} not found.", style="yellow")
        panel = Panel(
            message,
            title="[bold yellow]Task Not Found[/]",
            border_style="yellow"
        )
        console.print(panel)
