import typer
from rich.console import Console
from rich.panel import Panel
from cl_tasks.storage import get_store
from cl_tasks.theme import ICONS

def main(
    task_id: int = typer.Argument(..., help="ID of the task to pause")
):
    """Pause a running task.

    Args:
        task_id: The ID of the task to pause
    """
    console = Console()
    store = get_store()

    tasks = store.list_tasks()
    task_exists = any(task["id"] == task_id for task in tasks)

    if not task_exists:
        console.print(f"[bold red]{ICONS['error']} Task with ID #{task_id} does not exist.[/]")
        raise typer.Exit(1)

    with console.status(f"[bold yellow]{ICONS['pending']} Pausing task with ID #{task_id}...[/]"):
        success = store.pause_task(task_id)

    if success:
        console.print(Panel(
            f"[bold yellow]{ICONS['pending']} Task #{task_id} paused successfully.",
            title="[bold yellow]Task Paused[/]",
            border_style="yellow"
        ))
    else:
        console.print(Panel(
            f"[bold red]{ICONS['error']} Failed to pause task #{task_id}. Ensure it is running.",
            title="[bold red]Pause Failed[/]",
            border_style="red"
        ))
