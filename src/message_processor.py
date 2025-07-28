import json
import requests

from src.yolo_detection import url_file_prediction


class MessageProcessor:
    def __init__(self, logger):
        self.logger = logger

    def process(self, message):
        value = message.value().decode("utf-8")
        data = json.loads(value)

        if data["model"] == "object":
            data["model"] = "yolo11l"

        if data["model"] not in ["yolo11l", "yolo11m", "yolo11n", "yolo11x", "yolov8n"]:
            self.logger.error(f"Model not supported: {data['model']}")
            raise ValueError("Model not supported !")

        result = url_file_prediction(url = data['url'], model = data['model'])
        result = result.model_dump()

        if data["response"]["canal"] == "api":
            self.logger.api(f"Envoyé à l'API : {data["response"]["url"]}")
            payload = {
                "uuid": data["uuid"],
                "secret": data["secret"],
                "model": data["model"],
                "result": result
            }
            requests.put(data["response"]["url"], json = payload, timeout = 10)

        return result

        # response = requests.post(LOAD_API_URL, json=data, timeout=10)

        # if not response.ok:
        # raise ValueError(f"Erreur HTTP: {response.status_code} - {response.text}")

        # self.logger.api(f"Envoyé à l'API. Result : {response.json()}")

        # return response.json()
