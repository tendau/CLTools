# cl_tasks/commands/reorder.py

import typer
from rich.text import Text
from cl_tasks.storage import get_store
from cl_tasks.utils import console, show_error, show_success
from cl_tasks.theme import ICONS

def main(
    task_id: int = typer.Argument(..., help="ID of the task to reorder"),
    position: int = typer.Argument(..., help="New position for the task (1-based)")
):
    """Reorder a task to change its priority.
    
    Args:
        task_id: The ID of the task to reorder
        position: New position for the task (1-based)
    """
    store = get_store()
    
    # Validate inputs
    if position < 1:
        show_error(
            "Position must be 1 or greater.",
            title=f"[bold red]{ICONS['error']} Invalid Position[/]"
        )
        raise typer.Exit(1)
    
    # First confirm we have the task
    tasks = store.list_tasks()
    task_exists = any(task["id"] == task_id for task in tasks)
    
    if not task_exists:
        show_error(
            f"Task with ID #{task_id} not found.", 
            title=f"[bold red]{ICONS['error']} Task Not Found[/]"
        )
        raise typer.Exit(1)
    
    # Get current position for better UX
    current_position = next(i+1 for i, task in enumerate(tasks) if task["id"] == task_id)
    task_title = next(task["title"] for task in tasks if task["id"] == task_id)
    
    # Check if the task is already at the requested position
    if current_position == position:
        show_error(
            f"Task #{task_id} is already at position {position}.",
            title=f"[bold yellow]{ICONS['warning']} No Change Needed[/]"
        )
        return
    
    # Proceed with reordering
    direction = "down" if position > current_position else "up"
    with console.status(f"[bold blue]Moving task #{task_id} {direction} to position {position}...[/]"):
        success = store.reorder_task(task_id, position)

    if success:
        # Handle case where position was beyond list length
        final_position = position
        if position > len(tasks):
            final_position = len(tasks)
            
        show_success(
            Text.assemble(
                f"{ICONS['list']} Task ", 
                Text(f"#{task_id}", style="cyan"),
                f" ({task_title}) moved from position ",
                Text(f"{current_position}", style="yellow"),
                " to position ",
                Text(f"{final_position}", style="green")
            ),
            title="[bold green]Task Reordered[/]"
        )
    else:
        # This should never happen given our earlier check, but just in case
        show_error(
            f"Failed to reorder task #{task_id}.", 
            title=f"[bold red]{ICONS['error']} Reorder Failed[/]"
        )
