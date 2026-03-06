# R01 Orchestrator Pipeline Specification

This document defines the 11 canonical pipeline phases for `r01-orchestrator`.

## Shared Conventions
- `state.json` is the source of truth for orchestration state.
- `events.jsonl` and `cost.jsonl` are append-only logs.
- On any subagent failure: record event, mark phase blocked/failed, retry failed task, do not overwrite successful outputs.

## Phase 1: init
**Entry criteria**
- Project path exists under `~/Dropbox/AgentWorkspace/PaperAutoGen/{project-name}/`.
- `state.json.current_phase` is `init` or missing.

**Agent(s)**
- Orchestrator only (no subagent required).

**Actions**
1. Validate project directory and required files (`project.yaml`, `state.json`, `cost.jsonl`, `events.jsonl`).
2. Initialize missing state fields.
3. Create `ideas/findings_memory.json` as an empty array `[]` if it does not already exist.
4. Populate `state.json.writing_parallel` with dynamic aim entries: for each aim in `project.yaml.aims[]`, add `approach_aim{i}: {agent: r01-writer-{aim.domain_tag}, status: pending, attempt: 0, word_count: 0, draft_version: 0}`.
5. If the user provided an initial abstract or project description (the "30-line draft"), save it to `docs/user_input.md`. This file is read by the ideation agent, literature agents, and writers as the seed input and original author intent. It must be preserved unchanged throughout the pipeline.
6. Record initialization events.

**Output artifacts**
- `project.yaml` (existing or initialized)
- `state.json`
- `events.jsonl`
- `cost.jsonl`
- `ideas/findings_memory.json`
- `docs/user_input.md` (if user provided initial abstract)

**Exit criteria**
- `state.json.current_phase = metadata` and `state.json.phase_status.init = complete`.

**Error handling**
- If setup fails, set `phase_status.init = failed`, append error event, stop progression.

## Phase 1.5: metadata
**Entry criteria**
- `phase_status.init = complete`.
- `current_phase = metadata`.

**Agent(s)**
- Orchestrator (interactive dialog with user)
- `r01-foa-finder` (spawned if NIH context needs inference)

**Purpose**
Collect project meta-information that downstream phases depend on: investigator team, NIH institute targeting, clinical trial classification, FOA/RFA identification, and submission timeline. This runs before ideation so that even the first 30-line abstract can leverage PI and institute context.

**Actions**
1. Read `project.yaml` and check for missing metadata fields.
2. **Investigator collection** — check `project.yaml.investigators`:
   - If PI name is null: prompt user interactively: "Who is the PI on this project? (Name, institution, Google Scholar ID or ORCID if available)"
   - If co-investigators are empty: prompt: "Any co-investigators? (Name, role, expertise — or skip)"
   - If `scholar_id` is provided for any investigator: queue publication fetch for literature phase.
3. **Clinical trial classification** — check `project.yaml.nih_context.clinical_trial_classification`:
   - If null: prompt user: "Does this project involve a clinical trial? (not_allowed / optional / required)"
   - This determines which Parent R01 NOFO applies (PA-25-301/302/303).
4. **NIH context collection** — check `project.yaml.nih_context.target_institute` and `foa.number`:
   - If target_institute is null OR foa.number is null:
     a. Spawn `r01-foa-finder` with project topic, aims, clinical_trial_classification.
     b. Agent searches Grants.gov for active FOAs, NIH Reporter for funded project intelligence, Highlighted Topics for alignment.
     c. Agent writes `docs/foa_analysis.md` with ranked recommendations.
     d. Present recommendations to user: "Based on your topic, I recommend [IC] with [FOA]. Agree?"
     e. User confirms or overrides.
   - If user provides target_institute and foa.number directly: skip r01-foa-finder.
5. **Submission timeline** — check `project.yaml.submission.cycle`:
   - If null: calculate next R01 receipt date from current date (Feb 5 / Jun 5 / Oct 5).
   - Compute project_start (cycle + 9 months) and project_end (start + budget_period - 1 day).
   - Present to user for confirmation.
