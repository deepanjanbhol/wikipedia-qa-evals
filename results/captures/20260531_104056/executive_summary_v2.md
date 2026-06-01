# Executive Summary

Source: heuristic

Evaluated 1 version(s): v2. Overall correctness=3.792, completeness=3.667, faithfulness=4.042. Version snapshot: v2: correctness=3.792, citation=4.042, page_hit=0.708

## What Went Well

- Citation support is strong (4.042).
- Faithfulness is strong (4.042).

## What Did Not Go Well

- Correctness is moderate (3.792).
- Completeness is moderate (3.667).
- Context precision is weak (2.708).
- Context recall is moderate (3.625).
- Retrieval hit rate needs work (0.708).
- Abstention quality pass rate is low (0.708).

## Recommendations

- Prioritize prompt changes that improve the top failure category and retest across all slices.
- Review low-scoring slice/version combinations to tune decomposition and grounding instructions.
- Track changes with the same dataset and compare per-version reports before promoting a prompt.
