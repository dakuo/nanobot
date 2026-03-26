---
name: paper-orchestrator
description: "Central orchestrator for academic paper writing and revision. Manages multi-phase pipeline from literature review to export with parallel domain-specialized writers and reviewers. Supports CHI, CSCW, UIST, UbiComp/IMWUT, DIS venues. Triggers: 'write paper', 'new paper', 'resume paper', 'paper status', 'run paper pipeline', 'revise paper', 'respond to reviews'."
---

# Overview
The paper orchestrator drives a state-machine pipeline that reads `state.json`, determines the active phase, spawns the required specialized subagents, and advances only when each phase exit condition is satisfied. Unlike the R01 orchestrator, this pipeline targets peer-reviewed academic papers with venue-specific formatting, double-blind anonymization, and support for actual revise-and-resubmit (R&R) workflows.

# Quick Start
1. Copy `~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/paper_project.yaml` and `paper_state.json` into `~/Dropbox/AgentWorkspace/PaperAutoGen/chi-{paper-name}/`.
2. Edit `paper_project.yaml` for paper metadata, venue, contribution type, sections, and domain tags.
3. Tell the agent: `Write paper for chi-{paper-name}`.

# Pipeline Phases
| Phase | Agent assignment |
|---|---|
| init | orchestrator |
| literature | `literature` × N (parallel: one per domain_tag in project.yaml) → merge |
| outline | `writer-integrator` |
| writing | `writer-integrator` + domain writers (parallel) |
| figures | `figures` |
| review | `reviewer-{domain}` × N (parallel) + `reviewer-panel` |
| revision | `reviser` |
| export | orchestrator + `evolution` |

See `references/pipeline.md` for full phase contracts and transitions.

# Phase 1: Init
During the init phase, after validating the project directory:
1. Validate project path exists under `~/Dropbox/AgentWorkspace/PaperAutoGen/chi-{paper-name}/`.
2. Confirm `document_type` in `paper_project.yaml` is `"paper"` (not `"r01"`).
3. Validate `venue` is one of: CHI, CSCW, UIST, UbiComp, IMWUT, DIS.
4. Validate `contribution_type` is one of: empirical, artifact, methodological, theoretical, survey, opinion, benchmark.
5. Initialize `state.json` with paper-specific fields.
6. Create `reviews/findings_memory.json` as an empty array `[]` if the file does not already exist.
7. Populate `state.json.writing_parallel` with dynamic section entries: for each section in `paper_project.yaml.sections[]`, add `{section_name}: {agent: writer-{section.domain_tag}, status: pending, attempt: 0, word_count: 0, draft_version: 0}`.
8. If the user provided an abstract or paper description, save it to `docs/user_input.md`.

# Phase 2: Literature
Spawn N literature agents in parallel (one per `domain_tag` in `paper_project.yaml.domain_tags`):
1. Read `paper_project.yaml` → get domain tags (e.g., `[hci, ai]` for a two-domain paper).
2. Populate `state.json.literature_parallel` with one entry per domain.
3. Spawn literature subagents with **30-second stagger** between launches:
   - Each reads `literature` skill and is assigned one domain.
   - Task prompt must include `DOCUMENT_TYPE: paper` so the agent calibrates search scope for paper-length references (not grant-length).
   - Each agent runs multi-round search, snowball sampling via Semantic Scholar citation graph, and produces claim-evidence mappings.
4. **State tracking**: same pattern as all spawns — update `state.json` before/after each spawn, append events.
5. When all domain searches complete:
   - Merge `literature/references_{domain}.json` files into `literature/references.json`.
   - Deduplicate by DOI/URL, keeping highest-priority annotations.
   - Build `thematic_clusters` in the merged references (group references by theme for related work section).
   - Merge gap files into `literature/gaps.md`.
   - Validate: every `must-cite` reference has a non-empty `supports_claim`.

No investigator verification gate is required for papers (unlike R01). Author identity is not used in double-blind literature searches.

# Phase 3: Outline
Spawn `writer-integrator` with paper mode:
1. Pass `DOCUMENT_TYPE: paper`, `VENUE: {venue}`, `CONTRIBUTION_TYPE: {contribution_type}`.
2. The integrator reads `references/chi_paper_structures.md` (bundled with this skill) to select the canonical section structure matching the contribution type.
3. The integrator reads `~/Dropbox/AgentWorkspace/PaperAutoGen/_system/chi_section_specs.md` for venue-specific formatting.
4. Produces `docs/outline.md` with section headings, word budgets per section, and key arguments per section.
5. Trigger user checkpoint for structural review.

