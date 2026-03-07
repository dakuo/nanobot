"""Web tools: web_search and web_fetch."""

import html
import json
import os
import re
from typing import Any
from urllib.parse import urlparse

import httpx
from loguru import logger

from nanobot.agent.tools.base import Tool

# Shared constants
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36"
MAX_REDIRECTS = 5  # Limit redirects to prevent DoS attacks


def _strip_tags(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def _normalize(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _validate_url(url: str) -> tuple[bool, str]:
    """Validate URL: must be http(s) with valid domain."""
    try:
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            return False, f"Only http/https allowed, got '{p.scheme or 'none'}'"
        if not p.netloc:
            return False, "Missing domain"
        return True, ""
    except Exception as e:
        return False, str(e)


class WebSearchTool(Tool):
    """Search the web using Brave Search API or Exa (fallback)."""

    name = "web_search"
    description = "Search the web. Returns titles, URLs, and snippets."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query"},
            "count": {
                "type": "integer",
                "description": "Results (1-20)",
                "minimum": 1,
                "maximum": 20,
            },
        },
        "required": ["query"],
    }

    def __init__(
        self,
        api_key: str | None = None,
        exa_api_key: str | None = None,
        max_results: int = 5,
        proxy: str | None = None,
    ):
        self._init_api_key = api_key
        self._init_exa_key = exa_api_key
        self.max_results = max_results
        self.proxy = proxy

    @property
    def brave_api_key(self) -> str:
        """Resolve Brave API key at call time so env/config changes are picked up."""
        return self._init_api_key or os.environ.get("BRAVE_API_KEY", "")

    @property
    def exa_api_key(self) -> str:
        """Resolve Exa API key at call time so env/config changes are picked up."""
        return self._init_exa_key or os.environ.get("EXA_API_KEY", "")

    # Keep backward-compat property alias
    @property
    def api_key(self) -> str:
        return self.brave_api_key

    async def execute(self, query: str, count: int | None = None, **kwargs: Any) -> str:
        if self.brave_api_key:
            return await self._search_brave(query, count)
        if self.exa_api_key:
            return await self._search_exa(query, count)
        return (
            "Error: No search API key configured. "
            "Set BRAVE_API_KEY or EXA_API_KEY as an environment variable, "
            "or configure in ~/.nanobot/config.json under tools.web.search "
            "(apiKey for Brave, exaApiKey for Exa). Then restart the gateway."
        )

    async def _search_brave(self, query: str, count: int | None = None) -> str:
        """Search using Brave Search API."""
        try:
            n = min(max(count or self.max_results, 1), 20)
            logger.debug("WebSearch [brave]: {}", "proxy" if self.proxy else "direct")
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                r = await client.get(
                    "https://api.search.brave.com/res/v1/web/search",
                    params={"q": query, "count": n},
                    headers={
                        "Accept": "application/json",
                        "X-Subscription-Token": self.brave_api_key,
                    },
                    timeout=10.0,
                )
                r.raise_for_status()

            results = r.json().get("web", {}).get("results", [])[:n]
            if not results:
                return f"No results for: {query}"

            lines = [f"Results for: {query}\n"]
            for i, item in enumerate(results, 1):
                lines.append(f"{i}. {item.get('title', '')}\n   {item.get('url', '')}")
                if desc := item.get("description"):
                    lines.append(f"   {desc}")
            return "\n".join(lines)
        except httpx.ProxyError as e:
            logger.error("WebSearch [brave] proxy error: {}", e)
            return f"Proxy error: {e}"
        except Exception as e:
            logger.error("WebSearch [brave] error: {}", e)
            return f"Error: {e}"

    async def _search_exa(self, query: str, count: int | None = None) -> str:
        """Search using Exa API. Supports category='research paper' for academic queries."""
        try:
            n = min(max(count or self.max_results, 1), 20)
            logger.debug("WebSearch [exa]: {}", "proxy" if self.proxy else "direct")

            payload: dict[str, Any] = {
                "query": query,
                "numResults": n,
                "type": "auto",
            }
            # Auto-detect academic queries and use Exa's research paper category
            academic_signals = (
                "pubmed",
                "scholar",
                "systematic review",
                "meta-analysis",
                "clinical trial",
                "randomized",
                "cohort",
                "longitudinal",
                "doi.org",
                "arxiv",
                "bioRxiv",
                "medRxiv",
            )
            if any(signal in query.lower() for signal in academic_signals):
                payload["category"] = "research paper"

            async with httpx.AsyncClient(proxy=self.proxy) as client:
                r = await client.post(
                    "https://api.exa.ai/search",
                    json=payload,
                    headers={
                        "x-api-key": self.exa_api_key,
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    timeout=15.0,
                )
                r.raise_for_status()

            results = r.json().get("results", [])[:n]
            if not results:
                return f"No results for: {query}"

            lines = [f"Results for: {query}\n"]
            for i, item in enumerate(results, 1):
                title = item.get("title", "")
                url = item.get("url", "")
                lines.append(f"{i}. {title}\n   {url}")
                meta_parts = []
                if pub_date := item.get("publishedDate"):
                    meta_parts.append(pub_date[:10])
                if author := item.get("author"):
                    meta_parts.append(author)
                if meta_parts:
                    lines.append(f"   ({', '.join(meta_parts)})")
            return "\n".join(lines)
        except httpx.ProxyError as e:
            logger.error("WebSearch [exa] proxy error: {}", e)
            return f"Proxy error: {e}"
        except Exception as e:
            logger.error("WebSearch [exa] error: {}", e)
            return f"Error: {e}"


class WebFetchTool(Tool):
    """Fetch and extract content from a URL using Readability."""

    name = "web_fetch"
    description = "Fetch URL and extract readable content (HTML → markdown/text)."
    parameters = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "URL to fetch"},
            "extractMode": {"type": "string", "enum": ["markdown", "text"], "default": "markdown"},
            "maxChars": {"type": "integer", "minimum": 100},
        },
        "required": ["url"],
    }

    def __init__(self, max_chars: int = 50000, proxy: str | None = None):
        self.max_chars = max_chars
        self.proxy = proxy

    async def execute(
        self, url: str, extractMode: str = "markdown", maxChars: int | None = None, **kwargs: Any
    ) -> str:
        from readability import Document

        max_chars = maxChars or self.max_chars
        is_valid, error_msg = _validate_url(url)
        if not is_valid:
            return json.dumps(
                {"error": f"URL validation failed: {error_msg}", "url": url}, ensure_ascii=False
            )

        try:
            logger.debug("WebFetch: {}", "proxy enabled" if self.proxy else "direct connection")
            async with httpx.AsyncClient(
                follow_redirects=True,
                max_redirects=MAX_REDIRECTS,
                timeout=30.0,
                proxy=self.proxy,
            ) as client:
                r = await client.get(url, headers={"User-Agent": USER_AGENT})
                r.raise_for_status()

            ctype = r.headers.get("content-type", "")

            if "application/json" in ctype:
                text, extractor = json.dumps(r.json(), indent=2, ensure_ascii=False), "json"
            elif "text/html" in ctype or r.text[:256].lower().startswith(("<!doctype", "<html")):
                doc = Document(r.text)
                content = (
                    self._to_markdown(doc.summary())
                    if extractMode == "markdown"
                    else _strip_tags(doc.summary())
                )
                text = f"# {doc.title()}\n\n{content}" if doc.title() else content
                extractor = "readability"
            else:
                text, extractor = r.text, "raw"

            truncated = len(text) > max_chars
            if truncated:
                text = text[:max_chars]

            return json.dumps(
                {
                    "url": url,
                    "finalUrl": str(r.url),
                    "status": r.status_code,
                    "extractor": extractor,
                    "truncated": truncated,
                    "length": len(text),
                    "text": text,
                },
                ensure_ascii=False,
            )
        except httpx.ProxyError as e:
            logger.error("WebFetch proxy error for {}: {}", url, e)
            return json.dumps({"error": f"Proxy error: {e}", "url": url}, ensure_ascii=False)
        except Exception as e:
            logger.error("WebFetch error for {}: {}", url, e)
            return json.dumps({"error": str(e), "url": url}, ensure_ascii=False)

    def _to_markdown(self, html: str) -> str:
        """Convert HTML to markdown."""
        # Convert links, headings, lists before stripping tags
        text = re.sub(
            r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>',
            lambda m: f"[{_strip_tags(m[2])}]({m[1]})",
            html,
            flags=re.I,
        )
        text = re.sub(
            r"<h([1-6])[^>]*>([\s\S]*?)</h\1>",
            lambda m: f"\n{'#' * int(m[1])} {_strip_tags(m[2])}\n",
            text,
            flags=re.I,
        )
        text = re.sub(
            r"<li[^>]*>([\s\S]*?)</li>", lambda m: f"\n- {_strip_tags(m[1])}", text, flags=re.I
        )
        text = re.sub(r"</(p|div|section|article)>", "\n\n", text, flags=re.I)
        text = re.sub(r"<(br|hr)\s*/?>", "\n", text, flags=re.I)
        return _normalize(_strip_tags(text))
