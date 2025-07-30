import cv2
import dlib
import mediapipe as mp
import numpy as np
import os

import time
import requests

from src.models.output import DetectionResult, Speed, Box, ClassReport


def load_image(image_path) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de charger l'image à l'emplacement: {image_path}")
    return image


class FaceDetection:
    def __init__(
            self, face_rec_model_path='models/dlib_face_recognition_resnet_model_v1.dat'
    ):
        face_rec_model_path = os.path.abspath(face_rec_model_path)

        self.face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
        self.mp_face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence = 0.5)

    def detect_faces(self, image):
        # Timing for preprocessing
        preprocess_start = time.time()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        preprocess_time = (time.time() - preprocess_start) * 1000  # Convert to milliseconds

        # Timing for inference
        inference_start = time.time()
        results = self.mp_face_detection.process(rgb_image)
        inference_time = (time.time() - inference_start) * 1000  # Convert to milliseconds

        # Timing for postprocessing
        postprocess_start = time.time()

        # Create the detection result in the required format
        boxes = []
        classes = {}

        # Add face class info
        face_class_id = 1
        face_class_name = "face"
        classes[face_class_id] = ClassReport(class_name = face_class_name, count = 0)

        if results.detections:
            for detection in results.detections:
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                h, w, _ = image.shape

                # Convert relative coordinates to absolute
                xmin = max(0, bbox.xmin * w)
                ymin = max(0, bbox.ymin * h)
                width = bbox.width * w
                height = bbox.height * h
                xmax = min(w, xmin + width)
                ymax = min(h, ymin + height)

                # Add box to the list
                boxes.append(Box(
                    xmin = float(xmin),
                    ymin = float(ymin),
                    xmax = float(xmax),
                    ymax = float(ymax),
                    confidence = float(detection.score[0]),
                    predicted_class = face_class_id,
                    name = face_class_name
                ))

                # Increment face count
                classes[face_class_id].count += 1

        postprocess_time = (time.time() - postprocess_start) * 1000  # Convert to milliseconds

        # Create speed info
        speed = Speed(
            preprocess = preprocess_time,
            inference = inference_time,
            postprocess = postprocess_time
        )

        # Create and return the detection result
        detection_result = DetectionResult(
            shape = [image.shape[0], image.shape[1], image.shape[2]],
            speed = speed,
            boxes = boxes,
            classes = classes
        )

        return detection_result

    def url_file_prediction(self, url: str):
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Erreur lors de la récupération de l'image depuis l'URL: {url}")

        image_bytes = response.content
        image = np.frombuffer(image_bytes, dtype = np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return self.detect_faces(image)

    def close(self):
        self.mp_face_detection.close()
