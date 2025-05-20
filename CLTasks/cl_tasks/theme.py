# cl_tasks/theme.py
"""
Theme definitions and visual elements for the CLTasks application.
This module defines the visual elements and styling used throughout the app.
"""

from rich.theme import Theme
from rich.style import Style
from rich.text import Text
from rich.console import Console

# Create emoji icons for consistent usage
ICONS = {
    "add": "➕",
    "list": "📋",
    "start": "▶️",
    "complete": "✅",
    "delete": "🗑️", 
    "show": "🔍",
    "pending": "📝",
    "error": "⚠️",
    "success": "🎉",
    "info": "ℹ️",
    "warning": "⚠️",
    "help": "❓",
}

# Define the application theme and common styles
CL_THEME = Theme({
    # Base color palette
    "primary": "bold blue",
    "secondary": "cyan",
    "success": "green",
    "warning": "yellow",
    "danger": "red",
    "info": "blue",
    "muted": "dim",
    
    # Task states
    "task.id": "cyan",
    "task.title": "white",
    "task.completed": "green",
    "task.pending": "yellow",
    "task.error": "red",
    "task.success": "green",
    "task.duration": "dim",
    
    # UI Elements
    "panel.border": "blue",
    "table.header": "bold blue",
    "table.row": "white",
    "table.row.even": "white",
    "table.row.odd": "bright_black",
    "heading": "bold blue underline",
})
