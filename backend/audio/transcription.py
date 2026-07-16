import whisper

_model = whisper.load_model("small")


def transcribe(audio_path):
    """
    Transcribes a WAV file using Whisper "small" model.
    Returns dict: {"text": str, "words": [{"word": str, "start": float, "end": float}, ...]}
    """
    result = _model.transcribe(audio_path, word_timestamps=True)

    words = []
    for segment in result.get("segments", []):
        for w in segment.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": round(w["start"], 2),
                "end": round(w["end"], 2)
            })

    return {
        "text": result["text"].strip(),
        "words": words
    }