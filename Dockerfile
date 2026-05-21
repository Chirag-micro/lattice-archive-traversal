FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /repo

RUN apt-get update \
    && apt-get install -y --no-install-recommends git patch \
    && rm -rf /var/lib/apt/lists/*

COPY repo/ /repo/

RUN find /repo -type d \( \
        -name "__pycache__" -o \
        -name ".pytest_cache" -o \
        -name "*.egg-info" \
    \) -prune -exec rm -rf {} + \
    && find /repo -type f -name "*.pyc" -delete \
    && find /repo -type f -name "*.py" -exec sed -i 's/\r$//' {} + \
    && find /repo -type f -exec chmod 0644 {} + \
    && find /repo -type d -exec chmod 0755 {} +

RUN git config --global user.email "task-builder@local" \
    && git config --global user.name "Task Builder" \
    && rm -rf /repo/.git \
    && git init -q /repo \
    && git -C /repo checkout -q -b main \
    && git -C /repo add -A \
    && git -C /repo commit -qm "Initial vulnerable snapshot"

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install -e . pytest

RUN useradd -m -s /bin/bash appuser \
    && chown -R appuser:appuser /repo

USER appuser

RUN python -m pytest tests/ -q \
    && find /repo -type d \( \
        -name "__pycache__" -o \
        -name ".pytest_cache" -o \
        -name "*.egg-info" \
    \) -prune -exec rm -rf {} + \
    && find /repo -type f -name "*.pyc" -delete \
    && test -z "$(git -C /repo status --short)"

CMD ["python", "-m", "pytest", "tests/", "-q"]
