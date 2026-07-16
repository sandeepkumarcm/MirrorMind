def calculate_wpm(word_list, duration_sec):
    """
    word_list: list of {"word": str, "start": float, "end": float} from Whisper.
    duration_sec: total answer duration in seconds.
    Returns dict: {"wpm": float, "classification": str}
    """
    if duration_sec <= 0 or not word_list:
        return {"wpm": 0.0, "classification": "Too Slow"}

    word_count = len(word_list)
    minutes = duration_sec / 60.0
    wpm = word_count / minutes

    if wpm < 90:
        classification = "Too Slow"
    elif wpm <= 160:
        classification = "Good"
    else:
        classification = "Too Fast"

    return {
        "wpm": round(float(wpm), 1),
    
        "classification": classification
    }