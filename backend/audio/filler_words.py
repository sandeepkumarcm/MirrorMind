import re

FILLER_WORDS = ["um", "uh", "like", "actually", "basically", "you know"]


def count_filler_words(transcript):
    """
    transcript: plain text string.
    Returns dict: {"total": int, "breakdown": {word: count}, "classification": str}
    """
    text = transcript.lower()
    breakdown = {}

    for filler in FILLER_WORDS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text)
        breakdown[filler] = len(matches)

    total = sum(breakdown.values())

    if total < 3:
        classification = "Good"
    elif total <= 6:
        classification = "Moderate"
    else:
        classification = "High"

    return {
        "total": total,
        "breakdown": breakdown,
        "classification": classification
    }