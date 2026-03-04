---
name: r01-ideation
description: "Generate and refine NIH R01 research hypotheses using tree-search exploration. Scores ideas on novelty, feasibility, and NIH alignment. Triggers: 'generate ideas', 'brainstorm aims', 'explore hypotheses'."
---

# Mission
Generate 3-5 strong NIH R01 hypothesis branches for human-centered AI in medicine, then rank them with a transparent rubric so downstream agents can draft Specific Aims immediately.

# Working Context
- Operate inside `~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/`.
- Read project intent from `project.yaml`, notes in `ideas/`, and drafts in `docs/` if present.
- Review style and section constraints from `_system/` files when available.
- Mine examples from `~/Dropbox/AgentWorkspace/PriorNIHR01Examples/` for structure, not wording.

# Tree-Search Exploration Procedure
1. Define a root problem statement with measurable clinical burden and a target care setting.
2. Expand to 3-5 branches that vary intervention mechanism, user role, and data pipeline.
3. For each branch, write one central hypothesis that is falsifiable within a 5-year R01 timeline.
4. Derive 2-3 draft aims per branch and map each aim to outcomes.
5. Prune branches requiring unrealistic partnerships, inaccessible data, or unsupported infrastructure.
6. Keep at least one branch with conservative risk and one with higher innovation upside.

# Branch Requirements
Each branch must include:
- `title` with a concise translational focus.
- `clinical_problem` with disease area or workflow target.
- `target_users` including clinicians, patients, or care teams.
- `ai_component` describing model family or decision-support role.
- `hci_component` describing interaction and implementation strategy.
- `specific_aims` with measurable endpoints.
- `key_risks` and mitigation notes.

# Scoring Rubric
Score each branch on integer 1-5 scales.

- `novelty`: conceptual distinction from existing approaches.
- `feasibility`: practical achievability with expected team/data/resources.
- `nih_alignment`: fit to health impact, rigor, and public benefit.

Optional tie-break helper:
- `translational_readiness`: likelihood of real-world deployment trajectory.

Compute:
- `composite_score = novelty + feasibility + nih_alignment`

Tie-break order:
1. Higher `nih_alignment`
2. Higher `feasibility`
3. Higher `translational_readiness` if present

For every score, include a one-sentence evidence-based rationale.

# Prior Example Mining
- Read multiple proposals in `PriorNIHR01Examples/` and extract reusable rhetorical moves.
- Capture aim pattern types: mechanistic, implementation, evaluation.
- Capture risk framing patterns: contingency plans, milestone gates, external validation.
- Do not copy topic claims, values, or narrative phrasing.

# Output Contract
Write ranked output to `ideas/ideas.json` with this schema per branch:
- `id`
- `title`
- `central_hypothesis`
- `specific_aims`
- `clinical_problem`
- `target_users`
- `hci_component`
- `ai_component`
- `novelty`
- `feasibility`
- `nih_alignment`
- `composite_score`
- `score_rationale`
- `inspiration_examples`
- `key_risks`
- `mitigations`
- `tradeoff_summary`

Also include:
- `top_candidates`: top 3 branch IDs in descending score order.
- `selection_note`: short recommendation for orchestrator handoff.

# Quality Bar
- Every branch spans HCI + healthcare + AI, not a single-domain idea.
- Hypotheses are testable and linked to outcomes, not broad aspirations.
- Language is NIH-appropriate, concise, and reviewer-facing.
- Output is machine-parseable JSON with no trailing commentary.
