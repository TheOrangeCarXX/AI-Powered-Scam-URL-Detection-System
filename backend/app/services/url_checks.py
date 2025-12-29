import re
from urllib.parse import urlparse

SUSPICIOUS_TLDS = [
    ".xyz", ".tk", ".ml", ".cf", ".site", ".online", ".live"
]

URGENT_KEYWORDS = [
    "verify", "secure", "update", "refund", "alert", "kyc", "login"
]


def analyze_url(url: str) -> list[str]:
    flags = []

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # HTTPS check
    if not url.startswith("https://"):
        flags.append("Website does not use HTTPS")

    # Suspicious TLD check
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            flags.append("Suspicious top-level domain detected")

    # Urgency / phishing keywords
    if re.search("|".join(URGENT_KEYWORDS), url, re.IGNORECASE):
        flags.append("Urgency or phishing keywords found in URL")

    # IP-based URL
    if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
        flags.append("IP-based URL detected")

    return flags
