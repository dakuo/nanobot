# Paper Orchestrator Pipeline Specification

This document defines the 8 canonical pipeline phases for `paper-orchestrator`.

## Shared Conventions
- `state.json` is the source of truth for orchestration state.
- `events.jsonl` and `cost.jsonl` are append-only logs.
- On any subagent failure: record event, mark phase blocked/failed, retry failed task, do not overwrite successful outputs.
- All spawns must include `DOCUMENT_TYPE: paper`, `VENUE`, and `CONTRIBUTION_TYPE` in the task prompt.
- Workspace path: `~/Dropbox/AgentWorkspace/PaperAutoGen/chi-{paper-name}/`.

---

## Phase 1: init

**Entry criteria**
- Project path exists under `~/Dropbox/AgentWorkspace/PaperAutoGen/chi-{paper-name}/`.
- `state.json.current_phase` is `init` or missing.

**Agent(s)**
- Orchestrator only (no subagent required).

**Actions**
1. Validate project directory and required files (`paper_project.yaml`, `state.json`, `cost.jsonl`, `events.jsonl`).
2. Read `paper_project.yaml` and validate:
   - `document_type` is `"paper"` (reject if `"r01"`).
   - `venue` is one of: CHI, CSCW, UIST, UbiComp, IMWUT, DIS.
   - `contribution_type` is one of: empirical, artifact, methodological, theoretical, survey, opinion, benchmark.
   - `sections` array is non-empty and each section has `name`, `domain_tag`, and `word_target`.
   - `domain_tags` array is non-empty.
3. Initialize missing state fields in `state.json`.
4. Create `reviews/findings_memory.json` as an empty array `[]` if it does not already exist.
5. Populate `state.json.writing_parallel` with dynamic section entries from `paper_project.yaml.sections[]`.
6. If the user provided an abstract or paper description, save it to `docs/user_input.md`.
7. Create subdirectories: `docs/drafts/`, `literature/`, `figures/specs/`, `figures/exports/`, `reviews/`, `feedback/`, `export/`.
8. Record initialization events in `events.jsonl`.

**Output artifacts**
- `paper_project.yaml` (validated)
- `state.json` (initialized)
- `events.jsonl` (init event recorded)
- `cost.jsonl` (zero-cost init entry)
- `reviews/findings_memory.json`
- `docs/user_input.md` (if user provided initial abstract)

**Exit criteria**
- `state.json.current_phase = literature` and `state.json.phase_status.init = complete`.
- All validation checks pass.

**Error handling**
- If `document_type` is not `"paper"`: abort with clear error message directing user to r01-orchestrator.
- If venue or contribution_type is invalid: list valid options and ask user to fix `paper_project.yaml`.
- If setup fails: set `phase_status.init = failed`, append error event, stop progression.

---

## Phase 2: literature

**Entry criteria**
- `phase_status.init = complete`.
- `current_phase = literature`.

**Entry validation (mid-pipeline)**
To enter this phase directly (skipping prior phases):
- Required files: `paper_project.yaml`, `state.json` (initialized)
- state.json: `current_phase` set to `literature`, `phase_status.init` marked `complete` or `skipped`
- Auto-setup: Run init workspace scaffolding (create subdirectories, `findings_memory.json`, populate `writing_parallel`)
- Validation: Rarely entered mid-pipeline. If literature is itself skipped, set `phase_status.literature: skipped`, downstream writers will proceed without `references.json`

**Agent(s)**
- `literature` × N in parallel (one per domain tag in `paper_project.yaml.domain_tags`).

