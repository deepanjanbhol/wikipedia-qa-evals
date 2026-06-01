# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| No Failure | 7 |
| Retrieval Failure | 7 |
| Abstention Failure | 5 |
| Generation Failure | 3 |
| Ambiguity Failure | 1 |
| Grounding Failure | 1 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Retrieval Failure | 2 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 3 |
| Ambiguity Failure | 1 |

### comparison

| failure_category | count |
|---|---:|
| No Failure | 2 |
| Generation Failure | 1 |
| Grounding Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 4 |

### multi_hop

| failure_category | count |
|---|---:|
| Generation Failure | 2 |
| No Failure | 1 |
| Retrieval Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| No Failure | 4 |

## Failure Counts By Version

### v0

| failure_category | count |
|---|---:|
| No Failure | 7 |
| Retrieval Failure | 7 |
| Abstention Failure | 5 |
| Generation Failure | 3 |
| Ambiguity Failure | 1 |
| Grounding Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| mh_01 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_03 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_04 | multi_hop | Retrieval Failure | Expected evidence pages were not effectively retrieved. | Improve query rewriting/disambiguation and increase retrieval focus on expected entities. |
| cmp_02 | comparison | Grounding Failure | The faithfulness score is 3 and citation_support is 2, indicating the generated answer contains claims that are not well-grounded in the retrieved context. The context_precision and context_recall are both 1 (high), meaning the right context was retrieved, so Retrieval Failure is ruled out. The model generated content that diverges from or is unsupported by the source material despite having the correct context available. | Constrain generation to only make claims directly supported by the retrieved context. Add a faithfulness check or post-generation verification step that cross-references each claim against the source passages before returning the answer. |
| cmp_04 | comparison | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| amb_01 | ambiguous | Abstention Failure | The system should have abstained given the ambiguous query (should_abstain=true, abstention_quality_passed=false) but proceeded to generate an answer instead. The low scores across context_recall (2), correctness (2), and completeness (1) confirm the generated answer was unreliable, and the abstention_triggered=false flag is direct deterministic evidence that the system failed to withhold when it should have. | Implement a confidence threshold check before generation: when context_precision and context_recall are both low and the query is flagged as ambiguous, trigger an abstention response asking the user to clarify rather than producing a low-quality answer. |
| amb_02 | ambiguous | Abstention Failure | The system should have abstained given the ambiguous query (should_abstain=true, abstention_quality_passed=false) but instead produced a response. The low context_precision (1) and citation_support (2) further confirm the model proceeded without adequate grounding rather than flagging uncertainty. | Implement an abstention gate that checks query ambiguity and context_precision thresholds before generating a response. When should_abstain is true, the system should request clarification or explicitly acknowledge the ambiguity instead of producing a low-confidence answer. |
| amb_03 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the model answered when it should have withheld. The correctness score of 4 (not perfect) combined with the ambiguous slice confirms the model proceeded despite insufficient signal to give a reliable answer. While Ambiguity Failure is a contributing factor, the primary measurable failure is the model's failure to abstain when warranted. | Add an abstention gate that checks for ambiguity signals (low confidence, conflicting context, under-specified query) before generating an answer. When should_abstain conditions are met, the model should return a clarifying question or explicit uncertainty statement rather than a potentially incorrect response. |
| amb_04 | ambiguous | Ambiguity Failure | The low context_precision (2) and context_recall (3) scores indicate the system retrieved marginally relevant context, likely because the query was ambiguous enough to make it unclear what to retrieve. The should_abstain flag is true but abstention_quality_passed is also true, meaning the system did abstain appropriately — so Abstention Failure is not the right call. The core problem is that the ambiguous query led to poor retrieval targeting (context_precision=2), which is the hallmark of Ambiguity Failure rather than a retrieval mechanism failure per se. | Add a query clarification or disambiguation step before retrieval. When ambiguity is detected, prompt for clarification or expand the query into multiple interpretations and retrieve against each, then merge or present options to the user. |
| ie_01 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision scored 1, indicating the retrieval step failed to surface relevant documents. Despite high scores on faithfulness, recall, and correctness, the low context_precision and missing page hit confirm that the retrieved context was not precise or relevant enough to support the answer reliably. The should_abstain flag is true but abstention_triggered is false, which is a downstream consequence of poor retrieval — the system had insufficient evidence yet still produced an answer because it did not recognize the retrieval failure. | Improve retrieval precision by tuning the search index, query rewriting, or re-ranking pipeline so that the top retrieved passages are genuinely relevant. Additionally, add a post-retrieval confidence gate that checks context_precision scores and triggers abstention when the retrieved evidence is insufficient. |
| ie_02 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant documents. Despite this, the model still produced a confident answer (abstention_triggered=false) rather than flagging insufficient evidence. The root cause is that retrieval did not return useful context, which cascades into the grounding problem. | Improve retrieval recall by expanding the search query, adding fallback retrieval strategies, or lowering the similarity threshold so that relevant documents are surfaced before generation proceeds. |
| ie_03 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision and context_recall are both scored at 1, indicating the retrieval step failed to surface relevant evidence. Despite should_abstain being true and abstention_quality_passed being true, the root cause is that the retrieval pipeline did not return useful context, which is what forced the abstention scenario in the first place. | Improve the retrieval component by expanding the search corpus, tuning the query rewriting strategy, or increasing the number of retrieved passages (search_count was only 1) so that sufficient evidence can be found before deciding to abstain. |
| ie_04 | insufficient_evidence | Retrieval Failure | Expected evidence pages were not effectively retrieved. | Improve query rewriting/disambiguation and increase retrieval focus on expected entities. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Retrieval Failure | The context_precision score of 1 and context_recall score of 2 indicate that the retrieval step failed to surface relevant supporting documents. Despite page_hit being true, the retrieved context was largely irrelevant (low precision) and missed most of the needed information (low recall). The low citation_support score of 3 further confirms the generated answer lacked grounding in properly retrieved material. The system should have abstained (should_abstain=true) but didn't trigger abstention, which is a downstream consequence of the retrieval failure providing insufficient signal to trigger abstention thresholds. | Improve the retrieval pipeline by tuning relevance ranking, expanding the query, or using hybrid search to surface higher-quality context. Additionally, set abstention thresholds that trigger when context_precision and context_recall fall below acceptable minimums, so the system declines to answer when retrieved evidence is insufficient. |
| adv_03 | adversarial | Retrieval Failure | The deterministic snapshot shows page_hit=false and context_precision=1 and context_recall=2, indicating the retrieval step failed to surface relevant supporting documents. Despite this, the model did not abstain (abstention_triggered=false) and produced a high-scoring answer (correctness=5, completeness=5), which means it generated a response without grounded retrieved evidence — but the root cause is the upstream retrieval failing to return the right content (should_abstain=true was triggered by poor retrieval quality). | Improve the retrieval pipeline to increase recall and precision for adversarial queries — e.g., by using query rewriting, hybrid search, or re-ranking. Additionally, enforce abstention logic when context_recall and context_precision fall below a minimum threshold so the model does not hallucinate answers when retrieval fails. |
| adv_04 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
