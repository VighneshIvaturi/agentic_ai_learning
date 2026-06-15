import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
import json
load_dotenv()
from app.prompts import (
    PRESCRIPTION_IMAGE_PROMPT,
    PRESCRIPTION_TEXT_PROMPT
)
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"
def clean_and_parse_json(response_text: str) -> dict:
    cleaned_text = response_text.strip()

    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text.replace("```json", "").replace("```", "").strip()

    elif cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.replace("```", "").strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse Gemini response as JSON",
            "raw_response": response_text
        }
def analyze_prescription_image(image_path: str) -> dict:
    image = Image.open(image_path)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                PRESCRIPTION_IMAGE_PROMPT,
                image
            ]
        )

        return clean_and_parse_json(response.text)

    except Exception as e:
        return {
            "error": "Failed to analyze prescription image",
            "error_details": str(e)
        }


def analyze_prescription_text(prescription_text: str) -> dict:
    prompt = f"""
{PRESCRIPTION_TEXT_PROMPT}

Prescription text:
{prescription_text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return clean_and_parse_json(response.text)

    except Exception as e:
        return {
            "error": "Failed to analyze prescription text",
            "error_details": str(e)
        }