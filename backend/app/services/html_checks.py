from bs4 import BeautifulSoup

# Added common phishing input types
SENSITIVE_INPUT_TYPES = ["password", "tel", "number", "text", "email"]

# Common social engineering phrases often found in scams
SCAM_PHRASES = [
    "upi pin", "kyc update", "account blocked", "verify your account",
    "claim reward", "lottery winner", "customer care", "get cashback",
    "security alert", "unusual login", "support agent", "account number",
    "official login", "restore access", "mandatory update"
]

# Function to analyze HTML content for scam indicators
def analyze_html(html: str):
    flags = set()
    soup = BeautifulSoup(html, "html.parser")
    texts = []

    # Title Check
    title_tag = soup.title.string.lower() if soup.title else ""
    if title_tag:
        texts.append(f"Title: {title_tag}")
        if any(p in title_tag for p in ["sbi", "blocked", "alert", "login", "bank"]):
            flags.add("Suspicious keywords detected in page title")

    # Visible Text extraction
    visible_text = soup.get_text(separator=" ", strip=True).lower()
    texts.append(visible_text)

    # Social Engineering Phrase Check
    for phrase in SCAM_PHRASES:
        if phrase in visible_text:
            flags.add(f"Suspicious intent detected: '{phrase}'")

    # Input-related signals
    inputs = soup.find_all("input")
    if len(inputs) > 0:
        for inp in inputs:
            input_type = (inp.get("type") or "").lower()
            name = inp.get("name", "").lower()
            placeholder = inp.get("placeholder", "").lower()

            # If it's a small page asking for sensitive info, it's a high flag
            if input_type in SENSITIVE_INPUT_TYPES:
                flags.add("Page contains sensitive input fields")
            
            # Catching "PIN", "OTP", "PAN", "Aadhar", etc.
            if any(p in name or p in placeholder for p in ["pin", "otp", "password", "pan", "card"]):
                 flags.add("Input fields asking for highly sensitive credentials")

            texts.extend([name, placeholder])

    # Form Action Logic
    for form in soup.find_all("form"):
        action = (form.get("action") or "").lower()
        if action.startswith("http://"):
            flags.add("Form submits data over insecure HTTP")
        
        # IP Address check
        domain_part = action.split('/')[2:3]
        if domain_part and any(char.isdigit() for char in domain_part[0]): 
            flags.add("Form submits data to an IP address instead of a domain")
            
        if any(x in action for x in ["api", "submit.php", "post.php", "login.php"]):
            flags.add("Suspicious form submission endpoint detected")

    # Button Text Analysis
    for btn in soup.find_all("button"):
        btn_text = btn.get_text(strip=True).lower()
        texts.append(btn_text)
        if any(x in btn_text for x in ["verify", "unblock", "claim", "login"]):
            flags.add("Action button uses high-urgency language")

    # Final Text for AI Analysis
    page_text = " ".join(filter(None, texts))[:15000]

    return list(flags), page_text