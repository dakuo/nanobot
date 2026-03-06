---
name: r01-ideation
description: "5-step divergent-convergent ideation engine for NIH R01 hypotheses. DIVERGE, DEVELOP, FILTER, CONVERGE, CHECKPOINT. Triggers: 'generate ideas', 'brainstorm aims', 'explore hypotheses'."
---

# Mission

Generate strong NIH R01 hypothesis branches for human-centered AI in healthcare through a structured 5-step ideation pipeline: DIVERGE, DEVELOP, FILTER, CONVERGE, CHECKPOINT. Produce ranked, evidence-backed candidates so downstream agents can draft Specific Aims immediately.

# Working Context

- Operate inside `~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/`.
- Read project intent from `project.yaml`, notes in `ideas/`, and drafts in `docs/` if present.
- Review style and section constraints from `_system/` files when available.
- Mine examples from `~/Dropbox/AgentWorkspace/PriorNIHR01Examples/` for structure, not wording.
- Read `_system/ideation_preferences.json` for the PI's research taste profile. Use `hypothesis_framing.preferences` to bias seed generation toward preferred hypothesis types. Use `methodological_tendency` to favor preferred study designs. Use `risk_appetite` to calibrate how many high-risk aims to propose. Use `topic_preferences` to weight directions toward preferred themes. If the file has no preferences yet (empty arrays), proceed without bias.

# Scratchpad Pattern

Use `<THOUGHT>` and `<OUTPUT>` sections throughout. Perform all reasoning, comparison, and deliberation inside `<THOUGHT>`. Only structured output (JSON, scored tables, final branch descriptions) goes in `<OUTPUT>`. This separation ensures traceable reasoning without polluting deliverables.

# Prior Example Mining

Before generating ideas, read these inputs:
1. `docs/user_input.md` (if it exists) — the user's initial abstract or project description. This is the seed input and original author intent. In express mode, this IS the concept to adopt. In full mode, use it to inform topic direction and clinical context.
2. Proposals in `PriorNIHR01Examples/` — extract structural patterns:
   - Rhetorical moves: how authors frame significance, justify innovation, position against the field.
   - Aim pattern types: mechanistic (test a causal pathway), implementation (deploy and evaluate), evaluation (measure outcomes of an intervention).
   - Risk framing patterns: contingency plans, milestone gates, external validation strategies.
   - Do NOT copy topic claims, specific data values, or narrative phrasing. Extract structural patterns only.

Record extracted patterns in `<THOUGHT>` before proceeding to Step 1.

# Express Mode: User-Provided Concept

If the user provides a fully-formed research concept with specific aims already defined (e.g., in `project.yaml` or as input text), use express mode instead of the full 5-branch divergent pipeline:

1. **ADOPT**: Accept the user's concept as `branch-1`. Extract all Branch Requirements fields (see below) from the user's description. Fill in any missing fields with reasoned completions.
2. **DEVELOP**: Run Step 2 (3-Round Reflection Loop) on `branch-1` only — structured generation, literature grounding, self-critique with quoted evidence. This sharpens the concept without replacing it.
3. **REFINE** (optional): Generate 1-2 alternative framings of the same core idea that vary the intervention mechanism or methodological approach. These are presented as variations, not replacements. Label them `branch-1a`, `branch-1b`.
4. **FILTER + SCORE**: Run Step 3 (feasibility filter) and Step 4 (scoring) on all branches.
5. **CHECKPOINT**: Present the developed `branch-1` (and any variations) to the user for confirmation. The user's original concept is the default selection.

Express mode produces the same `ideas.json` output contract as full mode. The `generation_metadata.divergent_seeds` field should be set to 1 (or 1 + number of variations) and `generation_metadata.express_mode` should be `true`.

When to use express mode vs. full mode:
- **Express**: User provides a concept with 2+ specific aims, a clear clinical problem, and identifiable HCI/AI/healthcare components.
- **Full**: User provides only a topic area or problem statement without aims.

# Step 1: DIVERGE -- Generate 5 Orthogonal Directions

Inject: the topic and domain from `project.yaml`, extracted patterns from prior examples, and any domain constraints specified in `_system/` or `ideas/`.

