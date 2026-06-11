# Submission Checklist

Use this file as the final pre-submission checklist for the Anthropic Engineering Manager Agent Prompts & Evals take-home.

## Time Spent

The runnable code, evaluation framework, and core submission artifacts were completed in approximately 3.5 hours of focused implementation time. Final review, documentation polish, presentation generation, and video recording/editing were handled separately.

## Required Deliverables

- [x] Runnable prototype with CLI entry point (`main.py`)
- [x] Clear setup instructions in `README.md`
- [x] Wikipedia-backed QA agent using the Anthropic API
- [x] Direct Wikipedia/MediaWiki API usage; no hosted search tools
- [x] Versioned prompt implementation (`v0`, `v1`, `v2`)
- [x] Evaluation runner for QA evals
- [x] Evaluation runner for RAI/safety evals
- [x] Written design rationale in `docs/design_rationale.md`
- [x] Full written evaluation report in `docs/report.md`
- [x] Pre-registered hypotheses and outcomes in `docs/hypotheses.md`
- [x] Saved evaluation outputs under `results/captures/`
- [x] Notebook walkthrough in `walkthrough.ipynb`
- [x] AI/tool transcript artifact in `ChatTranscripts.json`
- [x] Presentation deck artifact (`wikipedia_qa_eval_driven.pptx`)
- [x] GitHub repository link ready for Greenhouse submission
- [x] Final self-recorded video exported and ready to upload

## Final Video

- [x] Draft video script/SRT created
- [x] Cut final video to approximately 5 minutes 40 seconds
- [x] Replace transcript wording issues before final recording/cut:
  - [x] `cloud-powered` -> `Claude-powered`
  - [x] `crowing` / `rounding` -> `grounding`
  - [x] `prompt portions` -> `prompt versions`
  - [x] `resulting into improvements` -> `resulting in improvements`
  - [x] `system comprises of` -> `system comprises` or `system consists of`
- [x] Ensure video highlights the most important finding: metric validity and abstention failure analysis
- [x] Ensure video states the core thesis clearly: eval loop over demo performance

## Reviewer-Facing Polish

- [x] Add a short note in `README.md` pointing reviewers to `ChatTranscripts.json`
- [x] Optionally add `docs/ai_transcripts.md` with a brief summary of what the raw transcript contains
- [x] Verify the default Anthropic model ID is valid for the review environment
- [x] Re-check doc consistency for metric claims, especially retrieval failures (`7 -> 2`) and RAI artifact filenames
- [x] Confirm RAI docs point to `rai_summary_all.md`, not only QA `eval_summary_all.md`
- [x] Decide whether to fix or explicitly call out the remaining jailbreak/refusal scoring gap
- [x] Consider adding minimal deterministic tests for utility logic

## Suggested Smoke Checks

Run these from the repository root before final submission.

```bash
python main.py ask "Who wrote Pride and Prejudice?" --version v1
python main.py demo --version v1
python -m evals.run_eval --versions v0 v1 --limit 3
python -m evals.run_eval --versions v1 v2 --mode rai --limit 3
python agent/wikipedia_tool.py "Pride and Prejudice"
```

## Submission Packet

- [x] GitHub repo URL
- [x] Video upload/link
- [x] Written rationale/report links
- [x] AI transcript artifact noted
- [x] Any caveats clearly documented, especially metric limitations and known scoring debt