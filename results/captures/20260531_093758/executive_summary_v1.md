# Executive Summary

Source: heuristic

Evaluated 1 version(s): v1. Overall correctness=4.583, completeness=4.458, faithfulness=4.5. Version snapshot: v1: correctness=4.583, citation=4.333, page_hit=0.833

## What Went Well

- Correctness is strong (4.583).
- Completeness is strong (4.458).
- Citation support is strong (4.333).
- Faithfulness is strong (4.5).
- Context recall is strong (4.042).
- Abstention quality pass rate is healthy (0.875).

## What Did Not Go Well

- Context precision is weak (3.167).
- Retrieval hit rate needs work (0.833).
- Top failure category is Abstention Failure (9 items).

## Recommendations

- Prioritize prompt changes that improve the top failure category and retest across all slices.
- Review low-scoring slice/version combinations to tune decomposition and grounding instructions.
- Track changes with the same dataset and compare per-version reports before promoting a prompt.
