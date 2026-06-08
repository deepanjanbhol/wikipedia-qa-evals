# Wikipedia-Grounded QA Agent with Evals

A Claude-powered question-answering agent grounded in Wikipedia, built with a structured eval-driven methodology. The project demonstrates a full hypothesis → evaluation → failure analysis → iteration loop across prompt versions (v0/v1 for QA hill-climb, then v2 for RAI hardening).

**Assignment:** Anthropic Engineering Manager — Agent Prompts & Evals

---

## Submission Artifacts

- Written evaluation report: [`docs/report.md`](docs/report.md)
- Required written design rationale: [`docs/design_rationale.md`](docs/design_rationale.md)
- Pre-registered hypotheses: [`docs/hypotheses.md`](docs/hypotheses.md)
- AI/tool transcript guide: [`docs/ai_transcripts.md`](docs/ai_transcripts.md)
- Raw AI/tool transcript export: `ChatTranscripts.json`
- Notebook walkthrough: `walkthrough.ipynb`

---

## Quick Start

```bash
# Install dependencies
pip install anthropic python-dotenv

# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Ask a question
python main.py ask "Which country was the birthplace of the scientist who discovered penicillin?"

# Run the demo
python main.py demo --version v1
```

---

## Setup

**Requirements:** Python 3.11+

```bash
pip install -r requirements.txt
```

**Environment variables:**

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key |
| `ANTHROPIC_MODEL` | No | Model override (default: `claude-sonnet-4-6`) |
| `ANTHROPIC_JUDGE_MODEL` | No | Separate model for eval judges (default: same as `ANTHROPIC_MODEL`) |

Copy `.env.example` to `.env` and fill in your key, or export directly.

The submitted evals were run with `claude-sonnet-4-6`. If this model ID is not available in your Anthropic account, set `ANTHROPIC_MODEL` in `.env` to any Claude Messages API model you have access to, such as a current Sonnet model. Set `ANTHROPIC_JUDGE_MODEL` separately if you want judge calls to use a different model; otherwise it defaults to `ANTHROPIC_MODEL`.

---

## CLI Usage

### Ask a single question

```bash
python main.py ask "Who invented the telephone?" --version v0
python main.py ask "What is the capital of the country where Marie Curie was born?" --version v1
```

### Run the demo (3 sample questions)

```bash
python main.py demo --version v0
python main.py demo --version v1
```

**Prompt versions:**

| Alias | Canonical name | Description |
|---|---|---|
| `v0` | `v0_base` | Naive single-search baseline — no decomposition, no abstention |
| `v1` | `v1_advanced` | Decomposition + grounding self-check + abstention policy |
| `v1b` | `v1b_ambiguity_fix` | v1 + search cap (max 2) + explicit abstention on ambiguous questions |
| `v2` | `v2_rai_guarded` | v1 + explicit RAI gate at Step 0 |

---

## Running Evaluations

```bash
# Evaluate v0 against the full dataset
python -m evals.run_eval --versions v0

# Compare v0 and v1 (hillclimb run)
python -m evals.run_eval --versions v0 v1

# Include all three versions
python -m evals.run_eval --versions v0 v1 v2

# Limit to first 5 questions (quick smoke test)
python -m evals.run_eval --versions v0 v1 --limit 5

# Cross-model validation (run agent on Haiku, judges stay on Sonnet)
python -m evals.run_eval --versions v0 v1 --model claude-haiku-4-5 --limit 6

# Run RAI eval only
python -m evals.run_eval --versions v1 v2 --mode rai

# Run both QA and RAI evals
python -m evals.run_eval --versions v0 v1 v2 --mode all

# Use a named run ID for reproducibility
python -m evals.run_eval --versions v0 v1 --run-id my_run_20260531
```

Outputs are written to `results/captures/<run_id>/`:

