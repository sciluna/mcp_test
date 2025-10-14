# syntax=docker/dockerfile:1.7-labs
FROM python:3.12-slim-trixie

RUN echo "v0.1"

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends git curl ca-certificates fontconfig fonts-dejavu-core \
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
    uv sync --no-dev --extra mcp

# Copy project packages
COPY tools ./tools
COPY server ./server

# Copy fonts
COPY fonts/*.ttf /usr/share/fonts/truetype/custom/
RUN fc-cache -f -v

# Document the port; publish with -p at runtime
EXPOSE 8000

# Run the FastMCP app
CMD ["uv", "run", "python", "-m", "server.app"]
