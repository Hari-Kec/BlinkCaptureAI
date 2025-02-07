import cv2
import mediapipe
from math import sqrt
import numpy
from screenshot import capture_screenshot
from ocr import extract_text
from llm_analysis import analyze_screenshot

from ui import show_explanation

COUNTER = 0
TOTAL_BLINKS = 0
BLINK_TRIGGER = 3  # Number of blinks to trigger screenshot

FONT = cv2.FONT_HERSHEY_SIMPLEX

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

mediapipe_face_mesh = mediapipe.solutions.face_mesh
face_mesh = mediapipe_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.6, min_tracking_confidence=0.7)

video_capture = cv2.VideoCapture(0)

def landmarksDetection(image, results, draw=False):
    image_height, image_width = image.shape[:2]
    mesh_coordinates = [(int(point.x * image_width), int(point.y * image_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw:
        [cv2.circle(image, i, 2, (0, 255, 0), -1) for i in mesh_coordinates]
    return mesh_coordinates

def euclideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    return sqrt((x1 - x)**2 + (y1 - y)**2)

def blinkRatio(landmarks, right_indices, left_indices):
    right_horizontal = euclideanDistance(landmarks[right_indices[0]], landmarks[right_indices[8]])
    right_vertical = euclideanDistance(landmarks[right_indices[12]], landmarks[right_indices[4]])
    left_horizontal = euclideanDistance(landmarks[left_indices[0]], landmarks[left_indices[8]])
    left_vertical = euclideanDistance(landmarks[left_indices[12]], landmarks[left_indices[4]])

    return ((right_horizontal / right_vertical) + (left_horizontal / left_vertical)) / 2

while True:
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        landmarks = landmarksDetection(frame, results, True)
        ratio = blinkRatio(landmarks, RIGHT_EYE, LEFT_EYE)

        if ratio > 3:
            COUNTER += 1
        else:
            if COUNTER > 4:
                TOTAL_BLINKS += 1
                COUNTER = 0
                if TOTAL_BLINKS == BLINK_TRIGGER:
                    screenshot_path = capture_screenshot()
                    text = extract_text(screenshot_path)
                    explanation = analyze_screenshot(screenshot_path)
                    show_explanation(explanation)
                    TOTAL_BLINKS = 0  # Reset counter

        cv2.putText(frame, f'Blinks: {TOTAL_BLINKS}', (30, 50), FONT, 1, (0, 255, 0), 2)

    cv2.imshow('Blink Detection', frame)
    if cv2.waitKey(2) == 27:
        break

video_capture.release()
cv2.destroyAllWindows()
