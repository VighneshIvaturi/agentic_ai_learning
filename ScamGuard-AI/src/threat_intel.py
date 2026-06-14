"""
Threat intelligence lookup for ScamGuard AI.
"""

import json
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parent.parent
THREAT_DB_PATH = PROJECT_ROOT / "data" / "threat_database.json"


def load_threat_database() -> dict:
    if not THREAT_DB_PATH.exists():
        raise FileNotFoundError(f"Threat database not found at: {THREAT_DB_PATH}")

    with open(THREAT_DB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_domain(url: str) -> str:
    url = url.strip().lower()

    if url.startswith("www."):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc.replace("www.", "")

    return domain


def check_known_scam_domain(url: str) -> dict:
    threat_db = load_threat_database()

    domain = normalize_domain(url)

    known_domains = [
        d.strip().lower().replace("www.", "")
        for d in threat_db.get("known_scam_domains", [])
    ]

    return {
        "domain": domain,
        "is_known_scam_domain": domain in known_domains,
        "known_domains_loaded": known_domains,
    }


def check_known_scam_keywords(message: str) -> dict:
    threat_db = load_threat_database()
    message_lower = message.lower()

    matched_keywords = []

    for keyword in threat_db.get("known_scam_keywords", []):
        if keyword.lower() in message_lower:
            matched_keywords.append(keyword)

    return {
        "matched_keywords": matched_keywords,
        "has_known_scam_pattern": len(matched_keywords) > 0,
    }