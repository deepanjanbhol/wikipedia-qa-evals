# Design Rationale

This document records the reasoning behind architectural, evaluation, and dataset decisions made during this project. It is written to be honest about tradeoffs and failures, not just to justify what was built.

---

## 1. Why a Single Agent with a Single Tool

The assignment could have been approached as a multi-agent pipeline: a planner, a retriever, an answer generator, a critic. That architecture would have looked more complex, but complexity is not the signal being evaluated here. The question is whether an eval-driven methodology can produce measurable improvement. A simpler runtime means fewer variables, cleaner attribution of failures, and less debugging time that could be spent on the evaluation layer instead.

The single `search_wikipedia` tool was a deliberate constraint. A richer toolset — full page fetch, section extraction, cross-page linking — would have raised the performance ceiling but made it harder to isolate whether improvements came from the prompt or the tool. Keeping the tool minimal forces the prompt to do the reasoning work, which is what is being evaluated.

---

## 2. Prompt Versioning Strategy

The initial QA hill-climb used two prompt versions: `v0_base` and `v1_advanced`. A third version, `v2_rai_guarded`, was added later for explicit RAI hardening.

`v0_base` is intentionally weak in specific, measurable ways. It issues exactly one search, does not decompose questions, and is explicitly told not to withhold answers under uncertainty. The goal was not to build the worst possible prompt but to build one whose failure modes are predictable. If v0 fails on multi-hop questions, it should be because it did not decompose — not because of an unrelated bug. Constraining v0 to single-search behavior makes the failure cause attributable, not accidental.

`v1_advanced` bundles decomposition, grounding self-check, and abstention into a single upgrade. Ideally these would be separated across a v1 and v2 to isolate which change drove which improvement. The decision to combine them was made for practical reasons: the assignment scope is bounded, and the two-version contrast produces a cleaner narrative than three versions with marginal deltas. The tradeoff is that if grounding and decomposition produce effects in opposite directions on some slice, they will partially cancel and appear as noise. This is acknowledged as a design limitation.

The original prompt design included a `"Do not include chain-of-thought"` instruction in the base rules. This was removed after recognizing that it suppressed the intermediate reasoning that decomposition and grounding checks require. The instruction conflated output format (JSON only in the final message) with reasoning process (which should be unconstrained between tool calls). The corrected instruction reads: "You may think and reason between tool calls. Only your final message must be JSON."

---

## 3. Evaluation Framework Design

The evaluation layer has four components: RAGAS-style Claude judges for retrieval and answer quality, a separate Claude judge for correctness and citation support, rule-based metrics for deterministic signals, and a failure taxonomy classifier.

The decision to implement RAGAS-style metrics as Claude judges rather than using the RAGAS library directly was driven by dependency minimization and transparency. The RAGAS library is opaque about its internal prompts; building equivalent judges from scratch means the rubrics are readable, auditable, and adjustable. The tradeoff is that the scores are not comparable to published RAGAS benchmarks, which would matter in a production setting but not here.

The failure taxonomy classifier uses deterministic signals first — page hit, abstention trigger, search count, metric thresholds — and calls Claude only when deterministic signals produce a tie. This hybrid approach keeps the classifier reproducible for clear cases while allowing nuanced judgment for ambiguous ones. A purely rule-based classifier would misclassify cases where retrieval succeeded but generation failed; a purely LLM-based classifier would be expensive and non-deterministic. The hybrid is the right balance for this scale.

One metric design flaw was discovered during the eval run and is documented here rather than hidden. The `rule_abstention_triggered` metric checks for lexical phrases such as "insufficient evidence" or "cannot determine." When the eval ran, the adversarial slice showed `abstain_consistency = 0.0`, which appeared to be a system failure. Reading the actual answers revealed the opposite: the model was correctly rejecting false premises by explaining why the premise was wrong, rather than using the expected abstention phrases. The Claude judge correctly marked these as passing (`judge_abstention_quality_passed = True`). The rule was penalizing intelligent behavior. This finding — that a metric which looks catastrophic can be evidence of correct behavior when examined at the answer level — is itself a finding about evaluation design, and is the reason the judge scores should be treated as primary for abstention quality, not the rule.

---

## 4. Dataset Design

The dataset has 24 questions across six slices. The slice distribution is intentionally non-uniform: simple factoids are underweighted (2 questions) because they are easy to answer and produce low signal; multi-hop questions are overweighted (6 questions) because they are the primary expected failure surface; adversarial questions are given 5 slots to accommodate both impossible-premise and plausible-wrong-premise types.

Complexity is defined operationally rather than intuitively. Easy questions require a single Wikipedia page and no reasoning chain. Medium questions require one or two pages and minimal inference such as identifying an entity and retrieving one of its attributes. Hard questions require three or more pages, multi-step reasoning, date arithmetic, or premise validation. The `hop_count` field on multi-hop questions makes complexity measurable: a 2-hop question should need two searches; a 3-hop question should need three. This allows the analysis to check whether search count scales with hop count as expected, which is one of the pre-registered hypotheses.

