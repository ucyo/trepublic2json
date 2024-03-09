FROM python:3.12-slim as base

ENV LANG="C.UTF-8" LC_ALL="C.UTF-8" PATH="/home/python/.rye/shims:/home/python/.rye/env:/home/python/.local/bin:$PATH" PIP_NO_CACHE_DIR="false"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 python && \
    useradd  --uid 1000 --gid python --shell /bin/bash --create-home python

USER python

ENV RYE_INSTALL_OPTION="--yes"
ENV RYE_VERSION="0.27.0"

RUN curl -sSf https://rye-up.com/get | bash

COPY --chown=python:python pyproject.toml README.md /workspaces/trepublic/

WORKDIR /workspaces/trepublic

RUN rye sync

FROM base as builder

RUN rye sync 
RUN rye install .
RUN rye build --clean --wheel

FROM python:3.12-slim as final

COPY --from=builder /workspaces/trepublic/dist/*.whl .

RUN pip install trepublic2json-*-py3-none-any.whl