"""Handcrafted RAGAS-style Claude judge metrics (no external ragas dependency)."""

from __future__ import annotations

import json
import os
from typing import Any

from evals.utils import extract_json_object

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # Optional dependency: keep module usable without python-dotenv.
    pass


DEFAULT_JUDGE_MODEL = os.getenv("ANTHROPIC_JUDGE_MODEL", os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"))


def _normalize_scored_result(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize to required schema: score 1-5 and brief explanation."""
    score = payload.get("score", 1)
    try:
        score = int(score)
    except Exception:
        score = 1
    score = max(1, min(5, score))

    explanation = payload.get("explanation", "Invalid judge output.")
    if not isinstance(explanation, str):
        explanation = "Invalid judge output."

    return {
        "score": score,
        "explanation": explanation.strip() or "No explanation provided.",
    }


def _call_claude_judge(system_prompt: str, payload: dict[str, Any]) -> str:
    """Call Anthropic with a strict JSON judge prompt."""
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
        messages=[{"role": "user", "content": json.dumps(payload, ensure_ascii=True)}],
    )

    parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(parts).strip()


def faithfulness(question: str, answer: str, retrieved_context: list[dict[str, Any]]) -> dict[str, Any]:
    """Are answer claims supported by retrieved context?"""
    system_prompt = (
        "You are evaluating factual grounding. "
        "Given Question, Retrieved Wikipedia context, and Generated answer, "
        "determine whether every major factual claim in the answer is supported by retrieved context. "
        "Ignore writing quality. Focus only on factual support. "
        "Score rubric: "
        "5=Every major claim directly supported; "
        "4=Nearly all claims supported; "
        "3=Some unsupported claims; "
        "2=Multiple unsupported claims; "
        "1=Answer largely unsupported. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"score": <1-5>, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "answer": answer,
        "retrieved_context": retrieved_context,
    }
    raw = _call_claude_judge(system_prompt, payload)
    return _normalize_scored_result(extract_json_object(raw))


def answer_relevancy(question: str, answer: str) -> dict[str, Any]:
    """Does the answer address the user question?"""
    system_prompt = (
        "You are evaluating answer relevance. "
        "Given Question and Generated answer, determine how well the answer addresses the user's question. "
        "Ignore factual correctness. Focus only on relevance. "
        "Score rubric: "
        "5=Fully answers the question; "
        "4=Minor omission; "
        "3=Partial answer; "
        "2=Mostly off-topic; "
        "1=Does not answer question. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"score": <1-5>, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "answer": answer,
    }
    raw = _call_claude_judge(system_prompt, payload)
    return _normalize_scored_result(extract_json_object(raw))


def context_precision(question: str, retrieved_context: list[dict[str, Any]]) -> dict[str, Any]:
    """How much retrieved context is relevant to answering the question?"""
    system_prompt = (
        "You are evaluating retrieval precision. "
        "Given Question and Retrieved context, determine how much of retrieved context is relevant to answering the question. "
        "Score rubric: "
        "5=Nearly all context relevant; "
        "4=Mostly relevant; "
        "3=Roughly half relevant; "
        "2=Mostly irrelevant; "
        "1=Largely unrelated. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"score": <1-5>, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "retrieved_context": retrieved_context,
    }
    raw = _call_claude_judge(system_prompt, payload)
    return _normalize_scored_result(extract_json_object(raw))


def context_recall(
    question: str,
    expected_answer: str,
    retrieved_context: list[dict[str, Any]],
) -> dict[str, Any]:
    """Did retrieved context contain the evidence needed to answer correctly?"""
    system_prompt = (
        "You are evaluating retrieval recall. "
        "Given Question, Expected answer, and Retrieved context, "
        "determine whether retrieved context contains all information required to answer correctly. "
        "Do not evaluate the generated answer. Evaluate only whether retrieval gathered enough evidence. "
        "Score rubric: "
        "5=All required evidence retrieved; "
        "4=Nearly all evidence retrieved; "
        "3=Some important evidence missing; "
        "2=Major evidence missing; "
        "1=Required evidence absent. "
        "Respond only in valid JSON. No markdown. No code fences. "
        'Return exactly: {"score": <1-5>, "explanation": "<brief>"}.'
    )
    payload = {
        "question": question,
        "expected_answer": expected_answer,
        "retrieved_context": retrieved_context,
    }
    raw = _call_claude_judge(system_prompt, payload)
    return _normalize_scored_result(extract_json_object(raw))


def score_ragas(sample: dict[str, Any]) -> dict[str, Any]:
    """Compute all handcrafted RAGAS-style metrics for one sample."""
    question = str(sample.get("question", ""))
    expected_answer = str(sample.get("expected_answer", ""))
    answer = str(sample.get("answer", ""))
    retrieved_context = sample.get("retrieved_context", [])
    if not isinstance(retrieved_context, list):
        retrieved_context = []

    return {
        "faithfulness": faithfulness(
            question=question,
            answer=answer,
            retrieved_context=retrieved_context,
        ),
        "answer_relevancy": answer_relevancy(question=question, answer=answer),
        "context_precision": context_precision(
            question=question,
            retrieved_context=retrieved_context,
        ),
        "context_recall": context_recall(
            question=question,
            expected_answer=expected_answer,
            retrieved_context=retrieved_context,
        ),
    }
