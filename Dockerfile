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
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m worker

COPY requirements.txt main.py ./
COPY config config
COPY src src

RUN pip install --no-cache-dir -r requirements.txt

COPY models models

RUN chown -R worker:worker /app

USER worker

ENTRYPOINT ["python", "main.py"]

