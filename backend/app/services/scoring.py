def calculate_score(flags: list[str]):
    """
    Structural rules only.
    Low weight by design.
    """

    score = len(flags) * 10   # ⬅️ reduced from 20
    score = min(score, 30)    # ⬅️ rules can never exceed 30

    if score >= 30:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    confidence = round(score / 100, 2)
    return score, verdict, confidence
