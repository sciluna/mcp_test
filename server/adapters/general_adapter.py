"""Expose general-purpose helpers as MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from tools import general


def register(mcp: FastMCP) -> None:
    """Register general-purpose tools."""

    @mcp.tool()
    def greet(name: str) -> str:
        return general.greet(name)

    @mcp.tool()
    def get_time() -> str:
        return general.get_time()

    @mcp.tool()
    def health() -> dict:
        return general.health()

    @mcp.tool()
    def search(query: str) -> dict:
        return general.search(query)


    @mcp.tool()
    def fetch(id: str) -> dict:
        return general.fetch(id)
