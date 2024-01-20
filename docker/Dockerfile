# syntax = docker/dockerfile:1.2
ARG BASE_CONTAINER=python:3.12-slim

# Build stage
FROM $BASE_CONTAINER AS build

ARG VERSION
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app
COPY README.md /app/
COPY pyproject.toml /app/
COPY src/ /app/src/
RUN pip install --disable-pip-version-check build
RUN SETUPTOOLS_SCM_PRETEND_VERSION=${VERSION} python -m build --wheel -o ./dist/ .

# Final stage
FROM $BASE_CONTAINER

ENV DEBIAN_FRONTEND noninteractive
ENV PIP_ROOT_USER_ACTION=ignore

# remove config avoiding apt caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# install apt packages
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update \
    && apt-get install -y --no-install-recommends build-essential tini \
    && rm -rf /var/lib/apt/lists/*

# add admin user
ENV USER=admin
RUN useradd -ms /bin/bash -u 1000 -g 100 ${USER}
ENV HOME=/home/${USER}
ENV PATH=${HOME}/.local/bin:$PATH
WORKDIR ${HOME}

# declare useful env variables
ENV SERVICE=prototapi.api.main:app
ENV SERVICE_RUNNER=uvicorn
ENV SERVICE_HOST=0.0.0.0
ENV SERVICE_PORT=44444

# install dependencies
COPY --from=build --chown=1000:100 /app/dist /app/dist
RUN --mount=type=cache,target=.cache/pip \
    --mount=type=secret,id=pip.conf,dst=/etc/pip.conf \
    pip install --disable-pip-version-check /app/dist/*.whl \
    && rm -rf /app/dist

# check status
USER ${USER}
RUN ${SERVICE_RUNNER} ${SERVICE} --version

# run application
ENTRYPOINT [ "tini", "-g", "--" ]
CMD ${SERVICE_RUNNER} ${SERVICE} --host ${SERVICE_HOST} --port ${SERVICE_PORT} --loop asyncio
