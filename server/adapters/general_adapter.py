"""Expose general-purpose and asset helpers as MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent

from tools import assets, general


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

    @mcp.tool()
    def cdbai_chat(chat: str) -> str:
        return general.cdbai_chat(chat)

    @mcp.tool()
    def get_star() -> ImageContent:
        data = assets.fetch_star_image()
        return Image(data=data, format="png").to_image_content()

    @mcp.tool()
    def get_star_link() -> str:
        return assets.get_star_link()
