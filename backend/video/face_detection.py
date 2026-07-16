import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

_detector = mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)

MIN_FACE_SIZE = 80  # pixels


def detect_face(frame):
    """
    Takes a BGR OpenCV frame.
    Returns (x, y, w, h) bounding box in pixel coords, or None.
    """
    if frame is None:
        return None

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = _detector.process(rgb_frame)

    if not results.detections:
        return None

    h, w, _ = frame.shape
    detection = results.detections[0]  # take the most confident face
    bbox = detection.location_data.relative_bounding_box

    x = int(bbox.xmin * w)
    y = int(bbox.ymin * h)
    box_w = int(bbox.width * w)
    box_h = int(bbox.height * h)

    if box_w < MIN_FACE_SIZE or box_h < MIN_FACE_SIZE:
        return None

    return (x, y, box_w, box_h)