"""Deterministic rule-based metrics for evaluation.

These metrics are designed to be stable and reproducible across runs.
"""

from __future__ import annotations

from collections.abc import Iterable


# Deterministic lexical triggers only (no semantic inference).
_ABSTENTION_TRIGGER_MARKERS = (
    "insufficient evidence",
    "not enough evidence",
    "cannot determine",
    "can't determine",
    "unable to determine",
    "unknown",
    "not clearly documented",
    "no reliable evidence",
    "cannot verify",
    "cannot be verified",
    "no evidence",
)


def _normalize_page_name(value: str) -> str:
    """Normalize page-like strings for deterministic comparisons."""
    text = (value or "").strip().lower()
    if not text:
        return ""

    text = text.replace("https://en.wikipedia.org/wiki/", "")
    text = text.replace("http://en.wikipedia.org/wiki/", "")
    text = text.replace("_", " ")
    return " ".join(text.split())


def page_hit_at_k(retrieved_titles: Iterable[str], expected_pages: Iterable[str]) -> bool:
    """Return True if any expected page is found in retrieved titles/pages.

    Comparison is deterministic and case-insensitive after light normalization.
    """
    retrieved_set = {
        _normalize_page_name(title)
        for title in retrieved_titles
        if isinstance(title, str) and _normalize_page_name(title)
    }
    expected_set = {
        _normalize_page_name(page)
        for page in expected_pages
        if isinstance(page, str) and _normalize_page_name(page)
    }

    if not retrieved_set or not expected_set:
        return False
    return bool(retrieved_set.intersection(expected_set))


def abstention_triggered(answer: str) -> bool:
    """Return True when answer text contains explicit abstention trigger phrases.

    This is intentionally lexical and deterministic. It does not evaluate whether
    abstention is semantically appropriate for the question.
    """
    normalized = " ".join((answer or "").strip().lower().split())
    if not normalized:
        return True
    return any(marker in normalized for marker in _ABSTENTION_TRIGGER_MARKERS)


def abstention_consistency(should_abstain: bool, answer: str) -> bool:
    """Return True if deterministic trigger behavior matches expected abstention."""
    return abstention_triggered(answer) == bool(should_abstain)


def search_count(searches_used: Iterable[str]) -> int:
    """Return count of non-empty search queries used."""
    return sum(1 for query in searches_used if isinstance(query, str) and query.strip())
