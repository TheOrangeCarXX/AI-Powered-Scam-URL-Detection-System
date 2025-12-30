def calculate_score(flags: list[str]):
    """
    Structural risk scoring (low confidence by design).
    Rules alone should not mark a site as SCAM.
    """

    score = len(flags) * 15      # Each flag adds 15 points
    score = min(score, 60)       # Cap from rules at 60

    if score >= 45:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    confidence = round(score / 100, 2)   # Confidence from rules (0.0 to 0.6)
    return score, verdict, confidence
