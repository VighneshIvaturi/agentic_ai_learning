from pathlib import Path

from src.gemini_client import generate_response
from src.utils import extract_json
from src.schemas import ScamAnalysis


PROMPT_DIR = Path("prompts")

SUPPORTED_MODES = {
    "zero_shot": "zero_shot.txt",
    "few_shot": "few_shot.txt",
    "cot": "cot_prompt.txt",
    "react": "react_prompt.txt",
}


def load_prompt(mode: str) -> str:
    if mode not in SUPPORTED_MODES:
        raise ValueError(
            f"Invalid mode '{mode}'. Use one of: {list(SUPPORTED_MODES.keys())}"
        )

    prompt_path = PROMPT_DIR / SUPPORTED_MODES[mode]

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")


def analyze_message(message: str, mode: str = "zero_shot") -> ScamAnalysis:
    prompt_template = load_prompt(mode)

    prompt = prompt_template.format(message=message)

    response = generate_response(prompt)

    json_response = extract_json(response)

    result = ScamAnalysis(**json_response)

    return result