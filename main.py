import logging

from src.config_loader import load_config
from src.kafka_consumer import KafkaConsumer
from src.models.signal_handler import SignalHandler

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    config = load_config()
    signal_handler = SignalHandler()
    consumer = KafkaConsumer(config)
    consumer.consume_messages(signal_handler)


if __name__ == "__main__":
    main()