Two specific improvements over the initial dataset are worth noting. First, `mh_04` originally asked "Which dynasty ruled China when the Roman Empire began?" The expected answer was "Han dynasty," but the Roman Republic began around 509 BC and the Han dynasty started 206 BC — the answer depends entirely on which beginning is meant. The question was rewritten to anchor to 27 BC, when Augustus became the first Roman Emperor, making it unambiguous and correctly answerable. Second, the adversarial question "Which country is the city of Atlantis in?" was replaced. During the v0.2 eval run, an early v2 guardrail variant answered "Palm Beach County, Florida" — technically correct, because a real city named Atlantis exists there. The question was rewritten as "On which continent is the legendary lost city of Atlantis located?" to close the trap.

An `answer_confidence` field was added to flag questions where the expected answer is contested or has caveats. The telephone invention question (`sf_01`) is marked `contested` because Wikipedia explicitly documents both Bell's patent and Meucci's prior device. A judge comparing a model answer of "Alexander Graham Bell" against the expected answer should not score it as fully correct, and the `answer_confidence` flag signals this to the evaluator.

---

## 5. What the Eval Run Revealed

The primary finding was that correctness is a saturated metric for this benchmark with Claude Sonnet as the base model. Across all versions, correctness stayed near 4.7/5.0. This is not because the prompts are all equally good — it is because Claude Sonnet has extensive parametric knowledge of Wikipedia content and answers many questions correctly regardless of what the retrieved evidence contains. Correctness is therefore measuring the base model, not the RAG system. For future iterations, two options exist: use a weaker base model to widen the gap, or design harder questions that require specific retrieved evidence rather than general knowledge.

The failure taxonomy told a more informative story. Retrieval failures dropped from 7 in v0 to 4 in v1_advanced, confirming that decomposition improved retrieval targeting. Abstention failures also dropped from 5 in v0 to 4 in v1_advanced, consistent with the grounding and abstention instructions taking effect. These are directional improvements, not large effect sizes, and with n=8 per slice per version a single question shifting its outcome represents a 12.5 percentage point change. All claims are therefore stated as directional and consistent with the hypotheses, not as confirmed results.

The ambiguous slice was the most consistently problematic. Three of the four ambiguous questions (`amb_01`, `amb_02`, `amb_03`) failed across all versions — the model picked an interpretation and answered rather than flagging ambiguity. `amb_04` (Springfield population) was the exception: the model correctly listed multiple cities and asked for clarification. The inconsistency suggests that ambiguity detection is question-dependent rather than driven by the prompt version, which points toward adding an explicit ambiguity classifier as a next step.

---

## 6. What Would Be Done Next

Given the findings, the most productive next iteration would not be another prompt version — it would be two changes to the evaluation infrastructure. First, replace `rule_abstention_triggered` with a semantic check that counts false-premise rejection as a valid form of abstention, not just phrase matching. Second, add a `parametric_knowledge_risk` flag to dataset items where the answer is likely in the model's training data, so correctness on those items can be separated from correctness on items that require genuine retrieval. Together these changes would sharpen the signal without changing the runtime architecture, which is the right priority order.

On the runtime side, increasing `top_k` on the Wikipedia tool from 3 to 5 for multi-hop questions would address the context truncation problem: the tool currently returns only 2 sentences per page, which is often insufficient for questions that require synthesizing evidence across sections.

---

## 7. Code Design Decisions and Known Debt

Two items from the original debt list have since been addressed in the repository: the duplicated JSON extraction helper was consolidated, and the RAI evaluator was moved off the lexical heuristic onto a Claude-based safety judge. The notes below separate completed cleanup from debt that still remains.

### Addressed: shared utility duplication

`_extract_json_object` — the function that parses a JSON object out of raw model text with three fallback strategies — was originally implemented independently in `claude_judge.py`, `ragas_metrics.py`, `failure_taxonomy.py`, and `run_eval.py`. That duplication has now been removed: the shared logic lives in `evals/utils.py` and those modules import it from there.

This was not refactored in the first pass because the eval runner, judge, and taxonomy modules were developed incrementally, and late extraction carried some risk against an already-validated eval loop. After the evaluation pipeline stabilized, this became a safe cleanup and was completed.

### Judge model is the same as agent model

The agent and all Claude judges run against the same model (`claude-sonnet-4-6` by default). This introduces a potential circularity: the model is evaluating its own outputs. In practice this is standard and accepted for LLM-as-judge setups, but it means judge scores may be systematically lenient on outputs that match the model's stylistic defaults. A mitigation would be to set `ANTHROPIC_JUDGE_MODEL` to a different model (e.g., Opus for higher-quality judging, or a different provider entirely) and check whether aggregate scores shift meaningfully. This was not done in this run.

### Addressed: RAI backend moved off lexical heuristic

The RAI evaluator now uses a Claude safety judge as its primary backend — a single structured API call that evaluates query-response pairs semantically for each safety category. This replaced the earlier lexical heuristic, which used keyword scanning and produced false positives (e.g., `violence_terms` included "kill", which would fire on a legitimate answer about World War I casualties). The Claude safety judge understands context and intent rather than surface form. A heuristic fallback remains in place for environments where the API key is unavailable.

One metric design gap still remains: the jailbreak expected_pass logic was originally written for the Azure-style classifier output and does not yet fully treat an explicit refusal as a passing mitigation signal. When v2 explicitly refuses a jailbreak prompt with "I can't assist with that request," the check can still mark it as failed even though the behavior is correct. The fix is to treat a clear refusal as a passing jailbreak mitigation in the scoring logic. This is a remaining scoring gap, not a safety failure.
