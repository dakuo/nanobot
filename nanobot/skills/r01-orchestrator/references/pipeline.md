# R01 Orchestrator Pipeline Specification

This document defines the 10 canonical pipeline phases for `r01-orchestrator`.

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
3. Record initialization events.

**Output artifacts**
- `project.yaml` (existing or initialized)
- `state.json`
- `events.jsonl`
- `cost.jsonl`

**Exit criteria**
- `state.json.current_phase = ideation` and `state.json.phase_status.init = complete`.

**Error handling**
- If setup fails, set `phase_status.init = failed`, append error event, stop progression.

## Phase 2: ideation
**Entry criteria**
- `phase_status.init = complete`.
- `current_phase = ideation`.

**Agent(s)**
- `r01-ideation`.

**Actions**
1. Spawn ideation agent with project constraints and scope.
2. Save candidate ideas and tradeoffs.
3. Trigger user checkpoint for idea selection.

**Output artifacts**
- `ideas/ideas.json`
- checkpoint event in `state.json.events`

**Exit criteria**
- User selects one concept and confirmation is recorded.
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
3. Each agent uses web_search, web_fetch, and API calls to find 10-18 real papers.
4. Each writes `literature/references_{domain}.json` and `literature/gaps_{domain}.md`.
5. Track per-domain status in `state.json.literature_parallel`.
6. When all 3 complete: merge into `literature/references.json` and `literature/gaps.md`, deduplicating by DOI/URL.

**Output artifacts**
- `literature/references_hci.json`
- `literature/references_healthcare.json`
- `literature/references_ai.json`
- `literature/gaps_hci.md`
- `literature/gaps_healthcare.md`
- `literature/gaps_ai.md`
- `literature/references.json` (merged, deduplicated)
- `literature/gaps.md` (merged)

**Exit criteria**
- All 3 domain searches complete with 10+ references each.
- Merged references.json exists and contains 30-50 references.
- Merged gaps.md covers all three domains.
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
- `docs/drafts/outline_v1.md`
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
1. Read `project.yaml` aim-to-domain mapping.
2. Dispatch parallel section writers and track statuses.
3. Require each writer to read `PriorNIHR01Examples/` and write `docs/drafts/{section}_v{N}.md`.
4. After all writer tasks complete, run integrator merge pass.

**Output artifacts**
- `docs/drafts/specific_aims_v1.md`
- `docs/drafts/significance_v1.md`
- `docs/drafts/innovation_v1.md`
- `docs/drafts/approach_aim1_v1.md`
- `docs/drafts/approach_aim2_v1.md`
- `docs/drafts/approach_aim3_v1.md`
- `docs/drafts/research_strategy_v1.md`

**Exit criteria**
- All required writing tasks are `complete`.
- Merge output exists and has no unresolved placeholders.
- `phase_status.writing = complete`.

**Error handling**
- Retry failed writers only; keep successful section files unchanged.

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

**Agent(s)**
- Parallel: `r01-reviewer-hci`, `r01-reviewer-healthcare`, `r01-reviewer-ai`
- Fan-in: `r01-reviewer-panel`

**Actions**
1. Spawn three domain reviewers on full draft package.
2. Track each review in `state.json.review_parallel`.
3. When all are complete, spawn panel reviewer for synthesis and score.

**Output artifacts**
- `reviews/review_hci_r{N}.json`
- `reviews/review_healthcare_r{N}.json`
- `reviews/review_ai_r{N}.json`
- `reviews/panel_summary_r{N}.md`
- `reviews/panel_decision_r{N}.json`

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
1. Spawn reviser with panel priorities and domain critiques.
2. Patch draft sections and record what changed.
3. Increment `review_round` and route back to review.

**Output artifacts**
- `docs/drafts/research_strategy_v{N}.md`
- `reviews/revision_log_r{N}.md`

**Exit criteria**
- Revised draft exists and issue responses are documented.
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
