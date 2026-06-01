"""Single-agent runner using Anthropic Messages API with tool use."""

from __future__ import annotations

import json
import os
from typing import Any

from .prompt import get_prompt
from .wikipedia_tool import search_wikipedia

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # Keep runner usable even if python-dotenv is not installed.
    pass

DEFAULT_MODEL = "claude-sonnet-4-6"
MAX_TOOL_ITERATIONS = 8
MAX_TOKENS = 2048


def _to_text(content_blocks: list[Any]) -> str:
    """Join assistant text blocks into a single string."""
    parts: list[str] = []
    for block in content_blocks:
        block_type = getattr(block, "type", None)
        if block_type == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(p for p in parts if p).strip()


def _to_assistant_content(content_blocks: list[Any]) -> list[dict[str, Any]]:
    """Convert SDK content blocks into request-compatible dicts."""
    serialized: list[dict[str, Any]] = []
    for block in content_blocks:
        block_type = getattr(block, "type", None)
        if block_type == "text":
            serialized.append({"type": "text", "text": getattr(block, "text", "") or ""})
        elif block_type == "tool_use":
            serialized.append(
                {
                    "type": "tool_use",
                    "id": getattr(block, "id", ""),
                    "name": getattr(block, "name", ""),
                    "input": getattr(block, "input", {}) or {},
                }
            )
    return serialized


def _extract_json_payload(text: str) -> dict[str, Any]:
    """Extract a JSON object from model text with robust fallbacks."""
    raw = (text or "").strip()
    if not raw:
        return {}

    # Fast path: pure JSON object.
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # Fenced JSON fallback.
    fence_start = raw.find("```")
    if fence_start != -1:
        fence_end = raw.rfind("```")
        if fence_end > fence_start:
            fenced_body = raw[fence_start + 3 : fence_end].strip()
            if fenced_body.lower().startswith("json"):
                fenced_body = fenced_body[4:].strip()
            try:
                data = json.loads(fenced_body)
                if isinstance(data, dict):
                    return data
            except json.JSONDecodeError:
                pass

    # Scan for first decodable JSON object in text.
    decoder = json.JSONDecoder()
    for idx, char in enumerate(raw):
        if char != "{":
            continue
        try:
            candidate, _ = decoder.raw_decode(raw[idx:])
            if isinstance(candidate, dict):
                return candidate
        except json.JSONDecodeError:
            continue

    return {}


def _normalize_final_output(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize final answer JSON into required fields."""
    answer = payload.get("answer")
    if not isinstance(answer, str):
        answer = ""

    sources_raw = payload.get("sources", [])
    sources = [s for s in sources_raw if isinstance(s, str) and s.strip()] if isinstance(sources_raw, list) else []

    confidence = payload.get("confidence", "low")
    if confidence not in {"high", "medium", "low"}:
        confidence = "low"

    searches_raw = payload.get("searches_used", [])
    searches_used = [q for q in searches_raw if isinstance(q, str) and q.strip()] if isinstance(searches_raw, list) else []

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
        "searches_used": searches_used,
    }


def run_question(question: str, prompt_version: str = "v0_base") -> dict:
    """Run one QA turn with tool-use and return structured output."""
    model = os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    base_response = {
        "question": question,
        "answer": "",
        "sources": [],
        "confidence": "low",
        "searches_used": [],
        "retrieved_context": [],
        "raw_messages": [],
    }

    if not api_key:
        base_response["answer"] = "Missing ANTHROPIC_API_KEY in environment."
        return base_response

    try:
        from anthropic import Anthropic
    except Exception:
        base_response["answer"] = "Anthropic SDK not installed. Please install dependencies."
        return base_response

    system_prompt = get_prompt(prompt_version)
    client = Anthropic(api_key=api_key)

    tools = [
        {
            "name": "search_wikipedia",
            "description": "Search Wikipedia and return compact evidence in JSON.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query for Wikipedia."},
                },
                "required": ["query"],
            },
        }
    ]

    messages: list[dict[str, Any]] = [{"role": "user", "content": question}]
    raw_messages: list[dict[str, Any]] = [{"role": "user", "content": question}]
    retrieved_context: list[dict[str, Any]] = []
    searches_used: list[str] = []

    final_text = ""

    try:
        for _ in range(MAX_TOOL_ITERATIONS):
            response = client.messages.create(
                model=model,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                messages=messages,
                tools=tools,
            )

            assistant_content = _to_assistant_content(response.content)
            raw_messages.append({"role": "assistant", "content": assistant_content})
            messages.append({"role": "assistant", "content": assistant_content})

            tool_uses = [b for b in response.content if getattr(b, "type", None) == "tool_use"]
            if not tool_uses:
                final_text = _to_text(response.content)
                break

            tool_result_blocks: list[dict[str, Any]] = []
            for tool_use in tool_uses:
                tool_name = getattr(tool_use, "name", "")
                tool_input = getattr(tool_use, "input", {}) or {}
                query = str(tool_input.get("query", "")).strip()

                if tool_name != "search_wikipedia":
                    tool_payload = {"error": f"Unknown tool requested: {tool_name}", "query": query, "results": []}
                else:
                    tool_payload = search_wikipedia(query=query)

                if query:
                    searches_used.append(query)
                retrieved_context.append(tool_payload)

                tool_result_blocks.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": getattr(tool_use, "id", ""),
                        "content": json.dumps(tool_payload, ensure_ascii=True),
                    }
                )

            user_tool_message = {"role": "user", "content": tool_result_blocks}
            raw_messages.append(user_tool_message)
            messages.append(user_tool_message)
        else:
            final_text = ""
    except Exception as exc:
        base_response["answer"] = f"Runner error: {exc}"
        base_response["retrieved_context"] = retrieved_context
        base_response["searches_used"] = list(dict.fromkeys(searches_used))
        base_response["raw_messages"] = raw_messages
        return base_response

    parsed = _extract_json_payload(final_text)
    normalized = _normalize_final_output(parsed)

    # If model omits searches_used, use observed tool queries.
    if not normalized["searches_used"]:
        normalized["searches_used"] = list(dict.fromkeys(searches_used))

    return {
        "question": question,
        "answer": normalized["answer"],
        "sources": normalized["sources"],
        "confidence": normalized["confidence"],
        "searches_used": normalized["searches_used"],
        "retrieved_context": retrieved_context,
        "raw_messages": raw_messages,
    }
