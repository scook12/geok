FROM python:3.7-slim

LABEL author="Sam Cook"

RUN mkdir -p /usr/src/lib
WORKDIR /usr/src/lib

COPY . .
RUN apt-get update
RUN apt-get install -y curl git
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install