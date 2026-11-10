
import cv2
import mediapipe as mp
import numpy as np
import time
import os

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Model file
MODEL_PATH = "hand_landmarker.task"

if not os.path.exists(MODEL_PATH):
    print("Hand landmark model not found!")
    exit()

# Hand tracking setup
base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6,
    min_tracking_confidence=0.6
)

# Create detector
detector = vision.HandLandmarker.create_from_options(options)

# Webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not open!")
    detector.close()
    exit()

canvas = None
px, py = 0, 0
color_index = 0
drawing = False
frame_count = 0

colors = [
    (255, 0, 255),
    (255, 255, 0),
    (0, 255, 0),
    (0, 165, 255),
    (255, 255, 255)
]

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    timestamp = int(frame_count * 1000 / 30)
    frame_count += 1

    result = detector.detect_for_video(
        mp_image, timestamp
    )

    drawing = False

    if result.hand_landmarks:

        for hand in result.hand_landmarks:

            # Landmark positions
            points = []

            for lm in hand:
                x = int(lm.x * w)
                y = int(lm.y * h)
                points.append((x, y))

            # Index finger
            ix, iy = points[8]

            index_up = hand[8].y < hand[6].y
            middle_up = hand[12].y < hand[10].y

            # Draw with index finger only
            if index_up and not middle_up:

                drawing = True

                if px == 0 and py == 0:
                    px, py = ix, iy

                cv2.line(
                    canvas,
                    (px, py),
                    (ix, iy),
                    colors[color_index],
                    5
                )

                px, py = ix, iy

                cv2.circle(
                    frame, (ix, iy), 10,
                    colors[color_index], -1
                )

            else:
                px, py = 0, 0

            # Draw hand skeleton
            connections = [
                (0,1),(1,2),(2,3),(3,4),
                (0,5),(5,6),(6,7),(7,8),
                (5,9),(9,10),(10,11),(11,12),
                (9,13),(13,14),(14,15),(15,16),
                (13,17),(17,18),(18,19),(19,20),
                (0,17)
            ]

            for a, b in connections:
                cv2.line(
                    frame, points[a], points[b],
                    (0, 255, 0), 2
                )

    # Neon effect
    blurred = cv2.GaussianBlur(canvas, (21, 21), 0)

    frame = cv2.addWeighted(
        frame, 1, blurred, 0.8, 0
    )

    frame = cv2.addWeighted(
        frame, 1, canvas, 1, 0
    )

    # Interface
    cv2.putText(
        frame, "HANDWALL - AI VIRTUAL WRITING",
        (15, 35), cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (255, 255, 255), 2
    )

    cv2.putText(
        frame, "INDEX UP = DRAW | LOWER = STOP",
        (15, 75), cv2.FONT_HERSHEY_SIMPLEX,
        0.55, (0, 255, 0), 2
    )

    cv2.putText(
        frame, "C: CLEAR | 1-5: COLORS | Q: QUIT",
        (15, 110), cv2.FONT_HERSHEY_SIMPLEX,
        0.55, (255, 255, 255), 2
    )

    status = "DRAWING" if drawing else "READY"

    cv2.putText(
        frame, status, (15, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7, colors[color_index], 2
    )

    cv2.imshow("HANDWALL - Virtual Writing", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('c'):
        canvas = np.zeros_like(frame)

    elif key in [ord('1'), ord('2'), ord('3'),
                 ord('4'), ord('5')]:
        color_index = int(chr(key)) - 1

cap.release()
detector.close()
cv2.destroyAllWindows()
