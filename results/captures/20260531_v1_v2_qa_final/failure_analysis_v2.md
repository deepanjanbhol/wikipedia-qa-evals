# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Abstention Failure | 7 |
| No Failure | 7 |
| Retrieval Failure | 5 |
| Ambiguity Failure | 2 |
| Multi-Hop Failure | 2 |
| Generation Failure | 1 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 4 |
| Retrieval Failure | 1 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Ambiguity Failure | 2 |

### comparison

| failure_category | count |
|---|---:|
| No Failure | 3 |
| Retrieval Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 3 |

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 3 |
| Multi-Hop Failure | 2 |
| Abstention Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| Generation Failure | 1 |
| No Failure | 1 |

## Failure Counts By Version

### v2

| failure_category | count |
|---|---:|
| Abstention Failure | 7 |
| No Failure | 7 |
| Retrieval Failure | 5 |
| Ambiguity Failure | 2 |
| Multi-Hop Failure | 2 |
| Generation Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| sf_01 | simple_factoid | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_01 | multi_hop | Multi-Hop Failure | Multi-hop linkage appears incomplete or incorrectly composed. | Force explicit sub-question decomposition and step-wise evidence chaining before synthesis. |
| mh_03 | multi_hop | Abstention Failure | The system abstained (abstention_triggered=true) when it should not have (should_abstain=false). Despite 11 search attempts, it failed to synthesize the retrieved context into an answer, incorrectly concluding it lacked sufficient information. The low context_precision and context_recall scores indicate retrieval was poor, but the primary failure mode is the unwarranted abstention rather than a complete retrieval gap. | Tune the abstention threshold so the system attempts to synthesize a best-effort answer when partial evidence is available. Additionally, improve the multi-hop retrieval strategy (e.g., iterative sub-query decomposition) so that chained facts are gathered before the confidence check that triggers abstention. |
| mh_05 | multi_hop | Multi-Hop Failure | Multi-hop linkage appears incomplete or incorrectly composed. | Force explicit sub-question decomposition and step-wise evidence chaining before synthesis. |
| cmp_02 | comparison | Retrieval Failure | Despite a page hit, context_precision and context_recall are both scored at 2, indicating the retrieved passages were poorly ranked and insufficiently complete to support the answer well. With 4 search calls, the system used adequate tool attempts but still failed to surface the most relevant context, as evidenced by the low faithfulness score of 3 alongside the low precision/recall. The answer scores high on relevancy and correctness, suggesting the model compensated with parametric knowledge rather than grounded retrieval. | Improve retrieval re-ranking and passage selection to surface higher-precision, higher-recall context chunks for comparison queries. Consider query reformulation or hybrid retrieval to better match the comparative structure of the question. |
| amb_01 | ambiguous | Abstention Failure | The system should have abstained given the ambiguous query (page_hit=false, should_abstain=true, abstention_triggered=false), but instead produced a low-quality response with poor context recall (2) and correctness (2). Despite 8 searches indicating retrieval struggles, the core failure is that the system confidently answered when it lacked sufficient grounding to do so. | Add a confidence-gating layer that checks context recall and context precision scores before generating a response; if both fall below a threshold (e.g., recall<3, precision<4), the system should surface a clarifying question or explicit abstention rather than producing a speculative answer. |
| amb_02 | ambiguous | Abstention Failure | The system triggered abstention (abstention_triggered=true) but abstention_quality_passed=false, meaning the abstention response itself was inadequate — it either failed to properly communicate uncertainty, gave a partial or misleading non-answer, or did not guide the user toward resolution. Despite should_abstain=true being correct, the low completeness (1) and context_recall (2) scores confirm the abstention response left the user without sufficient information. The correctness score of 4 suggests some partial content was attempted, which is inconsistent with a clean abstention. | When abstaining, the system should explicitly state what is ambiguous or unknown, cite what partial information is available, and suggest clarifying questions or alternative queries the user could try. A quality abstention should score high on completeness and citation_support even when declining to give a definitive answer. |
| amb_03 | ambiguous | Ambiguity Failure | The slice is tagged 'ambiguous' and should_abstain is true, yet abstention_triggered is false — the system answered instead of recognizing the ambiguous query required clarification or abstention. The correctness and completeness scores of 4 (not 5) confirm the answer was not fully reliable given the ambiguity. This is a classic Ambiguity Failure: the system failed to detect or handle the underspecified input, producing a definitive answer where it should have sought clarification or abstained. | Add an ambiguity-detection pre-processing step that identifies underspecified or multi-interpretable queries and routes them to a clarification prompt or controlled abstention path before retrieval and generation proceed. |
| amb_04 | ambiguous | Ambiguity Failure | The query is inherently ambiguous (slice='ambiguous', tag hint 'Ambiguity Failure'), and while scores are acceptable, should_abstain=true with abstention_quality_passed=true means the system did respond rather than seeking clarification on the ambiguity. The root cause is the system failing to detect and surface the ambiguity to the user rather than a retrieval or generation problem. | Add an ambiguity-detection step before retrieval that identifies underspecified queries and prompts the user for clarification before generating a response. |
| ie_01 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision and context_recall are both 1 (minimum), indicating the retrieval pipeline failed to surface relevant evidence. Despite should_abstain being true and abstention_quality_passed being true, the root cause is that the system never retrieved supporting documents, making the evidence insufficient from the start. | Improve retrieval coverage by expanding the index, tuning query reformulation, or adding fallback retrieval strategies so that relevant passages are surfaced before abstention logic is invoked. |
| ie_03 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision scored 1, indicating the retrieval step failed to surface relevant supporting documents. Despite this, the model produced a confident answer (abstention_triggered is false, correctness and faithfulness both score 5), which means the low-quality context was the root cause — the model never had the evidence it needed because retrieval did not return the right page. The should_abstain flag confirms insufficient evidence was available, pointing squarely at the retrieval layer rather than a generation or abstention decision. | Improve retrieval recall and precision by tuning the search query, expanding the index coverage, or using a re-ranker to ensure the relevant page is surfaced before generation proceeds. Add a confidence threshold on context_precision so that when it falls below a minimum value the system either re-queries or routes to abstention. |
| ie_04 | insufficient_evidence | Retrieval Failure | Expected evidence pages were not effectively retrieved. | Improve query rewriting/disambiguation and increase retrieval focus on expected entities. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_03 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_04 | adversarial | Retrieval Failure | context_precision is 1 and context_recall is 2, indicating the retrieval pipeline failed to surface relevant supporting documents (page_hit: false). Despite should_abstain being true and abstention_quality_passed being true, the root cause is that the retrieval returned poor-quality context, which is what triggered the need to abstain in the first place. The generation scores are all high (5), meaning the model performed well given what it received; the problem originates upstream in retrieval. | Improve the retrieval component by tuning the query rewriting, expanding the index coverage, or using hybrid search to increase recall and precision on adversarial queries. Ensuring relevant documents are retrieved would either provide sufficient grounding for a direct answer or supply better context for a calibrated abstention. |
| adv_05 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
