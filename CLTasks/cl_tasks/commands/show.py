# cl_tasks/commands/show.py

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from cl_tasks.storage import get_store
from cl_tasks.utils import create_task_panel, show_error

def main(task_id: int = typer.Argument(..., help="ID of the task to show")):
    """Show detailed information about a specific task.
    
    Args:
        task_id: The ID of the task to show
    """
    console = Console()
    store = get_store()
    tasks = store.list_tasks()
    
    # Find the task
    task = None
    for t in tasks:
        if t["id"] == task_id:
            task = t
            break
    
    if not task:
        show_error(
            f"Task with ID #{task_id} not found.", 
            title="[bold red]Task Not Found[/]"
        )
        raise typer.Exit(1)
    
    # Show task details in a nice panel
    panel = create_task_panel(
        task, 
        title=f"Task #{task_id} Details",
        border_style="blue"
    )
    console.print(panel)
