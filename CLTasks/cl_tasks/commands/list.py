# cl_tasks/commands/list.py

import typer
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import Box, ROUNDED
from cl_tasks.storage import get_store
from cl_tasks.utils import console, format_task_row, display_task_stats
from cl_tasks.theme import ICONS

def main(
    all: bool = typer.Option(False, "--all", "-a", help="Show completed tasks too"),
    stats: bool = typer.Option(False, "--stats", "-s", help="Show task statistics")
):
    """List all your tasks.
    
    By default, shows only uncompleted tasks.
    """
    store = get_store()
    
    with console.status(f"[bold blue]{ICONS['list']} Loading tasks...[/]"):
        tasks = store.list_tasks()
    
    # Keep the original list for stats
    all_tasks = tasks.copy()
    
    # Filter tasks based on the 'all' flag
    if not all:
        tasks = [task for task in tasks if not task["completed"]]
    
    # Sort tasks: incomplete first, then by ID
    tasks = sorted(tasks, key=lambda x: (x["completed"], x["id"]))
    
    if not tasks:
        console.print(Panel(
            f"[italic]No tasks found. Add some tasks with '{ICONS['add']} add' command![/italic]",
            title=f"[bold blue]{ICONS['list']} Tasks[/]",
            border_style="blue"
        ))
        return
    
    # Count completed and total tasks
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    
    # Create a beautiful table with rounded corners
    table = Table(
        title=f"{ICONS['list']} Your Tasks ({completed_tasks}/{total_tasks} completed)",
        box=ROUNDED,
        highlight=True,
        show_header=True,
        header_style="table.header"
    )
    
    # Add columns with better styling
    table.add_column("#", style="secondary", justify="center")
    table.add_column("Task", style="task.title", no_wrap=False)
    table.add_column("Status", style="task.completed", justify="center")
    table.add_column("Duration", style="task.duration", justify="center")

      # Add rows with different styles for completed/incomplete tasks
    for i, task in enumerate(tasks):
        task_row = format_task_row(task)
        # Use different styles for odd/even rows but respect completion status
        if task["completed"]:
            row_style = "dim"
        else:
            row_style = "table.row.even" if i % 2 == 0 else "table.row.odd"
        table.add_row(task_row[0], task_row[1], task_row[2], task_row[3], style=row_style)

    console.print(table)
    
    # Show statistics if requested
    if stats:
        display_task_stats(all_tasks)
    
    # Add helpful tips footer
    if all:
        tip_text = f"{ICONS['info']} [dim]Tip: Use '{ICONS['complete']} complete <id>' to mark a task as done[/dim]"
    else:
        tip_text = f"{ICONS['info']} [dim]Tip: Use '--all' to show completed tasks too[/dim]"
    
    console.print(tip_text)
