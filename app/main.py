from datetime import datetime, timezone
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent
import requests

mcp = FastMCP("My MCP Server")

@mcp.tool()
def get_star() -> ImageContent:
    """
    Fetches the star image and returns it in MCP image content format.
    """
    # URL of the star image
    url = "https://raw.githubusercontent.com/cannin/cannin.github.io/refs/heads/master/images/star_big.png"
    resp = requests.get(url)
    resp.raise_for_status()
    img_data = resp.content

    # Optionally: verify it’s PNG, or convert with PIL if needed
    # But for now, just wrap the raw bytes
    img = Image(data=img_data, format="png")
    return img.to_image_content()

@mcp.tool()
def get_star_link() -> str:
    """
    Fetches the star image and returns it in MCP image content format.
    """
    # URL of the star image
    url = "https://raw.githubusercontent.com/cannin/cannin.github.io/refs/heads/master/images/star_big.png"
    return url

@mcp.tool
def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"

@mcp.tool
def get_time() -> str:
    """Return current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

@mcp.tool
def health() -> dict:
    """Lightweight health check tool."""
    return {"status": "ok"}


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
