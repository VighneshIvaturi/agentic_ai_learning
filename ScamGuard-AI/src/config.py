"""
Configuration settings for ScamGuard AI
"""

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-1.5-flash"
)

TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 1024

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file"
    )