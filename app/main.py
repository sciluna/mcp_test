from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastmcp import FastMCP


mcp = FastMCP("TimeTools")


@mcp.tool
def get_time() -> str:
    """
    Return the current time in ISO 8601 (UTC).
    """
    # UTC with trailing 'Z' for clarity
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# Create the MCP ASGI app (served under /mcp)
mcp_app = mcp.http_app(path="/mcp")

app = FastAPI(title="FastMCP Time Server")


@app.get("/health")
def health() -> dict:
    """
    Lightweight health check endpoint.
    """
    return {"status": "ok"}


# Mount the MCP routes (served at /mcp/)
app.mount("/", mcp_app)
