#!/bin/bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push cooksamuel/geok_test:$VERSION
docker push cooksamuel/geok_test:latest
docker logout