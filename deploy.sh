#!/bin/bash
echo "$DOCKER_USERNAME" | docker login -u "$DOCKER_USERNAME" --pasword-stdin
docker push cooksamuel/geok_test:$VERSION
docker push cooksamuel/geok_test:latest