Generate exactly 5 maximally different research directions. Maximize conceptual distance by varying along three axes simultaneously:
- Intervention mechanism (e.g., predictive model vs. conversational agent vs. workflow redesign vs. sensor fusion vs. shared decision tool)
- User role (e.g., patient self-management vs. specialist clinician vs. care coordinator vs. caregiver vs. community health worker)
- Data pipeline (e.g., EHR-driven vs. wearable-stream vs. NLP-on-notes vs. patient-reported outcomes vs. imaging-plus-clinical)

Each direction: write one paragraph as a seed description. Every seed must span HCI + Healthcare + AI -- reject any single-domain idea before recording it.

# Step 2: DEVELOP -- 3-Round Reflection Loop Per Direction

For each of the 5 seeds, run three rounds of structured development.

## Round 1: Structured Generation

Expand the seed into a full branch using CycleResearcher 5-field structured chain-of-thought:

- Motivation: What gap exists in current understanding or practice? Cite the type of evidence missing.
- Main Idea: What is the proposed contribution? State the core technical or design claim.
- Interestingness: Why does this matter to the field? What assumption does it challenge or what new capability does it unlock?
- Feasibility Narrative: Why is this achievable within a 5-year R01 timeline and budget? Reference available data, team expertise patterns, and technology readiness.
- Novelty Narrative: What is genuinely new here? Distinguish from incremental improvements on existing work.

Also generate for each branch:
- id, title, central_hypothesis (falsifiable)
- specific_aims (2-4 with measurable endpoints and estimated timeline)
- clinical_problem, target_users, hci_component, ai_component

**Title guidance:** Titles must be concise and scannable by reviewers. Aim for 10-15 words maximum. Do not stack multiple descriptors or subclauses. Bad: "PREP-AI: Preparation Readiness and Engagement Platform using AI — Multimodal Home Monitoring for Colonoscopy Preparation Success Prediction and Intervention." Good: "AI-Driven Multimodal Monitoring to Improve Colonoscopy Preparation."

**Central hypothesis guidance:** The hypothesis must be falsifiable but should not include specific quantitative thresholds (e.g., "AUROC ≥ 0.80" or "≥ 30% reduction") unless grounded in pilot data or published benchmarks. Instead, state the directional claim and the measurable dimension. Bad: "will achieve AUROC ≥ 0.80 and reduce inadequate preparation by ≥ 30%." Good: "will significantly improve prediction of preparation failure beyond EHR-only baselines and enable timely interventions that reduce inadequate preparation rates."

**Per-aim timeline estimation:** Each aim must include a realistic timeline estimate that fits within the R01's budget period (typically 5 years). Consider parallelization potential — some aims can overlap. When estimating scope (participant counts, data volumes, deployment phases), work backward from the timeline to determine what is feasible. Example:
- HCI co-design and system implementation: ~1-1.5 years (Year 1 into Year 2)
- Prospective data collection: ~1.5-2 years (Years 2-3, can overlap with late Aim 1)
- Model development: ~1-1.5 years (Years 3-4, starts as Aim 2 data accumulates)
- Pilot evaluation: ~1 year (Years 4-5)
Record this in a `timeline_estimate` field per aim in the branch output.

**Realistic scope for HCI co-design aims:** Iterative co-design cannot tolerate large participant pools — the depth of engagement per participant is high. Realistic ranges:
- Formative stakeholder interviews/contextual inquiry: 10-15 patients, 8-10 clinicians
- Iterative design workshops: 6-10 participants per round, 2-3 rounds
- Usability testing: 8-12 participants per round, 2-3 rounds
- Do NOT propose recruiting 30+ patients and 10+ clinicians for co-design. This is a clinical trial scale, not a design research scale. Reserve large-N recruitment for data collection aims (Aim 2+).

## Round 2: Literature Grounding

Search Semantic Scholar (via web_search or web_fetch) for overlapping work on each branch. For each branch:
- Find 3-5 most relevant existing papers.
- Record them in `related_work_found`.
- Refine the hypothesis: sharpen the novelty claim by differentiating from found work. Adjust aims if a key assumption is already addressed.

