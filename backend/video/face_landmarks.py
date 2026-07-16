import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

# refine_landmarks=True adds iris points (needed later for eye_contact.py)
# Without this, you get 468 points. With it, you get 478 (468 face + 10 iris).
_face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def get_landmarks(frame):
    """
    Takes a BGR OpenCV frame.
    Returns a list of (x, y) pixel-coordinate tuples (478 points), or None.
    """
    if frame is None:
        return None

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = _face_mesh.process(rgb_frame)

    if not results.multi_face_landmarks:
        return None

    h, w, _ = frame.shape
    face_landmarks = results.multi_face_landmarks[0]

    points = [(int(lm.x * w), int(lm.y * h)) for lm in face_landmarks.landmark]
    return points