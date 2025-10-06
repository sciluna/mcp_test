"""Expose asset helpers from the tools package as MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent

from tools import assets


def register(mcp: FastMCP) -> None:
    """Register asset-related tools with the provided MCP instance."""

    @mcp.tool()
    def get_star() -> ImageContent:
        data = assets.fetch_star_image()
        return Image(data=data, format="png").to_image_content()

    @mcp.tool()
    def get_star_link() -> str:
        return assets.get_star_link()
