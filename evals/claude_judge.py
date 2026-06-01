"""Claude-based non-deterministic judges for eval scoring."""

from __future__ import annotations

import json
import os
from typing import Any
from evals.utils import extract_json_object

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # Optional dependency: keep module importable without python-dotenv.
    pass


DEFAULT_JUDGE_MODEL = os.getenv("ANTHROPIC_JUDGE_MODEL", os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"))

def _normalize_scored_result(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a scored judge response to required schema."""
    score = payload.get("score", 1)
    try:
        score = int(score)
    except Exception:
        score = 1
    score = max(1, min(5, score))

    explanation = payload.get("explanation", "Invalid judge output.")
    if not isinstance(explanation, str):
        explanation = "Invalid judge output."

    return {"score": score, "explanation": explanation.strip() or "No explanation provided."}


def _normalize_abstention_result(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize abstention judge response to required schema."""
    passed = payload.get("passed", False)
    if not isinstance(passed, bool):
        passed = False

    explanation = payload.get("explanation", "Invalid judge output.")
    if not isinstance(explanation, str):
        explanation = "Invalid judge output."

    return {"passed": passed, "explanation": explanation.strip() or "No explanation provided."}


def _call_claude_judge(system_prompt: str, user_payload: dict[str, Any]) -> str:
    """Call Anthropic Messages API for judge task and return text content."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return ""

    try:
        from anthropic import Anthropic
    except Exception:
        return ""

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=DEFAULT_JUDGE_MODEL,
        max_tokens=220,
        system=system_prompt,
        messages=[{"role": "user", "content": json.dumps(user_payload, ensure_ascii=True)}],
    )

    parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(parts).strip()


def judge_correctness(question: str, expected_answer: str, answer: str) -> dict[str, Any]:
    """Judge answer correctness on a 1-5 scale."""
    system_prompt = (
        "You are a strict evaluator for QA correctness. "
        "Compare answer against expected_answer for factual correctness and semantic match. "
        "Score 1 means incorrect; 5 means correct. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"score": <1-5>, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "expected_answer": expected_answer,
        "answer": answer,
    }
    raw = _call_claude_judge(system_prompt, payload)
    parsed = extract_json_object(raw)
    return _normalize_scored_result(parsed)


def judge_completeness(question: str, expected_answer: str, answer: str) -> dict[str, Any]:
    """Judge answer completeness on a 1-5 scale."""
    system_prompt = (
        "You are a strict evaluator for QA completeness. "
        "Check whether key expected information is fully covered, not just partially mentioned. "
        "Score 1 means very incomplete; 5 means complete. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"score": <1-5>, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "expected_answer": expected_answer,
        "answer": answer,
    }
    raw = _call_claude_judge(system_prompt, payload)
    parsed = extract_json_object(raw)
    return _normalize_scored_result(parsed)


def judge_citation_support(
    question: str,
    retrieved_context: list[dict[str, Any]],
    answer: str,
    sources: list[str],
) -> dict[str, Any]:
    """Judge whether answer claims are supported by retrieved evidence and cited sources."""
    system_prompt = (
        "You are a strict evaluator for citation support and grounding. "
        "Use only provided retrieved_context and sources to decide whether answer claims are supported. "
        "Score 1 means unsupported; 5 means well-supported. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"score": <1-5>, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_context": retrieved_context,
    }
    raw = _call_claude_judge(system_prompt, payload)
    parsed = extract_json_object(raw)
    return _normalize_scored_result(parsed)


def judge_abstention_quality(
    question: str,
    expected_answer: str,
    answer: str,
    should_abstain: bool,
) -> dict[str, Any]:
    """Judge whether abstention behavior is appropriate for the question."""
    system_prompt = (
        "You are a strict evaluator for abstention quality. "
        "Evaluate semantic appropriateness, not keyword matching. "
        "If should_abstain is true, answer should avoid fabricated specifics and clearly communicate uncertainty/insufficient evidence. "
        "If should_abstain is false, answer should provide a direct answer and not abstain unnecessarily. "
        "Prefer concise, truthful, and useful behavior. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"passed": true/false, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "expected_answer": expected_answer,
        "answer": answer,
        "should_abstain": should_abstain,
    }
    raw = _call_claude_judge(system_prompt, payload)
    parsed = extract_json_object(raw)
    return _normalize_abstention_result(parsed)


def judge_answer(sample: dict[str, Any]) -> dict[str, Any]:
    """Backward-compatible aggregate placeholder for higher-level orchestration.

    This helper runs correctness by default and keeps older callers functional.
    """
    return judge_correctness(
        question=str(sample.get("question", "")),
        expected_answer=str(sample.get("expected_answer", "")),
        answer=str(sample.get("answer", "")),
    )
