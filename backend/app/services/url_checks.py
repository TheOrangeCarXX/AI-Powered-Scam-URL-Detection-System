import re
from urllib.parse import urlparse

# Top-level domains considered highly trustworthy
TRUSTED_TLDS = [".bank.in", ".gov.in", ".edu.in", ".ac.in", ".org.in"]

# Domains with TLDs often associated with malicious activity
SUSPICIOUS_TLDS = [
    ".xyz", ".tk", ".ml", ".cf", ".site", ".online", ".live", ".shop", ".zip"
]

# Analyze the URL and return a list of flags based on structural checks
def analyze_url(url: str) -> list[str]:
    flags = []
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Official Infrastructure Check (The "Golden Pass")
    if any(domain.endswith(tld) for tld in TRUSTED_TLDS):
        flags.append("TRUSTED_TLD")
        return flags # Return early for high-trust domains

    # HTTPS Security Check
    if not url.startswith("https://"):
        flags.append("Website does not use HTTPS")

    # Suspicious TLD Detection
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            flags.append("Suspicious top-level domain detected")

    # IP-based URL Detection
    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", domain):
        flags.append("IP-based URL detected")

    return flags