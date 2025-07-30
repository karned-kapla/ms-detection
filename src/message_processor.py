import json
import requests
import numpy as np

from config.config import OBJECT_DETECTION_MODEL, FACE_ANALYZER_MODEL, AVAILABLE_FACE_MODELS, AVAILABLE_OBJECT_MODELS
from src.face_detection import FaceDetection
from src.kafka_client import KafkaClient
from src.yolo_detection import url_file_prediction

def convert_numpy_types(obj):
    """
    Recursively convert numpy types to standard Python types for JSON serialization.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    else:
        return obj


class MessageProcessor:
    def __init__(self, logger):
        self.logger = logger

    def process(self, message):
        value = message.value().decode("utf-8")
        data = json.loads(value)

        if data["model"] == "object":
            data["model"] = OBJECT_DETECTION_MODEL

        if data["model"] == "face":
            data["model"] = FACE_ANALYZER_MODEL

        is_face_model = data["model"] in AVAILABLE_FACE_MODELS

        if not is_face_model and data["model"] not in AVAILABLE_OBJECT_MODELS:
            self.logger.error(f"Model not supported: {data['model']}")
            raise ValueError("Model not supported !")

        if is_face_model:
            face_encoder = FaceDetection(model_name = data["model"])
            result = face_encoder.url_file_prediction(url = data["url"])
            self.logger.debug(f"Face prediction: {result}")
            result = result.model_dump()
        else:
            result = url_file_prediction(url = data['url'], model = data['model'])
            result = result.model_dump()

        payload = {
            "uuid": data["uuid"],
            "secret": data["secret"],
            "model": data["model"],
            "result": result
        }

        # Convert NumPy types to standard Python types for JSON serialization
        payload = convert_numpy_types(payload)

        for response_item in data["response"]:
            if response_item["canal"] == "api":
                self.logger.api(f"Envoyé à l'API : {response_item['url']}")
                requests.put(url = response_item["url"], json = payload, timeout = 10)
            elif response_item["canal"] == "kafka":
                self.logger.info(f"Message sent to Kafka topic: {response_item['topic']}")
                kafka_client = KafkaClient(self.logger)
                kafka_client.send_message(topic = response_item['topic'], message = payload)

        # Also convert the returned result for consistency
        return convert_numpy_types(result)
