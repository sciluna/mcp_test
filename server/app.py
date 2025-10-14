"""FastMCP application wiring for the server adapter package."""

from __future__ import annotations

from fastmcp import FastMCP

from .registry import register_all


__version__ = "0.0.5"


def create_app() -> FastMCP:
    """Create a FastMCP instance and register all available tools."""
    mcp = FastMCP(f"cdbai-mcp: {__version__}", stateless_http=True)
    register_all(mcp)
    return mcp


if __name__ == "__main__":
    app = create_app()
    app.run(transport="http", host="0.0.0.0", port=8000)
