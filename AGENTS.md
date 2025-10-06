# Repository Guidelines

## Project Structure & Module Organization
- `tools/` holds the framework-agnostic helpers (assets, general utilities, plotting, and `search.py` retriever wrappers). Keep this package independent of FastMCP so it remains portable across CLIs, notebooks, or services.
- `server/` adapts `tools` into FastMCP tools: `server/app.py` builds the app, `server/registry.py` registers adapters, and `server/adapters/` exposes each functional area (general adapter now handles greetings, health, search/fetch helpers, and asset tools; plotting and search stay isolated).
- Project metadata lives in `pyproject.toml`; build packaging uses the root `Dockerfile`. Populate runtime configuration in `.env` with project-specific values.

## Build, Test, and Development Commands
- `uv sync --extra mcp` — install the base `tools` dependencies plus the FastMCP/AWS extras for local development.
- `uv run python -m server.app` — launch the FastMCP HTTP server on port 8000 using the adapters wired through `registry.py`.
- `docker build -t fastmcp-time . && docker run --rm -p 8000:8000 fastmcp-time` — containerized build/run path mirroring deployment.

## Coding Style & Naming Conventions
- Adhere to PEP 8 with 4-space indentation; use snake_case for functions (`generate_sine_wave_plot`) and UPPER_SNAKE_CASE constants (`STAR_IMAGE_URL`).
- Keep `tools` functions pure and deterministic, returning raw data structures or bytes; encapsulate side effects (S3 uploads, tool decoration) inside `server/adapters`.
- Provide succinct docstrings and type hints for public helpers so they remain reusable beyond FastMCP.
- Search wrappers in `tools/search.py` should remain thin layers over `gpt-researcher`, handling only normalization and letting credentials flow from environment variables.

## Testing Guidelines
- Mirror the `tools` layout under `tests/` (e.g., `tests/plotting/test_sine_wave.py`, `tests/search/test_duckduckgo.py`) and target both happy-path and error-path behavior (`ValueError` on invalid sample rates, missing API keys).
- Use `pytest`; add it to `pyproject.toml` if not already present, and execute suites with `uv run pytest`.
- For adapters that reach external services, isolate integration checks or mock AWS clients to keep unit tests fast and deterministic.

## Commit & Pull Request Guidelines
- Start commit subjects with an imperative verb (`Add MCP adapter for tools.assets`) and include rationale or side effects in the body when helpful.
- Reference related issues in the footer (`Refs #123`, `Fixes #123`) and document new environment variables or dependency updates.
- Pull requests should summarize the change set, list local verification steps (commands executed, screenshots of generated plots), and highlight infrastructure adjustments.

## Environment & Security Notes
- `.env` lists required runtime variables (`AWS_S3_BUCKET`, `AWS_REGION`) plus search retriever keys (`GOOGLE_API_KEY`, `GOOGLE_CX_KEY`, `SEARX_URL`, `SERPAPI_API_KEY`, `TAVILY_API_KEY`, `NCBI_API_KEY`) with `FIXME` placeholders—replace them before deployment and avoid committing real secrets.
- Do not hardcode AWS credentials; rely on IAM roles or the standard AWS environment variables.
- Redact presigned URLs or bucket names in shared logs unless the bucket is intentionally public.
