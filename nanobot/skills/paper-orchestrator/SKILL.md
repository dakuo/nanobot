---
name: paper-orchestrator
description: "Central orchestrator for academic paper writing and revision. Manages multi-phase pipeline from literature review to export with parallel domain-specialized writers and reviewers. Supports CHI, CSCW, UIST, UbiComp/IMWUT, DIS venues. Triggers: 'write paper', 'new paper', 'resume paper', 'paper status', 'run paper pipeline', 'revise paper', 'respond to reviews', 'write section', 'edit section', 'write introduction', 'write related work', 'write method', 'write discussion', 'edit draft', 'improve section', 'rewrite section', 'review section', 'write for {project}', 'edit {section} for {project}'."
---

# Overview
The paper orchestrator drives a state-machine pipeline that reads `state.json`, determines the active phase, spawns the required specialized subagents, and advances only when each phase exit condition is satisfied. Unlike the R01 orchestrator, this pipeline targets peer-reviewed academic papers with venue-specific formatting, double-blind anonymization, and support for actual revise-and-resubmit (R&R) workflows.

# Quick Start
1. Copy `~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/paper_project.yaml` and `paper_state.json` into `~/Dropbox/AgentWorkspace/PaperAutoGen/chi-{paper-name}/`.
2. Edit `paper_project.yaml` for paper metadata, venue, contribution type, sections, and domain tags.
3. Tell the agent: `Write paper for chi-{paper-name}`.

# Mandatory Delegation Rule (NEVER SKIP)
**You MUST NEVER write, edit, or revise academic paper content directly as the main agent.** Every writing, editing, or revision task MUST be delegated to a spawned subagent with the appropriate writer or reviewer skill loaded.

This applies to ALL scenarios:
- Full pipeline runs (Phases 1-8)
- Ad-hoc single-section writing (user asks "write the related work")
- Draft edits (user asks "improve introduction_v4.md")
- Section rewrites (user asks "rewrite the discussion")
- Review tasks (user asks "review this draft")

## Writer Routing Table
Use the following table to determine which subagent to spawn. Read `paper_project.yaml.domain_tags` to determine the domain count.

### Single-Domain Papers (one domain_tag, e.g., `[hci]`)
| Section | Spawn Agent | Skill to Read |
|---|---|---|
| introduction | writer-{domain} | `nanobot/skills/writer-{domain}/SKILL.md` |
| related_work | writer-{domain} | `nanobot/skills/writer-{domain}/SKILL.md` |
| method / system / study / findings / evaluation | writer-{domain} | `nanobot/skills/writer-{domain}/SKILL.md` |
| discussion | writer-{domain} | `nanobot/skills/writer-{domain}/SKILL.md` |
| conclusion | writer-{domain} | `nanobot/skills/writer-{domain}/SKILL.md` |
| abstract + final assembly | writer-integrator | `nanobot/skills/writer-integrator/SKILL.md` |

For single-domain papers, the domain writer handles ALL content sections because it has the domain-specific voice, citation conventions, and framing expertise. The integrator only handles final assembly and abstract.

### Multi-Domain Papers (2+ domain_tags, e.g., `[hci, ai]`)
| Section | Spawn Agent | Skill to Read |
|---|---|---|
| introduction | writer-integrator | `nanobot/skills/writer-integrator/SKILL.md` |
| related_work | **domain writers → writer-integrator** | See Related Work Multi-Domain Workflow below |
| domain-specific sections | writer-{section.domain_tag} | `nanobot/skills/writer-{domain}/SKILL.md` |
| discussion | writer-integrator | `nanobot/skills/writer-integrator/SKILL.md` |
| conclusion | writer-integrator | `nanobot/skills/writer-integrator/SKILL.md` |
| abstract + final assembly | writer-integrator | `nanobot/skills/writer-integrator/SKILL.md` |

For multi-domain papers, the integrator handles cross-cutting sections that synthesize across domains. The integrator MUST read all domain voice files (`writing_voice_{domain}.md`) before writing any cross-cutting section.

#### Related Work Multi-Domain Workflow
For multi-domain papers, Related Work uses a **parallel-first → consolidation** workflow because RW subsections typically map to distinct domains:

