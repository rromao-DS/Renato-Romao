import os

from google import genai
from google.genai import types

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_reply(history: list[dict], system: str, tools: list | None = None) -> str:
    """Chama Gemini generate_content. tools=None hoje; preparado pra function calling depois."""
    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=1024,
        tools=tools,  # None hoje
    )
    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=history,
        config=config,
    )
    # TODO: handle function_call parts quando tools for usado
    return (response.text or "").strip()
