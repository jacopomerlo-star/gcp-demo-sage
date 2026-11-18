FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --no-dev --no-install-project

COPY src ./src
RUN uv sync --no-dev

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uv run uvicorn sage.webapp.app:app --host 0.0.0.0 --port ${PORT}"] 