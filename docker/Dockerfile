FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /repo

COPY repo/ /repo/

RUN apt-get update \
    && apt-get install -y --no-install-recommends git patch \
    && rm -rf /var/lib/apt/lists/* \
    && git init -b main /repo \
    && git -C /repo config user.email "task-builder@local" \
    && git -C /repo config user.name "Task Builder" \
    && git -C /repo add -A \
    && git -C /repo commit -m "Initial vulnerable snapshot" \
    && python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install -e . pytest \
    && useradd -m -s /bin/bash appuser \
    && chown -R appuser:appuser /repo

USER appuser

CMD ["bash"]
