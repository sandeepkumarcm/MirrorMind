import base64
import threading
import time
import cv2
from fastapi import APIRouter

from backend.video.webcam import webcam_stream
from backend.video.face_landmarks import get_landmarks
from backend.video.emotion_detection import detect_emotion
from backend.video.eye_contact import check_eye_contact, compute_eye_contact_percentage
from backend.video.head_pose import get_head_pose
from backend.video.emotion_smoothing import EmotionSmoother
from backend.core.state_manager import state_manager

router = APIRouter()

_smoother = EmotionSmoother()
_eye_contact_history = []
_loop_thread = None
_loop_running = False

EYE_CONTACT_WINDOW_SEC = 1.0


def _video_loop():
    """
    Runs in a background thread. Extracts landmarks ONCE per frame,
    then reuses them for emotion, eye contact, and head pose —
    no repeated face detection.
    """
    global _loop_running
    _loop_running = True
    last_eye_check = time.time()

    last_emotion_check = time.time()
    emotion_result = None
    EMOTION_INTERVAL_SEC = 1.0
    
    for frame in webcam_stream.get_frames():
        if not _loop_running:
            break

        landmarks = get_landmarks(frame)  # extracted once, reused below
        
        if time.time() - last_emotion_check >= EMOTION_INTERVAL_SEC:

            emotion_result = detect_emotion(frame)
            last_emotion_check = time.time()


        emotion_label = None
        emotion_confidence = None
        if emotion_result:
            emotion_label = _smoother.get_smoothed_emotion(emotion_result["label"])
            emotion_confidence = emotion_result["confidence"]
            print(f"Emotion: {emotion_label} ({emotion_confidence:.1f}%)")

        is_looking = check_eye_contact(landmarks)
        _eye_contact_history.append(is_looking)

        pose = get_head_pose(landmarks, frame.shape)

        if time.time() - last_eye_check >= EYE_CONTACT_WINDOW_SEC:
            eye_pct = compute_eye_contact_percentage(_eye_contact_history)
            _eye_contact_history.clear()
            last_eye_check = time.time()
            state_manager.update_video(eye_contact_pct=eye_pct)

        # encode frame as base64 JPEG so Streamlit can display it via HTTP
        _, buffer = cv2.imencode(".jpg", frame)
        frame_b64 = base64.b64encode(buffer).decode("utf-8")

        state_manager.update_video(
            frame_b64=frame_b64,
            emotion=emotion_label,
            emotion_confidence=emotion_confidence,
            head_pose=pose,
        )


def start_video_loop():
    global _loop_thread
    if _loop_thread is None or not _loop_thread.is_alive():
        webcam_stream.start()
        _loop_thread = threading.Thread(target=_video_loop, daemon=True)
        _loop_thread.start()


def stop_video_loop():
    global _loop_running
    _loop_running = False
    webcam_stream.stop()


@router.post("/video/start")
def start_video():
    start_video_loop()
    return {"status": "started"}


@router.post("/video/stop")
def stop_video():
    stop_video_loop()
    return {"status": "stopped"}


@router.get("/video/state")
def get_video_state():
    return state_manager.get_state()["video"]