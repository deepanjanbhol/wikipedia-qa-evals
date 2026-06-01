# Executive Summary

Source: heuristic

Evaluated 3 version(s): v0, v1, v2. Overall correctness=4.667, completeness=4.556, faithfulness=4.5. Version snapshot: v0: correctness=4.708, citation=4.208, page_hit=0.667 | v1: correctness=4.708, citation=4.208, page_hit=0.667 | v2: correctness=4.583, citation=4.25, page_hit=0.625

## What Went Well

- Correctness is strong (4.667).
- Completeness is strong (4.556).
- Citation support is strong (4.222).
- Faithfulness is strong (4.5).
- Context recall is strong (4.0).
- Abstention quality pass rate is healthy (0.875).

## What Did Not Go Well

- Context precision is weak (2.75).
- Retrieval hit rate needs work (0.653).

## Recommendations

- Prioritize prompt changes that improve the top failure category and retest across all slices.
- Review low-scoring slice/version combinations to tune decomposition and grounding instructions.
- Track changes with the same dataset and compare per-version reports before promoting a prompt.
