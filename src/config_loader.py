import os
import json
import logging
from pathlib import Path


def load_config():
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config.json"

    logging.info(f"Loading config from {config_path}")

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        logging.error(f"Erreur lors du chargement du fichier de configuration: {e}")
        config = {}

    logging.info(f"config loaded: {config}")

    return {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', config.get("bootstrap_servers", "kafka:9092")),
        'group.id': os.getenv('KAFKA_GROUP_ID', config.get("group_id", "ms-object-detection")),
        'auto.offset.reset': os.getenv('KAFKA_AUTO_OFFSET_RESET', config.get("auto_offset_reset", "earliest")),
        'topic': os.getenv('KAFKA_TOPIC', config.get("topic", "object-detection"))
    }
