FROM python:3.12-slim as base

ENV LANG="C.UTF-8" LC_ALL="C.UTF-8" PATH="/home/python/.rye/shims:/home/python/.rye/env:/home/python/.local/bin:$PATH" PIP_NO_CACHE_DIR="false"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 python && \
    useradd  --uid 1000 --gid python --shell /bin/bash --create-home python

USER python

WORKDIR /home/python/trepublic

ENV RYE_INSTALL_OPTION="--yes"
ENV RYE_VERSION="0.27.0"

RUN curl -sSf https://rye-up.com/get | bash

COPY --chown=python:python pyproject.toml README.md /home/python/trepublic/

WORKDIR /home/python/trepublic

RUN rye sync

FROM base as builder

COPY --chown=python:python ./src /home/python/trepublic/src

RUN rye sync && rye build --clean --wheel

FROM python:3.12-alpine3.19 as final

COPY --from=builder /home/python/trepublic/dist/trepublic2json-*-py3-none-any.whl .

RUN pip install trepublic2json-*-py3-none-any.whl