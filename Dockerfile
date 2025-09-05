FROM python:3.10-bullseye

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
    python3-dev \
    python3-pip \
    libgl1 \
    libgl1-mesa-dri \
    libglib2.0-0 \
    curl \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
    
RUN useradd -m worker

COPY requirements.txt main.py ./
COPY config config
COPY src src

RUN pip install --upgrade pip setuptools wheel && pip install -U numpy
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/models && \
    curl -L -o /app/models/yolo11n.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt && \
    curl -L -o /app/models/yolo11s.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt && \
    curl -L -o /app/models/yolo11m.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m.pt && \
    curl -L -o /app/models/yolo11l.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11l.pt && \
    curl -L -o /app/models/yolo11x.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt

# Pre-download InsightFace buffalo_l model
RUN mkdir -p /root/.insightface/models && \
    mkdir -p /app/.insightface/models && \
    python -c "from insightface.app import FaceAnalysis; FaceAnalysis(name='buffalo_l').prepare(ctx_id=0)" && \
    cp -r /root/.insightface/models/* /app/.insightface/models/

RUN chown -R worker:worker /app

USER worker

ENTRYPOINT ["python", "main.py"]
