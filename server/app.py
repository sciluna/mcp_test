"""FastMCP application wiring for the server adapter package."""

from __future__ import annotations

from fastmcp import FastMCP
from .registry import register_all

from importlib.metadata import version, PackageNotFoundError

import tomllib
import pathlib


def _load_version():
    p = pathlib.Path(__file__).parent.parent / "pyproject.toml"
    with open(p, "rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


def create_app() -> FastMCP:
    """Create a FastMCP instance and register all available tools."""
    mcp = FastMCP(f"cdbai-mcp: {__version__}, cdbai_chat: {__cdbai_version__}", stateless_http=True)
    register_all(mcp)
    return mcp


try:
    __cdbai_version__ = version("cdbai")
except PackageNotFoundError:
    __cdbai_version__ = "0.0.x"

__version__ = _load_version()

if __name__ == "__main__":
    app = create_app()
    app.run(transport="http", host="0.0.0.0", port=8000)
