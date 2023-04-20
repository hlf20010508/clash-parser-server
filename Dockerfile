FROM python:3.8.16-alpine3.17
WORKDIR /clash-parser-server
COPY ./ ./
RUN pip install --no-cache-dir flask requests