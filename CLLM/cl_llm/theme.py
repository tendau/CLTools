# cl_llm/theme.py
"""
Theme definitions and visual elements for the CLLM application.
This module defines the visual elements and styling used throughout the app.
"""

from rich.theme import Theme
from rich.style import Style
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.markdown import Markdown

# Create emoji icons for consistent usage
ICONS = {
    "ask": "🔮",
    "thinking": "🧠",
    "success": "✨",
    "error": "⚠️",
    "info": "ℹ️",
    "user": "🤷",
    "system": "🤖",
    "loading": "⏳",
    "exit": "🚪",
    "help": "❓",
    # Added 'llm' icon for LLM responses/indicators
    "llm": "✨",
}

# Define the application theme and common styles
CL_THEME = Theme({
    # Base color palette
    "primary": "bold #4B77BE",
    "secondary": "#9B59B6",
    "accent": "bold #3498DB",
    "success": "bold #2ECC71",
    "error": "bold #E74C3C",
    "warning": "bold #F39C12",
    "info": "bold #2980B9",
    
    # UI elements
    "heading": "bold #1ABC9C",
    "subheading": "italic #16A085",
    "prompt": "bold #27AE60",
    "user_input": "bold #F1C40F",
    
    # LLM output styling
    "llm.response": "#ECF0F1",
    "llm.code": "bold #2C3E50 on #ECF0F1",
    "llm.thinking": "italic #F39C12",
    "llm.error": "bold #E74C3C",
    
    # UI borders and panels
    "panel.border": "#3498DB",
    "panel.title": "bold #1ABC9C",
    "divider": "#7F8C8D",
})

# Create a shared console instance
console = Console(theme=CL_THEME, highlight=True)

# Helper functions for consistent UI elements
def create_header(title, subtitle=None):
    """Create a consistent header with optional subtitle."""
    header_text = Text()
    header_text.append(f"✨ {title} ✨\n", style="heading")
    if subtitle:
        header_text.append(f"{subtitle}", style="subheading")
    return Panel(header_text, border_style="panel.border", padding=(1, 2))

def create_user_message(message):
    """Format user messages as a right-aligned chat bubble with a modern blue/teal color."""
    return Panel(
        Text(message, style="bold #1ABC9C"),  # Teal/blue for user message
        title=f"{ICONS['user']} You",
        title_align="right",
        border_style="accent",
        padding=(1, 2),
        style="on #23272e",
        box=box.ROUNDED,
        subtitle="",
        subtitle_align="right"
    )

def create_system_message(message):
    """Format system messages as a left-aligned chat bubble with a double border and info color."""
    return Panel(
        Text(message, style="info"),
        title=f"{ICONS['system']} System",
        title_align="left",
        border_style="info",
        padding=(1, 1),
        style="on #1a2634",
        box=box.DOUBLE,
        subtitle="",
        subtitle_align="left"
    )

def create_llm_message(message):
    """Format LLM messages as a left-aligned bubble with Markdown/code support."""
    # Detect if message contains Markdown/code and render accordingly
    if '```' in message or '\n' in message:
        content = Markdown(message, code_theme="monokai")
    else:
        content = Text(message, style="llm.response")
    return Panel(
        content,
        title=f"{ICONS['llm']} Gemma",
        title_align="left",
        border_style="primary",
        padding=(1, 2),
        style="on #222b3a",
        box=box.HEAVY,
        subtitle="",
        subtitle_align="left"
    )

def create_divider():
    """Create a simple divider for separating sections."""
    return Text("─" * 80, style="divider")
