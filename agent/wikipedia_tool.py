"""Minimal Wikipedia search tool using MediaWiki public APIs."""

from __future__ import annotations

import json
import re
import sys
from html import unescape
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"


def _compact_text(text: str, max_len: int = 420) -> str:
    """Normalize whitespace and truncate text for compact responses."""
    normalized = " ".join(unescape(text or "").split())
    if len(normalized) <= max_len:
        return normalized
    return normalized[: max_len - 1].rstrip() + "…"


def _first_sentences(text: str, sentence_count: int = 2, max_chars: int = 320) -> str:
    """Return up to N sentences with a hard max length cap."""
    normalized = " ".join(unescape(text or "").split())
    if not normalized:
        return ""

    # Basic sentence splitting without external models.
    parts = re.split(r"(?<=[.!?])\s+", normalized)
    parts = [p.strip() for p in parts if p.strip()]

    if parts:
        selected = " ".join(parts[: max(1, sentence_count)])
    else:
        selected = normalized

    if len(selected) <= max_chars:
        return selected
    return selected[: max_chars - 1].rstrip() + "…"


def _fetch_json(params: dict[str, Any], timeout: int = 8) -> dict[str, Any]:
    """Fetch JSON from MediaWiki API and return parsed payload."""
    query = urlencode(params)
    url = f"{WIKIPEDIA_API}?{query}"
    request = Request(
        url,
        headers={
            "User-Agent": "wikipedia-qa-evals/0.1 (educational project)",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def search_wikipedia(query: str, top_k: int = 3) -> dict:
    """Search Wikipedia and return compact, structured JSON results.

    Return shape:
    {
            "schema_version": "1.1",
      "query": "...",
      "results": [
        {
          "title": "...",
          "url": "...",
                    "page_id": "...",
                    "result_rank": 1,
          "summary": "...",
          "evidence_chunks": [{"section": "summary", "text": "..."}]
        }
      ]
    }
    """
    clean_query = (query or "").strip()
    limit = max(1, min(int(top_k), 10))

    if not clean_query:
        return {"schema_version": "1.1", "query": clean_query, "results": []}

    try:
        search_payload = _fetch_json(
            {
                "action": "query",
                "list": "search",
                "srsearch": clean_query,
                "srlimit": limit,
                "format": "json",
                "utf8": 1,
            }
        )

        search_hits = search_payload.get("query", {}).get("search", [])
        if not search_hits:
            return {"schema_version": "1.1", "query": clean_query, "results": []}

        # Keep hit order from search results to preserve relevance.
        titles = [item.get("title", "").strip() for item in search_hits if item.get("title")]
        if not titles:
            return {"schema_version": "1.1", "query": clean_query, "results": []}

        pages_payload = _fetch_json(
            {
                "action": "query",
                "prop": "extracts|info",
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url",
                "redirects": 1,
                "titles": "|".join(titles),
                "format": "json",
                "utf8": 1,
            }
        )

        pages = pages_payload.get("query", {}).get("pages", {})
        by_title: dict[str, dict[str, Any]] = {}
        for page in pages.values():
            title = (page.get("title") or "").strip()
            if title:
                by_title[title] = page

        results = []
        for rank, title in enumerate(titles, start=1):
            page = by_title.get(title)
            if not page:
                continue

            fullurl = page.get("fullurl") or f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            summary = _compact_text(page.get("extract", ""), max_len=420)
            evidence_text = _first_sentences(page.get("extract", ""), sentence_count=2, max_chars=320)

            results.append(
                {
                    "title": title,
                    "url": fullurl,
                    "page_id": str(page.get("pageid", "")),
                    "result_rank": rank,
                    "summary": summary,
                    "evidence_chunks": [
                        {
                            "section": "summary",
                            "text": evidence_text,
                        }
                    ],
                }
            )

            if len(results) >= limit:
                break

        return {"schema_version": "1.1", "query": clean_query, "results": results}

    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        # Graceful failure: return empty results rather than raising.
        return {"schema_version": "1.1", "query": clean_query, "results": []}
    except Exception:
        # Last-resort safety net for unexpected parsing/network errors.
        return {"schema_version": "1.1", "query": clean_query, "results": []}


def wiki_search(query: str) -> dict:
    """Backwards-compatible alias for existing callers."""
    return search_wikipedia(query=query, top_k=3)


if __name__ == "__main__":
    sample_query = " ".join(sys.argv[1:]).strip() or "Who discovered penicillin?"
    output = search_wikipedia(sample_query, top_k=3)
    print(json.dumps(output, indent=2, ensure_ascii=True))
