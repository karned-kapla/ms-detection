from confluent_kafka import Consumer, Producer, KafkaException
from config import KAFKA_TOPIC, KAFKA_HOST, KAFKA_PORT, KAFKA_GROUP_ID
import time


class KafkaClient:
    def __init__(self, logger, max_retries=5, retry_interval=5):
        self.logger = logger
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.consumer = None
        self.producer = Producer({'bootstrap.servers': f"{KAFKA_HOST}:{KAFKA_PORT}"})
        self.topic = KAFKA_TOPIC

    def initialize(self):
        try:
            self.consumer = Consumer(
                {
                    'bootstrap.servers': f"{KAFKA_HOST}:{KAFKA_PORT}",
                    'group.id': KAFKA_GROUP_ID,
                    'auto.offset.reset': 'earliest'
                }
            )
            self.consumer.subscribe([self.topic])

            self.logger.init(f"Worker Kafka listen on '{self.topic}'")
            self.logger.config(f"Kafka: broker={KAFKA_HOST}:{KAFKA_PORT}, group={KAFKA_GROUP_ID}")

            return True
        except Exception as e:
            self.logger.failure(f"Erreur lors de l'initialisation de Kafka: {e}")
            return False

    def get_producer(self):
        return self.producer

    def poll_message(self, timeout=1.0):
        msg = self.consumer.poll(timeout)

        if msg is None:
            return None

        if msg.error():
            raise KafkaException(msg.error())

        return msg

    def commit_message(self, message):
        self.consumer.commit(message)

    def send_message(self, topic, message):
        try:
            self.producer.produce(topic = topic, key = 'file', value = str(message))
            self.producer.flush()
            self.logger.info(f"Message sent to Kafka topic '{self.topic}': {message}")
        except Exception as e:
            self.logger.error(f"Failed to send message to Kafka: {e}")
            raise KafkaException(f"Failed to send message: {e}")

    def connect_with_retries(self):
        retry_count = 0

        while retry_count < self.max_retries:
            try:
                self.logger.retry(f"Connecting to Kafka ({retry_count + 1}/{self.max_retries})...")

                metadata = self.consumer.list_topics(timeout = 10)
                if not metadata:
                    raise KafkaException("Impossible d'obtenir les métadonnées Kafka")

                self.logger.connect("Connected to Kafka")

                return True
            except KafkaException as ke:
                retry_count += 1
                self.logger.error(f"Kafka: {ke}")

                if retry_count >= self.max_retries:
                    self.logger.failure(f"Max try exceed ({self.max_retries}). Cancel.")
                    return False

                self.logger.waiting(f"Retry in {self.retry_interval} seconds...")
                time.sleep(self.retry_interval)
            except Exception as e:
                self.logger.failure(f"Fatal error: {e}")
                return False

        return False

    def close(self):
        if self.consumer:
            self.consumer.close()
            self.logger.disconnect("Close Kafka consumer")
