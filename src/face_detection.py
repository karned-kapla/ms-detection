import cv2
import numpy as np
import time
import requests
from insightface.app import FaceAnalysis

from src.models.output import DetectionResult, Speed, Box, ClassReport


def load_image(image_path) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de charger l'image à l'emplacement: {image_path}")
    return image


class FaceDetection:
    def __init__(self):
        # Initialize InsightFace model with more comprehensive analysis
        self.face_analyzer = FaceAnalysis(providers = ['CPUExecutionProvider'],
                                          allowed_modules = ['detection', 'recognition', 'genderage'])
        self.face_analyzer.prepare(ctx_id = 0, det_size = (640, 640))

    def detect_faces(self, image):
        # Timing for preprocessing
        preprocess_start = time.time()
        # InsightFace works with BGR images (OpenCV default), so no conversion needed
        preprocess_time = (time.time() - preprocess_start) * 1000  # Convert to milliseconds

        # Timing for inference
        inference_start = time.time()
        faces = self.face_analyzer.get(image)
        inference_time = (time.time() - inference_start) * 1000  # Convert to milliseconds

        # Timing for postprocessing
        postprocess_start = time.time()

        # Create the detection result in the required format
        boxes = []
        classes = {}

        # Add face class info
        face_class_id = 0
        face_class_name = "face"
        classes[face_class_id] = ClassReport(class_name = face_class_name, count = 0)

        if len(faces) > 0:
            for face in faces:
                # Get bounding box
                bbox = face.bbox.astype(int)
                xmin, ymin, xmax, ymax = bbox

                # Create additional info dictionary with InsightFace data
                additional_info = {
                    "gender": getattr(face, "gender", None),
                    "age": float(attr) if (attr := getattr(face, "age", None)) is not None else None,
                    "embedding": attr.tolist() if (attr := getattr(face, "embedding", None)) is not None else None,
                    "kps": attr.tolist() if (attr := getattr(face, "kps", None)) is not None else None,
                    "landmark_3d_68": attr.tolist() if (attr := getattr(face, "landmark_3d_68",
                                                                        None)) is not None else None,
                    "pose": attr.tolist() if (attr := getattr(face, "pose", None)) is not None else None
                }

                # Add box to the list
                boxes.append(Box(
                    xmin = float(xmin),
                    ymin = float(ymin),
                    xmax = float(xmax),
                    ymax = float(ymax),
                    confidence = float(face.det_score),
                    predicted_class = face_class_id,
                    name = face_class_name,
                    additional_info = additional_info
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
        # InsightFace doesn't require explicit cleanup
        pass
