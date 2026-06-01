# Evaluation Summary

Versions evaluated: v1, v2

## Overall

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 48 | 0.646 | 0.479 | 3.396 | 4.25 | 4.458 | 2.917 | 3.688 | 4.167 | 4.042 | 4.104 | 0.812 |

## By Slice

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| adversarial | 10 | 0.5 | 0.0 | 1.9 | 4.6 | 5.0 | 2.3 | 4.1 | 5.0 | 4.9 | 4.7 | 1.0 |
| ambiguous | 8 | 0.875 | 0.125 | 4.625 | 3.75 | 4.125 | 3.25 | 3.375 | 3.625 | 3.125 | 2.875 | 0.625 |
| comparison | 8 | 0.75 | 0.75 | 5.0 | 4.125 | 3.5 | 3.375 | 3.625 | 3.375 | 3.375 | 4.0 | 0.625 |
| insufficient_evidence | 6 | 0.167 | 0.167 | 1.833 | 5.0 | 5.0 | 1.0 | 4.333 | 5.0 | 5.0 | 5.0 | 1.0 |
| multi_hop | 12 | 0.75 | 0.917 | 4.0 | 4.167 | 4.417 | 3.5 | 3.5 | 3.833 | 3.833 | 4.167 | 0.75 |
| simple_factoid | 4 | 0.75 | 1.0 | 2.0 | 3.75 | 5.0 | 4.0 | 3.0 | 4.5 | 4.25 | 3.75 | 1.0 |

## By Complexity

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| easy | 6 | 0.667 | 0.667 | 5.333 | 3.0 | 3.667 | 3.167 | 3.333 | 3.5 | 3.667 | 2.833 | 0.667 |
| hard | 18 | 0.611 | 0.278 | 3.778 | 4.0 | 4.444 | 2.667 | 3.389 | 4.278 | 4.0 | 4.0 | 0.778 |
| medium | 24 | 0.667 | 0.583 | 2.625 | 4.75 | 4.667 | 3.042 | 4.0 | 4.25 | 4.167 | 4.5 | 0.875 |

## By Version

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v1 | 24 | 0.583 | 0.417 | 3.875 | 4.333 | 4.125 | 2.708 | 3.583 | 3.875 | 3.792 | 4.125 | 0.75 |
| v2 | 24 | 0.708 | 0.542 | 2.917 | 4.167 | 4.792 | 3.125 | 3.792 | 4.458 | 4.292 | 4.083 | 0.875 |
