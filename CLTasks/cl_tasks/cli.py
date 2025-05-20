# cl_tasks/cli.py
import typer
from typing import Optional
from rich import print as rprint
from rich.panel import Panel
from rich.columns import Columns
from cl_tasks.commands import add, list, complete, delete, show, reorder, start, pause  # Import the pause command
from cl_tasks.utils import console
from cl_tasks.theme import ICONS


app = typer.Typer(
    help="✨ CLTasks - A friendly task management CLI ✨",
    add_completion=False,
    rich_markup_mode="rich"
)


@app.callback()
def callback():
    """
    ✨ CLTasks - Manage your tasks with style! ✨
    
    A simple yet powerful CLI task manager.
    """
    pass


app.command("add", help="Add a new task")(add.main)
app.command("start", help="Start a task")(start.main)  # Alias for start
app.command("list", help="List all tasks")(list.main)
app.command("complete", help="Mark a task as complete")(complete.main)
app.command("delete", help="Delete a task")(delete.main)
app.command("show", help="Show details for a task")(show.main)
app.command("reorder", help="Reorder a task to change its priority")(reorder.main)
app.command("pause", help="Pause a running task")(pause.main)  # Add pause command


@app.command("help")
def help_cmd():
    """Show help information with command examples"""
    console.print("[bold blue underline]CLTasks Help[/]")
    console.print("\nAvailable commands:")
    
    commands = [
        Panel(
            "[bold]add [cyan]<title>[/cyan] [yellow]--position <pos>[/yellow][/]\n"
            "Add a new task\n"
            "[dim]Example: cltasks add \"Buy milk\"[/]\n"
            "[dim]Example: cltasks add \"Priority task\" --position 1[/]",
            title="Add Task",
            border_style="green"
        ),
        Panel(
            "[bold]start [cyan]<id>[/cyan][/]\n"
            "Start a task\n"
            "[dim]Example: cltasks start 1[/]",
            title="Start Task",
            border_style="yellow"
        ),
        Panel(
            "[bold]list [cyan]--all[/cyan][/]\n"
            "List all tasks\n"
            "[dim]Example: cltasks list[/]\n"
            "[dim]Example: cltasks list --all[/]",
            title="List Tasks",
            border_style="blue" 
        ),
        Panel(
            "[bold]show [cyan]<id>[/cyan][/]\n"
            "Show details for a task\n"
            "[dim]Example: cltasks show 1[/]",
            title="Show Task",
            border_style="cyan"
        ),
        Panel(
            "[bold]complete [cyan]<id>[/cyan][/]\n"
            "Mark a task as complete\n"
            "[dim]Example: cltasks complete 1[/]",
            title="Complete Task",
            border_style="green"
        ),
        Panel(
            "[bold]delete [cyan]<id>[/cyan] [yellow]--force[/yellow][/]\n"
            "Delete a task\n"
            "[dim]Example: cltasks delete 2[/]\n"
            "[dim]Example: cltasks delete 3 --force[/]",
            title="Delete Task",
            border_style="red"
        ),
        Panel(
            "[bold]reorder [cyan]<id> <position>[/cyan][/]\n"
            "Change task priority\n"
            "[dim]Example: cltasks reorder 3 1[/]",
            title="Reorder Task",
            border_style="magenta"
        ),
        Panel(
            "[bold]pause [cyan]<id>[/cyan][/]\n"
            "Pause a running task\n"
            "[dim]Example: cltasks pause 1[/]",
            title="Pause Task",
            border_style="yellow"
        )
    ]
    
    console.print(Columns(commands))


def show_app_info():
    """Show application info and version."""
    console.print("[bold blue]CLTasks[/bold blue] [dim]v0.1.0[/dim]")
    console.print("✨ [italic]Your friendly task manager[/italic] ✨")


if __name__ == "__main__":
    show_app_info()
