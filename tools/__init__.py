"""Framework-agnostic utilities used across MCP adapters and other runtimes."""

from .assets import fetch_star_image, get_star_link
from .general import cdbai_chat, get_time, greet, health
from .plotting import generate_sine_wave_plot
from .search import (
    arxiv_search,
    duckduckgo_search,
    google_custom_search,
    pubmed_central_search,
    searx_search,
    semantic_scholar_search,
    serpapi_google,
    tavily_search,
)

__all__ = [
    "fetch_star_image",
    "get_star_link",
    "cdbai_chat",
    "get_time",
    "greet",
    "health",
    "generate_sine_wave_plot",
    "arxiv_search",
    "duckduckgo_search",
    "google_custom_search",
    "pubmed_central_search",
    "searx_search",
    "semantic_scholar_search",
    "serpapi_google",
    "tavily_search",
]
