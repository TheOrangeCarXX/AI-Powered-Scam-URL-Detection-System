from bs4 import BeautifulSoup

SENSITIVE_INPUT_TYPES = ["password", "tel", "number"]

def analyze_html(html: str):
    flags = []
    soup = BeautifulSoup(html, "html.parser")

    texts = []

    # Visible text
    texts.append(soup.get_text(separator=" ", strip=True))

    # Input-related signals
    for inp in soup.find_all("input"):
        input_type = (inp.get("type") or "").lower()
        name = inp.get("name", "")
        placeholder = inp.get("placeholder", "")

        if input_type in SENSITIVE_INPUT_TYPES:
            flags.append("Page contains sensitive input fields")

        texts.extend([name, placeholder])

    # Button text
    for btn in soup.find_all("button"):
        texts.append(btn.get_text(strip=True))

    # Limit text safely
    page_text = " ".join(filter(None, texts))[:1500]

    return flags, page_text
