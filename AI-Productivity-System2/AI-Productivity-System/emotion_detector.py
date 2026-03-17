from deepface import DeepFace
import cv2

def detect_emotion(frame):

    try:

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = DeepFace.analyze(
            rgb,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend="opencv"
        )

        return result[0]["dominant_emotion"]

    except:
        return "Neutral"