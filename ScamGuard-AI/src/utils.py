"""
Utility functions for ScamGuard AI
"""

import json
import re


def extract_json(text: str):
    """
    Extract and parse JSON from Gemini response.

    Handles:
    - plain JSON
    - ```json fenced output
    - extra text before/after JSON
    """

    if not text:
        raise ValueError("Empty response received from Gemini")

    text = text.strip()

    # Remove markdown code fences
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    # First try direct JSON parsing
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract first JSON object from text
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError(f"No JSON object found in response: {text}")

    json_text = match.group(0)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from Gemini response. Error: {e}. Response: {text}"
        )