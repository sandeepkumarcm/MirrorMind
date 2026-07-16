PAUSE_THRESHOLD_SEC = 1.0
HESITATION_THRESHOLD_SEC = 4.0


def detect_pauses(word_list):
    """
    word_list: list of {"word": str, "start": float, "end": float} from Whisper.
    Returns dict: {"pause_count": int, "longest_pause": float, "hesitation": bool}
    """
    if not word_list or len(word_list) < 2:
        return {"pause_count": 0, "longest_pause": 0.0, "hesitation": False}

    pause_count = 0
    longest_pause = 0.0

    for i in range(1, len(word_list)):
        gap = word_list[i]["start"] - word_list[i - 1]["end"]
        if gap >= PAUSE_THRESHOLD_SEC:
            pause_count += 1
            longest_pause = max(longest_pause, gap)

    return {
        "pause_count": int(pause_count),
        "longest_pause": round(float(longest_pause), 2),
        "hesitation": bool(longest_pause > HESITATION_THRESHOLD_SEC)
    }