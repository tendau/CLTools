# cl_llm/commands/chat.py
"""
Implementation of the 'chat' command for the CLLM CLI.
This allows for interactive conversations with the LLM.
"""

import typer
from typing import Optional, List
from cl_llm.services.gemini import GeminiService
from cl_llm.theme import console, ICONS, create_user_message, create_header, create_system_message, create_llm_message
from cl_llm.utils import format_llm_response, stream_llm_response
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style as PTStyle


def main(
    chat_id: str = typer.Option("default", "--id", "-i", help="Chat session ID to continue an existing conversation"),
    initial_prompt: Optional[List[str]] = typer.Argument(None, help="Optional initial prompt to start the conversation")
):
    """
    Start an interactive chat session with the Gemini LLM.

    Args:
        chat_id: Identifier for the chat session
        initial_prompt: Optional starting prompt for the conversation
    """

    # Create custom key bindings for multiline input
    bindings = KeyBindings()

    @bindings.add("enter")
    def _(event):
        buffer = event.app.current_buffer
        if buffer.document.is_cursor_at_the_end and buffer.text.strip() != "":
            # Submit input
            event.app.exit(result=buffer.text)
        else:
            # Insert newline
            buffer.insert_text("\n")

    # Create a prompt session with custom key bindings
    session = PromptSession(
        multiline=True, 
        key_bindings=bindings,
        style=PTStyle.from_dict({
            'prompt': '#27AE60 bold',
        }),
        include_default_pygments_style=False,
        enable_history_search=False,
        prompt_continuation=None,
        refresh_interval=0
    )

    # Create LLM service
    service = GeminiService()
    
    # Show welcome header
    console.print(create_header(f"CLLM Chat Session: {chat_id}", "Interactive conversation with Gemini"))
    console.print(create_system_message("👋 Welcome to CLLM Chat! Type your messages and press Enter to send. Use Shift+Enter for a new line. Type 'exit' or press Ctrl+D to end the conversation."))
    # Add a little spacing for visual comfort
    console.print("")

    # Process initial prompt if provided
    if initial_prompt:
        initial_text = " ".join(initial_prompt)
        # Only show the user message in the chat bubble, not twice
        console.print(create_user_message(initial_text))
        response = service.send_chat_message(initial_text)
        thinking_panel = create_llm_message("[dim]Gemma is thinking...[/]")
        stream_llm_response(response, service, panel_fn=create_llm_message, initial_panel=thinking_panel)
        console.print("")

    # Begin interactive chat loop
    while True:
        try:
            prompt_text = f"{ICONS['user']} You: "
            # Read user input, then clear the line manually after printing the bubble
            user_input = session.prompt(prompt_text)
        except (KeyboardInterrupt, EOFError):
            console.print("")
            console.print(create_system_message("👋 Chat session ended. Goodbye!"))
            break

        if user_input.lower().strip() in ["exit", "quit", "q"]:
            console.print("")
            console.print(create_system_message(f"👋 Chat session '{chat_id}' ended. Goodbye!"))
            break

        if user_input.strip() == "":
            continue
        
        # Clear the previous input line from the terminal to avoid duplicate echo
        try:
            from rich.console import Console
            import sys
            # Move cursor up one line and clear it
            sys.stdout.write('\x1b[1A\x1b[2K')
            sys.stdout.flush()
        except Exception:
            pass
        # Display the user message in stylized format
        console.print(create_user_message(user_input))
        # Show Gemini is thinking in the Gemini chat bubble
        thinking_panel = create_llm_message("Gemma is thinking...")
        response = service.send_chat_message(user_input)
        stream_llm_response(response, service, panel_fn=create_llm_message, initial_panel=thinking_panel)
        # Add a little spacing after each response
        console.print("")


if __name__ == "__main__":
    # Run the chat command
    typer.run(main)
