# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| No Failure | 8 |
| Retrieval Failure | 6 |
| Abstention Failure | 4 |
| Ambiguity Failure | 2 |
| Generation Failure | 2 |
| Grounding Failure | 1 |
| Multi-Hop Failure | 1 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Retrieval Failure | 2 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 2 |
| Ambiguity Failure | 2 |

### comparison

| failure_category | count |
|---|---:|
| No Failure | 3 |
| Grounding Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 4 |

### multi_hop

| failure_category | count |
|---|---:|
| Generation Failure | 2 |
| Multi-Hop Failure | 1 |
| No Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| No Failure | 4 |

## Failure Counts By Version

### v2

| failure_category | count |
|---|---:|
| No Failure | 8 |
| Retrieval Failure | 6 |
| Abstention Failure | 4 |
| Ambiguity Failure | 2 |
| Generation Failure | 2 |
| Grounding Failure | 1 |
| Multi-Hop Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| mh_01 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_03 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_04 | multi_hop | Multi-Hop Failure | The low context_precision (1) and context_recall (1) scores combined with page_hit=false indicate the system failed to chain the necessary reasoning steps to retrieve and connect relevant evidence. Despite correct final answers (correctness=5, completeness=5), the supporting context was not properly retrieved or linked across multiple hops, as evidenced by citation_support=1 and faithfulness=3. The single search attempt was insufficient to gather the multi-step evidence needed. | Implement iterative multi-hop retrieval: after an initial search, extract intermediate entities/facts and issue follow-up searches to gather bridging evidence. Require citation grounding before finalizing answers, and increase search_count thresholds for queries tagged as multi-hop. |
| cmp_02 | comparison | Grounding Failure | The faithfulness score is 3 and citation_support is 2, while context_precision and context_recall are both at 1 (perfect). This pattern indicates the retrieved context was relevant and complete, but the generated answer made claims not properly grounded in or supported by that context. The model generated content that drifted from the source material despite having the right information available. | Improve answer generation constraints to ensure claims are explicitly traceable to retrieved passages. Add post-generation faithfulness checks or use extractive summarization techniques to anchor responses more tightly to source context. |
| amb_01 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true and abstention_quality_passed=false, meaning the system generated a response when it should have withheld or flagged uncertainty. Despite low context_recall (1) and low correctness/completeness (2), the system did not abstain. The ambiguity slice and tags suggest the query was underspecified, but the primary measurable failure is the system's failure to abstain when evidence was insufficient. | Add an abstention gate that checks combined signals — low context_recall, low citation_support, and ambiguous query patterns — before generating a response. When these thresholds are breached, the system should return a clarifying question or explicit uncertainty statement rather than a low-confidence answer. |
| amb_02 | ambiguous | Ambiguity Failure | The low context_precision (1) combined with should_abstain=true but abstention_triggered=false, alongside a faithfulness score of 3 and citation_support of 2, indicates the system failed to recognize that the query was ambiguous and required clarification before generating a response. Instead of seeking clarification or abstaining, it proceeded with a low-confidence answer grounded in imprecisely matched context. | Add an ambiguity detection layer before retrieval that identifies underspecified queries and prompts for clarification. If ambiguity cannot be resolved, trigger the abstention pathway rather than returning a low-confidence answer with poor citation support. |
| amb_03 | ambiguous | Abstention Failure | The deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the model answered a question it should have declined due to ambiguity. The completeness score of 2 and abstention_quality_passed=false confirm the model failed to recognize and surface the ambiguity, instead providing an incomplete or misleading answer. | Add an ambiguity detection step before generation: when the query is underspecified or matches multiple interpretations, the model should either ask a clarifying question or explicitly acknowledge the ambiguity rather than proceeding with a low-confidence answer. |
| amb_04 | ambiguous | Ambiguity Failure | The query is inherently ambiguous and the system should have sought clarification or flagged the ambiguity before attempting retrieval. Context precision and recall scores are both at 3, indicating the retrieval was partially off-target — likely because the ambiguous query led the retriever toward uncertain document selection. The page_hit being false and should_abstain being true further confirm the system encountered an unresolvable ambiguity but proceeded anyway rather than surfacing it. | Implement a pre-retrieval ambiguity detection step that identifies underspecified queries and either asks the user for clarification or generates multiple interpretations before retrieval, then reconciles the results. This would improve context precision and recall by grounding retrieval in a well-defined information need. |
| ie_01 | insufficient_evidence | Retrieval Failure | The deterministic snapshot shows page_hit=false and context_precision=1, indicating the retrieval step failed to surface relevant supporting documents. Although abstention_quality_passed=true and the model ultimately scored well on faithfulness and recall, the root cause is that the retrieval returned low-precision context (context_precision=1), meaning the evidence retrieved was not pertinent to the question. The model should have abstained given should_abstain=true, but the underlying driver is the retrieval not finding the right page/document. | Improve retrieval by tuning the query formulation, expanding the index coverage, or using hybrid search (dense+sparse) to increase context_precision. Additionally, if retrieval confidence remains low, wire a hard abstention guard so the model does not proceed when page_hit=false. |
| ie_02 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant evidence. Despite this, the model produced a confident answer (abstention_triggered=false) that happened to score well on other metrics, but the root cause is that the retrieval returned low-precision context rather than the model failing to abstain properly. | Improve the retrieval pipeline to increase page hit rate and context precision, for example by tuning the embedding model, adjusting chunking strategy, or expanding the search scope so that relevant evidence is actually surfaced before generation. |
| ie_03 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant supporting documents. Despite this, the model produced a confident answer (no abstention triggered, high faithfulness and correctness scores), meaning the root cause is that the retrieval pipeline did not return the right evidence rather than a generation or abstention decision problem. | Improve retrieval recall and precision by tuning the search query, expanding the index, or using re-ranking so that relevant passages are surfaced before generation proceeds. |
| ie_04 | insufficient_evidence | Retrieval Failure | Expected evidence pages were not effectively retrieved. | Improve query rewriting/disambiguation and increase retrieval focus on expected entities. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Retrieval Failure | The context_precision score of 1 combined with page_hit:false indicates the retrieval step failed to surface relevant documents. Despite this, the system did not abstain (abstention_triggered:false) even though should_abstain:true, but the root cause is that poor retrieval returned low-quality context (precision=1, recall=3), which propagated into an answer that should not have been generated. The retrieval failure is the initiating fault in the chain. | Improve retrieval recall and precision by tuning the retrieval pipeline (e.g., better embedding model, hybrid search, or re-ranking). Additionally, add a confidence gate that triggers abstention when context_precision falls below a threshold, which would have correctly suppressed the answer here. |
| adv_03 | adversarial | Retrieval Failure | The context_precision score of 1 and context_recall score of 2 indicate the retrieval system failed to surface relevant documents (page_hit: false), which cascaded into low faithfulness (3). The system should have abstained (should_abstain: true) but did not trigger abstention, and the root cause is that retrieved context was irrelevant or insufficient — a retrieval failure rather than a generation or abstention logic failure. | Improve retrieval coverage and precision for adversarial queries, potentially by adding query rewriting, hybrid search, or fallback retrieval strategies. Also add an abstention gate that checks context relevance scores before generating a response. |
| adv_04 | adversarial | Abstention Failure | The deterministic snapshot explicitly flags should_abstain=true but abstention_triggered=false, meaning the model generated a response when it should have declined or expressed uncertainty. The abstention_quality_passed=false confirms the failure mode. Despite adversarial signals and a completeness score of 2, the system proceeded to generate an answer rather than abstaining. | Add a pre-generation gate that evaluates confidence and adversarial signals before producing output; when should_abstain conditions are met (e.g., low completeness, adversarial slice, low context_precision), return a calibrated abstention response instead of generating a potentially unreliable answer. |
