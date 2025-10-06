"""Central registry that wires tools adapters into FastMCP."""

from __future__ import annotations

from fastmcp import FastMCP

from .adapters import general_adapter, plotting_adapter, search_adapter


def register_all(mcp: FastMCP) -> None:
    """Register every available adapter with the given MCP instance."""
    general_adapter.register(mcp)
    plotting_adapter.register(mcp)
    search_adapter.register(mcp)
