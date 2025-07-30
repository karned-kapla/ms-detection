import os
import importlib
from config.config import (
    FACE_ANALYZER_PROVIDERS, FACE_ANALYZER_ALLOWED_MODULES,
    FACE_ANALYZER_CTX_ID, FACE_ANALYZER_DET_SIZE_WIDTH,
    FACE_ANALYZER_DET_SIZE_HEIGHT, FACE_ANALYZER_MODEL
)
from src.utils.env_utils import parse_list_from_env
from src.face_detection import FaceDetection

# Print default environment variables
print("Default environment variables:")
print(f"FACE_ANALYZER_PROVIDERS: {FACE_ANALYZER_PROVIDERS}")
print(f"FACE_ANALYZER_ALLOWED_MODULES: {FACE_ANALYZER_ALLOWED_MODULES}")
print(f"FACE_ANALYZER_CTX_ID: {FACE_ANALYZER_CTX_ID}")
print(f"FACE_ANALYZER_DET_SIZE_WIDTH: {FACE_ANALYZER_DET_SIZE_WIDTH}")
print(f"FACE_ANALYZER_DET_SIZE_HEIGHT: {FACE_ANALYZER_DET_SIZE_HEIGHT}")
print(f"FACE_ANALYZER_MODEL: {FACE_ANALYZER_MODEL}")

# Test with default values
print("\nCreating FaceDetection with default values...")
face_detection = FaceDetection()
print("FaceDetection created successfully with default values.")

# Test with custom values
print("\nSetting custom environment variables:")
os.environ['FACE_ANALYZER_PROVIDERS'] = "['CUDAExecutionProvider', 'CPUExecutionProvider']"
os.environ['FACE_ANALYZER_ALLOWED_MODULES'] = "['detection', 'recognition']"
os.environ['FACE_ANALYZER_CTX_ID'] = "1"
os.environ['FACE_ANALYZER_DET_SIZE_WIDTH'] = "320"
os.environ['FACE_ANALYZER_DET_SIZE_HEIGHT'] = "320"
os.environ['FACE_ANALYZER_MODEL'] = "buffalo_s"

# Reload the config module to update the variables with the new environment values
import config.config

importlib.reload(config.config)
from config.config import (
    FACE_ANALYZER_PROVIDERS, FACE_ANALYZER_ALLOWED_MODULES,
    FACE_ANALYZER_CTX_ID, FACE_ANALYZER_DET_SIZE_WIDTH,
    FACE_ANALYZER_DET_SIZE_HEIGHT, FACE_ANALYZER_MODEL
)
import src.utils.env_utils

importlib.reload(src.utils.env_utils)

# Print updated environment variables
print(f"FACE_ANALYZER_PROVIDERS: {FACE_ANALYZER_PROVIDERS}")
print(f"FACE_ANALYZER_ALLOWED_MODULES: {FACE_ANALYZER_ALLOWED_MODULES}")
print(f"FACE_ANALYZER_CTX_ID: {FACE_ANALYZER_CTX_ID}")
print(f"FACE_ANALYZER_DET_SIZE_WIDTH: {FACE_ANALYZER_DET_SIZE_WIDTH}")
print(f"FACE_ANALYZER_DET_SIZE_HEIGHT: {FACE_ANALYZER_DET_SIZE_HEIGHT}")
print(f"FACE_ANALYZER_MODEL: {FACE_ANALYZER_MODEL}")

# Reload the face_detection module to ensure it uses the updated variables
import src.face_detection

importlib.reload(src.face_detection)
from src.face_detection import FaceDetection

# Create a new instance with the updated environment variables
print("\nCreating FaceDetection with custom values...")
face_detection = FaceDetection()
print("FaceDetection created successfully with custom values.")