## Round 3: Self-Critique with Quoted Evidence

For each branch, generate at least 3 criticisms. Each criticism MUST quote the specific weak point from the branch description -- do not make vague objections. Format:

<THOUGHT>
Criticism 1: The branch states "[quoted text from branch]" but this assumes X, which fails when Y.
Criticism 2: The feasibility narrative claims "[quoted text]" yet ignores Z.
Criticism 3: ...
</THOUGHT>

After critique, for each branch:
- Record criticisms in `self_critique` (with quoted text preserved).
- Add a `fallback_plan`: a concrete pivot if the primary approach encounters the identified weaknesses.

# Step 3: FILTER -- Feasibility and NIH Alignment Gate

Apply a binary pass/fail filter on 6 NIH-adapted criteria to each branch:

1. Requires inaccessible patient data? (e.g., data that cannot be obtained through IRB-approvable protocols or existing repositories)
2. Requires unavailable clinical partnerships? (e.g., partnerships not plausible to establish within Year 1)
3. Unrealistic timeline for 5-year R01? (e.g., requires longitudinal data collection exceeding the grant period)
4. Budget-impossible given R01 caps? (e.g., requires infrastructure or personnel exceeding standard R01 funding)
5. Requires unavailable infrastructure? (e.g., computing resources, clinical systems, or devices not accessible)
6. Contains logical inconsistencies? (e.g., aims that contradict each other, or endpoints that do not test the hypothesis)

Record results in `feasibility_filter_result` as a dict of the 6 criteria mapped to pass/fail.

Prune any branch that fails one or more criteria. If fewer than 3 branches survive, revisit the least-problematic pruned branch: attempt a scoped revision that resolves the failing criterion. If revision succeeds, restore it. Maintain at least 3 surviving branches.

# Step 4: CONVERGE -- Score and Rank

Score each surviving branch on three dimensions (integer 1-10):

- `novelty_score`: Conceptual distinction from existing literature found in Round 2. 10 = no close prior work; 1 = near-duplicate exists.
- `feasibility_score`: Practical achievability with realistic team, data, budget, and timeline. 10 = straightforward execution; 1 = requires multiple breakthroughs.
- `nih_alignment_score`: Fit to NIH priorities -- health impact, scientific rigor, reproducibility, and public benefit. 10 = direct alignment with active FOAs; 1 = tangential.

Compute exploration bonus:
- `diversity_bonus` = kappa * diversity_from_other_branches, where kappa = 0.5 and diversity is measured as average conceptual distance from all other surviving branches (scale 0-10, based on how different the intervention mechanism, user role, and data pipeline are).

Composite score:
- `composite_score = novelty_score + feasibility_score + nih_alignment_score + diversity_bonus`

Every score MUST include a one-sentence evidence-based rationale in `score_rationale`.

For ties in composite_score: conduct pairwise tournament ranking. Compare tied branches A vs B directly -- which has the stronger overall case? Record pairwise results in generation_metadata.

# Step 5: USER CHECKPOINT

Present the top 3 branches to the user with:
- Scores and composite ranking
- One-paragraph rationale per branch summarizing strengths and tradeoffs
- Key risks and mitigations for each

The user selects one branch (or requests modifications to a branch before selecting). Record the selection in `state.json` under the project directory with the selected branch id and any user-requested modifications.

Also record the selection in `_system/ideation_preferences.json` under `selection_history`:
- `project`: current project folder name
- `timestamp`: current ISO 8601
- `branches_presented`: number of branches offered
- `selected_branch_id`: which branch the user chose
- `rejected_branch_ids`: list of branches not chosen
- `rejection_reasons`: if user stated reasons, record them per branch; otherwise null
- `modifications_requested`: any changes the user requested before confirming

If 3+ entries in `selection_history` show a consistent pattern (e.g., user always picks mixed-methods designs, user always rejects survey-only studies), update the corresponding preference field (e.g., `methodological_tendency.preferred_designs` or `methodological_tendency.avoided_designs`). Flag the update to the user: "I noticed you consistently prefer X — I've added this to your ideation preferences."

