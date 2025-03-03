import os
import json
import signal
import logging
from confluent_kafka import Consumer, KafkaError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_config( config_path="config.json" ):
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erreur lors du chargement du fichier de configuration: {e}")
        return {}


config = load_config()

KAFKA_CONFIG = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', config.get("bootstrap_servers", "kafka:9092")),
    'group.id': os.getenv('KAFKA_GROUP_ID', config.get("group_id", "ms-object-detection")),
    'auto.offset.reset': os.getenv('KAFKA_AUTO_OFFSET_RESET', config.get("auto_offset_reset", "earliest"))
}

TOPIC = os.getenv('KAFKA_TOPIC', config.get("topic", "object-detection"))

consumer = Consumer(KAFKA_CONFIG)
consumer.subscribe([TOPIC])

logging.info(f"Consommateur Kafka démarré pour le topic '{TOPIC}'...")

running = True


def signal_handler( sig, frame ):
    global running
    logging.info("Signal reçu, arrêt du consommateur...")
    running = False


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    while running:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                logging.error(f"Erreur Kafka: {msg.error()}")
                break

        try:
            raw_value = msg.value()

            if raw_value is None or raw_value.strip() == b"":
                logging.warning("Message vide reçu, ignoré.")
                continue

            decoded_value = raw_value.decode('utf-8')

            data = json.loads(decoded_value)

            logging.info(f"Message reçu: {data}")

        except json.JSONDecodeError as e:
            logging.error(f"Erreur de décodage JSON: {e} - Message brut: {raw_value}")

        except Exception as e:
            logging.error(f"Erreur inattendue: {e}")

except Exception as e:
    logging.error(f"Erreur inattendue: {e}")

finally:
    consumer.close()
    logging.info("Consommateur arrêté proprement.")