1. **Identify RW subsections** from `docs/outline.md`. Map each subsection to a domain_tag based on content (e.g., "Usability Testing Challenges" → hci, "LLM Reasoning Architectures" → ai).
2. **Spawn domain writers in parallel**: For each domain-mapped subsection, spawn the corresponding `writer-{domain}` subagent to write that subsection. Each domain writer brings specialized voice, citation conventions, and framing expertise.
3. **Spawn writer-integrator for consolidation**: After all domain writers complete, spawn `writer-integrator` with the domain outputs. The integrator:
   - Writes the RW preamble sentence previewing subsection structure
   - Adds transitions between subsections
   - Writes positioning sentences at the end of each subsection
   - Resolves terminology conflicts across domain drafts
   - Ensures the RW reads as one coherent narrative, not stitched fragments
4. **Output**: A single `related_work_v{N}.md` file.

If a subsection spans multiple domains (e.g., "LLM Simulation of Human Behavior" spans both AI and HCI), assign it to the **primary domain** and instruct that writer to consult the secondary domain's voice file.

### Reviewer Routing
| Task | Spawn Agent | Skill to Read |
|---|---|---|
| HCI review | reviewer-hci | `nanobot/skills/reviewer-hci/SKILL.md` |
| AI review | reviewer-ai | `nanobot/skills/reviewer-ai/SKILL.md` |
| Healthcare review | reviewer-healthcare | `nanobot/skills/reviewer-healthcare/SKILL.md` |
| Panel synthesis | reviewer-panel | `nanobot/skills/reviewer-panel/SKILL.md` |

# Ad-Hoc Writing Requests
When the user asks to write, edit, or revise a specific section (outside the formal pipeline):

1. Identify which project the request is for (from user context or ask).
2. Read `paper_project.yaml` from the project directory to determine `domain_tags`.
3. Use the Writer Routing Table above to select the correct subagent.
4. Spawn with the following template:

```
spawn(
  task="You are a {role} subagent. Read the {skill_name} skill at {skill_path} and follow its instructions.\n\nPROJECT: {project_path}\nDOCUMENT_TYPE: paper\nVENUE: {venue}\nCONTRIBUTION_TYPE: {contribution_type}\nTASK: {user_request}\nSECTION: {section_name}\nINPUT FILE: {existing_draft_path_if_any}\nOUTPUT FILE: {output_path}\n\nMANDATORY READS (do ALL of these BEFORE writing any prose):\n- Project config: {project_path}/paper_project.yaml\n- Writing voice: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/writing_voice.md (READ the 'Forbidden Sentence Structures' section — these are ABSOLUTE BANS)\n- HCI writing voice: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/writing_voice_hci.md\n- Style guide: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/chi_style_guide.md\n- Literature: {project_path}/literature/references.json (if exists)\n- User input: {project_path}/docs/user_input.md (if exists)\n\nPOST-GENERATION SCAN (do AFTER writing, BEFORE delivering):\n- Scan output for em-dashes (—) — if found, rewrite those sentences\n- Scan for 'is not to' / 'is not X but' / 'rather than' (defensive negation) — if found, rewrite to state positive purpose directly\n- Scan for trailing participial phrases (', verb-ing') — if found, split into separate sentences\n- Scan for comma+gerund (', having') — if found, restructure\n- Scan for absolute words: 'must' (not in formal specs), 'absolutely', 'undeniably', 'certainly' — if found, replace with softer alternatives ('needs to', 'requires', 'should')\n- Scan for categorical claims: 'No existing', 'No current', 'All prior', 'No prior' — if found, soften ('Most existing', 'Few prior')\n- Check inter-paragraph cohesion: first sentence of each paragraph must explicitly connect to the prior paragraph's closing claim\n- Check for standalone bullet/numbered lists in Introduction body (except final contribution list) — if found, convert to inline prose\n\nINSTRUCTIONS:\n1. Read the skill file first.\n2. Read ALL mandatory files listed above — especially writing_voice.md Forbidden Sentence Structures.\n3. Read the existing draft (if any) to understand current state.\n4. {specific_task_instructions}\n5. Run the post-generation scan on your output.\n6. Write output to the specified file.",
  label="{section_name}-{action}",
  max_iterations=30,
  workspace="{project_path}"
)
```

