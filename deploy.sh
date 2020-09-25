#!/bin/bash
echo "$DOCKER_USERNAME" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push cooksamuel/geok_test:$VERSION
docker push cooksamuel/geok_test:latest