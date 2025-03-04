import json
import logging
from confluent_kafka import Consumer, KafkaError

from src.treat import treat
from src.yolo_detection import url_file_prediction


class KafkaConsumer:
    def __init__( self, config ):
        self.config = config
        self.topic = config['topic']
        self.consumer = Consumer(
            {
                'bootstrap.servers': config['bootstrap.servers'],
                'group.id': config['group.id'],
                'auto.offset.reset': config['auto.offset.reset']
            }
        )
        self.consumer.subscribe([self.topic])
        logging.info(f"Consommateur Kafka démarré pour le topic '{self.topic}'...")

    def consume_messages( self, running ):
        try:
            while running.is_running:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logging.error(f"Erreur Kafka: {msg.error()}")
                        break

                raw_value = ''

                try:
                    raw_value = msg.value()

                    if raw_value is None or raw_value.strip() == b"":
                        logging.warning("Message vide reçu, ignoré.")
                        continue

                    decoded_value = raw_value.decode('utf-8')
                    data = json.loads(decoded_value)
                    logging.info(f"Message reçu: {data}")

                    treat(data)

                except json.JSONDecodeError as e:
                    logging.error(f"Erreur de décodage JSON: {e} - Message brut: {raw_value}")

                except Exception as e:
                    logging.error(f"Erreur inattendue: {e}")

        except Exception as e:
            logging.error(f"Erreur inattendue: {e}")

        finally:
            self.close()

    def close( self ):
        self.consumer.close()
        logging.info("Consommateur Kafka arrêté proprement.")
