"""Expose search retrievers via FastMCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from tools import search


def register(mcp: FastMCP) -> None:
    """Register search-related tools backed by gpt-researcher retrievers."""

    @mcp.tool(name="duckduckgo_search")
    def duckduckgo_search(query: str, max_results: int = 5):
        return search.duckduckgo_search(query=query, max_results=max_results)

    @mcp.tool(name="google_custom_search")
    def google_custom_search(query: str, max_results: int = 10, query_domains: list[str] | None = None):
        return search.google_custom_search(query=query, max_results=max_results, query_domains=query_domains)

    @mcp.tool(name="searx_search")
    def searx_search(query: str, max_results: int = 10):
        return search.searx_search(query=query, max_results=max_results)

    @mcp.tool(name="serpapi_google")
    def serpapi_google(query: str, max_results: int = 7, query_domains: list[str] | None = None):
        return search.serpapi_google(query=query, max_results=max_results, query_domains=query_domains)

    @mcp.tool(name="tavily_search")
    def tavily_search(
        query: str,
        max_results: int = 10,
        topic: str = "general",
        query_domains: list[str] | None = None,
    ):
        return search.tavily_search(
            query=query,
            max_results=max_results,
            topic=topic,
            query_domains=query_domains,
        )

    @mcp.tool(name="arxiv_search")
    def arxiv_search(query: str, max_results: int = 5, sort: str = "Relevance"):
        return search.arxiv_search(query=query, max_results=max_results, sort=sort)

    @mcp.tool(name="semantic_scholar_search")
    def semantic_scholar_search(query: str, max_results: int = 20, sort: str = "relevance"):
        return search.semantic_scholar_search(query=query, max_results=max_results, sort=sort)

    @mcp.tool(name="pubmed_central_search")
    def pubmed_central_search(query: str, max_results: int = 10):
        return search.pubmed_central_search(query=query, max_results=max_results)
