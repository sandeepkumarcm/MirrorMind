from collections import deque, Counter

class EmotionSmoother:
    def __init__(self, window_size=20):
        # maxlen enforces a hard cap — old entries auto-drop, no memory growth
        # even after 10+ minutes of continuous frames
        self.window = deque(maxlen=window_size)

    def get_smoothed_emotion(self, new_label):
        """
        Appends new_label, returns the most frequent label
        in the current window (mode).
        """
        self.window.append(new_label)
        counts = Counter(self.window)
        smoothed_label, _ = counts.most_common(1)[0]
        return smoothed_label