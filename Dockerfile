FROM python:3.12-slim

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        wget \
    && rm -rf /var/lib/apt/lists/*

# uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# RUN uv venv

# Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    VIRTUAL_ENV=/workspace/.venv \
    PATH="/workspace/.venv/bin:$PATH"


# Initial workspaces volume
WORKDIR /workspace

# Copy application
COPY 'pyproject.toml' 'uv.lock' '.python-version' /workspace

RUN uv sync --locked

# RUN uv venv


