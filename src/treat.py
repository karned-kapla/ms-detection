import logging

from src.config_loader import load_config
from src.kafka_producer import KafkaProducer
from src.yolo_detection import url_file_prediction


def treat( data ):
    logging.info(f"Data: {data}")
    result = url_file_prediction(data['url'], data['model_name'])
    result = result.model_dump()

    config = load_config()
    producer = KafkaProducer(config)

    topic = f"{config['topic']}_response"
    message = {
        'uuid_detection': data["uuid_detection"],
        'model_name': data["model_name"],
        'result': result,
        'uuid_user': data["uuid_user"],
        'uuid_entity': data["uuid_entity"],
        'uuid_credentials': data["uuid_credentials"],
    }
    producer.send_message(topic, message)

    logging.info(f"Message envoyé sur {topic}")
