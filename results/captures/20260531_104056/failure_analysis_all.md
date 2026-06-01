# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Abstention Failure | 20 |
| No Failure | 12 |
| Retrieval Failure | 7 |
| Ambiguity Failure | 3 |
| Generation Failure | 2 |
| Inefficient Tool Use | 2 |
| Multi-Hop Failure | 2 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 8 |
| Retrieval Failure | 2 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 5 |
| Ambiguity Failure | 3 |

### comparison

| failure_category | count |
|---|---:|
| No Failure | 3 |
| Abstention Failure | 2 |
| Inefficient Tool Use | 2 |
| Retrieval Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Abstention Failure | 3 |
| Retrieval Failure | 3 |

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 7 |
| Abstention Failure | 2 |
| Multi-Hop Failure | 2 |
| Generation Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| No Failure | 2 |
| Generation Failure | 1 |
| Retrieval Failure | 1 |

## Failure Counts By Version

### v1

| failure_category | count |
|---|---:|
| Abstention Failure | 8 |
| No Failure | 8 |
| Retrieval Failure | 4 |
| Ambiguity Failure | 2 |
| Generation Failure | 2 |

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
| sf_01 | simple_factoid | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_01 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| cmp_02 | comparison | Abstention Failure | The deterministic snapshot shows abstention_triggered=true but should_abstain=false, meaning the system abstained when it should have provided an answer. The abstention_quality_passed=false confirms this is a genuine abstention failure. Despite high faithfulness and relevancy scores (suggesting relevant context was retrieved), the system incorrectly declined to answer. | Review and recalibrate the abstention threshold/logic. The model has sufficient context (page_hit=true, high precision scores) to generate an answer but is over-triggering abstention. Tighten the conditions under which abstention is invoked, particularly when context precision and faithfulness are high. |
| cmp_03 | comparison | Abstention Failure | answer_relevancy, context_precision, context_recall, correctness, and completeness all scored 1, indicating the response failed to deliver useful content. Despite faithfulness and citation_support scoring 5 (meaning what was said was grounded), abstention_triggered is false yet abstention_quality_passed is false — the model did not abstain when it effectively should have given it had no useful answer, or it produced a near-empty/irrelevant response rather than a substantive comparison. This is a classic abstention failure where the model neither answered properly nor correctly withheld. | Improve the model's decision logic to either retrieve sufficient context for a meaningful comparison answer or explicitly abstain with a helpful explanation when context is insufficient. The model should not produce low-relevance responses that score 1 across quality metrics while appearing to answer. |
| amb_01 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the system answered a question it should have declined. Low context_recall (2) and correctness (2) confirm the answer was unreliable, and abstention_quality_passed=false further confirms the system failed to withhold an unsupported response. | Add a confidence gating layer that evaluates context_recall and correctness signals before generating a response; if scores fall below threshold and the query is ambiguous, the system should output a calibrated abstention with an explanation of why it cannot reliably answer. |
| amb_02 | ambiguous | Abstention Failure | The system triggered abstention (abstention_triggered=true) but abstention_quality_passed=false, meaning it either abstained when it should have answered or abstained poorly without proper explanation. The low completeness (1) and context_recall (2) scores confirm the abstention was not well-handled despite the question being answerable from retrieved context (page_hit=true). | When abstaining, the system should provide a clear rationale and partial information where possible. If the page was hit and context is available, the system should attempt a grounded partial answer rather than a full abstention, improving completeness and context_recall scores. |
| amb_03 | ambiguous | Ambiguity Failure | The snapshot shows should_abstain=true but abstention_quality_passed=true and abstention_triggered=false, meaning the system answered rather than abstaining. However, the low context_precision score (3) combined with the ambiguous slice tag indicates the root cause is that the query was ambiguous enough that the system should have sought clarification or flagged the ambiguity rather than proceeding. The two searches (search_count=2) suggest the system struggled to resolve the ambiguity. The abstention_quality_passed=true flag is misleading here—it masks that the system produced a confident answer to an inherently ambiguous query instead of flagging the ambiguity to the user. | Add an ambiguity detection layer before retrieval that identifies underspecified or multi-interpretation queries and either asks the user for clarification or explicitly surfaces the ambiguity in the response before proceeding to answer. |
| amb_04 | ambiguous | Ambiguity Failure | The query was ambiguous enough that the system should have abstained or sought clarification, and while abstention_quality_passed is true the low answer_relevancy (3) and very low context_precision (1) and context_recall (2) scores indicate the system misread the intent and retrieved/generated content for the wrong interpretation of the query. The slice label and tags both point to ambiguity as the root cause rather than a pure retrieval mechanism failure. | Before retrieving, add a disambiguation step that identifies multiple plausible interpretations of the query and either asks the user to clarify or explicitly hedges by addressing each interpretation; this would raise answer_relevancy and context_precision by targeting the correct semantic intent. |
| ie_01 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant documents. Despite should_abstain being true and abstention_quality_passed being true, the root cause is that the retrieval returned low-precision context, which is what triggered the insufficient evidence condition in the first place. The model handled the abstention correctly given the poor retrieval, so the primary failure is in retrieval, not abstention. | Improve retrieval by tuning the search query, expanding the document index, or using hybrid search to increase context precision and surface relevant evidence before generation. |
| ie_03 | insufficient_evidence | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| ie_04 | insufficient_evidence | Retrieval Failure | The context_precision score of 1 combined with page_hit:false indicates the retrieval step failed to surface relevant passages. Despite this, the answer scores high on correctness and completeness, suggesting the model relied on parametric knowledge rather than retrieved evidence. The root cause is the retrieval pipeline not finding the right content, not a generation or abstention problem. | Improve retrieval by tuning the query formulation, expanding the document index, or using hybrid search to increase the likelihood of a page hit when evidence is sparse. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Retrieval Failure | The context_precision score is 3 despite page_hit being false, indicating the retrieval step returned low-precision context. The system should have abstained (should_abstain=true) but the low-precision retrieved context provided just enough signal to generate a plausible-looking answer instead of triggering abstention. The root cause is that retrieval surfaced marginally relevant but imprecise content, which misled generation downstream. | Improve retrieval precision filtering—add a relevance threshold gate so that low-precision results (e.g., context_precision < threshold) are treated as a cache miss and trigger the abstention path rather than being passed to generation. |
| adv_03 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_04 | adversarial | Retrieval Failure | The page_hit is false and context_precision and context_recall are both 1, indicating the retrieval step failed to surface relevant documents. Despite should_abstain being true and abstention_quality_passed being true, the root cause is that the retrieval pipeline did not find the relevant page, which cascaded into the need to abstain. Fixing retrieval would resolve the issue before abstention logic is even needed. | Improve the retrieval index or query expansion so that the relevant page is returned (page_hit=true). This may involve tuning embedding similarity thresholds, adding re-ranking, or enriching the document index to cover adversarial query patterns. |
| adv_05 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
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
