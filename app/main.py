from datetime import datetime, timezone
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

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
