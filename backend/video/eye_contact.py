# MediaPipe Face Mesh landmark indices (with refine_landmarks=True)
RIGHT_EYE_CORNERS = [33, 133, 159, 145]   # outer, inner, top, bottom
LEFT_EYE_CORNERS = [362, 263, 386, 374]   # inner, outer, top, bottom
RIGHT_IRIS = [469, 470, 471, 472]
LEFT_IRIS = [474, 475, 476, 477]

TOLERANCE_PCT = 0.15  # ±15%


def _region_center(points, indices):
    xs = [points[i][0] for i in indices]
    ys = [points[i][1] for i in indices]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def check_eye_contact(landmarks):
    """
    Takes 478 MediaPipe landmarks (already extracted — no re-detection here).
    Returns True if both eyes' iris centers are within ±15% of their
    eye-region center, else False.
    """
    if landmarks is None or len(landmarks) < 478:
        return False

    right_eye_center = _region_center(landmarks, RIGHT_EYE_CORNERS)
    left_eye_center = _region_center(landmarks, LEFT_EYE_CORNERS)
    right_iris_center = _region_center(landmarks, RIGHT_IRIS)
    left_iris_center = _region_center(landmarks, LEFT_IRIS)

    def within_tolerance(iris_c, eye_c, eye_indices, points):
        xs = [points[i][0] for i in eye_indices]
        ys = [points[i][1] for i in eye_indices]
        eye_width = max(xs) - min(xs)
        eye_height = max(ys) - min(ys)

        if eye_width == 0 or eye_height == 0:
            return False

        dx_pct = abs(iris_c[0] - eye_c[0]) / eye_width
        dy_pct = abs(iris_c[1] - eye_c[1]) / eye_height

        return dx_pct <= TOLERANCE_PCT and dy_pct <= TOLERANCE_PCT

    right_ok = within_tolerance(right_iris_center, right_eye_center, RIGHT_EYE_CORNERS, landmarks)
    left_ok = within_tolerance(left_iris_center, left_eye_center, LEFT_EYE_CORNERS, landmarks)

    return right_ok and left_ok


def compute_eye_contact_percentage(history):
    """
    Takes a list of booleans collected over a time window (e.g. 1 second).
    Returns the percentage that were True.
    """
    if not history:
        return 0.0

    true_count = sum(1 for h in history if h)
    return round((true_count / len(history)) * 100, 2)