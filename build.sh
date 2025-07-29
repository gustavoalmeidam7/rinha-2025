#!/bin/bash
set -e

IMAGE_NAME="gustavoalmeidam7-rinha-back-2025"
DOCKERFILE="Dockerfile"

docker build -t "$IMAGE_NAME" -f "$DOCKERFILE" .