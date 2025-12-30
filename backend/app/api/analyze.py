from fastapi import APIRouter
import requests

from app.models.schemas import AnalyzeRequest
from app.services.url_checks import analyze_url
from app.services.html_checks import analyze_html
from app.services.scoring import calculate_score
from app.services.gemini_ai import ai_analyze_page
from app.services.cache import get_cached, set_cache

router = APIRouter()


@router.post("")
def analyze(request: AnalyzeRequest):
    url = request.data.strip()

    cached = get_cached(url)
    if cached:
        return cached

    rule_flags = []
    html = ""

    # 1️⃣ Fetch HTML
    if request.html:
        html = request.html
    else:
        try:
            response = requests.get(url, timeout=6)
            html = response.text
        except Exception:
            rule_flags.append("Unable to fetch page content")

    # 2️⃣ URL + HTML checks
    url_flags = analyze_url(url)
    html_flags, page_text = analyze_html(html)

    rule_flags.extend(url_flags)
    rule_flags.extend(html_flags)

    # 🚨 GOLDEN PASS: Trusted TLD override
    if "TRUSTED_TLD" in rule_flags:
        response_data = {
            "verdict": "SAFE",
            "final_score": 10,
            "ai_explanation": (
                "This website uses an officially regulated domain "
                "(.bank.in / .gov.in). Scam risk is extremely low."
            )
        }
        set_cache(url, response_data)
        return response_data

    # 3️⃣ Rule-based scoring (intent-driven)
    rule_score, _, _ = calculate_score(rule_flags)

    # 4️⃣ AI analysis (NON-AUTHORITATIVE)
    ai_result = ai_analyze_page(url, page_text)
    ai_score = ai_result.get("ai_score", 10)
    ai_explanation = ai_result.get("ai_explanation", "")

    # 🧠 AI FAIL-SAFE LOGIC
    # If AI fallback is used, reduce its impact
    if ai_score <= 15:
        final_score = rule_score
    else:
        final_score = int((rule_score * 0.7) + (ai_score * 0.3))

    # 5️⃣ Final verdict
    if final_score >= 55:
        verdict = "SCAM"
    elif final_score >= 35:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    response_data = {
        "verdict": verdict,
        "final_score": final_score,
        "ai_explanation": ai_explanation
    }

    set_cache(url, response_data)
    return response_data
