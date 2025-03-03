import os
import json
import logging


def load_config( config_path="config.json" ):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        logging.error(f"Erreur lors du chargement du fichier de configuration: {e}")
        config = {}

    return {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', config.get("bootstrap_servers", "kafka:9092")),
        'group.id': os.getenv('KAFKA_GROUP_ID', config.get("group_id", "ms-object-detection")),
        'auto.offset.reset': os.getenv('KAFKA_AUTO_OFFSET_RESET', config.get("auto_offset_reset", "earliest")),
        'topic': os.getenv('KAFKA_TOPIC', config.get("topic", "object-detection"))
    }
