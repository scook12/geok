#!/bin/bash
echo "$DOCKER_USERNAME" | docker login -u "$DOCKER_USERNAME" --pasword-stdin
docker push cooksamuel/geok_test:$TRAVIS_JOB_ID
docker push cooksamuel/geok_test:latest