If the user asks to edit an existing file, the spawned subagent reads the file, applies changes, and writes back. If the user asks to write a new section, the subagent creates the file from scratch following the skill guidelines.

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

# Mid-Pipeline Entry (Draft Import)
When a user provides an existing paper draft instead of starting from scratch, the orchestrator must detect this, create the workspace, analyze the draft to determine the correct pipeline phase, and initialize `state.json` with prior phases marked as `skipped`. This section covers all mid-pipeline entry scenarios.

## Trigger Detection
Detect mid-pipeline entry when the user's message matches any of these patterns:
- **"revise this paper"**: user provides a full or partial draft (PDF or text) and wants revision feedback.
- **"review my paper"**: user provides a draft and wants simulated peer review without prior pipeline phases.
- **"improve this draft"**: user provides text and wants iterative improvement (enters review → revision loop).
- **"resume paper for {project-name}"**: user wants to continue an existing pipeline that was interrupted.
- **"continue paper pipeline"**: same as resume; orchestrator reads `state.json` from the most recent project or the project specified.

If the user's message contains one of these trigger phrases AND either attaches a file (PDF/text) or references an existing project directory, enter mid-pipeline mode instead of Phase 1: Init.

## Draft Analysis
When the user provides a draft (PDF attachment, pasted text, or file path), extract the following before creating the workspace:

1. **Venue**: Scan for venue identifiers in the text, including ACM template markers (`\acmConference`, `sigchi-a` class), explicit venue mentions ("submitted to CHI 2026"), or formatting cues (ACM CCS concepts, single-column vs. two-column). If no venue is detectable, ask the user. Do not guess.
2. **Contribution type**: Infer from section structure and content. Empirical papers have "Findings"/"Results" sections with statistical language; artifact papers have "System Design"/"Implementation"; methodological papers have "Method"/"Framework" as primary sections; surveys have "Taxonomy"/"Classification". Map to one of: empirical, artifact, methodological, theoretical, survey, opinion, benchmark.
3. **Section structure**: Parse all top-level headings (H1/H2) and their approximate word counts. Map each heading to the canonical section names used in the pipeline: `abstract`, `introduction`, `related_work`, `method`, `system`, `study`, `findings`, `discussion`, `conclusion`, `acknowledgments`. Flag any non-standard sections for user confirmation.
4. **Research questions / contributions**: Extract explicitly stated RQs (lines starting with "RQ1:", "Research Question", or bold/italic question formats) and contribution lists (typically in the introduction, often as numbered items after "contributions of this paper" or similar phrasing). Store these in `docs/extracted_rqs.md`.
5. **Existing references**: If the draft contains a bibliography or reference list, extract it to `literature/references_imported.json` in the same schema as `literature/references.json`. Set `source: "imported"` on each entry to distinguish from pipeline-generated references.

For PDF input: use available PDF text extraction tools. If the PDF is image-based (scanned), inform the user that OCR extraction may be lossy and ask them to provide a text version instead.

## Workspace Auto-Setup
After draft analysis, create the project workspace and configuration files:

1. **Create project directory**: `~/Dropbox/AgentWorkspace/PaperAutoGen/{venue}-{paper-name}/` where `{venue}` is lowercase (e.g., `chi`, `cscw`) and `{paper-name}` is derived from the paper title (lowercase, hyphens, no special characters). If the user did not provide a project name, generate one from the first 4-5 significant words of the title.
2. **Generate `paper_project.yaml`**: Populate from draft analysis results:
   - `document_type: "paper"`
   - `venue`: from draft analysis step 1
   - `contribution_type`: from draft analysis step 2
   - `sections[]`: from draft analysis step 3, with each section's `domain_tag` inferred from content (e.g., sections discussing user studies → `hci`, sections discussing model architecture → `ai`)
   - `domain_tags[]`: union of all section domain tags
   - `model_config`: use defaults from `_templates/paper_project.yaml`
   - `revision.mode`: set to `"actual"` if the user also provided reviewer comments, otherwise `"simulated"`
