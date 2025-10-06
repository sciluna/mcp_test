"""General-purpose helpers shared across adapters."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict


def greet(name: str) -> str:
    """Return a friendly greeting for the supplied name."""
    return f"Hello, {name}!"


def get_time() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def health() -> Dict[str, str]:
    """Provide a minimal health payload for diagnostics."""
    return {"status": "ok"}
