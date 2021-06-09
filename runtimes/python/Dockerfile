FROM inaccel/cli

FROM inaccel/buildpack-deps:grpc AS coral-api

RUN git clone --depth=1 --single-branch https://github.com/inaccel/coral-api /tmp/coral-api \
 && make --directory=/tmp/coral-api src/main/python/inaccel/coral/native/libcoral-api.so

FROM python:3.7

# Install production dependencies.
RUN pip install Flask gunicorn tensorflow==2.1.0 flask-cors

RUN git clone --branch=configurable_allocator --depth=1 --single-branch https://github.com/mattip/numpy /tmp/numpy \
 && git -C /tmp/numpy tag v1.22.0 \
 && pip install /tmp/numpy \
 && rm --force --recursive /tmp/numpy

RUN git clone --depth=1 --single-branch https://github.com/inaccel/numpy-allocator /tmp/numpy-allocator \
 && pip install /tmp/numpy-allocator \
 && rm --force --recursive /tmp/numpy-allocator

RUN --mount=from=coral-api,source=/tmp/coral-api,target=/tmp/coral-api pip install /tmp/coral-api

RUN git clone --depth 1 --single-branch https://github.com/inaccel/keras /tmp/keras \
 && pip install -r /tmp/keras/requirements.txt \
 && pip install /tmp/keras \
 && rm --force --recursive /tmp/keras

RUN apt-get update && apt-get install -y \
        libgl1-mesa-glx && \
        rm -rf /var/lib/apt/lists/*

COPY server.py /

ENV INACCEL_WORKDIR /kubeless
#ENV PYTHONUNBUFFERED True

HEALTHCHECK CMD curl localhost:${PORT:-8080}/healthz

ENTRYPOINT ["python", "/server.py"]
