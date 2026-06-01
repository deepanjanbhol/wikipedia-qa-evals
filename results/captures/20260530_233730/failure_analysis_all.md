# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| No Failure | 23 |
| Retrieval Failure | 17 |
| Abstention Failure | 16 |
| Generation Failure | 7 |
| Ambiguity Failure | 4 |
| Grounding Failure | 3 |
| Multi-Hop Failure | 2 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 8 |
| Retrieval Failure | 4 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 8 |
| Ambiguity Failure | 4 |

### comparison

| failure_category | count |
|---|---:|
| No Failure | 8 |
| Grounding Failure | 3 |
| Generation Failure | 1 |

### insufficient_evidence

| failure_category | count |
|---|---:|
| Retrieval Failure | 12 |

### multi_hop

| failure_category | count |
|---|---:|
| Generation Failure | 6 |
| No Failure | 3 |
| Multi-Hop Failure | 2 |
| Retrieval Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| No Failure | 12 |

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

### v1

| failure_category | count |
|---|---:|
| No Failure | 8 |
| Abstention Failure | 7 |
| Retrieval Failure | 4 |
| Generation Failure | 2 |
| Ambiguity Failure | 1 |
| Grounding Failure | 1 |
| Multi-Hop Failure | 1 |

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
| mh_01 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_03 | multi_hop | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_04 | multi_hop | Multi-Hop Failure | The low context_precision (1) and context_recall (1) combined with page_hit:false indicate the system failed to chain the intermediate retrieval steps needed to answer the question. While answer_relevancy and correctness are high (5), the citations are unsupported (citation_support:1) and faithfulness is low (3), meaning the final answer was generated without grounding in properly retrieved multi-hop evidence. The system likely guessed or hallucinated the answer rather than retrieving and linking the required intermediate facts. | Implement a multi-hop retrieval strategy that explicitly decomposes the question into sub-questions, retrieves evidence for each hop sequentially, and verifies that each reasoning step is grounded in retrieved context before generating the final answer. |
| cmp_02 | comparison | Grounding Failure | The scores reveal a critical disconnect between retrieved context and generated output: faithfulness is 3, context_precision is 1, context_recall is 2, and citation_support is 2. Despite the answer being relevant and complete (scores of 5), the response is not grounded in the retrieved context. The page was hit and retrieval occurred, but the generated answer does not faithfully reflect or cite the source material, indicating the model generated plausible-sounding comparison content without adequately anchoring it to the retrieved evidence. | Enforce stricter grounding by requiring the generation step to explicitly map claims to retrieved passages before outputting the comparison. Add a faithfulness check gate that rejects or revises responses where citation support falls below a threshold, and use retrieval-augmented prompting that instructs the model to quote or directly reference source snippets when making comparative statements. |
| amb_01 | ambiguous | Abstention Failure | The system should have abstained (should_abstain=true) but did not (abstention_triggered=false, abstention_quality_passed=false). Despite low context_recall (1) and context_precision (2) indicating poor retrieval quality, the system generated an answer anyway. The low correctness (2) and completeness (2) scores confirm the output was unreliable, yet the system proceeded without flagging uncertainty. | Implement an abstention gate that checks retrieval quality scores (e.g., context_recall and context_precision) before generating a response. When these fall below a threshold, the system should return a low-confidence or 'I don't know' response rather than producing a potentially incorrect answer. |
| amb_02 | ambiguous | Abstention Failure | The snapshot explicitly flags should_abstain=true and abstention_quality_passed=false, meaning the system generated an answer when it should have withheld or flagged uncertainty. The low faithfulness (2) and citation_support (1) scores confirm the generated content is not grounded in retrieved evidence, but the root cause is the failure to abstain despite low context_precision (1) signaling insufficient reliable context. | Add an abstention gate that checks context_precision and faithfulness scores before generating a final answer. If context_precision falls below a threshold (e.g., <2) or faithfulness is critically low, the system should return a calibrated uncertainty response rather than a potentially hallucinated answer. |
| amb_03 | ambiguous | Abstention Failure | The snapshot flags should_abstain=true but abstention_triggered=false, meaning the system responded when it should have withheld or clarified. The completeness score of 3 and correctness of 4 further indicate a partial or risky answer was produced instead of a proper abstention or clarification request. While Ambiguity Failure is a candidate tag, the deterministic evidence (should_abstain=true, abstention_quality_passed=false) makes Abstention Failure the primary root cause. | Add a pre-generation check that detects ambiguous or under-specified queries and routes them to a clarification prompt rather than producing a direct answer. If the confidence or context-coverage score falls below a threshold, the system should ask the user to disambiguate before continuing. |
| amb_04 | ambiguous | Ambiguity Failure | The question is ambiguous enough that the system should have flagged it and sought clarification, but instead it attempted a single retrieval pass and returned a partially relevant answer. Low context_precision and context_recall (both 3) indicate the retrieved content did not cleanly match the intent, which stems from the unresolved ambiguity rather than a retrieval mechanism failure per se. The should_abstain flag is true but abstention_quality_passed suggests the system's hedging was marginal rather than a clean abstention failure. | Add an ambiguity-detection pre-processing step that identifies underspecified queries and either asks a clarifying question or explicitly branches into multiple interpretations before retrieval, rather than committing to a single low-confidence retrieval pass. |
| ie_01 | insufficient_evidence | Retrieval Failure | context_precision scored 1 (very low) with page_hit false and search_count 1, indicating the single retrieval attempt failed to surface relevant supporting evidence. Despite this, the model did not abstain (abstention_triggered false) and produced a fully confident answer (all other scores at 5). The root cause is the retrieval step returning irrelevant or empty context, not a generation-side hallucination or abstention decision. | Increase search_count or broaden the retrieval query before generating an answer. Implement a context-quality gate: if context_precision falls below a threshold, trigger re-retrieval or fall back to abstention rather than generating from insufficient evidence. |
| ie_02 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision is 1, indicating the retrieval step failed to surface relevant supporting documents. Despite should_abstain being true, abstention_quality_passed is true meaning the model did handle the lack of evidence appropriately — the root cause is the retrieval pipeline not finding the relevant page, not a generation or abstention problem. | Improve retrieval recall by expanding the search index coverage, tuning embedding similarity thresholds, or adding fallback retrieval strategies (e.g., BM25 hybrid search) to increase the likelihood of a page_hit when relevant documents exist. |
| ie_03 | insufficient_evidence | Retrieval Failure | The page_hit is false and context_precision and context_recall are both scored at 1, indicating the retrieval step failed to surface relevant evidence. The system should have abstained (should_abstain=true) but the root cause is that the retriever never found supporting documents, leaving the generator without grounding material. The abstention quality passed only incidentally; the core breakdown is that relevant context was never retrieved. | Improve the retrieval pipeline by expanding the query, using hybrid search or re-ranking, and lowering the relevance threshold so that borderline-relevant passages are surfaced before the generation step decides whether to abstain. |
| ie_04 | insufficient_evidence | Retrieval Failure | Expected evidence pages were not effectively retrieved. | Improve query rewriting/disambiguation and increase retrieval focus on expected entities. |
| adv_01 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_02 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_03 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
| adv_04 | adversarial | Abstention Failure | Expected abstention but answer did not abstain. | Strengthen abstention policy: abstain on insufficient evidence and avoid fabricated specifics. |
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
