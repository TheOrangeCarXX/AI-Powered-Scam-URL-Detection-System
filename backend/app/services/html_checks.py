from bs4 import BeautifulSoup

SENSITIVE_KEYWORDS = ["otp", "pin", "password", "cvv", "pan"]


def analyze_html(html: str):
    flags = []
    soup = BeautifulSoup(html, "html.parser")

    # Extract visible text (for AI)
    page_text = soup.get_text(separator=" ", strip=True)

    # Detect sensitive input fields
    inputs = soup.find_all("input")
    for inp in inputs:
        placeholder = (inp.get("placeholder") or "").lower()
        name = (inp.get("name") or "").lower()

        for word in SENSITIVE_KEYWORDS:
            if word in placeholder or word in name:
                flags.append(f"Sensitive input requested: {word.upper()}")

    # Urgency / threat language
    lowered = page_text.lower()
    if any(
        phrase in lowered
        for phrase in ["account will be blocked", "urgent", "verify immediately"]
    ):
        flags.append("Urgency or threat-based language detected")

    return flags, page_text