| File | Contents |
|---|---|
| `eval_results_all.csv` | Per-question scores for all versions |
| `eval_summary_all.md` | Aggregate + slice + version breakdown table |
| `failure_analysis_all.md` | Failure taxonomy counts and examples |
| `executive_summary_all.md` | Claude-generated narrative summary |
| `report_all.html` | Interactive HTML report with hillclimb chart |
| `eval_results_<version>.csv` | Per-version CSV |
| `report_<version>.html` | Per-version HTML report |

RAI runs write separate safety-focused artifacts in the same capture directory, including `rai_results_all.csv`, `rai_summary_all.md`, `rai_results_<version>.csv`, and `rai_summary_<version>.md`.

---

## Running Tests

The deterministic utility tests do not call Anthropic or Wikipedia and can be run without an API key:

```bash
python -m unittest discover -s tests -v
```

---

## Jupyter Walkthrough

`walkthrough.ipynb` at the repo root steps through the full eval story as a developer would:

1. Setup and helper functions
2. Live agent demo — v0 vs v1 on a multi-hop question
3. Load v0 results → slice breakdown and failure taxonomy charts
4. Load v1 results → side-by-side metric comparison with delta annotations
5. Search count by slice — confirms decomposition is firing
6. RAI results and refusal rate chart
7. 2×2 executive summary dashboard (saved to `results/eval_dashboard.png`)

```bash
jupyter notebook walkthrough.ipynb
```

---

## AI Tool Transcript

The raw AI-assisted development transcript is included at `ChatTranscripts.json`. A short guide to what it contains is available in [`docs/ai_transcripts.md`](docs/ai_transcripts.md).

---

## Project Structure

```
.
├── main.py                        # CLI entry point (ask / demo)
├── requirements.txt
├── walkthrough.ipynb              # Developer eval walkthrough
│
├── agent/
│   ├── prompt.py                  # Prompt versions: v0_base, v1_advanced, v2_rai_guarded
│   ├── runner.py                  # Anthropic Messages API tool-use loop
│   └── wikipedia_tool.py          # MediaWiki API search tool (no external deps)
│
├── evals/
│   ├── dataset.json               # 24 questions across 6 slices (v0.3)
│   ├── rai_dataset.json           # RAI test cases (hate, self-harm, sexual, violence, jailbreak)
│   ├── run_eval.py                # Eval runner: QA + RAI modes, HTML/CSV/MD outputs
│   ├── claude_judge.py            # Correctness, completeness, citation, abstention judges
│   ├── ragas_metrics.py           # RAGAS-style judges: faithfulness, relevancy, precision, recall
│   ├── failure_taxonomy.py        # Failure classifier: deterministic + Claude tiebreak
│   ├── rai_checks.py              # RAI safety checks: Claude safety judge (single call) or heuristic fallback
│   └── rule_metrics.py            # Deterministic metrics: page_hit@k, search_count, abstention
│
├── docs/
│   ├── report.md                  # Full 11-section evaluation report
│   ├── hypotheses.md              # Pre-registered hypotheses (H1–H6) with outcomes
│   ├── design_rationale.md        # Architectural and methodology decisions
│   └── ai_transcripts.md          # Guide to raw AI tool transcript artifact
│
└── results/
    └── captures/                  # Timestamped eval run outputs
        └── <run_id>/
            ├── eval_results_all.csv
            ├── report_all.html
            └── ...
```

---

## Eval Framework

The evaluation system has four layers and three evaluator types.

**Four metric layers:**

| Layer | Metrics | Evaluator |
|---|---|---|
| Retrieval | context_precision, context_recall, page_hit@k | RAGAS-style judge + rule |
| Answer | answer_relevancy, correctness, completeness | Claude judge |
| Grounding | faithfulness, citation_support | RAGAS-style judge + Claude judge |
| Trust | abstention_quality, search_count, failure_category | Claude judge + rule + taxonomy |

**Failure taxonomy categories:** Retrieval Failure, Generation Failure, Multi-Hop Failure, Ambiguity Failure, Grounding Failure, Abstention Failure, Inefficient Tool Use, No Failure.

