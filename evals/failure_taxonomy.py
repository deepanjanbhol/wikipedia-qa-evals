"""Failure taxonomy classification for eval diagnostics."""

from __future__ import annotations

import json
import os
from typing import Any

from evals.utils import extract_json_object


FAILURE_CATEGORIES = [
    "Retrieval Failure",
    "Generation Failure",
    "Multi-Hop Failure",
    "Ambiguity Failure",
    "Grounding Failure",
    "Abstention Failure",
    "Inefficient Tool Use",
    "No Failure",
]


_SUGGESTED_FIX = {
    "Retrieval Failure": "Improve query rewriting/disambiguation and increase retrieval focus on expected entities.",
    "Generation Failure": "Tighten answer prompt for directness and verify output format plus relevance constraints.",
    "Multi-Hop Failure": "Force explicit sub-question decomposition and step-wise evidence chaining before synthesis.",
    "Ambiguity Failure": "Add ambiguity detection and require clarification or multi-interpretation retrieval before answering.",
    "Grounding Failure": "Enforce evidence-backed claims and reject unsupported statements before final answer generation.",
    "Abstention Failure": "Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics.",
    "Inefficient Tool Use": "Add query deduplication, stop criteria, and max-search budgeting tied to answer quality.",
    "No Failure": "No major fix needed; maintain current prompt and retrieval configuration.",
}


def _extract_score(metric: Any) -> int | None:
    """Extract numeric score from either int-like value or {'score': ...} payload."""
    if isinstance(metric, dict):
        value = metric.get("score")
    else:
        value = metric
    try:
        score = int(value)
    except Exception:
        return None
    return max(1, min(5, score))


def _normalize_json_result(payload: dict[str, Any]) -> dict[str, str]:
    """Normalize classifier output to required JSON schema."""
    category = payload.get("failure_category", "Generation Failure")
    if category not in FAILURE_CATEGORIES:
        category = "Generation Failure"

    explanation = payload.get("explanation", "Failure classification unavailable.")
    if not isinstance(explanation, str):
        explanation = "Failure classification unavailable."

    suggested_fix = payload.get("suggested_fix", _SUGGESTED_FIX[category])
    if not isinstance(suggested_fix, str):
        suggested_fix = _SUGGESTED_FIX[category]

    return {
        "failure_category": category,
        "explanation": explanation.strip() or "Failure classification unavailable.",
        "suggested_fix": suggested_fix.strip() or _SUGGESTED_FIX[category],
    }