6. Update `project.yaml` with all confirmed metadata.
7. Record metadata collection events.

**Interactive dialog pattern**
The orchestrator uses the same checkpoint mechanism as other user-facing phases. Questions are asked one group at a time, not all at once:
- Group 1: PI name, institution, scholar_id (most critical)
- Group 2: Clinical trial classification (affects FOA selection)
- Group 3: NIH institute + FOA (may require r01-foa-finder run between groups 2 and 3)
- Group 4: Submission cycle confirmation

If the user provides all metadata upfront in `project.yaml`, this phase auto-completes with no interaction.

**Output artifacts**
- `project.yaml` updated with `investigators`, `nih_context`, `submission` sections
- `docs/foa_analysis.md` (if r01-foa-finder was spawned)

**Exit criteria**
- `state.json.current_phase = ideation` and `state.json.phase_status.metadata = complete`.
- `project.yaml.investigators.pi.name` is not null.
- `project.yaml.nih_context.clinical_trial_classification` is not null.
- `project.yaml.nih_context.foa.number` is not null (at minimum, Parent R01).
- `project.yaml.submission.cycle` is not null.

**Error handling**
- If user does not respond to checkpoint: set `checkpoints_awaiting_user` with the pending question group, pause pipeline.
- If r01-foa-finder fails: log error, prompt user to provide NIH context manually.

## Phase 2: ideation
**Entry criteria**
- `phase_status.metadata = complete`.
- `current_phase = ideation`.

**Agent(s)**
- `r01-ideation`
- `r01-novelty-checker` (sub-step, spawned by orchestrator after FILTER)

**Mode selection**
The orchestrator determines which ideation mode to use:
- **Express mode**: If the user provides a fully-formed concept with 2+ specific aims, a clear clinical problem, and identifiable HCI/AI/healthcare components (e.g., aims are already defined in `project.yaml` with descriptions). The ideation agent adopts the user's concept as branch-1 and develops it through the reflection loop without generating 5 orthogonal alternatives.
- **Full mode**: If the user provides only a topic area or problem statement without specific aims. The ideation agent generates 5 orthogonal directions through the full DIVERGE/DEVELOP/FILTER/CONVERGE/CHECKPOINT pipeline.

The orchestrator communicates the mode to the ideation agent in the spawn prompt: "Use express mode — the user has provided a complete concept with N aims" or "Use full mode — generate 5 orthogonal directions from the topic."

**Actions**
1. Spawn ideation agent with project constraints and scope.
2. Ideation agent runs a 5-step flow:
   - **DIVERGE**: generate a broad set of candidate ideas without filtering.
   - **DEVELOP**: expand each candidate with a 5-field chain-of-thought (problem, mechanism, novelty claim, feasibility risk, NIH fit).
   - **FILTER**: apply feasibility criteria; drop ideas that fail on budget, timeline, or team capacity.
   - **CONVERGE**: rank surviving ideas; select top 3-5 for novelty checking.
   - **CHECKPOINT**: pause for user idea selection after novelty verdicts are in.
3. After FILTER, orchestrator spawns `r01-novelty-checker` as a sub-step. The novelty checker runs background literature retrieval, applies a dual-bias protocol, and writes `ideas/novelty_report.json`.
4. Ideation agent reads `ideas/novelty_report.json` before CONVERGE to incorporate novelty verdicts into final rankings.
5. Save candidate ideas with full 5-field CoT, novelty verdicts, and feasibility filter results to `ideas/ideas.json`.
6. Trigger user checkpoint for idea selection.

**Output artifacts**
- `ideas/ideas.json` (each entry includes 5-field CoT, novelty verdict, feasibility filter result)
- `ideas/novelty_report.json`
- checkpoint event in `state.json.events`

**Exit criteria**
- User selects one concept and confirmation is recorded.
- `ideas/ideas.json` entries include 5-field CoT, novelty verdicts, and feasibility filter results.
- `phase_status.ideation = complete`.

**Error handling**
- On failure, append failure event with task metadata and allow targeted retry.

