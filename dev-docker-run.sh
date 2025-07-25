#!/bin/bash

# Stop and remove the existing container if it exists
docker stop karned-ms-detection || true
docker rm karned-ms-detection || true

# Run the container with local directory mounted
docker run -d \
  --name karned-ms-detection \
  --network karned-network \
  -v "$(pwd):/app" \
  -p 9007:8000 \
  -e MS_NAME=ms-detection \
  -e KAFKA_HOST=karned-kafka \
  -e KAFKA_PORT=9092 \
  -e KAFKA_TOPIC=detections \
  -e KAFKA_TOPIC_DLQ=detections-dl \
  -e KAFKA_GROUP_ID=detections \
  -e KAFKA_OFFSET_RESET=earliest \
  -e LOG_LEVEL=debug \
  killiankopp/ms-detection:1.0.0 \
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "Development container started."
echo "Access the API at http://localhost:9007"
echo "To view logs: docker logs karned-ms-detection"
echo "To stop: docker stop karned-ms-detection"
