"""
Rule-based URL risk checker for ScamGuard AI.
This acts like a simple tool for the ReAct workflow.
"""

from urllib.parse import urlparse

from src.threat_intel import check_known_scam_domain


SUSPICIOUS_KEYWORDS = [
    "verify",
    "kyc",
    "login",
    "secure",
    "update",
    "reactivate",
    "claim",
    "reward",
    "free",
    "prize",
    "bank",
    "upi",
    "paytm",
    "sbi",
    "aadhaar",
]

SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".click",
    ".loan",
    ".win",
    ".tk",
]


def check_url_safety(url: str) -> dict:
    """
    Check URL for suspicious patterns and threat intelligence matches.
    """

    normalized_url = url.strip().lower()

    if normalized_url.startswith("www."):
        normalized_url = "http://" + normalized_url

    parsed = urlparse(normalized_url)
    domain = parsed.netloc

    risk_signals = []

    threat_result = check_known_scam_domain(url)

    if threat_result["is_known_scam_domain"]:
        risk_signals.append("Domain found in threat intelligence database")

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in normalized_url:
            risk_signals.append(f"Contains suspicious keyword: {keyword}")

    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            risk_signals.append(f"Uses suspicious domain extension: {tld}")

    if "-" in domain:
        risk_signals.append(
            "Domain contains hyphen, often used in impersonation URLs"
        )

    if len(domain) > 30:
        risk_signals.append("Domain name is unusually long")

    risk_score = min(len(risk_signals) * 20, 100)

    if threat_result["is_known_scam_domain"]:
        risk_score = 100

    return {
        "url": url,
        "domain": domain,
        "risk_score": risk_score,
        "risk_signals": risk_signals,
        "is_suspicious": risk_score >= 40,
        "is_known_scam_domain": threat_result["is_known_scam_domain"],
    }