# Executive Summary

Source: heuristic

Evaluated 2 version(s): v0, v1. Overall correctness=4.583, completeness=4.458, faithfulness=4.479. Version snapshot: v0: correctness=4.583, citation=4.042, page_hit=0.75 | v1: correctness=4.583, citation=4.333, page_hit=0.833

## What Went Well

- Correctness is strong (4.583).
- Completeness is strong (4.458).
- Citation support is strong (4.188).
- Faithfulness is strong (4.479).
- Abstention quality pass rate is healthy (0.875).

## What Did Not Go Well

- Context precision is weak (2.958).
- Context recall is moderate (3.875).
- Retrieval hit rate needs work (0.792).

## Recommendations

- Prioritize prompt changes that improve the top failure category and retest across all slices.
- Review low-scoring slice/version combinations to tune decomposition and grounding instructions.
- Track changes with the same dataset and compare per-version reports before promoting a prompt.
