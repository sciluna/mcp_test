"""FastMCP application wiring for the server adapter package."""

from __future__ import annotations

from fastmcp import FastMCP
from .registry import register_all

import tomllib
from pathlib import Path


def _load_version():
    # Locate pyproject.toml relative to this file
    base_dir = Path(__file__).parent.parent
    pyproject = base_dir / "pyproject.toml"

    # Parse TOML and extract version
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)

    # Support both [project] and [tool.poetry] layouts
    if "project" in data and "version" in data["project"]:
        return data["project"]["version"]
    raise KeyError("version not found in pyproject.toml")


def create_app() -> FastMCP:
    """Create a FastMCP instance and register all available tools."""
    mcp = FastMCP(f"cdbai-mcp: {__version__}", stateless_http=True)
    register_all(mcp)
    return mcp


__version__ = _load_version()

if __name__ == "__main__":
    app = create_app()
    app.run(transport="http", host="0.0.0.0", port=8000)
