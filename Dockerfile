FROM python:3.12-slim

ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092
ENV KAFKA_GROUP_ID=ms-object-detection
ENV KAFKA_AUTO_OFFSET_RESET=earliest
ENV KAFKA_TOPIC=object-detection

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m worker

COPY requirements.txt main.py ./
COPY src src

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/models && \
    curl -L -o /app/models/yolo11n.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt && \
    curl -L -o /app/models/yolo11s.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt && \
    curl -L -o /app/models/yolo11m.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m.pt && \
    curl -L -o /app/models/yolo11l.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11l.pt && \
    curl -L -o /app/models/yolo11x.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt

RUN chown -R worker:worker /app

USER worker

ENTRYPOINT ["python", "main.py"]

