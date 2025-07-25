import json
import traceback
from config import KAFKA_TOPIC_DLQ


class DLQHandler:
    def __init__(self, producer, logger):
        self.producer = producer
        self.logger = logger
        self.dlq_topic = KAFKA_TOPIC_DLQ

    def send_to_dlq(self, message, exception):
        dlq_content = {
            "topic": message.topic(),
            "partition": message.partition(),
            "offset": message.offset(),
            "key": message.key().decode() if message.key() else None,
            "value": message.value().decode("utf-8"),
            "erreur": str(exception),
            "trace": traceback.format_exc()
        }

        self.producer.produce(
            self.dlq_topic,
            key = message.key(),
            value = json.dumps(dlq_content).encode("utf-8")
        )

        self.producer.flush()

        self.logger.failure("Échec de traitement du message")
        self.logger.send(f"Message envoyé dans la DLQ : {self.dlq_topic}")
