from src.scam_analyzer import analyze_message


if __name__ == "__main__":

    message = input("Enter a message to analyze: ")

    print("\nChoose prompt mode:")
    print("1. Zero-shot")
    print("2. Few-shot")
    print("3. Chain-of-Thought")
    print("4. ReAct")

    choice = input("Enter choice: ").strip()

    if choice.startswith("2"):
        mode = "few_shot"
    elif choice.startswith("3"):
        mode = "cot"
    elif choice.startswith("4"):
        mode = "react"
    else:
        mode = "zero_shot"

    result = analyze_message(message, mode=mode)

    print("\n===== ScamGuard AI Result =====")
    print(f"Mode           : {mode}")
    print(f"Classification : {result.classification}")
    print(f"Intent Type    : {result.intent_type}")
    print(f"Risk Score     : {result.risk_score}/100")
    print(f"Reason         : {result.reason}")
    print(f"Safe Action    : {result.safe_action}")