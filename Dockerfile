FROM python:3.12-slim

WORKDIR /app

RUN useradd -m worker

COPY requirements.txt main.py ./
COPY src/ ./src

RUN pip install --no-cache-dir -r requirements.txt

USER worker

ENTRYPOINT ["python", "main.py"]