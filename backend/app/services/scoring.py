def calculate_score(flags: list[str]):
    """
    Each flag contributes equally.
    """

    score = len(flags) * 20
    score = min(score, 100)

    if score >= 70:
        verdict = "SCAM"
    elif score >= 40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SAFE"

    confidence = round(score / 100, 2)

    return score, verdict, confidence
