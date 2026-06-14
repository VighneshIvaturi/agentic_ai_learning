import sys
import time
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.scam_analyzer import analyze_message


DATA_PATH = PROJECT_ROOT / "data" / "dataset.csv"
RESULTS_DIR = PROJECT_ROOT / "evaluation"


def normalize_label(label: str) -> str:
    label = str(label).strip().lower()

    if label in ["scam", "fraud"]:
        return "scam"

    if label in ["not_scam", "not scam", "not scam ", "legitimate"]:
        return "not_scam"

    return "uncertain"


def normalize_intent(intent: str) -> str:
    intent = str(intent).strip().lower()

    mapping = {
        "service reminder": "service reminder",
        "marketing message": "marketing message",
        "account update": "account update",
        "informational alert": "informational alert",
        "order confirmation": "order confirmation",
        "transactional notification": "transactional notification",
        "account suspension": "account suspension",
        "loan scam": "loan scam",
        "advance-fee loan scam": "loan scam",
        "advance fee loan scam": "loan scam",
        "fake authority": "fake authority",
        "urgency": "urgency",
        "fear tactics": "fear tactics",
        "reward manipulation": "reward manipulation",
        "phishing": "phishing",
        "otp fraud": "otp fraud",
        "otp scam": "otp fraud",
        "legitimate communication": "transactional notification",
    }

    return mapping.get(intent, intent)


def evaluate_dataframe(
    df: pd.DataFrame,
    mode: str = "zero_shot",
    sample_size: int | None = None,
    sleep_time: float = 0.5,
    progress_callback=None,
) -> dict:
    """
    Evaluate ScamGuard on a dataframe.

    Required columns:
    - message_text
    - label
    - intent_type
    """

    required_columns = ["message_text", "label", "intent_type"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    if sample_size:
        df = df.sample(sample_size, random_state=42)

    actual_labels = []
    predicted_labels = []
    actual_intents = []
    predicted_intents = []
    rows = []

    total = len(df)

    for count, (_, row) in enumerate(df.iterrows(), start=1):
        message = row["message_text"]
        actual_label = normalize_label(row["label"])
        actual_intent = normalize_intent(row["intent_type"])

        try:
            result = analyze_message(message, mode=mode)

            predicted_label = normalize_label(result.classification)
            predicted_intent = normalize_intent(result.intent_type)

            risk_score = result.risk_score
            reason = result.reason
            safe_action = result.safe_action
            error = ""

        except Exception as e:
            predicted_label = "error"
            predicted_intent = "error"
            risk_score = None
            reason = ""
            safe_action = ""
            error = str(e)

        actual_labels.append(actual_label)
        predicted_labels.append(predicted_label)
        actual_intents.append(actual_intent)
        predicted_intents.append(predicted_intent)

        rows.append({
            "message_text": message,
            "actual_label": actual_label,
            "predicted_label": predicted_label,
            "actual_intent": actual_intent,
            "predicted_intent": predicted_intent,
            "risk_score": risk_score,
            "reason": reason,
            "safe_action": safe_action,
            "error": error,
        })

        if progress_callback:
            progress_callback(count, total)

        if sleep_time:
            time.sleep(sleep_time)

    valid_actual_labels = []
    valid_predicted_labels = []
    valid_actual_intents = []
    valid_predicted_intents = []

    for actual_label, predicted_label, actual_intent, predicted_intent in zip(
        actual_labels,
        predicted_labels,
        actual_intents,
        predicted_intents,
    ):
        if predicted_label != "error":
            valid_actual_labels.append(actual_label)
            valid_predicted_labels.append(predicted_label)
            valid_actual_intents.append(actual_intent)
            valid_predicted_intents.append(predicted_intent)

    label_accuracy = accuracy_score(
        valid_actual_labels,
        valid_predicted_labels
    )

    precision, recall, f1, _ = precision_recall_fscore_support(
        valid_actual_labels,
        valid_predicted_labels,
        average="weighted",
        zero_division=0,
    )

    intent_accuracy = accuracy_score(
        valid_actual_intents,
        valid_predicted_intents
    )

    cm = confusion_matrix(
        valid_actual_labels,
        valid_predicted_labels,
        labels=["scam", "not_scam", "uncertain"],
    )

    error_count = predicted_labels.count("error")

    result_df = pd.DataFrame(rows)
    result_df["risk_score"] = pd.to_numeric(result_df["risk_score"],errors="coerce")

    return {
        "mode": mode,
        "total_samples": total,
        "valid_samples": len(valid_actual_labels),
        "errors": error_count,
        "label_accuracy": label_accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "intent_accuracy": intent_accuracy,
        "confusion_matrix": cm,
        "results_df": result_df,
    }


def evaluate(mode: str = "zero_shot", sample_size: int = 20):
    df = pd.read_csv(DATA_PATH)

    results = evaluate_dataframe(
        df=df,
        mode=mode,
        sample_size=sample_size,
        sleep_time=1,
    )

    print("\n===== ScamGuard AI Evaluation Results =====")
    print(f"Mode                : {results['mode']}")
    print(f"Total Samples        : {results['total_samples']}")
    print(f"Valid Samples        : {results['valid_samples']}")
    print(f"Errors               : {results['errors']}")
    print(f"Label Accuracy       : {results['label_accuracy']:.4f}")
    print(f"Precision            : {results['precision']:.4f}")
    print(f"Recall               : {results['recall']:.4f}")
    print(f"F1 Score             : {results['f1_score']:.4f}")
    print(f"Intent Accuracy      : {results['intent_accuracy']:.4f}")

    print("\nConfusion Matrix:")
    print(results["confusion_matrix"])

    output_path = RESULTS_DIR / f"results_{mode}.csv"
    results["results_df"].to_csv(output_path, index=False)

    print(f"\nSaved prediction details to: {output_path}")


if __name__ == "__main__":
    evaluate(mode="zero_shot", sample_size=20)