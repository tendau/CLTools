"""
Utility functions and shared components for the CLLM application.
"""

import os
import re
from pathlib import Path
from dotenv import load_dotenv

from rich.console import Console, Group
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.rule import Rule

# Import theme elements
from cl_llm import tools
from cl_llm.theme import ICONS, CL_THEME, console


def load_api_key():
    """Load the Google API key from .env file in user's home directory."""
    load_dotenv()
    home_env = os.path.join(Path.home(), '.env')
    if os.path.exists(home_env):
        load_dotenv(home_env)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print(
            Panel(
                f"GOOGLE_API_KEY not found in environment variables or .env file.\n"
                f"Please set your Google API key by creating a .env file in your home directory with:\n"
                f"[bold]GOOGLE_API_KEY=your_api_key_here[/]",
                title=f"{ICONS['error']} API Key Missing",
                border_style="error",
                padding=(1, 2),
            )
        )
        return None
    return api_key


def format_llm_response(response_text: str) -> Panel:
    """Format an LLM response as a rich panel."""
    code_block_match = re.search(r"```(?:\w+)?\n(.*?)```", response_text, re.DOTALL)
    if code_block_match:
        code = code_block_match.group(1).strip()
        syntax = Syntax(code, "python", theme="monokai", line_numbers=False)
        return Panel(
            syntax,
            title=f"{ICONS['success']} Gemini Response (code)",
            border_style="panel.border",
            padding=(1, 2),
        )
    else:
        md = Markdown(response_text)
        return Panel(
            md,
            title=f"{ICONS['success']} Gemini Response",
            border_style="panel.border",
            padding=(1, 2),
        )


def stream_llm_response(response, service, panel_fn=None, initial_panel=None):
    """Stream an LLM response in the console, handling function calls and displaying output."""

    def handle_stream(response, live):
        response_text = ""
        tools_called = []
        function_call = None
        has_received_chunk = False

        if initial_panel:
            live.update(initial_panel)
        else:
            spinner = Spinner("dots", text="Processing...", style="llm.thinking")
            live.update(
                Panel(
                    spinner,
                    title=f"{ICONS['loading']} Gemini is thinking...",
                    border_style="secondary",
                    padding=(1, 2),
                )
            )

        for chunk in response:
            if not has_received_chunk:
                has_received_chunk = True

            content_parts = (
                chunk.candidates[0].content.parts if chunk.candidates[0].content.parts else []
            )

            for part in content_parts:
                if hasattr(part, "function_call") and part.function_call:
                    function_call = part.function_call
                elif hasattr(part, "text") and part.text:
                    response_text += part.text
                    if panel_fn:
                        live.update(panel_fn(response_text))
                    else:
                        # Use Group for spinner + markdown for smooth, clean live updates
                        spinner = Spinner("dots", text="Gemini is thinking...", style="llm.thinking")
                        group = Group(
                            spinner,
                            Markdown(response_text, code_theme="monokai"),
                        )
                        live.update(
                            Panel(
                                group,
                                title=f"{ICONS['loading']} Gemini Response",
                                border_style="accent",
                                padding=(1, 2),
                            )
                        )

        if function_call:
            live.update(
                Panel(
                    Spinner("dots", text="Calling function..."),
                    title="Gemini Response",
                    border_style="accent",
                    padding=(1, 2),
                )
            )
            tool_response = tools.call_tool(
                {
                    "tool_name": function_call.name,
                    "arguments": function_call.args,
                }
            )
            tools_called.append(
                {
                    "tool_name": function_call.name,
                    "function_response": tool_response,
                }
            )

        return tools_called, response_text

    with Live(
        initial_panel
        if initial_panel
        else Panel(
            Spinner("dots", text="Waiting for response..."),
            title="Gemini Response",
            border_style="accent",
            padding=(1, 2),
        ),
        refresh_per_second=8,
        console=console,
    ) as live:
        current_response = response
        final_text = ""

        while True:
            tools_called, text_output = handle_stream(current_response, live)
            final_text += text_output

            if tools_called:
                current_response = service.send_function_response(tools_called)
            else:
                break

    # --- Post-processing for clean copy-friendly output ---

    # Extract all code blocks
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", final_text, re.DOTALL)

    # Print main text nicely
    console.print()

    # Print code blocks with syntax highlighting and dividers
    for i, code in enumerate(code_blocks, start=1):
        console.print(Rule(title=f"Code Block #{i}", style="accent"))
        syntax = Syntax(code.strip(), "python", theme="monokai", line_numbers=False)
        console.print(syntax)
        console.print()

    return final_text
