"""General-purpose helpers shared across adapters."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from cdbai import cdbai_chat as _cdbai_chat


def greet(name: str) -> str:
    """Return a friendly greeting for the supplied name."""
    return f"Hello, {name}!"


def get_time() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def health() -> Dict[str, str]:
    """Provide a minimal health payload for diagnostics."""
    return {"status": "ok"}


def search(query: str) -> dict:
    """your logic to search your data and return matching IDs"""
    if query is not None:
        return {"ids": ["doc1", "doc2"]}


def fetch(id: str) -> dict:
    """fetch the full record for that id"""
    return {
        "id": id,
        "title": "Title of document",
        "content": "Full content text …",
        "metadata": "data"
    }


def cdbai_chat(prompt: str) -> str:
    """Return the JSON payload from the CDBAI chat service for the supplied prompt."""
    return _cdbai_chat(prompt)
