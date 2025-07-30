import os

# API Configuration
MS_NAME = os.environ.get('MS_NAME', 'ms-detection')
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Face Analyzer Configuration - using direct variables
FACE_ANALYZER_PROVIDERS = os.environ.get('FACE_ANALYZER_PROVIDERS', "['CPUExecutionProvider']")
FACE_ANALYZER_ALLOWED_MODULES = os.environ.get('FACE_ANALYZER_ALLOWED_MODULES',
                                               "['detection', 'recognition', 'genderage', 'landmark_3d', 'pose']")
FACE_ANALYZER_CTX_ID = int(os.environ.get('FACE_ANALYZER_CTX_ID', '0'))
FACE_ANALYZER_DET_SIZE_WIDTH = int(os.environ.get('FACE_ANALYZER_DET_SIZE_WIDTH', '640'))
FACE_ANALYZER_DET_SIZE_HEIGHT = int(os.environ.get('FACE_ANALYZER_DET_SIZE_HEIGHT', '640'))
FACE_ANALYZER_MODEL = os.environ.get('FACE_ANALYZER_MODEL', 'buffalo_l')

# Object Detection Configuration
OBJECT_DETECTION_MODEL = os.environ.get('OBJECT_DETECTION_MODEL', 'yolo11l')

# List of available models
AVAILABLE_FACE_MODELS = ['buffalo_l']
AVAILABLE_OBJECT_MODELS = ['yolo11l', 'yolo11m', 'yolo11n', 'yolo11x', 'yolov8n']

# Kafka Configuration
KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost')
KAFKA_PORT = int(os.environ.get('KAFKA_PORT', '5996'))
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'detections')
KAFKA_TOPIC_DLQ = os.environ.get('KAFKA_TOPIC_DLQ', 'detections_dl')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'detections')
KAFKA_OFFSET_RESET = os.environ.get('KAFKA_OFFSET_RESET', 'earliest')
