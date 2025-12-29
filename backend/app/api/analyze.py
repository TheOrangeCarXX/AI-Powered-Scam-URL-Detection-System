from fastapi import APIRouter, HTTPException
from urllib.parse import urlparse

from app.models.schemas import AnalyzeRequest
from app.services.url_checks import analyze_url
from app.services.html_checks import analyze_html
from app.services.scoring import calculate_score
from app.services.gemini_ai import ai_analyze_page
from app.services.cache import get_cached, set_cache

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("")
def analyze(request: AnalyzeRequest):
    rule_flags = []
    page_text = ""
    domain = None

    # -------- URL SCAN --------
    if request.type == "url":
        domain = urlparse(request.data).netloc

        # 🔥 CACHE CHECK
        cached = get_cached(domain)
        if cached:
            return cached

        rule_flags = analyze_url(request.data)
        page_text = request.data

    # -------- HTML SCAN --------
    elif request.type == "html":
        rule_flags, page_text = analyze_html(request.data)

    else:
        raise HTTPException(status_code=400, detail="Invalid input type")

    # -------- RULE SCORE --------
    rule_score, _, _ = calculate_score(rule_flags)

    # -------- AI ANALYSIS --------
    ai_result = ai_analyze_page(
        page_text=page_text,
        rule_flags=rule_flags
    )

    ai_score = ai_result["ai_score"]

    # -------- HYBRID FINAL SCORE --------
    final_score = int((rule_score * 0.6) + (ai_score * 0.4))

    if final_score >= 70:
        verdict = "SCAM"
    elif final_score >= 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    confidence = round(final_score / 100, 2)

    # 🔥 SAFE EXPLANATION FIX
    if verdict == "SAFE":
        ai_explanation = (
            "No common scam indicators were detected. "
            "This appears to be a legitimate website."
        )
    else:
        ai_explanation = ai_result["ai_explanation"]

    response = {
        "verdict": verdict,
        "final_score": final_score,
        "confidence": confidence,
        "rule_score": rule_score,
        "ai_score": ai_score,
        "reasons": rule_flags,
        "ai_explanation": ai_explanation,
        "recommended_action": (
            "Do not proceed. Close the page immediately."
            if verdict != "SAFE"
            else "No immediate action required."
        )
    }

    # 🔥 SAVE TO CACHE
    if domain:
        set_cache(domain, response)

    return response
