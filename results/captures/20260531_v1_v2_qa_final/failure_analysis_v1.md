# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Abstention Failure | 8 |
| No Failure | 6 |
| Retrieval Failure | 5 |
| Multi-Hop Failure | 2 |
| Ambiguity Failure | 1 |
| Generation Failure | 1 |
| Inefficient Tool Use | 1 |

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
| Ambiguity Failure | 1 |
| Inefficient Tool Use | 1 |

### comparison

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| No Failure | 1 |
| Retrieval Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 2 |
| Abstention Failure | 1 |

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 4 |
| Multi-Hop Failure | 2 |

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
| No Failure | 6 |
| Retrieval Failure | 5 |
| Multi-Hop Failure | 2 |
| Ambiguity Failure | 1 |
| Generation Failure | 1 |
| Inefficient Tool Use | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| sf_01 | simple_factoid | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_02 | multi_hop | Multi-Hop Failure | The system performed 4 searches but still failed to connect the intermediate reasoning steps needed to arrive at the correct answer. Low scores across answer relevancy, context precision, context recall, correctness, and completeness — combined with a page_hit of false — indicate that while some retrieval occurred, the model could not chain the retrieved facts into a coherent multi-hop conclusion. Faithfulness and citation support are high (5), meaning the model stayed grounded in what it found, but what it found was insufficient due to failed multi-hop traversal. | Implement explicit multi-hop decomposition: break the question into sub-questions, retrieve answers for each sub-question sequentially, and use intermediate answers as context for subsequent retrievals. A chain-of-thought reasoning step between hops would help the model recognize when an intermediate answer must feed the next query. |
| mh_04 | multi_hop | Multi-Hop Failure | The low scores across faithfulness, answer relevancy, context precision, context recall, correctness, and completeness—combined with page_hit:false and the multi_hop slice—indicate the system failed to correctly chain multiple reasoning steps. Despite 8 searches (suggesting retrieval attempts were made), the intermediate results were not properly synthesized into a coherent final answer, leading to an incorrect or incomplete response. | Implement explicit intermediate reasoning checkpoints that verify each hop's output before proceeding to the next. Use a structured chain-of-thought approach that stores and validates intermediate facts, and add a final consistency check to ensure the synthesized answer aligns with all retrieved evidence before returning a response. |
| cmp_01 | comparison | Abstention Failure | The system triggered abstention (abstention_triggered=true) but should_abstain=false, meaning the system had sufficient information to answer but chose not to. The answer_relevancy and correctness scores of 1 confirm the response failed to deliver a useful answer. Despite high faithfulness and context recall scores indicating good retrieved context, the system unnecessarily declined to answer the comparison query. | Calibrate the abstention threshold so the system does not abstain when high-quality context is available (context_precision=4, context_recall=5). The abstention logic should check for sufficient grounding evidence before triggering, and for comparison queries specifically, the system should synthesize the retrieved context into a direct comparative response. |
| cmp_02 | comparison | Abstention Failure | The system triggered abstention (abstention_triggered=true) when it should not have (should_abstain=false). Despite 12 searches being performed, the system chose to abstain rather than produce an answer, resulting in abstention_quality_passed=false and uniformly low scores across correctness and completeness. The core failure is the model refusing to answer when a valid answer was expected. | Review the abstention threshold and confidence calibration logic. The system should be tuned to provide a best-effort answer for comparison queries even when retrieval confidence is moderate, rather than defaulting to abstention. Consider lowering the abstention trigger threshold or adding a fallback generation step when sufficient context exists after multiple searches. |
| cmp_04 | comparison | Retrieval Failure | The page_hit is false and context_precision and context_recall are both 1, indicating the retrieval pipeline failed to surface relevant comparison documents. Despite 6 searches (suggesting repeated attempts), the retrieved context was not useful, leading to low answer relevancy and correctness scores even though faithfulness and citation_support are high (the model faithfully cited what little it retrieved). | Improve the retrieval strategy for comparison queries by using structured query decomposition that explicitly fetches documents for each entity being compared, then re-ranks results by relevance to the comparison dimension. |
| amb_01 | ambiguous | Abstention Failure | The deterministic snapshot explicitly flags should_abstain=true and abstention_quality_passed=false, meaning the system generated a response when it should have withheld or flagged uncertainty. Low context_recall (2) and citation_support (1) confirm the retrieved context was insufficient to ground a reliable answer, yet the system proceeded anyway rather than abstaining. | Implement an abstention gate that evaluates context_recall and citation_support scores before generation; if either falls below a minimum threshold (e.g., recall < 3 or citation_support < 2), the system should return a calibrated 'insufficient information' response instead of generating a potentially hallucinated answer. |
| amb_02 | ambiguous | Inefficient Tool Use | The system performed 8 searches (search_count=8) despite eventually producing a response with acceptable faithfulness and correctness scores, and abstention was not triggered when it should have been. The high search count relative to the output quality—combined with low context_precision (2) and moderate context_recall (3)—indicates the retrieval strategy was poorly targeted, retrieving irrelevant or redundant chunks across many queries rather than focusing on the right context efficiently. | Implement query planning before retrieval: analyze the question to identify the minimal set of distinct sub-queries needed, set a search budget (e.g., 3-4 searches max), and use re-ranking or query reformulation to improve precision before issuing additional searches. Also add an ambiguity detection step at query time to decide whether to clarify or abstain early rather than over-searching. |
| amb_03 | ambiguous | Abstention Failure | The deterministic snapshot flags should_abstain=true, meaning the system should have withheld or qualified its answer due to ambiguity or insufficient grounding, but abstention_triggered=false confirms it did not. Despite abstention_quality_passed=true (suggesting the abstention path would have been acceptable), the model forged ahead and produced a response, as evidenced by low citation_support=1 which indicates the answer lacks grounded backing. The ambiguity slice and candidate tags corroborate that the query warranted abstention. | Implement an abstention gate that evaluates query ambiguity and citation support scores before generating a response. When citation_support falls below a threshold (e.g., <2) and the query is flagged as ambiguous, the system should return a clarifying question or an explicit statement of uncertainty rather than a low-confidence answer. |
| amb_04 | ambiguous | Ambiguity Failure | The query was ambiguous enough that abstention was warranted (should_abstain=true), yet the system produced an answer rather than seeking clarification. The abstention_quality_passed flag indicates the abstention mechanism did activate and pass quality checks, but the root cause is that the ambiguous input was not resolved before generation, leading to a response of uncertain relevance (answer_relevancy=4) rather than a clarifying prompt. Tags and candidate categories both point to Ambiguity Failure as primary. | Add a pre-retrieval ambiguity classifier that detects underspecified or multi-interpretation queries and routes them to a clarification step before retrieval and generation proceed. |
| ie_01 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant documents. Despite 3 searches, the retrieved context was low quality, yet the model still produced a confident answer (abstention_triggered is false) with high faithfulness and correctness scores — suggesting the model got lucky or hallucinated rather than grounding on retrieved evidence. The root cause is the retrieval pipeline not finding the right content. | Improve retrieval by tuning query expansion, re-ranking, or embedding models to increase page hit rate and context precision. Add a confidence threshold so that when context_precision is below a minimum threshold, the system triggers abstention or escalates to a broader search strategy. |
| ie_03 | insufficient_evidence | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| ie_04 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant supporting evidence. Despite this, the model did not abstain (abstention_triggered is false) and produced a response that scored high on faithfulness and correctness — meaning the model generated an answer without grounded retrieved content. The root cause is the retrieval pipeline not returning useful context, which is a Retrieval Failure rather than an Abstention Failure since abstention_quality_passed is true (the abstention behavior itself was acceptable given what was retrieved). | Improve retrieval recall by expanding the query, using query rewriting or HyDE, or increasing the number of retrieved passages before ranking. Additionally, add a confidence threshold gate that triggers abstention when context_precision falls below a minimum threshold. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Abstention Failure | The snapshot shows page_hit=false and should_abstain=true, but abstention_triggered=false, meaning the system failed to abstain when it should have. Despite abstention_quality_passed=true (meaning when it did abstain the quality was fine), the core failure is that abstention was never triggered in the first place on an adversarial query where no supporting page was found. | Add a confidence gate that checks page_hit status before generating a response; if page_hit=false on an adversarial slice, route to the abstention handler rather than proceeding to generation. |
| adv_03 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_04 | adversarial | Retrieval Failure | The page_hit is false and context_precision is 1 with context_recall of 2, indicating the retrieval step failed to surface relevant supporting documents. Despite the system needing to abstain (should_abstain=true), the root cause is that the retrieval returned poor or irrelevant context, which then led to a response being generated without proper grounding. The abstention_quality_passed=true means the abstention mechanism itself did not malfunction, but the upstream retrieval failure is the primary deterministic evidence. | Improve retrieval by tuning the query formulation, expanding the index coverage, or adding a re-ranking step to ensure relevant documents are surfaced before generation proceeds. A confidence threshold on retrieval quality should also trigger abstention when context_precision and context_recall are low. |
| adv_05 | adversarial | Retrieval Failure | The context_precision score is 2, indicating that despite 7 searches the retrieved context was poorly ranked and largely irrelevant. The page_hit is false and should_abstain is true, meaning the system lacked adequate grounding but still generated a response. The root cause is that retrieval failed to surface the right documents, which cascaded into a response that should have triggered abstention but didn't due to low-quality context rather than a generation flaw. | Improve retrieval ranking and relevance filtering so that low-precision context is detected early; when context_precision falls below a threshold, route to an abstention path rather than generating a potentially unsupported answer. |
