FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends g++ \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir kaggle-environments==1.32.7

WORKDIR /workspace