# Phase 4: Writing (Parallel Dispatch)

## Batching Strategy
| Batch | Agent | Sections | Parallel? |
|-------|-------|----------|-----------|
| A | writer-integrator | introduction, related_work, discussion, conclusion | Yes (with B..N) |
| B..N | writer-{section.domain_tag} | method/system sections (from project.yaml.sections) | Yes |
| F | writer-integrator | abstract + merge all into paper_draft_v1.md | After A..N complete |

## Dispatch Steps
1. Read `paper_project.yaml` → get section-to-domain mapping and model overrides.
2. Dynamically populate `state.json.writing_parallel` with one entry per section.
3. Mark sections as `running` for batch A and all domain batches.
4. Spawn simultaneously for batch A + N domain batches, each with:
   - `max_iterations=30`
   - `model` from `paper_project.yaml.model_config.overrides`
   - `workspace="~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/"`
5. As each batch completes, mark its sections `complete`.
6. When batch A and all domain batches complete, spawn batch F (assembly + abstract).
7. When batch F completes, mark remaining sections + `writing_integration` as `complete`.

## Spawn Prompt Template
Every paper subagent spawn must include ALL of the following:

```
You are a {role} subagent. Read the {skill_name} skill at {skill_path} and follow its instructions.

PROJECT: {project_path}
DOCUMENT_TYPE: paper
VENUE: {paper_project.yaml.venue}
CONTRIBUTION_TYPE: {paper_project.yaml.contribution_type}
SECTIONS TO WRITE: {section_list_with_word_targets}
OUTPUT FILES: {output_file_paths}

REQUIRED INPUTS (read these before writing):
- Project config: {project_path}/paper_project.yaml
- Paper outline: {project_path}/docs/outline.md (find your section specs here)
- Literature: {project_path}/literature/references.json and {project_path}/literature/gaps.md
- System style guide: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/chi_style_guide.md
- Section specs: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/chi_section_specs.md
- Writing voice: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/writing_voice.md
- HCI writing voice: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/writing_voice_hci.md

INSTRUCTIONS:
1. Read the skill file first for your role and quality standards.
2. Read outline.md and locate YOUR assigned section(s) — use the heading structure and word targets there.
3. Read references.json and gaps.md to incorporate citations and address gaps.
4. Write each section to its output file. Use markdown with proper heading hierarchy.
5. Each section MUST meet its word target (±10%).
6. Cite references using [AuthorYear] format matching references.json entries.
7. Follow venue-specific formatting requirements from chi_section_specs.md.
```

Do NOT ask the subagent to update state.json — the orchestrator tracks completion externally.

# Phase 5: Figures
Spawn `figures` skill:
1. Pass `DOCUMENT_TYPE: paper` and `VENUE: {venue}`.
2. Generate figure plan from paper draft.
3. All figures must comply with ACM accessibility guidelines:
   - Color-blind safe palettes (avoid red-green only distinctions).
   - Minimum font size 7pt in figures.
   - Alt-text descriptions for each figure.
   - Vector formats preferred (SVG/PDF) for camera-ready.
4. Draft captions following venue conventions.

# Phase 6: Review (Parallel Dispatch)
Spawn N domain reviewers matching `paper_project.yaml.domain_tags`:
1. For each domain tag, spawn `reviewer-{domain}` (e.g., `reviewer-hci`, `reviewer-ai`).
2. Each reviewer receives `DOCUMENT_TYPE: paper`, `VENUE: {venue}`, `CONTRIBUTION_TYPE: {contribution_type}`.
3. Each reviewer uses the venue-appropriate scoring scale (NOT the NIH 1-9 scale):
   - CHI/CSCW/DIS: Reject / Revise / Accept with scores 1.0-5.0
   - UIST: Strong Reject / Reject / Borderline / Accept / Strong Accept
   - UbiComp/IMWUT: Reject / Major Revision / Minor Revision / Accept
4. Each reviewer produces structured JSON with: `venue_dimensions` (scored per venue criteria), `background_findings`, `review_confidence` (0-1), `critique_items`.
5. When all domain reviewers complete, spawn `reviewer-panel` to synthesize.
6. Panel produces overall recommendation, revision priority matrix, and `findings_memory_entry`.
7. Panel appends `findings_memory_entry` to `reviews/findings_memory.json`.
8. If recommendation is not "accept" and `review_round < max_review_rounds`, route to revision.

# Phase 7: Revision
Two modes based on `paper_project.yaml.revision.mode`:

## Simulated Mode (default)
Same as standard review-revision loop:
1. Reviser reads `reviews/findings_memory.json` for cumulative findings.
2. Generates revision plan from panel priorities and domain critiques.
3. Patches draft sections, produces `reviews/revision_diffs_r{N}.json`.
4. Increments `review_round`, routes back to Phase 6.

## Actual R&R Mode
When the user has received real reviewer comments from a venue:
1. User sets `paper_project.yaml.revision.mode: "actual"`.
2. User provides reviewer comments file at `paper_project.yaml.revision.reviewer_comments_path`.
3. Orchestrator spawns `reviser` with `mode="actual"` and the reviewer comments path.
4. Reviser generates:
   - Point-by-point response letter at `reviews/response_letter_r{N}.md` (see `references/response_letter_guide.md`).
   - Revised paper with tracked changes at `docs/drafts/paper_draft_v{N+1}.md`.
   - Change summary for latexdiff at `reviews/change_summary_r{N}.md`.
5. User reviews response letter + revision at checkpoint.
6. User can iterate (multiple R&R rounds — especially for CSCW which allows 2+ rounds).
7. Each round increments N and produces new response letter + revised draft.

# Phase 8: Export + Evolution
1. Run anonymization final check — read `references/anonymization_checklist.md` and verify compliance:
   - Author names removed from all document text.
   - Self-citations use third-person or [Anonymous Year].
   - No institutional affiliations in acknowledgments.
   - PDF metadata is clean.
2. Package final paper:
   - `export/paper_submission_v{N}/paper.md` (anonymized)
   - `export/paper_submission_v{N}/figures/` (all figure files)
   - `export/paper_submission_v{N}/supplementary/` (if applicable)
   - `export/paper_submission_v{N}/response_letter.md` (if R&R mode)
   - `export/export_manifest.md`
3. Post final checkpoint to user for review.
4. After user approval, spawn `evolution` agent to extract cross-project learning:
   - Reads all review JSONs, revision diffs, findings memory.
   - Updates `_system/reviewer_patterns.json` with paper-specific patterns.
   - Appends entries to `_system/evolution_log.json`.
   - May propose `_system/chi_style_guide.md` changes (user approval required).

# User Checkpoints
- After outline: user reviews structure and section allocation.
- After writing: user reviews drafts (can provide inline edits, style notes, content notes).
- After review: user decides accept current / revise further.
- For actual R&R: user pastes real reviewer comments → system generates response letter + revision.
- After export: user reviews final anonymized package.

## Outline Feedback Checkpoint
After `docs/outline.md` is produced:
1. Present the outline to the user.
2. Ask: "Any structural changes? Section emphasis adjustments? Framing you'd change?"
3. Classify feedback as structural (→ integrator revision) or voice/framing (→ evolution for style update).
4. Record in `feedback/outline_feedback_{project}.json`.
5. Only proceed to writing after user confirms.

## Draft Feedback Checkpoint
After domain writers produce drafts:
1. Present each section draft to the user.
2. Accept: inline edits, style notes, content notes.
3. Route style feedback → `evolution` for voice file update.
4. Route content feedback → accumulate for revision phase.
5. Record in `feedback/draft_feedback_{project}.json`.

## Actual R&R Checkpoint
When user triggers actual R&R:
1. User sets `revision.mode: "actual"` in `paper_project.yaml`.
2. User provides reviewer comments file path.
3. Orchestrator spawns reviser with actual mode.
4. Present response letter + revision to user.
5. User can request changes to response letter tone, add rebuttals, or accept.
6. Iterate until user approves for resubmission.

# State Management
- Always read `state.json` before dispatching or transitioning phases.
- Write phase/task updates atomically in `state.json`.
- Append lifecycle events to `events.jsonl` (`spawned`, `completed`, `failed`, `checkpoint_wait`, `checkpoint_resumed`).
- Append per-agent cost entries to `cost.jsonl` after each subagent completion. Each entry: `timestamp`, `phase`, `agent`, `model`, `prompt_tokens`, `completion_tokens`, `cost_usd`, `task_description`.
- Treat `events.jsonl` and `cost.jsonl` as append-only ledgers.

# Workspace Constraint
- All file operations are restricted to `~/Dropbox/AgentWorkspace/` and `~/.nanobot/workspace/`.
- Never access files outside these two roots.

# References
- `references/pipeline.md` — Full phase contracts and transitions
- `references/chi_paper_structures.md` — Section templates per contribution type
- `references/venue_review_criteria.md` — Venue-specific scoring and review dimensions
- `references/anonymization_checklist.md` — Double-blind compliance checklist
- `references/response_letter_guide.md` — R&R response letter format and best practices
