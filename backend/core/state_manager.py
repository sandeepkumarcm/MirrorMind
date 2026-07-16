import threading
import copy


class StateManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._state = {
            "video": {
                "frame_b64": None,
                "emotion": None,
                "emotion_confidence": None,
                "eye_contact_pct": 0.0,
                "head_pose": "Unknown",
            },
            "audio": {
                "transcript": "",
                "wpm": 0.0,
                "wpm_classification": "",
                "filler_count": 0,
                "filler_classification": "",
                "pause_count": 0,
                "longest_pause": 0.0,
                "hesitation": False,
                "answer_duration": 0.0,
                "answer_classification": "",
                "recording": False,
            },
        }

    def update_video(self, **kwargs):
        with self._lock:
            self._state["video"].update(kwargs)

    def update_audio(self, **kwargs):
        with self._lock:
            self._state["audio"].update(kwargs)

    def get_state(self):
        with self._lock:
            return copy.deepcopy(self._state)


# Single shared instance — routes and loops import this
state_manager = StateManager()