import re
from urllib.parse import urlparse

SUSPICIOUS_TLDS = [
    ".xyz", ".tk", ".ml", ".cf", ".site", ".online", ".live"
]

def analyze_url(url: str) -> list[str]:
    flags = []

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # HTTPS check (structural, valid)
    if not url.startswith("https://"):
        flags.append("Website does not use HTTPS")

    # Suspicious TLDs (structural, valid)
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            flags.append("Suspicious top-level domain detected")

    # ✅ FIX: true IP-based URL detection
    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", domain):
        flags.append("IP-based URL detected")

    return flags
