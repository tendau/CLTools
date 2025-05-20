# cl_tasks/utils.py
"""
Utility functions and shared components for the CLTasks application.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from typing import Dict, Any, Optional

# Import theme elements
from cl_tasks.theme import ICONS, CL_THEME

# Create a shared console instance with our theme
console = Console(theme=CL_THEME)

def format_task_id(task_id: int) -> Text:
    """Format a task ID consistently with # prefix and cyan color."""
    return Text(f"#{task_id}", style="task.id")

def format_task_status(completed: bool) -> Text:
    """Format task status with appropriate icon and color."""
    if completed:
        return Text(f"{ICONS['complete']} Completed", style="task.completed")
    else:
        return Text(f"{ICONS['pending']} Pending", style="task.pending")

def create_task_panel(
    task: Dict[str, Any], 
    title: str = "Task Details",
    border_style: str = "blue"
) -> Panel:
    """Create a panel displaying task information.
    
    Args:
        task: The task dictionary
        title: The panel title
        border_style: The color for the panel border
        
    Returns:
        A rich Panel object
    """
    task_id = task["id"]
    task_title = task["title"]
    completed = task["completed"]
    
    # Format the task ID and status
    id_text = Text(f"#{task_id}", style="cyan")
    
    if completed:
        status_text = Text(f"{ICONS['complete']} Completed", style="green")
        title_style = "dim strike"
    else:
        status_text = Text(f"{ICONS['pending']} Pending", style="yellow")
        title_style = "white"
    
    # Assemble the text content
    content = Text()
    content.append("ID: ", style="dim")
    content.append(id_text)
    content.append("\nTitle: ", style="dim")
    content.append(task_title, style=title_style)
    content.append("\nStatus: ", style="dim")
    content.append(status_text)
    
    # Add creation timestamp if available
    if "created_at" in task:
        content.append("\nCreated: ", style="dim")
        content.append(task["created_at"], style="dim")
    
    return Panel(
        content,
        title=f"[bold blue]{title}[/bold blue]",
        border_style=border_style
    )

def show_success(message: str, title: Optional[str] = None) -> None:
    """Display a success message in a green panel.
    
    Args:
        message: The message to display
        title: Optional title for the panel
    """
    panel_title = title or f"[bold success]{ICONS['success']} Success![/bold success]"
    console.print(Panel(message, title=panel_title, border_style="success"))

def show_error(message: str, title: Optional[str] = None) -> None:
    """Display an error message in a red panel.
    
    Args:
        message: The message to display
        title: Optional title for the panel
    """
    panel_title = title or f"[bold danger]{ICONS['error']} Error[/bold danger]"
    console.print(Panel(message, title=panel_title, border_style="danger"))

def show_warning(message: str, title: Optional[str] = None) -> None:
    """Display a warning message in a yellow panel.
    
    Args:
        message: The message to display
        title: Optional title for the panel
    """
    panel_title = title or f"[bold warning]{ICONS['warning']} Warning[/bold warning]"
    console.print(Panel(message, title=panel_title, border_style="warning"))

def show_info(message: str, title: Optional[str] = None) -> None:
    """Display an info message in a blue panel.
    
    Args:
        message: The message to display
        title: Optional title for the panel
    """
    panel_title = title or f"[bold info]{ICONS['info']} Info[/bold info]"
    console.print(Panel(message, title=panel_title, border_style="info"))
    
    
def display_task_stats(tasks: list) -> None:
    """Display pretty statistics about tasks.
    
    Args:
        tasks: List of tasks to analyze
    """
    total = len(tasks)
    completed = sum(1 for task in tasks if task["completed"])
    pending = total - completed
    
    if total == 0:
        console.print("[dim]No tasks found. Add some tasks with the 'add' command![/dim]")
        return
    
    # Calculate completion percentage
    percent = int((completed / total) * 100) if total > 0 else 0
    
    console.print(f"\n[bold]Task Statistics[/bold]")
    console.print(f"Total Tasks: {total}")
    console.print(f"Completed: [green]{completed}[/green] | Pending: [yellow]{pending}[/yellow]")
    console.print(f"Progress: [bold]{percent}%[/bold] complete")
    
    # Optional: Add a simple ASCII progress bar
    bar_width = 30
    filled = int(bar_width * percent / 100)
    bar = "[" + "█" * filled + "·" * (bar_width - filled) + "]"
    console.print(bar, style="bold green")


def format_task_row(task: Dict[str, Any]) -> list:
    """Format a task for display in a table row.
    
    Args:
        task: The task dictionary
        
    Returns:
        List of formatted strings for table row
    """
    task_id = str(task["id"])
    title = task["title"]
    duration = task["duration"] if "duration" in task else "N/A"

    if task["completed"]:
        status_icon = ICONS["complete"]
        row_style = "dim"
        title = f"[strike]{title}[/strike]"
    elif "start_time" in task and task["start_time"] is not None:
        status_icon = ICONS["start"]
        row_style = "bold"
    else:
        status_icon = ICONS["pending"]
        row_style = ""

    return [task_id, title, status_icon, duration, row_style]