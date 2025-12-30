import re
from urllib.parse import urlparse

TRUSTED_TLDS = [".bank.in", ".gov.in", ".edu.in", ".ac.in", ".org.in"]

SUSPICIOUS_TLDS = [
    ".xyz", ".tk", ".ml", ".cf", ".site", ".online", ".live", ".shop", ".zip"
]

def analyze_url(url: str) -> list[str]:
    flags = []
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # 1. Official Infrastructure Check (The "Golden Pass")
    if any(domain.endswith(tld) for tld in TRUSTED_TLDS):
        flags.append("TRUSTED_TLD")
        return flags # Return early for high-trust domains

    # 2. HTTPS Security Check
    if not url.startswith("https://"):
        flags.append("Website does not use HTTPS")

    # 3. Suspicious TLD Detection
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            flags.append("Suspicious top-level domain detected")

    # 4. IP-based URL Detection
    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", domain):
        flags.append("IP-based URL detected")

    return flags