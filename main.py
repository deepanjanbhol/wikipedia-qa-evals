"""CLI entry point for Wikipedia QA runner."""

from __future__ import annotations

import argparse

from agent.runner import run_question

VERSION_ALIASES = {
    "v0": "v0_base",
    "v1": "v1_advanced",
    "v2": "v2_rai_guarded",
    # Backward compatibility.
    "v0_baseline": "v0_base",
    "v1_decomposition": "v1_advanced",
    "v2_grounding_abstention": "v2_rai_guarded",
}

DEMO_QUESTIONS = [
    "Who invented the telephone?",
    "Which country was the birthplace of the scientist who discovered penicillin?",
    "What was Einstein's favorite breakfast?",
]


def _resolve_version(version: str) -> str:
    """Resolve short version aliases to canonical prompt version keys."""
    return VERSION_ALIASES.get((version or "").strip(), (version or "").strip() or "v0_base")


def _print_result(result: dict) -> None:
    """Print the required output fields for a single question."""
    print(f"Question: {result.get('question', '')}")

    searches = result.get("searches_used", [])
    print("Searches used:")
    if isinstance(searches, list) and searches:
        for search in searches:
            print(f"- {search}")
    else:
        print("- none")

    sources = result.get("sources", [])
    print("Sources:")
    if isinstance(sources, list) and sources:
        for source in sources:
            print(f"- {source}")
    else:
        print("- none")

    print(f"Answer: {result.get('answer', '')}")
    print(f"Confidence: {result.get('confidence', 'low')}")


def _run_ask(question: str, version: str) -> int:
    """Run one ask command and print response."""
    resolved_version = _resolve_version(version)
    result = run_question(question=question, prompt_version=resolved_version)
    _print_result(result)
    return 0


def _run_demo(version: str) -> int:
    """Run demo with predefined sample questions."""
    resolved_version = _resolve_version(version)
    for idx, question in enumerate(DEMO_QUESTIONS, start=1):
        print(f"--- Demo {idx} ---")
        result = run_question(question=question, prompt_version=resolved_version)
        _print_result(result)
        if idx != len(DEMO_QUESTIONS):
            print()
    return 0


def _build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(description="Wikipedia QA CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ask_parser = subparsers.add_parser("ask", help="Ask one question")
    ask_parser.add_argument("question", type=str, help="Question to ask")
    ask_parser.add_argument("--version", default="v0", help="Prompt version (e.g., v0, v1, v2)")

    demo_parser = subparsers.add_parser("demo", help="Run demo questions")
    demo_parser.add_argument("--version", default="v0", help="Prompt version (e.g., v0, v1, v2)")

    return parser


def main() -> int:
    """Parse args and dispatch commands."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "ask":
        return _run_ask(question=args.question, version=args.version)
    if args.command == "demo":
        return _run_demo(version=args.version)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
