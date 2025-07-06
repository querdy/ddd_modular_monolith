FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR .
ENV PYTHONPATH="/:/"

COPY pyproject.toml .
RUN uv pip install --system --no-cache-dir -r pyproject.toml


COPY . .