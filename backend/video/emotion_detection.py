from deepface import DeepFace

CONFIDENCE_THRESHOLD = 40.0  # percent


def detect_emotion(frame):
    """
    Takes a BGR OpenCV frame.
    Returns dict of 7 emotion probabilities + top label, or None if no face.
    """
    try:
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            detector_backend='mediapipe',
            enforce_detection=False
        )

        # DeepFace returns a list when input could contain multiple faces
        if isinstance(result, list):
            result = result[0]

        emotions = result.get("emotion", {})
        if not emotions:
            return None

        top_label = max(emotions, key=emotions.get)
        top_confidence = emotions[top_label]

        if top_confidence < CONFIDENCE_THRESHOLD:
            return {
                "label": "Uncertain",
                "confidence": round(top_confidence, 2),
                "all_scores": emotions
            }

        return {
            "label": top_label,
            "confidence": round(top_confidence, 2),
            "all_scores": emotions
        }

    except Exception:
        # No face detected, or DeepFace internal error — don't crash the loop
        return None