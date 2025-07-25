import json
import requests

from src.yolo_detection import url_file_prediction


class MessageProcessor:
    def __init__(self, logger):
        self.logger = logger

    def process(self, message):
        value = message.value().decode("utf-8")
        data = json.loads(value)

        result = url_file_prediction(data['url'], data['model_name'])
        result = result.model_dump()

        self.logger.debug(result)

        return result

        # response = requests.post(LOAD_API_URL, json=data, timeout=10)

        # if not response.ok:
        # raise ValueError(f"Erreur HTTP: {response.status_code} - {response.text}")

        # self.logger.api(f"Envoyé à l'API. Result : {response.json()}")

        # return response.json()
