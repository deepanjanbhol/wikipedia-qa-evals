# Executive Summary

Source: heuristic

Evaluated 2 version(s): v1, v2. Overall correctness=4.167, completeness=4.042, faithfulness=4.25. Version snapshot: v1: correctness=3.875, citation=4.125, page_hit=0.583 | v2: correctness=4.458, citation=4.083, page_hit=0.708

## What Went Well

- Citation support is strong (4.104).
- Faithfulness is strong (4.25).

## What Did Not Go Well

- Correctness is moderate (4.167).
- Completeness is moderate (4.042).
- Context precision is weak (2.917).
- Context recall is moderate (3.688).
- Retrieval hit rate needs work (0.646).
- Abstention quality pass rate is low (0.812).

## Recommendations

- Prioritize prompt changes that improve the top failure category and retest across all slices.
- Review low-scoring slice/version combinations to tune decomposition and grounding instructions.
- Track changes with the same dataset and compare per-version reports before promoting a prompt.
