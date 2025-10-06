"""Central registry that wires tools adapters into FastMCP."""

from __future__ import annotations

from fastmcp import FastMCP

from .adapters import assets_adapter, general_adapter, plotting_adapter, search_adapter


def register_all(mcp: FastMCP) -> None:
    """Register every available adapter with the given MCP instance."""
    assets_adapter.register(mcp)
    general_adapter.register(mcp)
    plotting_adapter.register(mcp)
    search_adapter.register(mcp)
