import hashlib
from urllib.parse import urlparse

# Utility helper function for text normalization
def normalize_text(text: str) -> str:
    """
    Normalize text for consistent processing.
    """
    if not text:
        return ""
    return " ".join(text.strip().lower().split())


# Utility helper function to extract domain from URL
def extract_domain(url: str) -> str:
    """
    Extract domain name from a URL.
    Example:
    https://sub.example.com/path -> example.com
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        return domain.replace("www.", "")
    except Exception:
        return ""


# Utility helper function to hash a value using SHA-256
def hash_value(value: str) -> str:
    """
    Generate SHA-256 hash.
    Useful for:
    - Ethereum on-chain proof
    - Privacy-safe logging
    """
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


# Utility helper function to clamp score between 0 and 100
def clamp_score(score: int) -> int:
    """
    Ensure score is always between 0 and 100.
    """
    return max(0, min(score, 100))


# Utility helper function to convert score to verdict
def verdict_from_score(score: int) -> str:
    """
    Convert numeric score to verdict.
    """
    if score >= 70:
        return "SCAM"
    elif score >= 40:
        return "SUSPICIOUS"
    return "SAFE"

