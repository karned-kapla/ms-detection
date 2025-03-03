#!/bin/sh

cd ..

docker run -d \
--name ms-object-detection \
--network karned \
-e KAFKA_BOOTSTRAP_SERVERS=kafka:9092 \
-v ".:/app" \
killiankopp/ms-object-detection:dev