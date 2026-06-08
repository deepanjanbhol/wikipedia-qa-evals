# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| Ambiguity Failure | 3 |
| Abstention Failure | 1 |

## Failure Counts By Slice

### ambiguous

| failure_category | count |
|---|---:|
| Ambiguity Failure | 3 |
| Abstention Failure | 1 |

## Failure Counts By Version

### v1

| failure_category | count |
|---|---:|
| Ambiguity Failure | 3 |
| Abstention Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| amb_01 | ambiguous | Abstention Failure | The system triggered abstention (abstention_triggered=true) but abstention_quality_passed=false, meaning the abstention response was poor—likely either abstaining when it shouldn't have or providing a low-quality refusal. The completeness score of 1 and correctness score of 3 confirm the response failed to deliver adequate information. Despite 9 searches (page_hit=true), the system did not produce a satisfactory answer or a well-reasoned abstention. | Improve the abstention quality gate: when the system decides to abstain, it should provide a clear, helpful explanation of why it cannot answer and offer partial information or alternative guidance. Additionally, review whether abstention was warranted given that the page was hit and context was retrieved—the system may have been too aggressive in abstaining when sufficient context was available. |
| amb_02 | ambiguous | Ambiguity Failure | The query was ambiguous enough that the system should have sought clarification or abstained, but instead it produced a low-relevance answer (answer_relevancy: 3) with very poor context precision and recall (both 1), indicating the system misinterpreted the ambiguous intent and retrieved off-target context rather than resolving the ambiguity first. | Add an ambiguity-detection pre-processing step that identifies underspecified queries and either requests clarification from the user or generates multiple interpretations before retrieval, ensuring the correct intent is targeted before committing to a response. |
| amb_03 | ambiguous | Ambiguity Failure | The question is inherently ambiguous (slice='ambiguous', should_abstain=true), but the model did not abstain (abstention_triggered=false). The low citation_support score (1) and correctness/completeness scores of 4 suggest the model produced a confident answer to an underspecified query rather than seeking clarification or flagging the ambiguity. The root cause is failure to recognize and handle the ambiguous input, not a retrieval or grounding issue. | Add an ambiguity detection step before generation: if the query matches known ambiguous patterns or confidence in query intent is low, the model should either ask a clarifying question or explicitly acknowledge the ambiguity and present multiple interpretations with caveats rather than committing to one answer. |
| amb_04 | ambiguous | Ambiguity Failure | The slice tag and deterministic snapshot both point to an ambiguous query as the root cause. should_abstain is true and abstention_quality_passed is also true, meaning the model did attempt to handle the uncertainty, but the underlying issue is that the question itself was ambiguous enough to require abstention in the first place. The slightly reduced answer_relevancy score (4 vs 5) further suggests the response did not fully resolve the ambiguity for the user. Retrieval and generation metrics are strong, ruling out those failure modes. | Detect ambiguous queries earlier in the pipeline and prompt the user for clarification before attempting retrieval and generation. Alternatively, surface multiple interpretations of the query with corresponding answers so the user can select the intended meaning. |
