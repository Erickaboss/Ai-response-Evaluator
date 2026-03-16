"""
feedback.py
Generates a human-readable evaluation report from individual criterion scores.
"""

CRITERIA_WEIGHTS = {
    "Clarity":              0.20,
    "Completeness":         0.25,
    "Reasoning":            0.25,
    "Example Usage":        0.15,
    "Length & Readability": 0.15,
}


def compute_final_score(scores: dict[str, int]) -> float:
    """Compute a weighted final score (1-10) from individual criterion scores."""
    total = sum(scores[criterion] * weight
                for criterion, weight in CRITERIA_WEIGHTS.items())
    return round(total, 1)


def generate_report(prompt: str, response: str, scores: dict[str, int],
                    rationales: dict[str, str]) -> str:
    """
    Build and return a formatted evaluation report string.
    Includes per-criterion scores, rationales, and a final weighted score.
    """
    final = compute_final_score(scores)
    lines = [
        "=" * 60,
        "        AI RESPONSE EVALUATION REPORT",
        "=" * 60,
        f"\nPROMPT:\n  {prompt}\n",
        f"RESPONSE PREVIEW:\n  {response[:120].strip()}{'...' if len(response) > 120 else ''}\n",
        "-" * 60,
        "CRITERION SCORES",
        "-" * 60,
    ]

    for criterion, weight in CRITERIA_WEIGHTS.items():
        score = scores[criterion]
        rationale = rationales[criterion]
        bar = "#" * score + "-" * (10 - score)
        lines.append(f"\n[{criterion}]  (weight: {int(weight*100)}%)")
        lines.append(f"  Score    : {score}/10  [{bar}]")
        lines.append(f"  Feedback : {rationale}")

    lines += [
        "\n" + "=" * 60,
        f"  FINAL WEIGHTED SCORE: {final} / 10",
        _verdict(final),
        "=" * 60,
    ]

    return "\n".join(lines)


def _verdict(score: float) -> str:
    """Return a short verdict label based on the final score."""
    if score >= 8.5:
        return "  Verdict : Excellent response."
    elif score >= 7.0:
        return "  Verdict : Good response with minor room for improvement."
    elif score >= 5.0:
        return "  Verdict : Acceptable, but notable gaps exist."
    else:
        return "  Verdict : Poor response — significant improvements needed."
