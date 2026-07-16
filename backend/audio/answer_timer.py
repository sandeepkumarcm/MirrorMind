def evaluate_answer_length(duration_sec):
    """
    Returns dict: {"duration": float, "classification": str}
    """
    if duration_sec < 45:
        classification = "Too Short"
    elif duration_sec <= 90:
        classification = "Good Length"
    else:
        classification = "Too Long"

    return {
        "duration": round(float(duration_sec), 1),
        "classification": classification
    }