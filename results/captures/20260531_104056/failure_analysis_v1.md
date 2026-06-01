# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Abstention Failure | 8 |
| No Failure | 8 |
| Retrieval Failure | 4 |
| Ambiguity Failure | 2 |
| Generation Failure | 2 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 3 |
| Retrieval Failure | 2 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Ambiguity Failure | 2 |

### comparison

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| No Failure | 2 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 2 |
| Abstention Failure | 1 |

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 5 |
| Generation Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| Generation Failure | 1 |
| No Failure | 1 |

## Failure Counts By Version

### v1

| failure_category | count |
|---|---:|
| Abstention Failure | 8 |
| No Failure | 8 |
| Retrieval Failure | 4 |
| Ambiguity Failure | 2 |
| Generation Failure | 2 |

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
