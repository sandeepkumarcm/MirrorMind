import cv2

class WebcamStream:
    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.running = False

    def start(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW = faster startup on Windows
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam. Check if another app is using it.")

        self.running = True

    def stop(self):
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def get_frames(self):
        """Generator: yields BGR frames while self.running is True."""
        if self.cap is None:
            self.start()

        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue
            yield frame

        # cleanup when loop exits (running set to False)
        self.stop()


# Single shared instance — routes import this, don't create new ones
webcam_stream = WebcamStream()