import re
import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


def ai_analyze_page(url: str, page_text: str) -> dict:
    page_text = page_text[:1200]

    prompt = f"""
You are a cybersecurity and fraud detection expert.

Analyze the following WEBSITE:

URL:
{url}

VISIBLE PAGE TEXT:
\"\"\"
{page_text}
\"\"\"

TASKS:
1. Decide whether this website appears to be a legitimate, well-known service.
2. Decide whether there are signs of scam or fraud intent.
3. Assign a scam risk score from 0 to 100.

IMPORTANT:
- Legitimate websites may still have login forms.
- Scam sites often misuse brand names, urgency, or fear language.

OUTPUT FORMAT (STRICT):
Legitimate: YES | NO | UNCERTAIN
RiskScore: <number>
Explanation: <short explanation>
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # ✅ Neutral defaults (important)
        risk_score = 40
        trust_level = "MEDIUM"
        explanation = "No strong scam indicators detected."

        for line in text.splitlines():
            line_clean = line.strip().lower()

            # ✅ Robust RiskScore parsing
            if "riskscore" in line_clean:
                nums = re.findall(r"\d+", line_clean)
                if nums:
                    risk_score = int(nums[0])

            # ✅ Robust TrustLevel parsing
            elif "trustlevel" in line_clean:
                if "high" in line_clean:
                    trust_level = "HIGH"
                elif "low" in line_clean:
                    trust_level = "LOW"
                else:
                    trust_level = "MEDIUM"

            # ✅ Robust Explanation parsing
            elif "explanation" in line_clean:
                explanation = line.split(":", 1)[-1].strip()

        return {
            "ai_score": max(0, min(risk_score, 100)),
            "trust_level": trust_level,
            "ai_explanation": explanation
        }

    except Exception:
        # ⚠️ FAIL-SAFE: NEUTRAL, NOT SAFE
        return {
            "ai_score": 40,
            "trust_level": "MEDIUM",
            "ai_explanation": (
                "AI analysis could not be completed. "
                "Using neutral confidence based on available signals."
            )
        }
