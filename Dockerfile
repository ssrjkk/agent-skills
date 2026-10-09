FROM python:3.12-slim

LABEL maintainer="ssrjkk"
LABEL description="Claude Skills Action - Validate, audit, and catalog Claude Code skills"

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir -e .

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
