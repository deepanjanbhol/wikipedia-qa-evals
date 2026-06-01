# Evaluation Summary

Versions evaluated: v0, v1

## Overall

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 48 | 0.792 | 0.5 | 2.208 | 4.479 | 4.771 | 2.958 | 3.875 | 4.583 | 4.458 | 4.188 | 0.875 |

## By Slice

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| adversarial | 10 | 0.5 | 0.0 | 1.2 | 4.5 | 5.0 | 2.2 | 3.4 | 4.9 | 4.8 | 4.3 | 1.0 |
| ambiguous | 8 | 0.875 | 0.125 | 3.375 | 4.125 | 4.125 | 2.5 | 3.125 | 3.75 | 3.125 | 3.5 | 0.375 |
| comparison | 8 | 1.0 | 0.875 | 3.0 | 3.875 | 4.5 | 3.5 | 3.5 | 4.25 | 4.25 | 3.5 | 0.875 |
| insufficient_evidence | 6 | 0.333 | 0.0 | 1.333 | 5.0 | 5.0 | 1.0 | 5.0 | 5.0 | 5.0 | 5.0 | 1.0 |
| multi_hop | 12 | 1.0 | 1.0 | 2.583 | 4.667 | 5.0 | 3.917 | 4.417 | 5.0 | 5.0 | 4.333 | 1.0 |
| simple_factoid | 4 | 1.0 | 1.0 | 1.0 | 5.0 | 5.0 | 4.75 | 4.0 | 4.25 | 4.25 | 5.0 | 1.0 |

## By Complexity

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| easy | 6 | 1.0 | 0.833 | 3.0 | 3.5 | 4.333 | 3.333 | 3.333 | 4.333 | 4.333 | 3.0 | 0.833 |
| hard | 18 | 0.722 | 0.278 | 2.611 | 4.278 | 4.667 | 2.444 | 3.333 | 4.444 | 4.111 | 3.778 | 0.722 |
| medium | 24 | 0.792 | 0.583 | 1.708 | 4.875 | 4.958 | 3.25 | 4.417 | 4.75 | 4.75 | 4.792 | 1.0 |

## By Version

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v0 | 24 | 0.75 | 0.5 | 1.375 | 4.458 | 4.958 | 2.75 | 3.708 | 4.583 | 4.458 | 4.042 | 0.875 |
| v1 | 24 | 0.833 | 0.5 | 3.042 | 4.5 | 4.583 | 3.167 | 4.042 | 4.583 | 4.458 | 4.333 | 0.875 |
