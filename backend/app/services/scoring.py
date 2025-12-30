def calculate_score(flags: list[str]):
    """
    Structural risk scoring (low confidence by design).
    Rules alone should not mark a site as SCAM.
    """

    score = len(flags) * 15      # ⬅️ reduced from 20
    score = min(score, 60)       # ⬅️ rules never exceed 60

    if score >= 45:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    confidence = round(score / 100, 2)
    return score, verdict, confidence
