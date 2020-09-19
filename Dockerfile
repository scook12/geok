FROM python:3.7-slim

LABEL author="Sam Cook"

RUN mkdir -p /usr/src/lib
WORKDIR /usr/src/lib

COPY . .
RUN pip install poetry
RUN poetry install