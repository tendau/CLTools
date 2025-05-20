# cl_llm/commands/ask.py
"""
Implementation of the 'ask' command for the CLLM CLI.
"""

import typer
from typing import List
from cl_llm.services.gemini import GeminiService
from cl_llm.theme import console, ICONS, create_user_message, create_header, create_divider
from cl_llm.utils import format_llm_response

def main(
    prompt: List[str] = typer.Argument(..., help="The prompt to send to the LLM model")
):
    """
    Ask a question to the Gemini LLM.
    
    Args:
        prompt: The text prompt to send to the model
    """
    # Join multiple arguments into a single prompt string
    prompt_text = " ".join(prompt)
    
    # Show welcome header
    console.print(create_header("CLLM Ask", "One-shot Q&A with Gemini"))
    console.print(create_divider())
    
    # Print a stylized version of the user's prompt
    console.print(create_user_message(prompt_text))
    
    # Create the service and get a response
    service = GeminiService()
    response_text = service.ask(prompt_text)
    
    # Display the formatted response if we got one
    if response_text:
        console.print(format_llm_response(response_text))
