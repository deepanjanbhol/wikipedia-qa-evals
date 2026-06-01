# Evaluation Summary

Versions evaluated: v1, v2

## Overall

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| overall | 48 | 0.729 | 0.479 | 3.417 | 4.271 | 4.271 | 2.875 | 3.75 | 4.062 | 3.938 | 4.208 | 0.771 |

## By Slice

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| adversarial | 10 | 0.6 | 0.0 | 1.4 | 4.8 | 4.9 | 3.1 | 4.4 | 5.0 | 5.0 | 4.8 | 1.0 |
| ambiguous | 8 | 0.875 | 0.25 | 5.625 | 3.25 | 3.75 | 2.625 | 2.875 | 3.625 | 3.0 | 3.25 | 0.5 |
| comparison | 8 | 0.75 | 0.875 | 5.0 | 3.625 | 4.0 | 2.625 | 2.875 | 3.5 | 3.5 | 3.25 | 0.75 |
| insufficient_evidence | 6 | 0.5 | 0.0 | 1.5 | 5.0 | 5.0 | 1.0 | 5.0 | 5.0 | 5.0 | 5.0 | 1.0 |
| multi_hop | 12 | 0.833 | 0.833 | 4.083 | 4.333 | 4.0 | 3.583 | 3.833 | 3.583 | 3.583 | 4.333 | 0.667 |
| simple_factoid | 4 | 0.75 | 1.0 | 1.75 | 5.0 | 4.0 | 4.0 | 3.5 | 3.75 | 3.5 | 5.0 | 0.75 |

## By Complexity

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| easy | 6 | 0.833 | 0.833 | 4.5 | 3.333 | 4.333 | 3.167 | 3.333 | 4.0 | 4.167 | 3.0 | 0.833 |
| hard | 18 | 0.667 | 0.278 | 4.0 | 4.056 | 3.944 | 2.611 | 3.333 | 4.0 | 3.722 | 3.889 | 0.667 |
| medium | 24 | 0.75 | 0.542 | 2.708 | 4.667 | 4.5 | 3.0 | 4.167 | 4.125 | 4.042 | 4.75 | 0.833 |

## By Version

| group | n | page_hit | abstain_consistency | avg_searches | faithfulness | answer_rel | ctx_precision | ctx_recall | correctness | completeness | citation | abstention_quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v1 | 24 | 0.75 | 0.5 | 3.292 | 4.5 | 4.417 | 3.042 | 3.875 | 4.333 | 4.208 | 4.375 | 0.833 |
| v2 | 24 | 0.708 | 0.458 | 3.542 | 4.042 | 4.125 | 2.708 | 3.625 | 3.792 | 3.667 | 4.042 | 0.708 |