# Branch Requirements

Each fully developed branch must include all of the following fields:

- `id`: unique identifier (e.g., "branch-1")
- `title`: concise translational focus (10-15 words maximum)
- `central_hypothesis`: falsifiable within a 5-year R01 (directional claims, no unsupported numeric thresholds)
- `specific_aims`: list of 2-4 aims, each with measurable endpoints and `timeline_estimate` (e.g., "Year 1-2")
- `clinical_problem`: disease area or workflow target
- `target_users`: clinicians, patients, care teams, or other stakeholders
- `hci_component`: interaction design and implementation strategy
- `ai_component`: model family, decision-support role, or algorithmic contribution
- `motivation`: gap in current understanding (from Round 1)
- `main_idea`: proposed contribution (from Round 1)
- `interestingness`: why this matters to the field (from Round 1)
- `feasibility_narrative`: why achievable in 5-year R01 (from Round 1)
- `novelty_narrative`: what is genuinely new (from Round 1)
- `related_work_found`: list of relevant papers from Semantic Scholar (from Round 2)
- `self_critique`: list of quoted-evidence criticisms (from Round 3)
- `feasibility_filter_result`: dict of 6 criteria mapped to pass/fail (from Step 3)
- `fallback_plan`: concrete pivot strategy (from Round 3)
- `novelty_score`: integer 1-10 with rationale
- `feasibility_score`: integer 1-10 with rationale
- `nih_alignment_score`: integer 1-10 with rationale
- `diversity_bonus`: float, computed from kappa * distance
- `composite_score`: sum of above
- `score_rationale`: one-sentence evidence-based justification per score dimension
- `key_risks`: list of identified risks
- `mitigations`: list of mitigation strategies corresponding to risks

# Output Contract

Write ranked output to `ideas/ideas.json` with the following structure:

Top-level keys:
- `generation_metadata`: object containing:
  - `divergent_seeds`: number of initial seeds generated (should be 5)
  - `reflection_rounds`: number of reflection rounds per branch (should be 3)
  - `filtered_out`: list of branch ids that failed the feasibility filter, with reason
  - `pairwise_rankings`: list of pairwise comparison results for tied branches (if any)
- `branches`: list of branch objects, each containing all fields from Branch Requirements above, ordered by composite_score descending
- `top_candidates`: list of the top 3 branch ids in descending score order
- `selection_note`: short recommendation for orchestrator handoff (which branch is strongest and why)

After user selection at CHECKPOINT, also write to `state.json`:
- `selected_branch_id`
- `user_modifications` (if any)
- `selection_timestamp`

# Agent Learnings Output
At the end of your work, append an `agent_learnings` JSON block to your final output. This enables cross-agent learning without requiring the generic self-improvement skill.

```json
{
  "agent_learnings": [
    {"type": "error_recovered|better_approach|style_observation", "detail": "specific description"}
  ]
}
```

Log only genuinely useful observations:
- API or tool behavior that differed from expectation
- Writing patterns that worked well or poorly for this section type
- Citation sources that were unexpectedly productive or barren
- Style guide rules that needed interpretation for this domain
Do not log routine operations. The orchestrator collects these and routes to the evolution agent.

# Quality Bar

- Every branch spans HCI + healthcare + AI. Reject single-domain ideas.
- Hypotheses are falsifiable and linked to measurable outcomes, not broad aspirations. Do not include specific numeric thresholds (AUROC values, percentage reductions) unless supported by cited pilot data.
- Titles are concise (10-15 words). Do not stack sub-titles or explanatory clauses.
- Each aim includes a realistic timeline estimate that fits within 5-year R01 budget period.
- HCI co-design aims propose realistic participant counts (10-15 patients, 8-10 clinicians for formative work, not clinical trial scale recruitment).
- Self-critiques quote specific text from the branch -- no generic objections.
- Literature search is real: use Semantic Scholar, record actual paper titles and findings.
- Scores have evidence-based rationales, not unsupported numbers.
- Language is NIH-appropriate, concise, and reviewer-facing.
- Output is machine-parseable JSON with no trailing commentary.
