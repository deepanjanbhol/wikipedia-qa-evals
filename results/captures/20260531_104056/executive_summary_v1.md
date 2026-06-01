# Executive Summary

Source: heuristic

Evaluated 1 version(s): v1. Overall correctness=4.333, completeness=4.208, faithfulness=4.5. Version snapshot: v1: correctness=4.333, citation=4.375, page_hit=0.75

## What Went Well

- Correctness is strong (4.333).
- Completeness is strong (4.208).
- Citation support is strong (4.375).
- Faithfulness is strong (4.5).

## What Did Not Go Well

- Context precision is weak (3.042).
- Context recall is moderate (3.875).
- Retrieval hit rate needs work (0.75).
- Abstention quality pass rate is low (0.833).

## Recommendations

- Prioritize prompt changes that improve the top failure category and retest across all slices.
- Review low-scoring slice/version combinations to tune decomposition and grounding instructions.
- Track changes with the same dataset and compare per-version reports before promoting a prompt.