## Phase 3: literature
**Entry criteria**
- `phase_status.ideation = complete`.
- `current_phase = literature`.

**Agent(s)**
- `r01-literature` × 3 in parallel (one per domain: hci, healthcare, ai).

**Actions**
1. Populate `state.json.literature_parallel` with entries for hci, healthcare, ai.
2. Spawn 3 literature subagents simultaneously, each assigned one domain.
3. Each agent runs a multi-round search workflow:
   - Steps 1-4: Build query packs, execute searches, fetch paper details, filter and prioritize.
   - Step 4.5: Citation graph traversal (snowball sampling via Semantic Scholar API — forward citations and backward references from top 5 must-cite papers, capped at 10 additional papers).
   - Step 4.7: Iterative query refinement — assess per-aim coverage, generate refined queries from discovered terminology, run up to 3 total search rounds, exit early when all aims have 5+ papers.
   - Step 5: Annotate each reference with structured fields including `supports_claim` (claim-evidence mapping — one-sentence proposal claim the reference supports).
   - Step 6: Gap analysis with contradiction detection (flag conflicting findings across papers) and evidence synthesis tables (per-aim: paper, population, method, outcome, finding, limitation, our advantage).
4. Each writes `literature/references_{domain}.json` (with `_metadata` header tracking rounds and snowball stats) and `literature/gaps_{domain}.md`.
5. Track per-domain status in `state.json.literature_parallel`.
6. When all 3 complete, merge:
   - Combine `literature/references_{hci,healthcare,ai}.json` into `literature/references.json`. Deduplicate by DOI/URL — when duplicates exist, keep the annotation with higher priority (`must-cite` > `supporting` > `optional`). Merge `_metadata` into a combined summary.
   - Combine `literature/gaps_{hci,healthcare,ai}.md` into `literature/gaps.md`. Preserve all domain-specific sections. Consolidate cross-domain contradictions and evidence synthesis tables.
   - Validate `supports_claim` coverage: every `must-cite` reference in the merged file must have a non-empty `supports_claim`.

**Output artifacts**
- `literature/references_hci.json`
- `literature/references_healthcare.json`
- `literature/references_ai.json`
- `literature/gaps_hci.md`
- `literature/gaps_healthcare.md`
- `literature/gaps_ai.md`
- `literature/references.json` (merged, deduplicated, with combined _metadata)
- `literature/gaps.md` (merged, with cross-domain contradictions and synthesis tables)

**Exit criteria**
- All 3 domain searches complete with 10+ references each.
- Merged references.json exists and contains 30-50 references.
- Every `must-cite` reference has a non-empty `supports_claim` field.
- Merged gaps.md covers all three domains, includes contradiction detection results, and has evidence synthesis tables.
- `phase_status.literature = complete`.

**Error handling**
- Log failure in `events.jsonl`, set blocked status, retry literature only.

## Phase 4: outline
**Entry criteria**
- `phase_status.literature = complete`.
- `current_phase = outline`.

**Agent(s)**
- `r01-writer-integrator`.

**Actions**
1. Build proposal skeleton and section ordering.
2. Map aims to sections and dependencies.
3. Set up writing task plan in `state.json.writing_parallel`.

**Output artifacts**
- `docs/outline.md`
- updated `state.json.writing_parallel`

**Exit criteria**
- Outline approved by orchestrator checks.
- `phase_status.outline = complete`.

**Error handling**
- Record failure, keep prior outputs, retry integrator task.

## Phase 5: writing
**Entry criteria**
- `phase_status.outline = complete`.
- `current_phase = writing`.

**Agent(s)**
- `r01-writer-integrator` and domain writers:
  - `r01-writer-hci`
  - `r01-writer-healthcare`
  - `r01-writer-ai`

**Actions**
1. Read `project.yaml` aim-to-domain mapping and model overrides.
2. Dynamically generate one writer batch per aim from `project.yaml.aims[]`:
   - Batch A: `r01-writer-integrator` → specific_aims, significance, innovation
   - Batches B..N: For each aim `i` in `project.yaml.aims[]`, dispatch `r01-writer-{aims[i].domain_tag}` → `approach_aim{i}`
