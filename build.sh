#!/bin/bash
set -e

IMAGE_NAME_PAYMENTS="gustavoalmeidam7/rinhaback-payments-2025"
DOCKERFILE_PAYMENTS="Payments/Dockerfile"

docker build -t "$IMAGE_NAME_PAYMENTS" -f "$DOCKERFILE_PAYMENTS" .

IMAGE_NAME_WORKERS="gustavoalmeidam7/rinhaback-workers-2025"
DOCKERFILE_WORKERS="Workers/Dockerfile"

docker build -t "$IMAGE_NAME_WORKERS" -f "$DOCKERFILE_WORKERS" .
