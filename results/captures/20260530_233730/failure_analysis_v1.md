# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| No Failure | 8 |
| Abstention Failure | 7 |
| Retrieval Failure | 4 |
| Generation Failure | 2 |
| Ambiguity Failure | 1 |
| Grounding Failure | 1 |
| Multi-Hop Failure | 1 |

## Failure Counts By Slice

### adversarial

| failure_category | count |
|---|---:|
| Abstention Failure | 4 |

### ambiguous

| failure_category | count |
|---|---:|
| Abstention Failure | 3 |
| Ambiguity Failure | 1 |

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

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
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
