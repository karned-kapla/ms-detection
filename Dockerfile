FROM python:3.12-slim

ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV KAFKA_BOOTSTRAP_SERVERS=kafka:9092
ENV KAFKA_GROUP_ID=ms-object-detection
ENV KAFKA_AUTO_OFFSET_RESET=earliest
ENV KAFKA_TOPIC=object-detection

WORKDIR /app

RUN useradd -m worker

COPY requirements.txt main.py ./
COPY src src

RUN pip install --no-cache-dir -r requirements.txt

USER worker

ENTRYPOINT ["python", "main.py"]

