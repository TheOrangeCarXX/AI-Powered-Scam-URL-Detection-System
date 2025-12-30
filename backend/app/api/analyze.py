from fastapi import APIRouter, HTTPException
import requests

from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.url_checks import analyze_url
from app.services.html_checks import analyze_html
from app.services.scoring import calculate_score
from app.services.gemini_ai import ai_analyze_page
from app.services.cache import get_cached, set_cache

router = APIRouter()


@router.post("")
def analyze(request: AnalyzeRequest):
    url = request.data.strip()

    # ✅ Cache by full URL
    cached = get_cached(url)
    if cached:
        return cached

    rule_flags: list[str] = []

    # Fetch page
    try:
        response = requests.get(url, timeout=6)
        html = response.text
    except Exception:
        html = ""
        rule_flags.append("Unable to fetch page content")

    # Structural rule checks
    url_flags = analyze_url(url)                 # list[str]
    html_flags, page_text = analyze_html(html)   # (list[str], str)

    rule_flags.extend(url_flags)
    rule_flags.extend(html_flags)

    # Rule-based score (low weight by design)
    rule_score, rule_verdict, rule_confidence = calculate_score(rule_flags)

    # AI analysis (semantic intent)
    ai_result = ai_analyze_page(url, page_text)
    ai_score = ai_result.get("ai_score", 40)
    trust_level = ai_result.get("trust_level", "MEDIUM")
    ai_explanation = ai_result.get("ai_explanation", "")

    # ✅ TrustLevel HIGH should not blindly override
    if trust_level == "HIGH" and rule_score < 10:
        verdict = "SAFE"
        final_score = 0
    else:
        # Final score = AI dominant + rule influence
        final_score = (max(ai_score, 40) * 0.75) + (rule_score * 0.25)

        verdict = (
            "SCAM"
            if final_score >= 70
            else "SUSPICIOUS"
            if final_score >= 40
            else "SAFE"
        )

    response_data = {
        "verdict": verdict,
        "final_score": final_score,
        "ai_explanation": ai_explanation
    }

    set_cache(url, response_data)
    return response_data
