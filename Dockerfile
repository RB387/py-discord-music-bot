FROM python:3.8-alpine

COPY requirements.txt requirements.txt

# Install
# 1. build dependencies
# 2. dependencies
# 3. pip dependencies
# must run in one layer for image size optimization
RUN apk add --no-cache --virtual .build-deps \
      build-base==0.5-r2 \
      libffi-dev==3.3-r2 \
      libsodium-dev==1.0.18-r0 && \
  \
  apk add --no-cache \
      ca-certificates==20191127-r5 \
      ffmpeg==4.4-r1 \
      opus-dev==1.3.1-r1 \
      libffi==3.3-r2 \
      libsodium==1.0.18-r0 \
      gcc==10.3.1_git20210424-r2 && \
  \
  pip3 install --no-cache-dir -r requirements.txt && \
  apk del .build-deps

COPY . ./

CMD ["python", "main.py"]