# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Abstention Failure | 15 |
| No Failure | 13 |
| Retrieval Failure | 10 |
| Multi-Hop Failure | 4 |
| Ambiguity Failure | 3 |
| Generation Failure | 2 |
| Inefficient Tool Use | 1 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 7 |
| Retrieval Failure | 3 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 4 |
| Ambiguity Failure | 3 |
| Inefficient Tool Use | 1 |

### comparison

| failure_category | count |
|---|---:|
| No Failure | 4 |
| Abstention Failure | 2 |
| Retrieval Failure | 2 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 5 |
| Abstention Failure | 1 |

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 7 |
| Multi-Hop Failure | 4 |
| Abstention Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| Generation Failure | 2 |
| No Failure | 2 |

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