3. Dispatch batch A and all aim batches simultaneously, each with `max_iterations=30` and per-skill `model`.
4. Each writer reads: SKILL.md, outline.md, refs.json, gaps.md, ideas.json, PriorNIHR01Examples/, style_guide.md, r01_section_specs.md.
5. After all parallel batches complete, spawn assembly batch: `r01-writer-integrator` for timeline, crosscutting, project_narrative, project_summary + merge all into research_strategy_v1.md.
6. See `parallel_execution.md` for full prompt templates.

**Output artifacts**
- `docs/drafts/specific_aims_v1.md`
- `docs/drafts/significance_v1.md`
- `docs/drafts/innovation_v1.md`
- `docs/drafts/approach_aim{1..N}_v1.md` (one per aim in `project.yaml`)
- `docs/drafts/approach_timeline_v1.md`
- `docs/drafts/approach_crosscutting_v1.md`
- `docs/drafts/project_narrative_v1.md`
- `docs/drafts/project_summary_v1.md`
- `docs/drafts/research_strategy_v1.md` (merged)

**Exit criteria**
- All writing_parallel tasks are `complete`.
- `writing_integration.status = complete`.
- Merged research_strategy_v1.md exists and has no unresolved placeholders.
- `phase_status.writing = complete`.

**Error handling**
- Retry failed batches only; keep successful section files unchanged.
- If a domain writer batch fails, do not retry integrator batches.

## Phase 6: figures
**Entry criteria**
- `phase_status.writing = complete`.
- `current_phase = figures`.

**Agent(s)**
- `r01-figures`.

**Actions**
1. Generate figure plan from research strategy.
2. Draft captions and figure-text alignment notes.

**Output artifacts**
- `figures/specs/F{N}.yaml`
- `figures/exports/F{N}.svg`
- `figures/exports/F{N}.png`
- `figures/captions.md`

**Exit criteria**
- Figure plan and captions are present and linked to aims.
- `phase_status.figures = complete`.

**Error handling**
- Log failure and retry figure generation without rerunning writing.

## Phase 7: budget
**Entry criteria**
- `phase_status.writing = complete`.
- `current_phase = budget`.

**Agent(s)**
- `r01-budget`.

**Actions**
1. Draft budget assumptions from timeline and staffing.
2. Produce line-item narrative and justification text.

**Output artifacts**
- `budget/budget_table.md`
- `budget/budget_justification.md`

**Exit criteria**
- Budget draft is complete and consistent with scope.
- `phase_status.budget = complete`.

**Error handling**
- Log failure and retry budget phase independently.

## Phase 8: review
**Entry criteria**
- `phase_status.writing = complete`.
- `phase_status.figures = complete`.
- `phase_status.budget = complete`.
- `current_phase = review`.

**Pre-review gate (optional)**
Before spawning the three domain reviewers, the orchestrator MAY spawn `r01-writer-integrator` in a lightweight self-review mode to catch obvious issues (missing sections, broken citations, unresolved placeholders, word-count violations) cheaply. If blocking issues are found, route back to writing for targeted fixes. Record the outcome in `state.json.pre_review_gate`.

**Agent(s)**
- Parallel: `r01-reviewer-hci`, `r01-reviewer-healthcare`, `r01-reviewer-ai`
- Fan-in: `r01-reviewer-panel`

**Actions**
1. Spawn three domain reviewers on full draft package.
2. Each reviewer runs a background retrieval step to pull relevant prior art before scoring.
3. Each reviewer applies a dual-bias protocol (one pass as skeptic, one as advocate) to reduce anchoring.
4. Each reviewer produces structured JSON output.
5. Track each review in `state.json.review_parallel`.
6. When all are complete, spawn panel reviewer for synthesis and score.
7. Panel runs a reflection loop: reads all three domain reviews, identifies conflicts, resolves them with explicit reasoning.
8. Panel produces `panelist_perspectives`, a revision priority matrix, and a `findings_memory_entry` object.
9. Panel appends its `findings_memory_entry` to `ideas/findings_memory.json`.

