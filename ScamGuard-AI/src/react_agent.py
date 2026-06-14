"""
True ReAct-style agent for ScamGuard AI.
Uses language detection, URL extraction, threat intelligence,
URL safety checking, LLM analysis, and final risk scoring.
"""

from src.scam_analyzer import analyze_message
from src.url_extractor import extract_urls
from src.url_checker import check_url_safety
from src.risk_engine import combine_risk_scores, summarize_url_risks
from src.schemas import ScamAnalysis
from src.threat_intel import check_known_scam_keywords
from src.language_detector import prepare_message_for_analysis


def analyze_with_tools(message: str) -> dict:
    """
    Analyze message using LLM + language detection + URL tool layer.
    """

    language_info = prepare_message_for_analysis(message)
    analysis_message = language_info["analysis_message"]

    urls = extract_urls(analysis_message)

    keyword_threats = check_known_scam_keywords(analysis_message)

    url_results = [
        check_url_safety(url)
        for url in urls
    ]

    llm_result: ScamAnalysis = analyze_message(
        message=analysis_message,
        mode="react"
    )

    final_risk_score = combine_risk_scores(
        llm_result.risk_score,
        url_results
    )

    url_summary = summarize_url_risks(url_results)

    return {
        "original_message": language_info["original_message"],
        "detected_language": language_info["detected_language"],
        "classification": llm_result.classification,
        "intent_type": llm_result.intent_type,
        "llm_risk_score": llm_result.risk_score,
        "final_risk_score": final_risk_score,
        "reason": llm_result.reason,
        "safe_action": llm_result.safe_action,
        "urls_found": urls,
        "url_analysis": url_results,
        "url_summary": url_summary,
        "threat_keyword_matches": keyword_threats["matched_keywords"],
        "known_scam_pattern": keyword_threats["has_known_scam_pattern"],
    }