# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-slim-trixie

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy project metadata
COPY pyproject.toml ./

# Install dependencies (no lockfile; resolves fresh each time)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# Copy app code
COPY app ./app

# Document the port; publish with -p at runtime
EXPOSE 3011

# Run the FastAPI + FastMCP app with uvicorn via uv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3011"]
