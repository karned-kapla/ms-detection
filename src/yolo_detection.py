import requests
from ultralytics import YOLO
import cv2
import numpy as np

from src.models.output import Box, ClassInfo, ClassReport, DetectionResult

from fastapi import HTTPException
from google.cloud import storage
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def load_model( model_name: str ) -> YOLO:
    return YOLO(f"models/{model_name}.pt")


def add_shape( image: np.ndarray, datas: dict ) -> dict:
    datas["shape"] = image.shape
    return datas


def add_speed( results: list, datas: dict ) -> dict:
    datas["speed"] = results[0].speed
    return datas


def add_boxes( model: YOLO, results: list, datas: dict ) -> dict:
    detections = []
    for result in results:
        for box in result.boxes:
            if box.conf[0] > 0.5:
                detections.append(
                    {
                        "xmin": float(box.xyxy[0][0]),
                        "ymin": float(box.xyxy[0][1]),
                        "xmax": float(box.xyxy[0][2]),
                        "ymax": float(box.xyxy[0][3]),
                        "confidence": float(box.conf[0]),
                        "predicted_class": int(box.cls[0]),
                        "name": model.names[int(box.cls[0])]
                    }
                )
    datas["boxes"] = detections
    return datas


def add_classes( model: YOLO, results: list, datas: dict ) -> dict:
    classes = {}
    for result in results:
        for box in result.boxes:
            if box.conf[0] > 0.5:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                if class_id not in classes:
                    classes[class_id] = {
                        "class_name": class_name,
                        "count": 0
                    }

                classes[class_id]["count"] += 1
    datas["classes"] = classes
    return datas


def construct_datas( model: YOLO, results: list, image: np.ndarray ) -> dict:
    datas = {}
    datas = add_shape(image=image, datas=datas)
    datas = add_speed(results=results, datas=datas)
    datas = add_boxes(model=model, results=results, datas=datas)
    datas = add_classes(model=model, results=results, datas=datas)
    return datas


def treat_image( image_bytes: bytes ) -> np.ndarray:
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def download_image_from_bucket( uri: str ) -> bytes:
    if uri.startswith("gs://"):
        return download_image_from_gcs(uri)
    elif uri.startswith("s3://"):
        return download_image_from_s3(uri)
    else:
        raise ValueError("L'URI doit commencer par 'gs://' pour GCS ou 's3://' pour S3")


def download_image_from_gcs( gcs_uri: str ) -> bytes:
    try:
        if gcs_uri.startswith("gs://"):
            gcs_uri = gcs_uri[5:]
        bucket_name, blob_path = gcs_uri.split('/', 1)

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        image_bytes = blob.download_as_bytes()
        return image_bytes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'image : {str(e)}")


def download_image_from_s3( s3_uri: str ) -> bytes:
    try:
        if s3_uri.startswith("s3://"):
            s3_uri = s3_uri[5:]
        bucket_name, object_key = s3_uri.split("/", 1)

        s3_client = boto3.client("s3")

        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        image_bytes = response["Body"].read()

        return image_bytes
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'image : {str(e)}")


def prediction( image_bytes: bytes, model_name: str ) -> DetectionResult:
    image = treat_image(image_bytes)
    model = load_model(model_name)
    results = model.predict(image)
    datas = construct_datas(model=model, results=results, image=image)

    detection_result = DetectionResult(
        shape=datas["shape"],
        speed=datas["speed"],
        boxes=datas["boxes"],
        classes=datas["classes"]
    )

    return detection_result


def uri_file_prediction( uri: str, model_name: str ) -> DetectionResult:
    image_bytes = download_image_from_bucket(uri)
    return prediction(image_bytes, model_name)


def url_file_prediction( url: str, model_name: str ) -> DetectionResult:
    image_bytes = requests.get(url).content
    return prediction(image_bytes, model_name)
