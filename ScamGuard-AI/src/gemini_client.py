"""
Gemini client for ScamGuard AI using the new google-genai SDK
"""

from google import genai
from google.genai import types

from src.config import (
    GOOGLE_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
)


client = genai.Client(api_key=GOOGLE_API_KEY)


def generate_response(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns text response.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )

    if not response or not response.text:
        raise ValueError("Empty response received from Gemini")

    return response.text