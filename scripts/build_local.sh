#!/bin/sh

cd ..

docker build \
-t killiankopp/ms-object-detection:dev \
--platform=linux/amd64 \
.