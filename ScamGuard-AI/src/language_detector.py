"""
Simple language handling module for ScamGuard AI.
Gemini can understand many Indian languages, so this module
adds language detection metadata and prepares the system for translation.
"""

import re


def detect_language(text: str) -> str:
    """
    Lightweight rule-based language detector.
    Returns probable language.
    """

    if re.search(r"[\u0900-\u097F]", text):
        return "Hindi"

    if re.search(r"[\u0C00-\u0C7F]", text):
        return "Telugu"

    if re.search(r"[\u0B80-\u0BFF]", text):
        return "Tamil"

    if re.search(r"[\u0C80-\u0CFF]", text):
        return "Kannada"

    if re.search(r"[\u0D00-\u0D7F]", text):
        return "Malayalam"

    return "English"


def prepare_message_for_analysis(text: str) -> dict:
    """
    Detect language and return analysis-ready message metadata.
    """

    language = detect_language(text)

    return {
        "original_message": text,
        "detected_language": language,
        "analysis_message": text,
    }