3. **Save the draft**: Copy the provided text to `docs/drafts/paper_draft_v0.md` (the "v0" indicates it was imported, not pipeline-generated). If the user provided a PDF, also save the original to `docs/drafts/original_import.pdf`.
4. **Initialize `state.json`**: Set `current_phase` to the determined entry phase (see phase determination below). For every phase that precedes the entry phase, set `phase_status` to `"skipped"` with a `skip_reason` field:
   - `init`: `"skipped"` with `skip_reason: "workspace auto-created from imported draft"`
   - `literature`: `"skipped"` with `skip_reason: "references imported from draft"` (only if the draft contained a bibliography; otherwise set to `"pending"` so the pipeline can run literature search before review)
   - `outline`: `"skipped"` with `skip_reason: "structure extracted from imported draft"`
   - `writing`: `"skipped"` with `skip_reason: "draft imported directly"`
   - `figures`: `"skipped"` with `skip_reason: "figures present in imported draft"` (only if figures were detected; otherwise `"pending"`)
5. **Create `reviews/findings_memory.json`** as an empty array `[]`.
6. **Populate `state.json.writing_parallel`**: Create entries for each detected section with `status: "skipped"`, `word_count` set to the detected word count, and `draft_version: 0`.
7. **Log the import event**: Append to `events.jsonl`: `{event: "mid_pipeline_import", source: "pdf"|"text"|"file_path", sections_detected: [...], entry_phase: "...", timestamp: "..."}`.

## Phase Determination
Determine which phase to enter based on what the user provided and requested:

- **User says "revise this paper" + provides full draft** → Enter Phase 6 (review). All prior phases are `skipped`. The review phase runs the full parallel reviewer dispatch on the imported draft. After review, the pipeline proceeds normally through revision and export.
- **User says "review intro and related work" + provides partial text** → Enter Phase 6 (review) with partial scope (see Partial Scope below). Only the specified sections are reviewed.
- **User provides draft + reviewer comments** → Enter Phase 7 (revision) in actual R&R mode. Set `revision.mode: "actual"` in `paper_project.yaml`. Save reviewer comments to the path specified by `revision.reviewer_comments_path`. Phases 1-6 are all `skipped`. The reviser generates a response letter and revised draft.
- **User says "resume paper for {project-name}"** → Do NOT create a new workspace. Read the existing `state.json` from `~/Dropbox/AgentWorkspace/PaperAutoGen/{project-name}/state.json`. Resume from `current_phase`. If `current_phase` has `phase_status: "running"`, check for incomplete subtasks and resume them. If `phase_status: "failed"`, read the failure reason from events and retry. If `phase_status: "complete"`, advance to the next phase.
- **User provides partial draft (e.g., only introduction + method)** → Enter Phase 4 (writing) for the missing sections only. Mark provided sections as `complete` in `writing_parallel` with their imported word counts. Mark missing sections as `pending`. The pipeline writes only the missing sections, then proceeds to figures → review → revision → export.

Validate the entry phase against the phase contracts in `references/pipeline.md`: confirm that all required inputs for the target phase exist (either imported from the draft or generated during workspace setup). If a required input is missing (e.g., entering review but no `literature/references.json` exists and the draft had no bibliography), either run the missing prerequisite phase first or warn the user that review quality will be limited without literature context.

## Partial Scope
When the user requests review or revision of specific sections only (not the full paper):

