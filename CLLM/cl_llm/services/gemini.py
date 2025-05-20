# cl_llm/services/gemini.py
"""
Gemini LLM service for handling interactions with Google's Gemini API.
"""

from pathlib import Path
from google import genai
from google.genai import types
from typing import Optional
from cl_llm.theme import console, ICONS
from cl_llm.tools import get_user_profile, get_self_personality
from cl_llm.utils import load_api_key

get_user_profile_function_declaration = {
    "name": "get_user_profile",
    "description": "Returns all known facts and mannerisms about the user. Call this before updating user information to avoid repetition.",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

update_user_function_declaration = {
    "name": "update_user",
    "description": (
        "Use this function to update your internal understanding of the user. "
        "Trigger this when the user reveals personal facts (e.g., 'My name is Sam', 'I hate meetings') "
        "or exhibits consistent behavior or communication style (e.g., 'sarcastic tone', 'formal language'). "
        "You may infer facts from context or patterns. These entries help future interactions feel more personal. "
        "Avoid submitting facts that are already known."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "entry_type": {
                "type": "string",
                "enum": ["fact", "mannerism"],
                "description": (
                    "'fact' is objective information (e.g., 'They work in finance', 'They are learning Rust'). "
                    "'mannerism' is about how they communicate (e.g., 'They speak formally', 'They use a lot of emojis')."
                )
            },
            "entry": {
                "type": "string",
                "description": (
                    "A single, clear sentence summarizing the observation. "
                    "Examples: 'They are from New York', 'They joke often', 'They dislike overly verbose answers'."
                )
            }
        },
        "required": ["entry_type", "entry"]
    }
}

update_self_personality_function_declaration = {
    "name": "update_self_personality",
    "description": (
        "Use this function to update your own personality traits or behavioral style. "
        "Call it when you decide to adapt how you interact based on what you’ve learned about the user. "
        "For example, if the user is sarcastic, you might adopt a wittier tone. "
        "If the user is very concise, you might choose to be more direct. "
        "These entries help guide how you behave in future conversations with this user. "
        "Avoid redundant entries—only submit new or significantly refined traits."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "trait": {
                "type": "string",
                "description": (
                    "A concise sentence describing how you intend to adjust your personality or tone. "
                    "For example: 'I will be more playful and informal', 'I will respond with bullet points', "
                    "'I will avoid making jokes', 'I will mirror the user’s poetic tone'."
                )
            }
        },
        "required": ["trait"]
    }
}

class GeminiService:
    """Service for interacting with Google's Gemini API."""
    
    def __init__(self, model_name: str = "gemini-pro"):
        """
        Initialize the Gemini service.
        
        Args:
            model_name: The name of the Gemini model to use
        """
        self.model_name = model_name
        self.chat = None
        self.api_key = load_api_key()
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        
    def ask(self, prompt: str) -> Optional[str]:
        """
        Send a prompt to Gemini and get a response.
        
        Args:
            prompt: The text prompt to send to the model
            
        Returns:
            The model's response text or None if there was an error
        """
        if not self.api_key:
            return None
            
        try:
            with console.status(f"[llm.thinking]{ICONS['thinking']} Thinking...", spinner="dots"):
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash-preview-04-17",
                    contents=[prompt],
                )
                
            if response.text:
                return response.text
            else:
                console.print(f"[error]{ICONS['error']} Error: Empty response from Gemini[/error]")
                return None
                
        except Exception as e:
            console.print(f"[error]{ICONS['error']} Error: {str(e)}[/error]")
            return None
            
    def send_chat_message(self, message: str) -> Optional[str]:
        """
        Send a chat message to Gemini and get a response.

        Args:
            history: A list of message dictionaries with 'role' and 'content' keys
            
        Returns:
            The model's response text or None if there was an error
        """
        if self.chat is None:
            profile = get_user_profile()
            template_file = "system_message.txt"
            template_path = Path(__file__).parent / template_file
            template = template_path.read_text()

            # Assume get_user_profile() returns a profile with 'facts' and 'mannerisms'
            # Assume get_self_personality() returns a list of personality strings

            profile = get_user_profile()
            self_traits = get_self_personality()

            formatted_prompt = template.format(
                user_facts="\n- " + "\n- ".join(profile["facts"]) if profile["facts"] else "None",
                user_mannerisms="\n- " + "\n- ".join(profile["mannerisms"]) if profile["mannerisms"] else "None",
                self_traits="\n- " + "\n- ".join(self_traits) if self_traits else "None"
            )

            tools = types.Tool(function_declarations=[update_user_function_declaration, get_user_profile_function_declaration, update_self_personality_function_declaration])
            config = types.GenerateContentConfig(tools=[tools], system_instruction=formatted_prompt)
            self.chat = self.client.chats.create(model="gemini-2.5-flash-preview-04-17", config=config)
        try:            
            response = self.chat.send_message_stream(message)

            return response
                
        except Exception as e:
            console.print(f"[error]{ICONS['error']} Error: {str(e)}[/error]")
            return None
        
    def send_function_response(self, tools_called: list[dict]) -> Optional[str]:
        """
        Send a function response to Gemini and get a response.

        Args:
            function_response: The function response to send

        Returns:
            The model's response text or None if there was an error
        """

        if self.chat is None:
            return None
        try:            
            parts = []
            for tool in tools_called:
                # Create a function response part
                function_response_part = types.Part.from_function_response(
                    name=tool["tool_name"],
                    response={"result": tool["function_response"]},
                )
                parts.append(function_response_part)

            response = self.chat.send_message_stream(parts)

            return response
                
        except Exception as e:
            console.print(f"[error]{ICONS['error']} Error: {str(e)}[/error]")
            return None