import threading
import time
from fastapi import APIRouter

from backend.audio.recorder import audio_recorder
from backend.audio.transcription import transcribe
from backend.audio.wpm import calculate_wpm
from backend.audio.pause_detection import detect_pauses
from backend.audio.filler_words import count_filler_words
from backend.audio.answer_timer import evaluate_answer_length
from backend.core.state_manager import state_manager

router = APIRouter()

AUDIO_OUTPUT_PATH = "backend/temp/current_answer.wav"


def _record_and_process(duration_sec):
    """
    Runs on its OWN thread — this is what keeps audio recording
    from blocking the video loop above.
    """
    state_manager.update_audio(recording=True)
    start = time.time()

    audio_recorder.record_audio(duration_sec=duration_sec, output_path=AUDIO_OUTPUT_PATH)
    actual_duration = time.time() - start

    result = transcribe(AUDIO_OUTPUT_PATH)
    wpm_result = calculate_wpm(result["words"], actual_duration)
    pause_result = detect_pauses(result["words"])
    filler_result = count_filler_words(result["text"])
    timer_result = evaluate_answer_length(actual_duration)

    state_manager.update_audio(
        transcript=result["text"],
        wpm=wpm_result["wpm"],
        wpm_classification=wpm_result["classification"],
        filler_count=filler_result["total"],
        filler_classification=filler_result["classification"],
        pause_count=pause_result["pause_count"],
        longest_pause=pause_result["longest_pause"],
        hesitation=pause_result["hesitation"],
        answer_duration=timer_result["duration"],
        answer_classification=timer_result["classification"],
        recording=False,
    )


@router.post("/audio/start")
def start_audio_recording(duration_sec: int = 90):
    thread = threading.Thread(target=_record_and_process, args=(duration_sec,), daemon=True)
    thread.start()
    return {"status": "recording_started", "duration_sec": duration_sec}


@router.post("/audio/stop")
def stop_audio_recording():
    audio_recorder.stop()
    return {"status": "stop_requested"}


@router.get("/audio/state")
def get_audio_state():
    return state_manager.get_state()["audio"]