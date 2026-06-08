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

### v1b

| failure_category | count |
|---|---:|
| Ambiguity Failure | 3 |
| Abstention Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| amb_01 | ambiguous | Abstention Failure | The deterministic snapshot explicitly flags should_abstain=true and abstention_quality_passed=false, meaning the system generated an answer when it should have recognized the query was too ambiguous or underspecified to answer confidently. The low correctness (2) and completeness (1) scores confirm the generated answer was poor, but the root cause is the system's failure to withhold or seek clarification rather than producing a low-quality response. | Implement an abstention gate that checks for ambiguity signals (low context_precision, low context_recall, ambiguous slice tag) before generating a final answer. When these signals exceed a threshold, the system should either ask a clarifying question or explicitly state it cannot provide a reliable answer rather than guessing. |
| amb_02 | ambiguous | Ambiguity Failure | The low answer_relevancy (3) and context_precision (2) scores indicate the system failed to identify or resolve the ambiguity in the query before generating a response. Despite page hits and two searches, the retrieved context is imprecise, suggesting the query's ambiguity led to poorly targeted retrieval and a response that does not fully address the user's actual intent. The should_abstain flag is true but abstention_quality_passed indicates the system did attempt some form of hedging — the core failure is upstream at the ambiguity resolution stage, not the abstention stage. | Add an ambiguity detection and clarification step before retrieval: when a query is flagged as ambiguous, either prompt the user for clarification or explicitly enumerate multiple interpretations and retrieve context for each, then present results transparently. This would improve context_precision and answer_relevancy. |
| amb_03 | ambiguous | Ambiguity Failure | The slice is tagged 'ambiguous' and the deterministic snapshot shows should_abstain=true but abstention_triggered=false, meaning the system responded confidently to an ambiguous query instead of seeking clarification or flagging the ambiguity. The scores are high (4-5) suggesting the response looks plausible, but the underlying issue is that the query itself was ambiguous and the system failed to recognize or surface that ambiguity rather than failing to abstain per se. | Add an ambiguity-detection step before retrieval that identifies underspecified or multi-interpretable queries and either asks a clarifying question or hedges the response with the different possible interpretations. |
| amb_04 | ambiguous | Ambiguity Failure | The snapshot shows should_abstain=true but abstention_quality_passed=true, meaning the system did attempt to hedge appropriately. However, the slice is tagged 'ambiguous' and the scores are uniformly moderate (4-5) without a clear correct answer, indicating the root failure is that the query itself was ambiguous and the system did not seek clarification or flag the ambiguity explicitly before generating a response. The two search calls suggest the system tried to resolve an underspecified query through retrieval rather than clarifying intent. | Detect ambiguous queries earlier in the pipeline and prompt for clarification or explicitly enumerate the multiple interpretations before proceeding with retrieval and generation. |
