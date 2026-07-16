import cv2
import numpy as np

# Generic 3D face model points (in mm, arbitrary reference frame)
MODEL_POINTS = np.array([
    (0.0, 0.0, 0.0),          # Nose tip
    (0.0, -330.0, -65.0),     # Chin
    (-225.0, 170.0, -135.0),  # Left eye left corner
    (225.0, 170.0, -135.0),   # Right eye right corner
    (-150.0, -150.0, -125.0), # Left mouth corner
    (150.0, -150.0, -125.0),  # Right mouth corner
], dtype=np.float64)

# MediaPipe Face Mesh indices matching the 6 points above
LANDMARK_IDX = {
    "nose_tip": 1,
    "chin": 152,
    "left_eye_corner": 33,
    "right_eye_corner": 263,
    "left_mouth_corner": 61,
    "right_mouth_corner": 291,
}

YAW_PITCH_THRESHOLD = 15.0  # degrees


def get_head_pose(landmarks, frame_shape):
    """
    landmarks: list of (x, y) pixel points from face_landmarks.py
    frame_shape: (height, width) of the frame
    Returns one of: "Forward", "Left", "Right", "Up", "Down", "Unknown"
    """
    if landmarks is None:
        return "Unknown"

    h, w = frame_shape[:2]

    try:
        image_points = np.array([
            landmarks[LANDMARK_IDX["nose_tip"]],
            landmarks[LANDMARK_IDX["chin"]],
            landmarks[LANDMARK_IDX["left_eye_corner"]],
            landmarks[LANDMARK_IDX["right_eye_corner"]],
            landmarks[LANDMARK_IDX["left_mouth_corner"]],
            landmarks[LANDMARK_IDX["right_mouth_corner"]],
        ], dtype=np.float64)
    except (IndexError, TypeError):
        return "Unknown"

    focal_length = w
    center = (w / 2, h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype=np.float64)

    dist_coeffs = np.zeros((4, 1))  # assume no lens distortion

    success, rotation_vector, translation_vector = cv2.solvePnP(
        MODEL_POINTS, image_points, camera_matrix, dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return "Unknown"

    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    proj_matrix = np.hstack((rotation_matrix, translation_vector))
    euler_angles = cv2.decomposeProjectionMatrix(proj_matrix)[6]

    pitch, yaw, roll = [float(a) for a in euler_angles.flatten()]

    # Correct pitch wraparound (common solvePnP quirk)
    if pitch > 90:
        pitch -= 180
    elif pitch < -90:
        pitch += 180

    if abs(yaw) <= YAW_PITCH_THRESHOLD and abs(pitch) <= YAW_PITCH_THRESHOLD:
        return "Forward"
    elif abs(yaw) > YAW_PITCH_THRESHOLD:
        return "Right" if yaw > 0 else "Left"
    else:
        return "Down" if pitch > 0 else "Up"