def _claude_tiebreak(
    slice_name: str,
    tags: list[str],
    deterministic_snapshot: dict[str, Any],
    candidate_categories: list[str],
) -> dict[str, str] | None:
    """Use Claude only for unresolved/tied failure decisions."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return None

    try:
        from anthropic import Anthropic
    except Exception:
        return None

    model = os.getenv("ANTHROPIC_JUDGE_MODEL", os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"))
    client = Anthropic(api_key=api_key)

    system_prompt = (
        "You are a failure taxonomy judge for QA evals. "
        "Choose exactly one failure category from the allowed list. "
        "Prefer deterministic evidence and use tags only as tie-break hints. "
        "Respond only in valid JSON. No markdown. No code fences. "
        "Allowed categories: Retrieval Failure, Generation Failure, Multi-Hop Failure, "
        "Ambiguity Failure, Grounding Failure, Abstention Failure, Inefficient Tool Use, No Failure. "
        'Return exactly: {"failure_category":"...","explanation":"...","suggested_fix":"..."}.'
    )

    payload = {
        "slice": slice_name,
        "tags": tags,
        "deterministic_snapshot": deterministic_snapshot,
        "candidate_categories": candidate_categories,
    }

    response = client.messages.create(
        model=model,
        max_tokens=220,
        system=system_prompt,
        messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=True)}],
    )

    parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    parsed = extract_json_object("\n".join(parts).strip())
    if not parsed:
        return None
    return _normalize_json_result(parsed)


def classify_failure(
    *,
    slice_name: str,
    tags: list[str] | None = None,
    should_abstain: bool | None = None,
    page_hit: bool | None = None,
    abstention_triggered: bool | None = None,
    searches_used: list[str] | None = None,
    faithfulness: dict[str, Any] | int | None = None,
    answer_relevancy: dict[str, Any] | int | None = None,
    context_precision: dict[str, Any] | int | None = None,
    context_recall: dict[str, Any] | int | None = None,
    correctness: dict[str, Any] | int | None = None,
    completeness: dict[str, Any] | int | None = None,
    citation_support: dict[str, Any] | int | None = None,
    abstention_quality: dict[str, Any] | None = None,
    use_claude_tiebreak: bool = True,
) -> dict[str, str]:
    """Classify likely failure category from eval metrics.

    Returns JSON-shaped dict:
    {
      "failure_category": "...",
      "explanation": "...",
      "suggested_fix": "..."
    }
    """
    tags = list(tags or [])
    search_count = sum(1 for q in (searches_used or []) if isinstance(q, str) and q.strip())

    faith = _extract_score(faithfulness)
    relev = _extract_score(answer_relevancy)
    cprec = _extract_score(context_precision)
    crec = _extract_score(context_recall)
    corr = _extract_score(correctness)
    comp = _extract_score(completeness)
    cite = _extract_score(citation_support)

    abstain_passed = None
    if isinstance(abstention_quality, dict):
        passed = abstention_quality.get("passed")
        abstain_passed = passed if isinstance(passed, bool) else None

    candidates: list[tuple[str, str]] = []

    # 1) Abstention failures are obvious if expected and behavior mismatches.
    if should_abstain is True and abstention_triggered is False:
        candidates.append(("Abstention Failure", "Expected abstention but answer did not abstain."))
    if should_abstain is False and abstention_triggered is True and (relev is None or relev <= 3):
        candidates.append(("Abstention Failure", "Unnecessary abstention on answerable query."))
    if abstain_passed is False:
        candidates.append(("Abstention Failure", "Abstention quality judge marked behavior as inappropriate."))

    # 2) Retrieval-centric failures.
    if page_hit is False and ((crec is not None and crec <= 3) or (cprec is not None and cprec <= 3)):
        candidates.append(("Retrieval Failure", "Expected evidence pages were not effectively retrieved."))
    elif (crec is not None and crec <= 2) and (cprec is not None and cprec <= 3):
        candidates.append(("Retrieval Failure", "Retrieved context lacks necessary and relevant evidence."))

    # 3) Grounding failures (answer unsupported despite available context).
    if (faith is not None and faith <= 2) and (page_hit is True or (crec is not None and crec >= 3)):
        candidates.append(("Grounding Failure", "Answer claims are weakly supported despite available retrieval evidence."))
    if cite is not None and cite <= 2:
        candidates.append(("Grounding Failure", "Citation support score indicates poor claim-to-evidence grounding."))

    # 4) Slice-specific reasoning failures.
    if slice_name == "multi_hop" and ((crec is not None and crec <= 3) or (corr is not None and corr <= 3)):
        candidates.append(("Multi-Hop Failure", "Multi-hop linkage appears incomplete or incorrectly composed."))

    if slice_name == "ambiguous" and should_abstain is True and abstention_triggered is False:
        candidates.append(("Ambiguity Failure", "Ambiguous query was answered directly without clarification/abstention."))
    elif slice_name == "ambiguous" and (relev is not None and relev <= 2):
        candidates.append(("Ambiguity Failure", "Ambiguous question handling appears misinterpreted or off-target."))

    # 5) Inefficient tool use.
    quality_low = any(v is not None and v <= 3 for v in (corr, comp, relev, faith, crec))
    if search_count >= 5 and quality_low:
        candidates.append(("Inefficient Tool Use", "High search count with weak quality indicates inefficient tool strategy."))

    # 6) Generation failure when retrieval is acceptable but response quality is poor.
    retrieval_ok = (page_hit is True) or ((crec is not None and crec >= 4) and (cprec is not None and cprec >= 3))
    generation_low = any(v is not None and v <= 2 for v in (corr, comp, relev))
    if generation_low and retrieval_ok:
        candidates.append(("Generation Failure", "Retrieved evidence appears adequate but generated answer quality is low."))

    # 7) No failure when strong metrics and no prior signals.
    strong = all(
        v is None or v >= 4 for v in (faith, relev, cprec, crec, corr, comp, cite)
    )
    abstention_ok = (abstain_passed is None) or abstain_passed
    if not candidates and strong and abstention_ok:
        candidates.append(("No Failure", "Metrics indicate healthy retrieval, grounding, and answer behavior."))

    if not candidates:
        candidates.append(("Generation Failure", "No clear deterministic category dominated; defaulting to generation issue."))

    # De-duplicate while preserving order.
    deduped: list[tuple[str, str]] = []
    seen = set()
    for cat, reason in candidates:
        if cat in seen:
            continue
        deduped.append((cat, reason))
        seen.add(cat)
    candidates = deduped

    # Prefer tag-aligned category when deterministic candidates tie.
    selected = candidates[0]
    if len(candidates) > 1 and tags:
        tag_set = {t for t in tags if isinstance(t, str)}
        for cat, reason in candidates:
            if cat in tag_set:
                selected = (cat, reason)
                break

    # Claude fallback only for unresolved multi-candidate cases.
    if use_claude_tiebreak and len(candidates) > 1:
        snapshot = {
            "page_hit": page_hit,
            "abstention_triggered": abstention_triggered,
            "search_count": search_count,
            "scores": {
                "faithfulness": faith,
                "answer_relevancy": relev,
                "context_precision": cprec,
                "context_recall": crec,
                "correctness": corr,
                "completeness": comp,
                "citation_support": cite,
            },
            "should_abstain": should_abstain,
            "abstention_quality_passed": abstain_passed,
        }
        llm_choice = _claude_tiebreak(
            slice_name=slice_name,
            tags=tags,
            deterministic_snapshot=snapshot,
            candidate_categories=[c[0] for c in candidates],
        )
        if llm_choice:
            return llm_choice

    category, reason = selected
    return _normalize_json_result(
        {
            "failure_category": category,
            "explanation": reason,
            "suggested_fix": _SUGGESTED_FIX.get(category, "Tune prompts and retrieval settings based on failing slice."),
        }
    )
