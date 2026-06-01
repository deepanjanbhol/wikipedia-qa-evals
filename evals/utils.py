"""Shared utility helpers for eval modules."""

from __future__ import annotations

import json
from typing import Any


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract first JSON object from text with tolerant fallbacks."""
    raw = (text or "").strip()
    if not raw:
        return {}

    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    if "```" in raw:
        start = raw.find("```")
        end = raw.rfind("```")
        if end > start:
            body = raw[start + 3 : end].strip()
            if body.lower().startswith("json"):
                body = body[4:].strip()
            try:
                parsed = json.loads(body)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass

    decoder = json.JSONDecoder()
    for idx, char in enumerate(raw):
        if char != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(raw[idx:])
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            continue

    return {}
