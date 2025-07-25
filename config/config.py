import os

# API Configuration
MS_NAME = os.environ.get('MS_NAME', 'ms-detection')
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Kafka Configuration
KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost')
KAFKA_PORT = int(os.environ.get('KAFKA_PORT', '5996'))
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'detections')
KAFKA_TOPIC_DLQ = os.environ.get('KAFKA_TOPIC_DLQ', 'detections_dl')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'detections')
KAFKA_OFFSET_RESET = os.environ.get('KAFKA_OFFSET_RESET', 'earliest')