1. **Parse the scope request**: Identify which sections the user named. Match against the canonical section names from draft analysis. Accept both formal names ("related work", "discussion") and informal references ("intro", "methods section", "RW").
2. **Set `state.json.review_scope`**: Add a `review_scope` field as an array of section names to review, e.g., `["introduction", "related_work"]`. If this field is absent or empty, reviewers review the full paper (default behavior).
3. **Reviewer dispatch with scope**: When spawning reviewers in Phase 6 with a non-empty `review_scope`, add `REVIEW_SCOPE: {section_list}` to the spawn prompt. Reviewers must focus their critique on the specified sections only, though they may note cross-section issues (e.g., introduction promises something the method doesn't deliver) as secondary observations.
4. **Revision with scope**: If review was scoped, the subsequent revision phase also inherits the scope. The reviser only patches the sections that were reviewed. Other sections remain untouched in the draft.
5. **Scope expansion**: If a scoped review reveals issues that require changes in out-of-scope sections (e.g., reviewer says "the introduction overpromises relative to the findings"), flag this to the user at the review checkpoint. The user can choose to expand scope or defer those changes.
6. **State tracking**: Log the scope in `events.jsonl`: `{event: "partial_scope_set", sections: [...], timestamp: "..."}`. When the scoped review-revision cycle completes, set only the reviewed sections' statuses to `complete` in `writing_parallel`. Unreviewed sections retain their prior status.

# Phase 2: Literature
Spawn N literature agents in parallel (one per `domain_tag` in `paper_project.yaml.domain_tags`):
1. Read `paper_project.yaml` → get domain tags (e.g., `[hci, ai]` for a two-domain paper).
2. Populate `state.json.literature_parallel` with one entry per domain.
3. Spawn literature subagents with **30-second stagger** between launches:
   - Each reads `literature` skill and is assigned one domain.
   - Task prompt must include `DOCUMENT_TYPE: paper` so the agent calibrates search scope for paper-length references (not grant-length).
   - Each agent runs multi-round search, snowball sampling via Semantic Scholar citation graph, and produces claim-evidence mappings.
4. **State tracking**: same pattern as all spawns. Update `state.json` before/after each spawn, append events.
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

**Routing depends on domain count.** Read `paper_project.yaml.domain_tags` first.

### Single-Domain Papers (1 domain_tag)
| Batch | Agent | Sections | Parallel? |
|-------|-------|----------|-----------|
| A | writer-{domain} | ALL content sections: introduction, related_work, method/system, discussion, conclusion | Yes |
| F | writer-integrator | abstract + merge all into paper_draft_v1.md | After A completes |

### Multi-Domain Papers (2+ domain_tags)
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
2. Read outline.md and locate YOUR assigned section(s). Use the heading structure and word targets there.
3. Read references.json and gaps.md to incorporate citations and address gaps.
4. Read docs/user_input.md (if present) for the user's preferred framing, positioning language, and system description.
5. Write each section to its output file. Use markdown with proper heading hierarchy.
6. Each section MUST meet its word target (±10%).
7. Cite references using [AuthorYear] format matching references.json entries.
8. Follow venue-specific formatting requirements from chi_section_specs.md.
9. CROSS-CHECK: If your section describes system components/modules, verify the count and names match outline.md and user_input.md exactly. Do not omit components.
```

Do NOT ask the subagent to update state.json. The orchestrator tracks completion externally.

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

## Minimum Review Rounds Policy
**The pipeline MUST complete at least 2 full review→revision cycles before presenting results to the user at a checkpoint.** This applies to ALL writing and revision tasks, whether full-paper or scoped to specific sections. The rationale: Round 1 catches obvious issues; Round 2 stress-tests the fixes and catches second-order problems introduced by the revision. Only after Round 2 (or later) should the orchestrator pause for user feedback.

- `min_review_rounds`: 2 (hardcoded, not configurable)
- `max_review_rounds`: read from `project.yaml` (default 3)
- After Round 1 revision completes → automatically route back to Phase 6 (review) without user checkpoint.
- After Round 2 revision completes → present to user at checkpoint. If `review_round < max_review_rounds` and user requests further revision, continue.
- Do NOT insert a `checkpoint_wait` event before `review_round >= min_review_rounds`.

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
6. User can iterate (multiple R&R rounds, especially for CSCW which allows 2+ rounds).
7. Each round increments N and produces new response letter + revised draft.

# Phase 8: Export + Evolution
1. Run anonymization final check. Read `references/anonymization_checklist.md` and verify compliance:
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
- `references/pipeline.md`: Full phase contracts and transitions
- `references/chi_paper_structures.md`: Section templates per contribution type
- `references/venue_review_criteria.md`: Venue-specific scoring and review dimensions
- `references/anonymization_checklist.md`: Double-blind compliance checklist
- `references/response_letter_guide.md`: R&R response letter format and best practices
