"""Asset retrieval helpers with no MCP coupling."""

from __future__ import annotations

from typing import Optional

import requests

STAR_IMAGE_URL = "https://raw.githubusercontent.com/cannin/cannin.github.io/refs/heads/master/images/star_big.png"


def fetch_star_image(url: Optional[str] = None) -> bytes:
    """Download the star image and return the raw PNG bytes."""
    target = url or STAR_IMAGE_URL
    response = requests.get(target, timeout=30)
    response.raise_for_status()
    return response.content


def get_star_link() -> str:
    """Return the canonical URL for the star image asset."""
    return STAR_IMAGE_URL