The classifier applies deterministic rules first and calls Claude only when signals conflict — keeping the taxonomy reproducible for unambiguous cases while allowing nuanced judgment for borderline ones.

**Note on RAGAS:** Metrics are implemented as Claude judges with explicit rubrics rather than using the RAGAS library. This makes every rubric readable and adjustable; the tradeoff is that scores are not directly comparable to published RAGAS benchmarks.

---

## Key Findings

Full analysis is in [`docs/report.md`](docs/report.md) and [`docs/hypotheses.md`](docs/hypotheses.md).

**Hill-climb summary (v0 → v1):**

| Metric | v0_base | v1_advanced | Change |
|---|---|---|---|
| Retrieval failures | 7 | 2 | **-5 ✅** |
| Context recall | 3.71 | 4.04 | +0.33 ↑ |
| Context precision | 2.75 | 3.17 | +0.42 ↑ |
| Citation support | 4.04 | 4.33 | +0.29 ↑ |
| Avg searches/question | 1.38 | 3.04 | +1.67 (decomposition firing) |
| Correctness | 4.58 | 4.58 | flat (ceilinged — see below) |

**Why correctness is flat:** Claude Sonnet answers many multi-hop Wikipedia questions from parametric memory regardless of what was retrieved. Correctness is measuring the base model, not the RAG system. The meaningful optimization signal is the failure taxonomy — specifically Retrieval Failure dropping from 7 to 2 — and the secondary metrics: context recall, citation support, faithfulness.

**Key tradeoff:** v1_advanced's aggressive search behavior (5.5 searches/question on ambiguous queries) increases abstention failures from 4 to 9. More evidence makes the model more confident, which reduces abstention on questions where it should withhold. A v2 would add a search-budget cap and an ambiguity stop rule.

**RAI hill-climb (v1 → v2):** Evaluated with a Claude safety judge (run `20260531_115854`; see `results/captures/20260531_115854/rai_summary_all.md`). v2_rai_guarded's Step 0 gate raises refusal_like_rate from 0.0 to 0.833 and expected_pass_rate from 0.167 to 0.750. All four primary harmful categories (hate, self-harm, violence, sexual) are refused explicitly. The WWI causes question is now answered correctly in v2 where v1 was returning an empty answer — confirming no over-refusal on legitimate content.

---

## Dataset

`evals/dataset.json` — 24 questions, 6 slices, dataset version v0.3.

| Slice | n | Focus |
|---|---|---|
| simple_factoid | 2 | Single-hop, one Wikipedia page |
| multi_hop | 6 | 2–3 sequential hops, entity carry-forward required |
| comparison | 4 | Two entities, common dimension synthesis |
| ambiguous | 4 | Underspecified questions — should trigger clarification or abstention |
| insufficient_evidence | 3 | Answer not on Wikipedia — should abstain |
| adversarial | 5 | False premises, plausible wrong answers |

Questions include `answer_confidence` flags (`high`, `medium`, `contested`) and `hop_count` for multi-hop questions. The telephone question (`sf_01`) is marked `contested` because Wikipedia explicitly documents both Bell's patent and Meucci's prior device.

---

## Adding a New Prompt Version

1. Add an entry to `PROMPT_VERSIONS` in `agent/prompt.py`
2. Add an alias to `PROMPT_VERSION_ALIASES` if desired
3. Run the eval: `python -m evals.run_eval --versions v0 v1 <your_new_version>`
4. Compare the HTML report hillclimb chart and failure taxonomy

---

## Design Decisions

See [`docs/design_rationale.md`](docs/design_rationale.md) for the reasoning behind:
- Single-agent vs. multi-agent architecture
- Prompt versioning strategy and tradeoffs
- RAGAS-style judges vs. RAGAS library
- Dataset slice distribution rationale
- The `rule_abstention_triggered` metric flaw and why judge scores are primary for abstention quality
