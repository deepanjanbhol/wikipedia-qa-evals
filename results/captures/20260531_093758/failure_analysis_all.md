# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| No Failure | 14 |
| Abstention Failure | 13 |
| Retrieval Failure | 9 |
| Generation Failure | 6 |
| Ambiguity Failure | 4 |
| Grounding Failure | 1 |
| Multi-Hop Failure | 1 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 6 |
| Retrieval Failure | 3 |
| Grounding Failure | 1 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 4 |
| Ambiguity Failure | 4 |

### comparison

| failure_category | count |
|---|---:|
| No Failure | 5 |
| Retrieval Failure | 2 |
| Abstention Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 4 |
| Abstention Failure | 2 |

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 7 |
| Generation Failure | 4 |
| Multi-Hop Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| Generation Failure | 2 |
| No Failure | 2 |

## Failure Counts By Version

### v0

| failure_category | count |
|---|---:|
| Retrieval Failure | 7 |
| No Failure | 6 |
| Abstention Failure | 4 |
| Generation Failure | 3 |
| Ambiguity Failure | 2 |
| Grounding Failure | 1 |
| Multi-Hop Failure | 1 |

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
| mh_03 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_05 | multi_hop | Multi-Hop Failure | The low context_precision (3) and context_recall (3) scores alongside a single search attempt indicate the system failed to chain multiple retrieval steps needed to gather all supporting evidence. While the final answer scored well on correctness and completeness, the citation_support score (2) reveals that intermediate reasoning hops were not properly grounded in retrieved sources, a hallmark of multi-hop reasoning breakdown rather than a pure grounding failure. | Implement iterative or decomposed retrieval: break the question into sub-questions, retrieve evidence for each hop sequentially, and aggregate before generating the final answer. Increase search_count budget to allow follow-up queries when initial context recall is insufficient. |
| cmp_01 | comparison | Retrieval Failure | Context precision and context recall are both scored at 2, indicating the retrieval pipeline surfaced poorly ranked or largely irrelevant chunks despite the answer ultimately being correct (faithfulness=4, correctness=5, completeness=5). The system used 3 searches yet still failed to retrieve high-quality, precisely relevant context, suggesting the retrieval step is the primary weakness even though the generation layer compensated adequately. | Improve retrieval ranking and chunk selection for comparison queries—consider using a re-ranker, hybrid dense-sparse retrieval, or query decomposition so that the most relevant passages are surfaced with higher precision and recall before generation. |
| cmp_02 | comparison | Retrieval Failure | The context_precision score of 1 indicates the retrieved context was not well-targeted to the question, and context_recall of 1 suggests relevant information was not successfully retrieved. Despite high correctness and completeness scores (5/5), the citation_support score of 1 and faithfulness score of 2 indicate the answer is not grounded in the retrieved context — meaning the model generated a correct answer without proper supporting context being retrieved. This points to a retrieval failure where the right documents were not surfaced. | Improve retrieval ranking and query formulation to surface more precise and relevant context chunks. Consider using hybrid search or re-ranking to boost context_precision and context_recall, ensuring answers are grounded in retrieved content rather than relying on parametric knowledge. |
| amb_01 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the model generated an answer when it should have recognized the query was too ambiguous or underspecified to answer reliably. The low context_recall (2) and correctness (2) scores confirm the generated answer was poor, yet the model proceeded instead of abstaining. The ambiguity slice tag corroborates that the query was ambiguous, but the primary failure is the model's failure to abstain when it should have. | Implement an ambiguity detection pre-check that evaluates query specificity before retrieval. If the query is flagged as ambiguous and retrieved context confidence is low (e.g., context_recall below a threshold), trigger clarification prompts or an abstention response rather than generating a low-quality answer. |
| amb_02 | ambiguous | Abstention Failure | The deterministic snapshot explicitly flags should_abstain=true and abstention_quality_passed=false, meaning the system generated a response when it should have recognized insufficient confidence or ambiguity and declined to answer. The low faithfulness (3) and citation_support (2) scores further confirm the answer was not well-grounded, but the root cause is the failure to abstain rather than a pure grounding or ambiguity issue. | Implement an abstention gate that checks confidence thresholds before generating a response; when context_precision is very low (1) and the query is flagged ambiguous, the system should return a clarification request or explicit uncertainty disclaimer rather than a low-quality answer. |
| amb_03 | ambiguous | Ambiguity Failure | The slice is tagged 'ambiguous' and should_abstain is true, yet the system did not abstain (abstention_triggered is false). The root cause is that the query was ambiguous enough to warrant abstention, but the system failed to recognize the ambiguity and instead generated a confident response. The relatively high scores (faithfulness 5, relevancy 5) indicate the system produced a plausible-sounding answer rather than flagging the ambiguity, which is characteristic of Ambiguity Failure rather than pure Abstention Failure. | Add an ambiguity detection pre-pass that identifies underspecified or multi-interpretation queries before retrieval. When ambiguity is detected above a threshold, the system should either request clarification from the user or explicitly hedge its response and note the ambiguity, triggering appropriate abstention behavior. |
| amb_04 | ambiguous | Ambiguity Failure | The low context_precision score (2) combined with should_abstain=true and abstention_quality_passed=false indicates the query was ambiguous enough that the system should have sought clarification or abstained, but instead it retrieved loosely relevant context and generated a response. The slice tag 'ambiguous' and the candidate categories confirm the root cause is an unresolved ambiguity in the query rather than a retrieval mechanism failure per se. | Detect ambiguous queries before retrieval and either prompt the user for clarification or explicitly hedge the response to acknowledge multiple interpretations. Add an ambiguity classifier upstream that triggers a clarification dialogue or conditional abstention when query intent is underspecified. |
| ie_01 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant evidence. Despite this, the model still produced a high-scoring answer (correctness, completeness, faithfulness all at 5), which means it likely relied on parametric knowledge rather than retrieved context. The root cause is the retrieval not returning the right document, not an abstention failure since abstention_quality_passed is true and the model did not need to abstain in this case. | Improve retrieval by expanding the query, using hybrid search or re-ranking, and ensuring the relevant document is indexed and retrievable. Add a confidence threshold so that when page_hit is false and context_precision is very low, the system flags low-confidence answers rather than silently falling back to parametric knowledge. |
| ie_03 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant evidence. Despite should_abstain being true and abstention_quality_passed being true, the root cause is that the retrieval returned low-precision context, forcing the system into an evidence-poor state. The abstention itself passed quality checks, so Abstention Failure is not the primary issue. | Improve the retrieval pipeline by tuning the query rewriting or re-ranking step to surface higher-precision passages before the generation or abstention decision is made. |
| ie_04 | insufficient_evidence | Retrieval Failure | context_precision scored 1 (very low) with page_hit false and only 1 search performed, indicating the retrieval step failed to surface relevant supporting evidence. The system should have abstained (should_abstain=true) but did not trigger abstention, which is a downstream effect of poor retrieval rather than a generation or abstention policy failure per se. | Improve retrieval by expanding the search query, increasing the number of searches, or using hybrid/semantic search to surface relevant passages before generation. If evidence remains insufficient after retry, the abstention policy should then trigger correctly. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_03 | adversarial | Retrieval Failure | Context precision is 1 and context recall is 2, indicating the retrieval pipeline pulled in largely irrelevant documents and missed the key supporting evidence. The system should have abstained (should_abstain=true) but did not trigger abstention (abstention_triggered=false); the root cause is that poor retrieval gave the model enough seemingly-relevant surface content to proceed confidently instead of recognising the gap and abstaining. | Improve retrieval relevance ranking (e.g., re-ranking, query expansion, or hybrid dense-sparse search) so that either the correct supporting context is surfaced—enabling a grounded answer—or the absence of relevant context is clearly signalled to the abstention layer so it can decline to answer. |
| adv_04 | adversarial | Retrieval Failure | The context_precision score is 1 and context_recall is 2, with page_hit false, indicating the retrieval step failed to surface relevant supporting documents. The model nonetheless generated a confident answer (answer_relevancy 5, correctness 5) without grounded evidence, which is a downstream symptom of the retrieval failure rather than an independent generation or abstention failure. should_abstain is true but abstention_quality_passed is also true, meaning the abstention behavior itself was acceptable — the root cause is the retrieval pipeline not returning useful context. | Improve the retrieval pipeline for adversarial queries: tune chunking and embedding strategies, add query rewriting or HyDE, and enforce a minimum relevance threshold so low-confidence retrievals trigger abstention or escalation rather than hallucinated confident answers. |
| adv_05 | adversarial | Grounding Failure | The deterministic snapshot shows page_hit=false, context_precision=1, context_recall=2, and citation_support=2, indicating the retrieved context was poor or irrelevant. Despite this, the model generated a response (abstention_triggered=false) that scored low on faithfulness (3), meaning claims in the response are not grounded in the available evidence. The model fabricated or asserted information not supported by retrieved context rather than recognizing the weak grounding and abstaining. | Implement a grounding check that evaluates context quality scores before generating a response. When context_precision and context_recall fall below acceptable thresholds, the system should either trigger abstention or explicitly caveat that the answer is uncertain due to insufficient retrieved evidence. |
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
