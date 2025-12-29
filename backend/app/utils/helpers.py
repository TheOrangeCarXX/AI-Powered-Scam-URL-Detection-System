import hashlib
from urllib.parse import urlparse


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent processing.
    """
    if not text:
        return ""
    return " ".join(text.strip().lower().split())


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


def hash_value(value: str) -> str:
    """
    Generate SHA-256 hash.
    Useful for:
    - Ethereum on-chain proof
    - Privacy-safe logging
    """
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def clamp_score(score: int) -> int:
    """
    Ensure score is always between 0 and 100.
    """
    return max(0, min(score, 100))


def verdict_from_score(score: int) -> str:
    """
    Convert numeric score to verdict.
    """
    if score >= 70:
        return "SCAM"
    elif score >= 40:
        return "SUSPICIOUS"
    return "SAFE"

