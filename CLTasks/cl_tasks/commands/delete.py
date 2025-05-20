import typer
from rich.panel import Panel  # Added import for Panel
from rich.text import Text
from cl_tasks.storage import get_store
from cl_tasks.utils import console, show_warning, show_success, show_error

def main(
    task_id: int = typer.Argument(..., help="ID of the task to delete"),
    force: bool = typer.Option(
        False, "--force", "-f", 
        help="Skip confirmation prompt"
    )
):
    """Delete a task from your list.
    
    Args:
        task_id: The ID of the task to delete
    """
    store = get_store()
    
    # First confirm we have the task
    tasks = store.list_tasks()
    task_exists = any(task["id"] == task_id for task in tasks)
    
    if not task_exists:
        show_error(
            f"Task with ID #{task_id} not found.", 
            title="[bold red]Task Not Found[/]"
        )
        raise typer.Exit(1)
    
    # Get the task title for better UX
    task_title = next(task["title"] for task in tasks if task["id"] == task_id)
    
    # Add confirmation unless force flag is used
    if not force:
        confirmed = typer.confirm(
            f"Are you sure you want to delete task #{task_id}: '{task_title}'?",
            default=False
        )
        if not confirmed:
            console.print("[yellow]Operation cancelled.[/yellow]")
            raise typer.Exit()
    
    # Proceed with deletion
    with console.status(f"[bold red]Deleting task #{task_id}...[/]"):
        success = store.delete_task(task_id)

    if success:
        show_success(
            Text.assemble(
                "🗑️  Task ", 
                Text(f"#{task_id}", style="bold cyan"),
                Text(" has been deleted", style="bold")
            ),
            title="[bold red]Task Deleted[/]"
        )
    else:
        # This should never happen given our earlier check, but just in case
        show_error(
            f"Task with ID #{task_id} not found.", 
            title="[bold red]Task Not Found[/]"
        )