**Actions**
1. Read `paper_project.yaml` → get `domain_tags` array (e.g., `[hci, ai]` for a two-domain paper, or `[hci, healthcare, ai]` for three).
2. Populate `state.json.literature_parallel` with one entry per domain.
3. Spawn N literature subagents with **30-second stagger** between launches to avoid API rate limits:
   - Each reads `literature` skill and is assigned one domain.
   - Task prompt: "You are the {domain} literature agent. Read the literature skill at {skill_path} and follow its instructions. Your domain assignment is: {domain}. DOCUMENT_TYPE: paper. Project path: ~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/. Find 8-15 references for the {domain} domain. Use citation graph traversal and iterative query refinement. Write to literature/references_{domain}.json and literature/gaps_{domain}.md."
   - Spawn call: `spawn(task=..., label="lit-{domain}", max_iterations=30, model=..., workspace="~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/")`
4. **State tracking (MANDATORY, do this for EVERY spawn and retry):**
   - **Before each spawn**: Read `state.json`, set `literature_parallel.{domain}.status = "running"`, increment `attempt`, write back. Append event.
   - **On agent success**: Set status to `"complete"`, append event.
   - **On agent failure**: Set status to `"failed"`, append event with failure reason.
   - **Max retries**: If `attempt >= 3` and still `"failed"`, mark phase `"blocked"` and request user intervention.
5. When all domain searches complete:
   - Merge `literature/references_{domain}.json` files into `literature/references.json`.
   - Deduplicate by DOI/URL, keep highest-priority annotation (`must-cite` > `supporting` > `optional`).
   - Build `thematic_clusters` in merged references: group references by theme/topic for the related work section. Each cluster has a `theme_label`, `description`, and list of `reference_ids`.
   - Merge gap files into `literature/gaps.md`, consolidating cross-domain findings.
   - Validate: every `must-cite` reference has a non-empty `supports_claim`.

**Output artifacts**
- `literature/references_{domain}.json` (one per domain)
- `literature/gaps_{domain}.md` (one per domain)
- `literature/references.json` (merged, deduplicated, with thematic_clusters)
- `literature/gaps.md` (merged)

**Exit criteria**
- All domain searches complete with 8+ references each.
- Merged `references.json` exists with 15-40 references (scaled to paper length, not grant length).
- Every `must-cite` reference has a non-empty `supports_claim`.
- `thematic_clusters` array is non-empty in merged references.
- `phase_status.literature = complete`.

