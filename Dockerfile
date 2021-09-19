FROM python:3.8-alpine

COPY . ./

# Install build dependencies
RUN apk update && apk add --no-cache --virtual .build-deps \
  build-base \
  libffi-dev \
  libsodium-dev

# Install dependencies
RUN apk update && apk add --no-cache \
  ca-certificates \
  ffmpeg \
  opus-dev \
  libffi \
  libsodium \
  gcc

# Install pip dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Clean up build dependencies
RUN apk del .build-deps

ENTRYPOINT ["python", "main.py"]