**Output artifacts**
- `reviews/review_hci_r{N}.json` (fields: `nih_dimensions`, `background_findings`, `review_confidence`, `critique_items`)
- `reviews/review_healthcare_r{N}.json` (same fields)
- `reviews/review_ai_r{N}.json` (same fields)
- `reviews/panel_summary_r{N}.md`
- `reviews/panel_decision_r{N}.json` (fields: `impact_score`, `panelist_perspectives`, `revision_priority_matrix`, `findings_memory_entry`)

**Exit criteria**
- Panel review includes impact score (1-9) and prioritized issues.
- If score `< 5` and rounds remain: route to revision.
- Otherwise: `phase_status.review = complete`.

**Error handling**
- Retry only failed reviewer tasks; do not discard completed review files.

## Phase 9: revision
**Entry criteria**
- Review route requests revision (`score < 5`).
- `review_round < max_review_rounds`.
- `current_phase = revision`.

**Agent(s)**
- `r01-reviser`.

**Actions**
1. Reviser reads `ideas/findings_memory.json` to understand cumulative findings across all prior rounds.
2. Reviser generates its own revision plan from the panel priorities, domain critiques, and findings memory.
3. Patch draft sections according to the revision plan.
4. Produce `reviews/revision_diffs_r{N}.json` documenting what changed and why.
5. Append a revision summary entry to `ideas/findings_memory.json`.
6. Increment `review_round` and route back to review.

**Output artifacts**
- `docs/drafts/research_strategy_v{N}.md`
- `reviews/revision_log_r{N}.md`
- `reviews/revision_diffs_r{N}.json`
- `ideas/findings_memory.json` (updated with revision summary entry)

**Exit criteria**
- Revised draft exists and issue responses are documented.
- `reviews/revision_diffs_r{N}.json` records all section-level changes.
- `phase_status.revision = complete`.

**Error handling**
- Log failure, preserve previous draft, retry reviser only.

## Phase 10: export
**Entry criteria**
- Review is passing or user accepts current package.
- `current_phase = export`.

**Agent(s)**
- Orchestrator only (assembly/checkpoint handling).

**Actions**
1. Assemble final narrative, figures, and budget packet.
2. Generate export manifest.
3. Post final checkpoint to Slack and wait for user sign-off.

**Output artifacts**
- `export/r01_submission_bundle_v1/`
- `export/export_manifest_v1.md`

**Exit criteria**
- User final approval recorded.
- `phase_status.export = complete` and pipeline marked complete.

**Error handling**
- Record assembly errors, keep intermediate artifacts, and retry export assembly.

## Phase 11: evolution
**Entry criteria**
- `phase_status.export = complete`.
- User has approved the final export package OR user has provided real NIH reviewer feedback.
- `current_phase = evolution`.

**Agent(s)**
- `r01-evolution`.

**Actions**
1. Read all review JSONs, revision diffs, findings memory, and user/NIH feedback from the completed project.
2. Identify weakness patterns, strength patterns, and revision effectiveness.
3. Update `_system/reviewer_patterns.json` with new or incremented patterns.
4. Append learning entries to `_system/evolution_log.json`.
5. If evidence suggests style guide changes, propose them to the user and wait for approval.
6. Cross-reference patterns against all prior projects to detect high-frequency patterns (3+) for potential promotion to style guide.

**Output artifacts**
- Updated `_system/reviewer_patterns.json`
- Updated `_system/evolution_log.json` (at least one new entry)
- Optionally updated `_system/style_guide.md` (user approval required)
- Evolution summary report presented to user

**Exit criteria**
- `reviewer_patterns.json` updated with at least one new or incremented pattern.
- `evolution_log.json` has at least one new entry for this project.
- User has been presented with any proposed style guide changes.
- `phase_status.evolution = complete`.

**Error handling**
- Log failure but do not block pipeline completion — the export is already done. Evolution failure is non-fatal.
- Retry evolution independently without affecting exported artifacts.
