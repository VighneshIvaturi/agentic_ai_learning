"""
Extract URLs from message text.
"""

import re
from typing import List


URL_PATTERN = r"(https?://[^\s]+|www\.[^\s]+)"


def extract_urls(text: str) -> List[str]:
    """
    Extract all URLs from a given text message.
    """

    if not text:
        return []

    urls = re.findall(URL_PATTERN, text)

    cleaned_urls = [
        url.strip(".,!?;:)")
        for url in urls
    ]

    return cleaned_urls