**Error handling**
- Log failure in `events.jsonl`, set blocked status, retry only the failed domain.
- If a single domain fails after 3 retries, allow the user to proceed with partial literature (other domains' references are still valid).

---

## Phase 3: outline

**Entry criteria**
- `phase_status.literature = complete`.
- `current_phase = outline`.

**Entry validation (mid-pipeline)**
To enter this phase directly (skipping prior phases):
- Required files: `literature/references.json` OR literature phase skipped; `paper_project.yaml`, `state.json`
- state.json: `current_phase` set to `outline`, `phase_status.init` and `phase_status.literature` marked `complete` or `skipped`
- Auto-setup: If `literature/references.json` is absent, set `phase_status.literature: skipped` so writers know no references exist
- Validation: Verify `paper_project.yaml.sections` is non-empty and `writing_parallel` is populated

**Agent(s)**
- `writer-integrator`.

**Actions**
1. Spawn `writer-integrator` with paper outline mode:
   - Task prompt includes: `DOCUMENT_TYPE: paper`, `VENUE: {venue}`, `CONTRIBUTION_TYPE: {contribution_type}`.
   - Instruct agent to read `references/chi_paper_structures.md` (bundled reference) for canonical section structure matching the contribution type.
   - Instruct agent to read `~/Dropbox/AgentWorkspace/PaperAutoGen/_system/chi_section_specs.md` for venue formatting.
2. The integrator produces a 3-pass outline:
   - **Pass 1 (skeleton)**: Top-level section headings based on contribution type template.
   - **Pass 2 (detail)**: Subsection headings, key arguments per section, citation anchors from references.json.
   - **Pass 3 (review)**: Word budget allocation per section (respecting venue page limits), cross-reference consistency.
3. Map sections to domain writers based on `paper_project.yaml.sections`.
4. Update `state.json.writing_parallel` with finalized section assignments and word targets.
5. Trigger user checkpoint for outline review.

**Output artifacts**
- `docs/outline.md` (full outline with section headings, word budgets, key arguments, citation anchors)
- Updated `state.json.writing_parallel`

**Exit criteria**
- `docs/outline.md` exists and covers all sections from `paper_project.yaml.sections`.
- Word budgets sum to within venue page limits (±10%).
- User has approved the outline at checkpoint.
- `phase_status.outline = complete`.

**Error handling**
- If integrator fails: record failure, retry. Keep any partial outline for user inspection.
- If user requests structural changes: re-spawn integrator with feedback, do not start from scratch.

---

## Phase 4: writing

**Entry criteria**
- `phase_status.outline = complete`.
- `current_phase = writing`.

**Entry validation (mid-pipeline)**
To enter this phase directly (skipping prior phases):
- Required files: `docs/outline.md`, `paper_project.yaml`, `state.json`
- state.json: `current_phase` set to `writing`, prior phases (`init`, `literature`, `outline`) marked `complete` or `skipped`
- Auto-setup: If user provided an outline, copy it to `docs/outline.md`. If entering from a draft import, auto-generate outline from draft section headers
- Validation: `docs/outline.md` must cover all sections from `paper_project.yaml.sections`; `writing_parallel` must be populated

**Agent(s)**
- `writer-integrator` (integrative sections + assembly)
- Domain writers per `paper_project.yaml.sections[].domain_tag`:
  - `writer-hci` for HCI-tagged sections
  - `writer-healthcare` for healthcare-tagged sections
  - `writer-ai` for AI-tagged sections

**Actions**
1. Read `paper_project.yaml` → get section-to-domain mapping and model overrides.
2. Group sections into batches:
   - **Batch A** (writer-integrator): introduction, related_work, discussion, conclusion.
   - **Batches B..N** (domain writers): For each domain-specific section in `paper_project.yaml.sections[]` (e.g., methodology, system_design, evaluation, analysis), dispatch `writer-{section.domain_tag}`.
3. Dispatch batch A and all domain batches simultaneously:
   - Each spawn includes the full spawn prompt template (see SKILL.md).
   - `max_iterations=30`, per-skill `model`, `workspace` set to project directory.
4. Each writer reads: skill file, `outline.md`, `references.json`, `gaps.md`, `chi_style_guide.md`, `chi_section_specs.md`, `writing_voice.md`, `writing_voice_hci.md`.
5. As each batch completes, mark its sections `complete` in `state.json.writing_parallel`.
6. When batch A and all domain batches complete, spawn **Batch F** (assembly):
   - `writer-integrator` writes abstract (informed by all sections) and merges all sections into `docs/drafts/paper_draft_v1.md`.
   - Integrator checks cross-section consistency: terminology, citation completeness, argument flow.
7. When batch F completes, mark `writing_integration` as `complete`.
8. Trigger user checkpoint for draft review.

**Output artifacts**
- `docs/drafts/introduction_v1.md`
- `docs/drafts/related_work_v1.md`
- `docs/drafts/discussion_v1.md`
- `docs/drafts/conclusion_v1.md`
- `docs/drafts/{section_name}_v1.md` (one per domain-specific section)
- `docs/drafts/abstract_v1.md`
- `docs/drafts/paper_draft_v1.md` (merged full paper)

**Exit criteria**
- All `writing_parallel` tasks are `complete`.
- `writing_integration.status = complete`.
- Merged `paper_draft_v1.md` exists with no unresolved placeholders.
- Each section meets its word target (±10%).
- `phase_status.writing = complete`.

**Error handling**
- Retry failed batches only; keep successful section files unchanged.
- If a domain writer fails, do not retry integrator batches that already succeeded.
- If assembly fails, retry assembly only (all individual section drafts are preserved).

---

## Phase 5: figures

**Entry criteria**
- `phase_status.writing = complete`.
- `current_phase = figures`.

**Entry validation (mid-pipeline)**
To enter this phase directly (skipping prior phases):
- Required files: `docs/drafts/paper_draft_v1.md` (or `paper_draft_v0.md` from import), `paper_project.yaml`, `state.json`
- state.json: `current_phase` set to `figures`, phases 1–4 marked `complete` or `skipped`, `writing_parallel` populated from draft section headers
- Auto-setup: Most common skip-to when user has a complete draft but needs figures. Populate `writing_parallel` by parsing section headers from the existing draft
- Validation: Draft file must exist and contain at least the sections listed in `paper_project.yaml.sections`

**Agent(s)**
- `figures`.

**Actions**
1. Spawn `figures` skill with `DOCUMENT_TYPE: paper`, `VENUE: {venue}`.
2. Read paper draft to identify figure opportunities: system architecture, study results, workflow diagrams, comparison tables.
3. Generate figure specifications in YAML format.
4. Render figures using matplotlib/seaborn/plotly.
5. Apply ACM accessibility compliance:
   - Color-blind safe palettes (no red-green only distinctions).
   - Minimum 7pt font size in all figure text.
   - Alt-text descriptions for every figure.
   - Vector format preferred (SVG/PDF) for camera-ready; also export 300 DPI PNG.
6. Draft figure captions following venue conventions (caption below figure, descriptive not interpretive).
7. Run VLM quality review loop on generated figures.

**Output artifacts**
- `figures/specs/F{N}.yaml` (one per figure)
- `figures/exports/F{N}.svg` and `figures/exports/F{N}.png`
- `figures/captions.md` (all captions with figure references)

**Exit criteria**
- Figure plan and captions are present and linked to paper sections.
- All figures pass accessibility checks.
- `phase_status.figures = complete`.

**Error handling**
- Log failure and retry figure generation without rerunning writing.
- If a specific figure fails rendering, skip it and note in the manifest for manual creation.

---

## Phase 6: review

**Entry criteria**
- `phase_status.writing = complete`.
- `phase_status.figures = complete`.
- `current_phase = review`.

**Entry validation (mid-pipeline)**
To enter this phase directly (skipping prior phases):
- Required files: `docs/drafts/paper_draft_v1.md` (or `paper_draft_v0.md` from import), `paper_project.yaml`, `state.json`
- state.json: `current_phase` set to `review`, phases 1–5 marked `complete` or `skipped`, `writing_parallel` populated from draft section headers
- Auto-setup: **This is the MOST COMMON mid-pipeline entry**: user provides existing draft for review. Parse draft section headers to populate `state.json.writing_parallel`. If figures phase is skipped, set `phase_status.figures: skipped`
- Validation: Draft file must exist; `writing_parallel` must have entries for all sections in `paper_project.yaml.sections`

**Agent(s)**
- Parallel: `reviewer-{domain}` for each domain in `paper_project.yaml.domain_tags`
- Fan-in: `reviewer-panel`

**Actions**
1. Spawn N domain reviewers in parallel (matching `paper_project.yaml.domain_tags`):
   - Each receives `DOCUMENT_TYPE: paper`, `VENUE: {venue}`, `CONTRIBUTION_TYPE: {contribution_type}`.
   - Each reviewer uses the venue-specific scoring scale (see `references/venue_review_criteria.md`).
2. Each reviewer runs:
   - Background retrieval step to pull relevant prior art for comparison.
   - Dual-bias protocol: one pass as skeptic, one as advocate.
   - Produces structured JSON with `venue_dimensions` (per venue criteria), `background_findings`, `review_confidence`, `critique_items`.
3. Track each review in `state.json.review_parallel`.
4. When all domain reviewers complete, spawn `reviewer-panel` to synthesize:
   - Panel reads all domain reviews, identifies conflicts, resolves with explicit reasoning.
   - Panel uses venue-appropriate scoring (e.g., CHI 1.0-5.0 scale, not NIH 1-9).
   - Panel produces `panelist_perspectives`, revision priority matrix, and `findings_memory_entry`.
5. Panel appends `findings_memory_entry` to `reviews/findings_memory.json`.
6. Decision logic:
   - If recommendation is "accept": proceed to export.
   - If recommendation is "revise" AND `review_round < max_review_rounds`: route to revision.
   - If `review_round >= max_review_rounds`: present to user with recommendation to accept current quality or manually revise.

**Output artifacts**
- `reviews/review_{domain}_r{N}.json` (one per domain reviewer)
- `reviews/panel_summary_r{N}.md`
- `reviews/panel_decision_r{N}.json` (fields: `recommendation`, `venue_score`, `panelist_perspectives`, `revision_priority_matrix`, `findings_memory_entry`)

**Exit criteria**
- Panel review includes venue-appropriate score and prioritized issues.
- Routing decision made (accept → export, revise → revision).
- `phase_status.review = complete` (if accepting) or transition to revision.

**Error handling**
- Retry only failed reviewer tasks; do not discard completed reviews.
- If panel synthesis fails, retry panel only with existing domain review files.

---

## Phase 7: revision

**Entry criteria**
- Review recommends revision.
- `review_round < max_review_rounds`.
- `current_phase = revision`.

**Entry validation (mid-pipeline)**
To enter this phase directly (skipping prior phases):
- Required files: `reviews/panel_decision_r{N}.json` OR user-provided reviewer comments file, `docs/drafts/paper_draft_v{N}.md`, `paper_project.yaml`, `state.json`
- state.json: `current_phase` set to `revision`, phases 1–6 marked `complete` or `skipped`, `review_round` set appropriately
- Auto-setup: For actual R&R, set `revision.mode: "actual"` and `revision.reviewer_comments_path` in `paper_project.yaml`. Create `reviews/findings_memory.json` if absent
- Validation: Either `panel_decision_r{N}.json` exists or `reviewer_comments_path` points to a valid file; draft must exist

**Agent(s)**
- `reviser`.

**Actions. Simulated Mode** (`paper_project.yaml.revision.mode = "simulated"` or unset):
1. Reviser reads `reviews/findings_memory.json` for cumulative findings across all prior rounds.
2. Generates a self-directed revision plan from panel priorities and domain critiques.
3. Patches draft sections according to the plan.
4. Produces `reviews/revision_diffs_r{N}.json` documenting what changed and why.
5. Appends a revision summary entry to `reviews/findings_memory.json`.
6. Updates `docs/drafts/paper_draft_v{N+1}.md` with revised content.
7. Increments `review_round` and routes back to Phase 6 (review).

**Actions. Actual R&R Mode** (`paper_project.yaml.revision.mode = "actual"`):
1. Orchestrator reads `paper_project.yaml.revision.reviewer_comments_path` to locate the real reviewer comments file.
2. Spawn `reviser` with `mode="actual"` and the reviewer comments path:
   - Task prompt: "You are the reviser in ACTUAL R&R mode. Read the reviser skill. Reviewer comments are at: {reviewer_comments_path}. Generate a point-by-point response letter and revised draft."
3. Reviser generates:
   - **Response letter** at `reviews/response_letter_r{N}.md`:
     - Summary of major changes (1 paragraph).
     - Per-reviewer responses: quote each comment → state action taken → point to specific location in revised paper.
     - Follow format in `references/response_letter_guide.md`.
   - **Revised draft** at `docs/drafts/paper_draft_v{N+1}.md` with inline change markers.
   - **Change summary** at `reviews/change_summary_r{N}.md` for latexdiff generation.
4. Trigger user checkpoint:
   - Present response letter for review.
   - User can request tone changes, add rebuttals, modify responses.
   - User approves or requests another iteration.
5. If user approves: proceed to export.
6. If user requests changes: iterate (re-spawn reviser with user feedback).
7. Multiple R&R rounds are supported (increment N each round). CSCW allows 2+ rounds; CHI typically has 1.

**Output artifacts. Simulated:**
- `docs/drafts/paper_draft_v{N+1}.md`
- `reviews/revision_log_r{N}.md`
- `reviews/revision_diffs_r{N}.json`
- `reviews/findings_memory.json` (updated)

**Output artifacts. Actual R&R:**
- `reviews/response_letter_r{N}.md`
- `docs/drafts/paper_draft_v{N+1}.md`
- `reviews/change_summary_r{N}.md`
- `reviews/revision_diffs_r{N}.json`

**Exit criteria. Simulated:**
- Revised draft exists and all high-priority issues are addressed.
- `revision_diffs_r{N}.json` records all changes.
- `phase_status.revision = complete`.

**Exit criteria. Actual R&R:**
- Response letter exists with per-reviewer point-by-point responses.
- Revised draft exists with all changes marked.
- User has approved the response letter and revision.
- `phase_status.revision = complete`.

**Error handling**
- Log failure, preserve previous draft, retry reviser only.
- In actual mode, never discard user-approved response letter content, only append/modify.

---

## Phase 8: export + evolution

**Entry criteria**
- Review passes (accept recommendation) OR user accepts current quality OR actual R&R revision approved.
- `current_phase = export`.

**Entry validation (mid-pipeline)**
To enter this phase directly (skipping prior phases):
- Required files: `docs/drafts/paper_draft_v{N}.md` at final revision, `paper_project.yaml`, `state.json`
- state.json: `current_phase` set to `export`, all prior phases marked `complete` or `skipped`
- Auto-setup: Rarely entered mid-pipeline. Ensure `figures/exports/` contains any referenced figures; create `export/` directory if absent
- Validation: Final draft must exist with no unresolved placeholders; if actual R&R mode, `reviews/response_letter_r{N}.md` must also exist

**Agent(s)**
- Orchestrator (assembly + anonymization check)
- `evolution` (post-export learning)

**Actions. Export:**
1. Run anonymization checklist (read `references/anonymization_checklist.md`):
   - Scan full paper text for author names, institutional affiliations, grant numbers.
   - Verify self-citations use third-person or [Anonymous Year].
   - Check PDF metadata fields are clean (no author names in document properties).
   - Verify supplementary materials contain no identifying information.
   - Verify figures contain no identifying logos, watermarks, or institutional branding.
   - If any check fails: report violations to user, do NOT proceed until fixed.
2. Assemble final submission package:
   - `export/paper_submission_v{N}/paper.md`, anonymized full paper.
   - `export/paper_submission_v{N}/figures/`, all figure files (SVG + PNG).
   - `export/paper_submission_v{N}/supplementary/`, supplementary materials (if applicable).
   - `export/paper_submission_v{N}/response_letter.md`, response letter (if actual R&R mode).
   - `export/export_manifest.md`, file listing, word count, figure count, venue, contribution type.
3. Validate word count against venue limits (see `references/venue_review_criteria.md`).
4. Post final checkpoint to user for sign-off.

**Actions. Evolution (after user approval):**
5. Spawn `evolution` agent with the completed project path.
6. Evolution agent reads all review JSONs, revision diffs, findings memory, and user feedback files.
7. Updates `_system/reviewer_patterns.json` with new or incremented patterns.
8. Appends entries to `_system/evolution_log.json`.
9. May propose `_system/chi_style_guide.md` changes (user approval required).
10. Set `phase_status.evolution = complete`.

**Output artifacts**
- `export/paper_submission_v{N}/` (complete submission package)
- `export/export_manifest.md`
- Updated `_system/reviewer_patterns.json`
- Updated `_system/evolution_log.json`

**Exit criteria**
- Anonymization checklist passes with no violations.
- Export package is complete and manifest is accurate.
- User has approved the final package.
- Evolution agent has completed (or failed non-fatally).
- `phase_status.export = complete` and pipeline marked complete.

**Error handling**
- If anonymization check finds violations: list all violations, block export, return to user for fixes.
- If export assembly fails: record error, keep intermediate artifacts, retry assembly.
- Evolution failure is non-fatal, the export is already done. Log and continue.
