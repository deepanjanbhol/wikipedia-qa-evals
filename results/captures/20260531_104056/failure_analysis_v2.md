# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Abstention Failure | 12 |
| No Failure | 4 |
| Retrieval Failure | 3 |
| Inefficient Tool Use | 2 |
| Multi-Hop Failure | 2 |
| Ambiguity Failure | 1 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 5 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 3 |
| Ambiguity Failure | 1 |

### comparison

| failure_category | count |
|---|---:|
| Inefficient Tool Use | 2 |
| No Failure | 1 |
| Retrieval Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Retrieval Failure | 1 |

### multi_hop

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Multi-Hop Failure | 2 |
| No Failure | 2 |

### simple_factoid

| failure_category | count |
|---|---:|
| No Failure | 1 |
| Retrieval Failure | 1 |

## Failure Counts By Version

### v2

| failure_category | count |
|---|---:|
| Abstention Failure | 12 |
| No Failure | 4 |
| Retrieval Failure | 3 |
| Inefficient Tool Use | 2 |
| Multi-Hop Failure | 2 |
| Ambiguity Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| sf_01 | simple_factoid | Retrieval Failure | page_hit is false and context_precision and context_recall are both 1, indicating the retrieval pipeline failed to surface the relevant document. Despite 4 searches, the correct supporting content was never found, which cascaded into a low-quality answer (correctness and completeness both 1). The faithfulness score of 5 simply means the answer was consistent with the (wrong) retrieved context, confirming the root cause is retrieval, not generation. | Improve retrieval by tuning the query formulation for simple factoid questions, expanding the index coverage, or using a hybrid dense+sparse retrieval strategy to increase page hit rate. |
| mh_01 | multi_hop | Multi-Hop Failure | The system performed 4 searches but still failed to retrieve the correct answer (page_hit=false, correctness=1, completeness=1). The low context_precision and context_recall scores indicate that while individual retrieval steps may have returned some content, the system could not successfully chain the intermediate results needed to arrive at the final answer. This is characteristic of a multi-hop reasoning breakdown where connecting evidence across documents was not achieved. | Implement explicit multi-hop reasoning chains that decompose the question into sub-questions, verify each intermediate answer before proceeding, and maintain a working memory of intermediate facts to bridge across retrieval steps. |
| mh_03 | multi_hop | Multi-Hop Failure | The system performed 6 searches (indicating effort) but still failed to retrieve the correct answer, as evidenced by low scores across answer_relevancy, context_precision, context_recall, correctness, and completeness (all scoring 1). The page_hit being false and the multi_hop slice tag confirm the system could not successfully chain the intermediate reasoning steps needed to arrive at the final answer. While retrieval also contributed, the root cause is the failure to connect multiple reasoning hops rather than a simple single-document retrieval miss. | Implement explicit multi-hop decomposition: break the query into sub-questions, retrieve and verify intermediate facts sequentially, and use the resolved intermediate answers as context for subsequent retrieval steps before synthesizing a final response. |
| mh_04 | multi_hop | Abstention Failure | The deterministic snapshot shows abstention_triggered=true but should_abstain=false, and abstention_quality_passed=false. The system incorrectly abstained when it had sufficient information to answer. Despite 9 searches and a page hit, the model chose not to produce an answer, resulting in low scores across correctness and completeness. | Adjust the abstention threshold so the model commits to an answer when relevant context has been retrieved. Improve confidence calibration to distinguish genuine knowledge gaps from retrievable multi-hop answers. |
| mh_06 | multi_hop | Abstention Failure | The snapshot shows abstention_triggered=true but should_abstain=false, meaning the model refused to answer when it should have provided an answer. Correctness and completeness scores of 1 confirm the model failed to deliver the expected response. Despite high context_recall (5) indicating the relevant information was retrieved, the model still abstained unnecessarily. | Adjust the abstention threshold or confidence calibration so the model commits to an answer when sufficient context is available. The high context_recall score indicates the evidence was present; the model simply failed to synthesize it into a final response. |
| cmp_01 | comparison | Inefficient Tool Use | The search_count of 5 with a context_precision of 1 and page_hit of false indicates the system performed multiple searches yet still failed to land on the directly relevant page. Despite the high retrieval recall and faithfulness scores, the repeated searches without a page hit suggest the tool was queried redundantly or with suboptimal strategies rather than efficiently targeting the right source on fewer attempts. | Implement query refinement logic that analyzes intermediate search results and adjusts subsequent queries rather than repeating similar searches. A targeted two-step strategy—broad discovery followed by a precise drill-down—would reduce search count and improve page hit rate. |
| cmp_02 | comparison | Retrieval Failure | Context precision and context recall are both scored at 2, indicating that while the answer is correct and complete (scores of 5), the retrieval pipeline is surfacing low-relevance chunks and missing high-relevance ones. The 5 searches performed did not consistently return the most pertinent passages, leading to poor grounding signal (citation_support: 2) despite the final answer being accurate — likely due to the model relying on parametric knowledge rather than retrieved context. | Improve retrieval ranking and query formulation for comparison-type queries: use structured re-ranking, ensemble retrieval (dense + sparse), or query decomposition to surface more precise passages. Investigate why 5 searches still yielded low precision/recall and consider adding a relevance filtering step before generation. |
| cmp_04 | comparison | Inefficient Tool Use | High search count with weak quality indicates inefficient tool strategy. | Add query deduplication, stop criteria, and max-search budgeting tied to answer quality. |
| amb_01 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the system produced an answer when it should have recognized the query was too ambiguous or underspecified to answer reliably. Low context_recall (2) and correctness (2) confirm the answer was poor, and abstention_quality_passed=false confirms the abstention check failed. Despite ambiguity tags, the primary measurable failure is the system's failure to abstain when it should have. | Implement an abstention gate that evaluates query ambiguity and context confidence scores before generating a response. When context_recall and correctness signals fall below thresholds, the system should either request clarification or explicitly abstain rather than producing a low-quality answer. |
| amb_02 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_quality_passed=false, meaning the system either failed to abstain when it should have, or abstained in a low-quality manner (e.g., with insufficient explanation or incorrect framing). The low context_recall score (2) and low correctness score (3) confirm the system did not properly handle the ambiguous or under-specified query, producing a poor abstention response rather than cleanly declining or seeking clarification. | When the system detects an ambiguous or unanswerable query, it should produce a high-quality abstention that clearly states what information is missing or ambiguous, asks targeted clarifying questions, and avoids generating speculative or low-confidence content. Implement abstention quality checks to ensure the abstention response meets minimum standards before returning it to the user. |
| amb_03 | ambiguous | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| amb_04 | ambiguous | Ambiguity Failure | The query was ambiguous enough that abstention was warranted (should_abstain=true), yet the model produced a full answer instead of seeking clarification. The abstention_quality_passed flag indicates the system recognized the ambiguity but the generation path resolved it arbitrarily rather than surfacing the ambiguity to the user. The slice label and candidate categories both point to Ambiguity Failure as the root cause over Abstention Failure, since the problem originates in unresolved query ambiguity rather than a policy failure to withhold an answer. | Add a pre-generation disambiguation step: when ambiguity signals exceed a threshold, route to a clarification prompt that asks the user to specify intent before retrieval and generation proceed. Alternatively, generate multiple interpretations with conditional answers and ask the user to confirm the intended one. |
| ie_01 | insufficient_evidence | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| ie_03 | insufficient_evidence | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| ie_04 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant supporting documents. Despite this, the model generated a confident answer (abstention_triggered is false, correctness and faithfulness scores are high), which means the root cause is that the retrieval pipeline did not return the right evidence — the model had nothing meaningful to ground against. The should_abstain flag being true further confirms the evidence was insufficient due to poor retrieval, not a generation or abstention policy failure. | Improve retrieval recall and precision by tuning the query formulation, expanding the index coverage, or using hybrid retrieval (dense + sparse). Add a relevance threshold gate so that low-precision retrievals trigger a fallback or abstention before generation proceeds. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_03 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_04 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_05 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
