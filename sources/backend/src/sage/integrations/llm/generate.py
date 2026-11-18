"""Text generation via Vertex AI (Gemini)."""

from google.genai import types

from sage.config import get_app_config
from sage.integrations.llm.client import get_genai_client


async def generate_text(prompt: str, system_instruction: str | None = None) -> str:
    config = get_app_config()
    client = get_genai_client()
    gen_config = (
        types.GenerateContentConfig(system_instruction=system_instruction)
        if system_instruction
        else None
    )
    response = await client.aio.models.generate_content(
        model=config.chat_model,
        contents=prompt,
        config=gen_config,
    )
    return response.text or "" 