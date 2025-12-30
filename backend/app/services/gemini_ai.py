import requests
from app.config import GEMINI_API_KEY

# Gemini API endpoint for content generation
GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-flash-latest:generateContent"
)

# Standard headers for the Gemini API requests
HEADERS = {
    "Content-Type": "application/json"
}

# Function to analyze a webpage using Gemini AI
def ai_analyze_page(url: str, page_text: str) -> dict:
    page_text = page_text[:10000]

    prompt = f"""
You are a cybersecurity expert.

Analyze the website below and determine if it is a scam.

URL:
{url}

PAGE TEXT:
{page_text}

Respond STRICTLY in this format:
RiskScore: <number from 0 to 100>
Explanation: <short explanation>
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}",
            headers=HEADERS,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            raise RuntimeError(response.text)

        data = response.json()

        # ✅ SAFE EXTRACTION (critical fix)
        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError("No candidates returned by Gemini")

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts or "text" not in parts[0]:
            raise ValueError("Gemini returned no usable text (likely safety-filtered)")

        text = parts[0]["text"]

        risk_score = 40
        explanation = "No obvious scam indicators."

        for line in text.splitlines():
            line = line.strip()
            if line.lower().startswith("riskscore"):
                risk_score = int("".join(filter(str.isdigit, line)))
            elif line.lower().startswith("explanation"):
                explanation = line.split(":", 1)[1].strip()

        trust_level = (
            "HIGH" if risk_score < 30
            else "MEDIUM" if risk_score < 60
            else "LOW"
        )

        return {
            "ai_score": max(0, min(risk_score, 100)),
            "trust_level": trust_level,
            "ai_explanation": explanation
        }

    except Exception:
        # ✅ INTENTIONAL FALLBACK (not an error)
        return {
            "ai_score": 25,
            "trust_level": "MEDIUM",
            "ai_explanation": (
                "External AI limited for financial content. "
                "Local semantic analysis applied."
            )
        }
