from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest
from app.services.url_checks import analyze_url
from app.services.html_checks import analyze_html
from app.services.scoring import calculate_score
from app.services.gemini_ai import ai_analyze_page

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("")
def analyze(request: AnalyzeRequest):
    rule_flags = []
    page_text = ""

    # 1️⃣ Rule-based checks
    if request.type == "url":
        rule_flags = analyze_url(request.data)
        page_text = request.data

    elif request.type == "html":
        rule_flags, page_text = analyze_html(request.data)

    else:
        raise HTTPException(status_code=400, detail="Invalid input type")

    # 2️⃣ Rule-based score
    rule_score, _, _ = calculate_score(rule_flags)

    # 3️⃣ Gemini AI full-page analysis
    ai_result = ai_analyze_page(
        page_text=page_text,
        rule_flags=rule_flags
    )

    ai_score = ai_result["ai_score"]

    # 4️⃣ HYBRID FINAL SCORE
    final_score = int((rule_score * 0.6) + (ai_score * 0.4))

    if final_score >= 70:
        verdict = "SCAM"
    elif final_score >= 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    confidence = round(final_score / 100, 2)

    if verdict == "SAFE":
        ai_explanation = (
            "No common scam indicators were detected. "
            "This appears to be a legitimate website."
        )
    else:
        ai_explanation = ai_result["ai_explanation"]

    return {
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
