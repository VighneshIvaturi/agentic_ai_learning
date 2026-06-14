"""
Risk scoring engine for ScamGuard AI.
Combines LLM risk score and URL tool risk.
"""


def combine_risk_scores(llm_score: int, url_results: list) -> int:
    """
    Combine Gemini risk score with URL checker risk score.
    """

    if not url_results:
        return llm_score

    max_url_score = max(
        result["risk_score"]
        for result in url_results
    )

    final_score = max(llm_score, max_url_score)

    if any(result["is_suspicious"] for result in url_results):
        final_score = min(final_score + 10, 100)

    return final_score


def summarize_url_risks(url_results: list) -> str:
    """
    Create readable summary of URL risk signals.
    """

    if not url_results:
        return "No URLs found in the message."

    summaries = []

    for result in url_results:
        if result["risk_signals"]:
            signals = "; ".join(result["risk_signals"])
        else:
            signals = "No major suspicious URL signals found."

        summaries.append(
            f"{result['url']} -> Risk {result['risk_score']}/100. {signals}"
        )

    return " | ".join(summaries)