FROM python:3.12-slim

LABEL maintainer="ssrjkk"
LABEL description="Claude Skills Action - Validate, audit, and catalog Claude Code skills"

# Deterministic locale-free runtime: UTF-8 everywhere (C-locale VMs included),
# no .pyc writes, no pip cache bloat.
ENV PYTHONUTF8=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /workspace

# Runtime deps only (no pytest/mypy/twine in the action image).
COPY requirements-action.txt .
RUN pip install --no-cache-dir -r requirements-action.txt

# .dockerignore keeps this layer to src + scripts + packaging metadata.
COPY . .

RUN pip install --no-cache-dir -e . --no-deps

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
