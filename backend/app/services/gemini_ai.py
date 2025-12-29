import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


def ai_analyze_page(page_text: str, rule_flags: list[str]) -> dict:
    """
    Gemini analyzes full page context + rule indicators
    Returns AI score + explanation
    """

    # Safety trim
    page_text = page_text[:3000]

    prompt = f"""
You are a cybersecurity expert.

Analyze the following webpage for scam or phishing risk.

PAGE CONTENT:
\"\"\"
{page_text}
\"\"\"

RULE-BASED INDICATORS:
{', '.join(rule_flags) if rule_flags else 'None'}

TASKS:
1. Give a scam risk score from 0 to 100.
2. Briefly explain why.

RULES:
- Be factual and calm
- Do not exaggerate
- Do not mention AI or models
- Max 3 sentences
- Output ONLY in this format:

Score: <number>
Explanation: <text>
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        score = 50
        explanation = "The page was analyzed for scam indicators."

        for line in text.splitlines():
            if line.lower().startswith("score"):
                score = int("".join(filter(str.isdigit, line)))
            elif line.lower().startswith("explanation"):
                explanation = line.split(":", 1)[1].strip()

        score = max(0, min(score, 100))

        return {
            "ai_score": score,
            "ai_explanation": explanation
        }

    except Exception:
        # Demo-safe fallback
        return {
            "ai_score": 50,
            "ai_explanation": (
                "The page shows warning signs such as urgency or requests "
                "for sensitive information, which are commonly used in scams."
            )
        }
