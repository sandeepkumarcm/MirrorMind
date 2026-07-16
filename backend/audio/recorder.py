import sounddevice as sd
from scipy.io.wavfile import write as wav_write
from scipy.signal import resample
import numpy as np

RECORD_SAMPLE_RATE = 44100
SAMPLE_RATE = 16000
CHANNELS = 1
MAX_DURATION_SEC = 120


class AudioRecorder:
    def __init__(self):
        self.recording = False

    def record_audio(self, duration_sec, output_path):
        duration_sec = min(duration_sec, MAX_DURATION_SEC)
        self.recording = True

        num_frames = int(duration_sec * RECORD_SAMPLE_RATE)

        audio_data = sd.rec(
            num_frames,
            samplerate=RECORD_SAMPLE_RATE,
            channels=CHANNELS,
        
            dtype='int16'
        )
        sd.wait()  # blocks until recording finishes

        self.recording = False

        if audio_data is None or np.abs(audio_data).max() == 0:
            raise RuntimeError("No audio captured — check microphone permissions/device.")

        # Resample from 44100 Hz down to 16000 Hz for Whisper
        num_samples = int(len(audio_data) * SAMPLE_RATE / RECORD_SAMPLE_RATE)
        audio_data = resample(audio_data, num_samples).astype(np.int16)

        wav_write(output_path, SAMPLE_RATE, audio_data)

        return output_path

    def stop(self):
        """
        sd.rec() can't be stopped mid-way as cleanly as a stream callback.
        This calls sd.stop() to halt any in-progress recording early.
        """
        sd.stop()
        self.recording = False


audio_recorder = AudioRecorder()