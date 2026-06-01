# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Abstention Failure | 9 |
| No Failure | 8 |
| Generation Failure | 3 |
| Ambiguity Failure | 2 |
| Retrieval Failure | 2 |

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
| Abstention Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Retrieval Failure | 1 |

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 4 |
| Generation Failure | 2 |

### simple_factoid

| failure_category | count |
|---|---:|
| Generation Failure | 1 |
| No Failure | 1 |

## Failure Counts By Version

### v1

| failure_category | count |
|---|---:|
| Abstention Failure | 9 |
| No Failure | 8 |
| Generation Failure | 3 |
| Ambiguity Failure | 2 |
| Retrieval Failure | 2 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| sf_01 | simple_factoid | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_01 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_05 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| cmp_02 | comparison | Abstention Failure | The system triggered abstention (abstention_triggered=true) when it should not have (should_abstain=false), and abstention_quality_passed=false confirms the abstention was incorrect. Despite page_hit=true and 10 searches returning relevant context (context_precision=2, context_recall=2), the model refused to generate an answer rather than using the available information to respond. | Tune the abstention threshold or confidence scoring logic so the model does not abstain when sufficient grounded context is available. Review the decision boundary that triggered abstention despite a page hit and adequate retrieval scores. |
| amb_01 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the system answered when it should have recognized the ambiguity and withheld or clarified. Low context_recall (2) and correctness (2) confirm the answer was unreliable, yet the system generated a response anyway instead of abstaining. | Add an ambiguity/confidence gate before generation: if the query is flagged ambiguous and context_recall falls below a threshold, the system should either ask a clarifying question or explicitly state it cannot provide a reliable answer rather than generating a low-quality response. |
| amb_02 | ambiguous | Abstention Failure | The system triggered abstention (abstention_triggered=true) but abstention_quality_passed=false, meaning the abstention response was inadequate. Despite should_abstain=true being correct, the low completeness (1) and context_recall (3) scores indicate the system failed to properly communicate why it was abstaining or what information was missing, resulting in a poor-quality abstention rather than a clean, informative one. | When abstaining, the system should clearly articulate what is ambiguous or unknown, provide any partial information that is reliably grounded, and guide the user on how to refine their query. The abstention message itself should be complete and contextually relevant rather than a generic refusal. |
| amb_03 | ambiguous | Ambiguity Failure | The query was flagged as ambiguous (slice='ambiguous'), page_hit=false, and context_precision/recall are both 1, indicating the system failed to clarify or resolve the ambiguous intent before attempting retrieval. Despite should_abstain=true, abstention_quality_passed=true means the abstention itself was acceptable, so the root cause is the system not handling the ambiguity upfront rather than an abstention failure per se. | Add an ambiguity detection step before retrieval that identifies underspecified queries and either prompts the user for clarification or generates multiple interpretations to search against, improving context precision and recall. |
| amb_04 | ambiguous | Ambiguity Failure | The query is inherently ambiguous (slice='ambiguous', tag hint confirms), yet the system did not abstain despite should_abstain=true. However, abstention_quality_passed=true and abstention_triggered=false together indicate the system produced an answer rather than seeking clarification. The core failure is that the system failed to recognize and surface the ambiguity to the user, proceeding to answer without resolving which interpretation was intended. | Add an ambiguity-detection pre-processing step that flags underspecified queries and prompts the user for clarification before retrieval and generation, rather than silently resolving ambiguity by picking one interpretation. |
| ie_01 | insufficient_evidence | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| ie_03 | insufficient_evidence | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| ie_04 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant evidence. Despite high scores on faithfulness, recall, and correctness, the underlying context retrieved was poor quality. The system should have abstained (should_abstain=true) but the root cause is that retrieval did not return sufficient evidence to support a confident answer — it is a retrieval problem that cascades into insufficient evidence. | Improve retrieval by expanding the search query, increasing the number of retrieved documents, or using a hybrid retrieval strategy to ensure relevant evidence is surfaced before generation. Also add a confidence threshold check post-retrieval to trigger abstention when context_precision is below a minimum threshold. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the system should have declined to answer (adversarial input) but instead generated a response. The page_hit=false confirms no grounding evidence was retrieved, yet the model proceeded to answer rather than abstain. Despite high faithfulness and correctness scores, the core failure is that the system did not recognize it should have withheld a response. | Add an adversarial intent classifier or confidence gate before generation. When page_hit=false on adversarial-tagged queries, route to an abstention handler that returns a safe refusal rather than proceeding to generation. |
| adv_03 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_04 | adversarial | Retrieval Failure | The deterministic snapshot shows page_hit=false and context_precision=1 and context_recall=1, indicating the retrieval step failed to surface relevant supporting documents. Although abstention_triggered=false and should_abstain=true, the root cause is that the retriever did not find the correct page/passage, which cascades into the model having no grounded content to reason from. The generation scores are all high (5) suggesting the model produced a fluent response, but it was built on empty or irrelevant context — a retrieval failure upstream. | Improve the retrieval pipeline by tuning embedding similarity thresholds, expanding the document index, or adding query rewriting/expansion so that adversarial queries still match relevant passages. Additionally, add a fallback abstention guard that triggers when context_precision and context_recall are both at minimum (1) to prevent confident responses on empty retrieval. |
| adv_05 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
