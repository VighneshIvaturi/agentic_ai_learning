"""
Feedback manager for ScamGuard AI.
Stores user corrections for future few-shot improvement.
"""

import csv
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEEDBACK_PATH = PROJECT_ROOT / "data" / "feedback.csv"


def save_feedback(
    message: str,
    predicted_label: str,
    predicted_intent: str,
    user_feedback: str,
    correct_label: str = "",
    correct_intent: str = "",
) -> None:
    """
    Save user feedback to feedback.csv.
    """

    file_exists = FEEDBACK_PATH.exists()

    with open(FEEDBACK_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "message",
                "predicted_label",
                "predicted_intent",
                "user_feedback",
                "correct_label",
                "correct_intent",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "message": message,
            "predicted_label": predicted_label,
            "predicted_intent": predicted_intent,
            "user_feedback": user_feedback,
            "correct_label": correct_label,
            "correct_intent": correct_intent,
        })