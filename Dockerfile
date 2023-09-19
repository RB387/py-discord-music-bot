FROM python:3.8-alpine

COPY requirements.txt requirements.txt

RUN apk add --no-cache git

# Install
# 1. build dependencies
# 2. dependencies
# 3. pip dependencies
# must run in one layer for image size optimization
RUN apk add --no-cache --virtual .build-deps \
      build-base \
      libffi-dev \
      libsodium-dev && \
  \
  apk add --no-cache \
      ca-certificates \
      ffmpeg \
      opus-dev \
      libffi \
      libsodium \
      gcc && \
  \
  pip3 install --no-cache-dir -r requirements.txt && \
  apk del .build-deps

COPY . ./

CMD ["python", "main.py"]
