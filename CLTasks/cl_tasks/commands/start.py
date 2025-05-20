import typer
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from cl_tasks.storage import get_store
from cl_tasks.theme import ICONS

def main(
    id: int = typer.Argument(..., help="ID of the task to start"),
):
    """Start a task in your list.

    Args:
        id: The ID of the task to start
    """
    console = Console()
    store = get_store()

    tasks = store.list_tasks()
    task_exists = any(task["id"] == id for task in tasks)

    if not task_exists:
        console.print(f"[bold red]Task with ID #{id} does not exist.[/]")
        raise typer.Exit(1)

    with console.status(f"[bold green]Starting task with ID #{id}...[/]"):
        success = store.start_task(id)

    if success:
        console.print(f"[bold green]Task with ID #{id} started successfully.[/]")
        message = Text.assemble(
            "✅ Started task: ", 
            Text(f"#{id}", style="bold cyan"),
            Text(" ", style="bold white"),
        )
    else:
        console.print(f"[bold red]Failed to start task with ID #{id}.[/]")
        

    # Display in a nice panel
    panel = Panel(
        message,
        title="[bold green]Task Started[/]",
        border_style="green"
    )
    console.print(panel)
