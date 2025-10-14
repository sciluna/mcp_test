"""Search retrievers powered by gpt-researcher."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from gpt_researcher.retrievers import (
    ArxivSearch,
    Duckduckgo,
    GoogleSearch,
    PubMedCentralSearch,
    SearxSearch,
    SemanticScholarSearch,
    SerpApiSearch,
    TavilySearch,
)


def _normalize(items: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """Normalize retriever outputs to dictionaries with title/href/body keys."""
    if not items:
        return []

    normalized: List[Dict[str, Any]] = []
    for entry in items:
        if not isinstance(entry, dict):
            continue
        title = entry.get("title")
        href = entry.get("href") or entry.get("url")
        body = entry.get("body") or entry.get("raw_content")
        if title or href or body:
            normalized.append({"title": title, "href": href, "body": body})
    return normalized


def duckduckgo_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """DuckDuckGo text search (no API key)."""
    retriever = Duckduckgo(query)
    return _normalize(retriever.search(max_results=max_results))


def google_custom_search(
    query: str,
    max_results: int = 7,
    query_domains: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Google Programmable Search (requires GOOGLE_API_KEY and GOOGLE_CX_KEY)."""
    retriever = GoogleSearch(query, headers={}, query_domains=query_domains or None)
    return _normalize(retriever.search(max_results=max_results))


def searx_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """SearxNG meta-search (requires SEARX_URL)."""
    retriever = SearxSearch(query)
    return _normalize(retriever.search(max_results=max_results))


def serpapi_google(
    query: str,
    max_results: int = 7,
    query_domains: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """SerpApi Google results (requires SERPAPI_API_KEY)."""
    retriever = SerpApiSearch(query, query_domains=query_domains or None)
    return _normalize(retriever.search(max_results=max_results))


def tavily_search(
    query: str,
    max_results: int = 10,
    topic: str = "general",
    query_domains: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Tavily search (requires TAVILY_API_KEY)."""
    retriever = TavilySearch(query=query, topic=topic, query_domains=query_domains or None)
    return _normalize(retriever.search(max_results=max_results))


def arxiv_search(query: str, max_results: int = 5, sort: str = "Relevance") -> List[Dict[str, Any]]:
    """arXiv preprint search (no API key required)."""
    retriever = ArxivSearch(query, sort=sort)
    return _normalize(retriever.search(max_results=max_results))


def semantic_scholar_search(
    query: str,
    max_results: int = 20,
    sort: str = "relevance",
) -> List[Dict[str, Any]]:
    """Semantic Scholar academic search (no API key)."""
    retriever = SemanticScholarSearch(query, sort=sort)
    return _normalize(retriever.search(max_results=max_results))


def pubmed_central_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """PubMed Central search (requires NCBI_API_KEY)."""
    retriever = PubMedCentralSearch(query)
    return _normalize(retriever.search(max_results=max_results))

