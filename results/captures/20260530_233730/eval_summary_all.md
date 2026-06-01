# Evaluation Summary

Versions evaluated: v0, v1, v2

## Overall

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 72 | 0.653 | 0.542 | 1.111 | 4.5 | 4.917 | 2.75 | 4.0 | 4.667 | 4.556 | 4.222 | 0.875 |

## By Slice

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| adversarial | 12 | 0.667 | 0.0 | 1.167 | 4.5 | 4.833 | 2.083 | 3.583 | 4.75 | 4.667 | 4.5 | 0.917 |
| ambiguous | 12 | 0.833 | 0.0 | 1.083 | 3.917 | 4.667 | 2.667 | 3.333 | 3.333 | 2.667 | 3.0 | 0.333 |
| comparison | 12 | 1.0 | 1.0 | 1.167 | 4.417 | 5.0 | 3.417 | 4.0 | 5.0 | 5.0 | 4.167 | 1.0 |
| insufficient_evidence | 12 | 0.0 | 0.25 | 1.0 | 5.0 | 5.0 | 1.0 | 4.333 | 4.917 | 5.0 | 5.0 | 1.0 |
| multi_hop | 12 | 0.75 | 1.0 | 1.0 | 4.167 | 5.0 | 2.75 | 3.75 | 5.0 | 5.0 | 3.75 | 1.0 |
| simple_factoid | 12 | 0.667 | 1.0 | 1.25 | 5.0 | 5.0 | 4.583 | 5.0 | 5.0 | 5.0 | 4.917 | 1.0 |

## By Complexity

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| easy | 21 | 0.667 | 0.857 | 1.19 | 4.714 | 5.0 | 3.476 | 4.476 | 5.0 | 5.0 | 4.524 | 1.0 |
| hard | 24 | 0.625 | 0.25 | 1.042 | 3.958 | 4.833 | 2.042 | 3.0 | 4.292 | 4.042 | 3.25 | 0.792 |
| medium | 27 | 0.667 | 0.556 | 1.111 | 4.815 | 4.926 | 2.815 | 4.519 | 4.741 | 4.667 | 4.852 | 0.852 |

## By Version

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v0 | 24 | 0.667 | 0.542 | 1.083 | 4.458 | 4.875 | 2.667 | 4.0 | 4.708 | 4.583 | 4.208 | 0.875 |
| v1 | 24 | 0.667 | 0.542 | 1.042 | 4.5 | 4.958 | 2.75 | 3.958 | 4.708 | 4.583 | 4.208 | 0.875 |
| v2 | 24 | 0.625 | 0.542 | 1.208 | 4.542 | 4.917 | 2.833 | 4.042 | 4.583 | 4.5 | 4.25 | 0.875 |
