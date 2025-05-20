from cl_tasks.cli import app
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time
import sys

def show_splash_screen():
    console = Console()
    
    # Clear screen for better presentation
    console.clear()
    
    logo = """
    ╔═══╗╔╗   ╔════╗        ╔╗    
    ║╔══╝║║   ║╔╗╔╗║        ║║    
    ║╚══╗║║   ╚╝║║╚╝╔══╗╔══╗║║╔╗╔═══╗
    ║╔══╝║║     ║║  ║╔╗║║══╣║╚╝╝║╔═╗║
    ║║   ║╚═╗  ╔╝╚╗ ║╚╝║╠══║║╔╗╗║╚═╝║
    ╚╝   ╚══╝  ╚══╝ ╚══╝╚══╝╚╝╚╝╚═══╝
    """
    
    # Create a nice panel with the logo
    panel = Panel(
        Text(logo, style="bold blue"),
        subtitle="[dim]v0.1.0[/dim]",
        subtitle_align="right"
    )
    
    console.print(panel)
    console.print("[bold]✨ Your friendly task manager[/bold]")
    console.print("[dim]Loading...[/dim]")
    
    # Simple loading animation
    for i in range(5):
        console.print(".", end="", style="bold blue")
        time.sleep(0.1)
    console.print("\n")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        show_splash_screen()
    app()
