#!/bin/bash

docker exec $ID poetry config pypi-token.pypi $POETRY_PYPI_TOKEN_PYPI
docker exec $ID poetry publish --build

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push cooksamuel/geok_test:$VERSION
docker push cooksamuel/geok_test:latest
docker logout