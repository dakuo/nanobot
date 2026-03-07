---
name: r01-orchestrator
description: "Central orchestrator for NIH R01 proposal auto-generation. Manages multi-phase pipeline from ideation to export with parallel domain-specialized writers and reviewers. Triggers: 'start R01', 'new proposal', 'resume proposal', 'proposal status', 'run pipeline', 'check project'."
---

# Overview
The orchestrator drives a state-machine pipeline that reads `state.json`, determines the active phase, spawns the required specialized subagents, and advances only when each phase exit condition is satisfied.

# Quick Start
1. Copy `~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/` into `~/Dropbox/AgentWorkspace/PaperAutoGen/{project-name}/`.
2. Edit `project.yaml` for project metadata, aims, and domain mapping.
3. Tell the agent: `Start R01 pipeline for {project-name}`.

# Pipeline Phases
| Phase | Agent assignment |
|---|---|
| init | orchestrator |
| metadata | orchestrator (interactive) → `r01-foa-finder` (if NIH context missing) |
| ideation | `r01-ideation` → `r01-novelty-checker` (sub-step) |
| investigator verification | orchestrator (blocking gate — verify all PIs findable before literature) |
| literature | `r01-literature` × 3 (parallel: hci, healthcare, ai) → merge |
| outline | `r01-writer-integrator` |
| writing | `r01-writer-integrator` + domain writers |
| figures | `r01-figures` (with optional Figma MCP sync) |
| budget | `r01-budget` |
| pre-review gate | `r01-writer-integrator` (quick self-review, optional) |
| review | `r01-reviewer-hci`, `r01-reviewer-healthcare`, `r01-reviewer-ai`, `r01-reviewer-panel` |
| revision | `r01-reviser` |
| export | orchestrator |
| evolution | `r01-evolution` |

See `references/pipeline.md` for full phase contracts and transitions.

# Findings Memory Initialization
During the init phase, after validating the project directory:
1. Create `ideas/findings_memory.json` as an empty array `[]` if the file does not already exist.
2. Populate `state.json.writing_parallel` with dynamic aim entries: for each aim in `project.yaml.aims[]`, add `approach_aim{i}: {agent: r01-writer-{aim.domain_tag}, status: pending, attempt: 0, word_count: 0, draft_version: 0}`.
This file accumulates cross-round review findings and is read by the reviser at the start of each revision cycle.

# Metadata Collection (Phase 1.5)
After init, the orchestrator collects project meta-information through interactive dialog. This runs before ideation so downstream phases can leverage PI and institute context from the start.

The orchestrator checks `project.yaml` for missing fields and prompts the user in groups:
1. **Investigators**: PI name, institution, scholar_id. Co-investigators if available.
2. **Clinical trial classification**: not_allowed / optional / required. Determines Parent R01 NOFO.
3. **NIH context**: Target institute + FOA. If missing, spawn `r01-foa-finder` to search Grants.gov and NIH Reporter, then present recommendations for user confirmation.
4. **Submission timeline**: Next receipt date, project start/end. Auto-calculated if not specified.

If all metadata is already present in `project.yaml`, this phase auto-completes with no interaction.

See `references/pipeline.md` Phase 1.5 for the full specification.

# Investigator Verification Gate (Phase 2.5 — between ideation and literature)

**BLOCKING GATE**: Do NOT start literature search until all investigators are verified. Literature agents need investigator names, institutions, and ideally scholar_ids/ORCIDs to search for team publications effectively. Missing or incorrect PI info wastes entire literature search cycles.

## Verification checks (run after ideation completes, before literature dispatch):
1. **For each investigator** in `project.yaml.investigators` (PI + all co-PIs):
   - `name` is present and non-null.
   - `institution` is present and non-null.
   - `expertise` has at least 1 entry.
   - `scholar_id` (Google Scholar ID or ORCID) is present. If missing, **ask the user** for it. Explain: "I need scholar IDs to find each investigator's publications for citation. This significantly improves literature search quality."
2. **Verify each investigator is findable**: For each investigator, run a quick web search (`web_search(query="{name}" {institution})`) to confirm they exist at that institution. If no match is found:
   - Ask the user: "I couldn't verify {name} at {institution}. Could you confirm the correct name/affiliation or provide their ORCID?"
   - Do NOT proceed to literature search with unverified investigators.
3. **Record verification** in `state.json`:
   ```json
   "investigator_verification": {
     "pi": {"verified": true, "scholar_id": "...", "method": "orcid_lookup"},
     "co_pi_1": {"verified": true, "scholar_id": "...", "method": "web_search"},
     "co_pi_2": {"verified": false, "issue": "not_found_at_institution", "awaiting_user": true}
   }
   ```
4. **Only proceed to Phase 3 (literature)** when all investigators have `verified: true`.

This gate prevents the failure mode where literature agents spend their entire budget on domain queries without finding any PI publications.

# Ideation Flow (Phase 2)
The orchestrator first determines the ideation mode:
- **Express mode**: If `project.yaml` contains aims with descriptions and the user provided a complete concept. Spawn ideation agent with "Use express mode."
- **Full mode**: If only a topic is provided. Spawn ideation agent with "Use full mode."

In full mode, the ideation agent runs a 5-step DIVERGE/DEVELOP/FILTER/CONVERGE/CHECKPOINT flow:
1. **DIVERGE** — generate a broad set of candidate ideas without filtering.
2. **DEVELOP** — expand each candidate with a 5-field chain-of-thought (problem, mechanism, novelty claim, feasibility risk, NIH fit).
3. **FILTER** — apply feasibility criteria; drop ideas that fail on budget, timeline, or team capacity.
4. **CONVERGE** — rank surviving ideas and select the top 3-5 for novelty checking.
5. **CHECKPOINT** — pause for user idea selection after novelty verdicts are in.

After FILTER, the orchestrator spawns `r01-novelty-checker` as a sub-step. The novelty checker runs background literature retrieval, applies a dual-bias protocol, and writes `ideas/novelty_report.json`. The ideation agent reads this report before CONVERGE to incorporate novelty verdicts into final rankings.

# Parallel Literature Dispatch (Phase 3)
1. Read `project.yaml` → get domain tags.
2. Populate `state.json.literature_parallel` with one entry per domain.
3. Spawn 3 literature subagents with **30-second stagger** between launches to avoid API rate limits (Semantic Scholar: 10 req/5min without key; PubMed E-utilities: 3 req/10s):
   - Each reads `r01-literature` skill and is assigned one domain: `hci`, `healthcare`, or `ai`.
   - **CRITICAL**: Pass `workspace` parameter pointing to the project directory so relative file paths resolve correctly:
   - Task prompt: "You are the {domain} literature agent. Read the r01-literature skill at {skill_path} and follow its instructions. Your domain assignment is: {domain}. Project path: ~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/. Find 10-18 references for the {domain} domain. IMPORTANT: Run Step 0 (Investigator Publication Search) and Step 0.5 (Seed Reference Ingestion from project.yaml.seed_references) BEFORE domain queries. Use citation graph traversal and iterative query refinement as specified in the skill. Write to literature/references_{domain}.json and literature/gaps_{domain}.md."
   - Spawn call: `spawn(task=..., label="lit-{domain}", max_iterations=30, model=..., workspace="~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/")`
   - Each agent runs multi-round search (up to 3 rounds), snowball sampling via Semantic Scholar citation graph, and produces claim-evidence mappings, contradiction detection, and evidence synthesis tables.
4. **State tracking (MANDATORY — do this for EVERY spawn and retry):**
   - **Before each spawn**: Read `state.json`, set `literature_parallel.{domain}.status = "running"`, increment `attempt` by 1, write `state.json` back. Append an event: `{"timestamp": ..., "event": "literature_spawn", "domain": "{domain}", "attempt": N}`.
   - **On agent success**: Set `literature_parallel.{domain}.status = "complete"`, write `state.json`. Append event: `{"timestamp": ..., "event": "literature_complete", "domain": "{domain}", "attempt": N}`.
   - **On agent failure**: Set `literature_parallel.{domain}.status = "failed"`, write `state.json`. Append event with failure reason: `{"timestamp": ..., "event": "literature_failed", "domain": "{domain}", "attempt": N, "reason": "..."}`.
   - **Max retries**: If `literature_parallel.{domain}.attempt >= 3` and status is still `"failed"`, do NOT re-spawn. Mark phase as `"blocked"`, append event, and request user intervention. Three failed attempts with the same strategy will not succeed a fourth time.
5. When all 3 domain searches complete (status = `"complete"` for all domains):
   - Merge `literature/references_hci.json`, `literature/references_healthcare.json`, `literature/references_ai.json` into `literature/references.json`.
   - Deduplicate references (same DOI or URL → keep highest-priority annotation, preserving `supports_claim` fields).
   - Merge `literature/gaps_hci.md`, `literature/gaps_healthcare.md`, `literature/gaps_ai.md` into `literature/gaps.md`, consolidating cross-domain contradictions and evidence synthesis tables.
   - Validate: every `must-cite` reference must have a non-empty `supports_claim`.
   - Update `state.json.artifacts.literature_refs` and `state.json.artifacts.literature_gaps`.

# Parallel Writing Dispatch (Phase 5)

## Batching Strategy
Instead of separate spawns per section, batch into **1 integrator + N aim batches (parallel) + 1 assembly (sequential)**:

| Batch | Agent | Sections | Parallel? |
|-------|-------|----------|-----------|
| A | r01-writer-integrator | specific_aims, significance, innovation | Yes (with B..N) |
| B..N | r01-writer-{aim.domain_tag} | approach_aim{i} (one batch per aim in project.yaml) | Yes |
| E | r01-writer-integrator | timeline, crosscutting, project_narrative, project_summary + merge all into research_strategy_v1.md | After A..N complete |

## Dispatch Steps
1. Read `project.yaml` → get aim-to-domain mapping and model overrides.
2. Dynamically populate `state.json.writing_parallel` with one `approach_aim{i}` entry per aim.
3. Mark sections in `state.json.writing_parallel` as `running` for batch A and all aim batches.
4. Call `spawn` simultaneously for batch A + N aim batches, each with:
   - `max_iterations=30` (writers need headroom for reading inputs + drafting)
   - `model` from `project.yaml.model_config.overrides` for the assigned skill
   - `workspace="~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/"` so relative paths in writer skills resolve correctly
5. As each batch completes, mark its sections `complete` in `state.json.writing_parallel`.
6. When batch A and all aim batches are `complete`, spawn batch E (assembly).
7. When batch E completes, mark remaining sections + `writing_integration` as `complete`.

## Spawn Prompt Template
Every writer spawn must include ALL of the following in the task string. Also pass `workspace="~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/"` so the subagent's file tools resolve relative paths against the project directory.

```
You are a writing subagent. Read the {skill_name} skill at {skill_path} and follow its instructions.

PROJECT: {project_path}
SECTIONS TO WRITE: {section_list_with_word_targets}
OUTPUT FILES: {output_file_paths}

REQUIRED INPUTS (read these before writing):
- Project config: {project_path}/project.yaml
- Proposal outline: {project_path}/docs/outline.md (find your section specs here)
- Literature: {project_path}/literature/refs.json and {project_path}/literature/gaps.md
- Selected idea: {project_path}/ideas/ideas.json
- Style references: ~/Dropbox/AgentWorkspace/PriorNIHR01Examples/ (read 1-2 for voice calibration)
- System style guide: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/style_guide.md
- Section specs: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/r01_section_specs.md

INSTRUCTIONS:
1. Read the skill file first for your role and quality standards.
2. Read outline.md and locate YOUR assigned section(s) — use the heading structure and word targets there.
3. Read refs.json and gaps.md to incorporate citations and address gaps.
4. Read 1-2 prior examples for NIH voice calibration.
5. Write each section to its output file. Use markdown with proper heading hierarchy.
6. Each section MUST meet its word target (±10%).
7. Cite references using [AuthorYear] format matching refs.json entries.
```

Do NOT ask the subagent to update state.json — the orchestrator tracks completion externally.

# Pre-Review Self-Check (Phase 7 Gate)
Before spawning the three domain reviewers, the orchestrator MAY run a quick self-review by spawning `r01-writer-integrator` in a lightweight review mode. This catches obvious issues (missing sections, broken citations, unresolved placeholders, word-count violations) cheaply, before committing to the more expensive parallel reviewer spawns.

If the self-check finds blocking issues, route back to writing for targeted fixes. If it passes or finds only minor issues, proceed to full review dispatch. Record the self-check outcome in `state.json.pre_review_gate`.

# Parallel Review Dispatch (Phase 8)
1. Spawn 3 domain reviewers in parallel:
   - `r01-reviewer-hci`
   - `r01-reviewer-healthcare`
   - `r01-reviewer-ai`
2. Each reviewer runs a background retrieval step to pull relevant prior art before scoring, then applies a dual-bias protocol (one pass as a skeptic, one as an advocate) to reduce anchoring.
3. Each reviewer produces structured JSON with fields: `nih_dimensions` (scored 1-9 per criterion), `background_findings` (retrieved context used), `review_confidence` (0-1), and `critique_items` (prioritized list).
4. When all 3 complete, spawn `r01-reviewer-panel` to synthesize.
5. The panel runs a reflection loop: it reads all three domain reviews, identifies conflicts, resolves them with explicit reasoning, and produces `panelist_perspectives`, a revision priority matrix, and a `findings_memory_entry` object.
6. The panel writes its `findings_memory_entry` to `ideas/findings_memory.json` (append to array).
7. Panel produces overall impact score (1-9) and summary.
8. If score `< 5` and `review_round < max_review_rounds`, route to Phase 9 (revision).

## Review/Revision Loop
- The panel writes one `findings_memory_entry` per round to `ideas/findings_memory.json`.
- At the start of each revision, the reviser reads the full `findings_memory.json` array to understand cumulative findings across all prior rounds, not just the most recent critique.
- Loop control: continue while `score < 5` AND `review_round < max_review_rounds`. When either condition breaks, exit to export.

# Post-Export Evolution (Phase 11)
After the export phase completes and the user has approved the final package, spawn the `r01-evolution` agent to extract cross-project learning.

1. Spawn `r01-evolution` with the completed project path.
2. The evolution agent reads all review JSONs, revision diffs, findings memory, and any user feedback files.
3. It updates `_system/reviewer_patterns.json` with new or incremented patterns.
4. It appends entries to `_system/evolution_log.json`.
5. It may propose `_system/style_guide.md` changes that require user approval.
6. Set `phase_status.evolution = complete` when done.

This phase is also triggered manually when the user provides real NIH reviewer feedback (Summary Statement) after submission. In that case, spawn `r01-evolution` with the project path and the feedback file path.

# User Checkpoints
- After ideation, pause for user idea selection (see Idea Feedback Checkpoint below).
- After outline, pause for user structural review (see Outline Feedback Checkpoint below).
- After writing, pause for user draft review (see Draft Feedback Checkpoint below).
- After export, pause for final user review.
- After evolution, present the summary of patterns extracted and any proposed style guide changes for approval.
- At each checkpoint, post to Slack and wait for explicit user confirmation.

# Feedback Checkpoints and Voice Calibration

## Checkpoint A: Idea Feedback (after ideation, during user selection)
The existing ideation checkpoint pauses for idea selection. Extend it:
1. Present top 3-5 ideas with scores, rationales, risks.
2. User selects one idea (or requests modifications).
3. Record **why** the user selected this idea and **why** they rejected others:
   - Ask: "Any reason you preferred this one? Anything about the others that didn't appeal?"
   - If user provides reasons, record in `feedback/idea_feedback_{project}.json`.
   - If user declines to elaborate, record selection without reasons.
4. The ideation agent records the selection in `_system/ideation_preferences.json` under `selection_history`.
5. After 3+ projects, the ideation agent auto-detects patterns and updates preference fields (with user notification).

## Checkpoint B: Outline Feedback (after outline, before writing dispatch)
After the integrator produces `docs/outline.md`:
1. Present the outline to the user.
2. Ask: "Any structural changes? Section emphasis adjustments? Framing you'd change?"
3. Classify user feedback:
   - **Structural** (aim ordering, section emphasis, scope) → route to integrator for revision.
   - **Voice/framing** (how something is framed, word choices, argumentation style) → route to `r01-evolution` for `writing_voice.md` update.
4. Record all feedback in `feedback/outline_feedback_{project}.json`.
5. Only proceed to writing dispatch after the user confirms the outline.

## Checkpoint C: Draft Feedback (after writing, before review)
After domain writers produce drafts in `docs/drafts/`:
1. Present each domain's draft to the user (or the user's domain collaborator).
2. Accept three types of feedback per draft:
   - **Inline edits**: Direct rewrites of sentences/paragraphs → route to reviser.
   - **Style notes**: "too hedgy", "doesn't sound like me", "I'd never frame it this way" → route to `r01-evolution` for voice file update.
   - **Content notes**: "missing X", "wrong emphasis on Y" → route to reviser.
3. Feedback can be attributed to a specific collaborator: "Dr. Smith's feedback on the healthcare sections" → routes style corrections to `writing_voice_healthcare.md` specifically.
4. Record all feedback in `feedback/draft_feedback_{project}.json` with fields:
   ```
   {
     "section": "approach_aim1",
     "domain": "hci",
     "collaborator": "user" or collaborator name,
     "feedback_type": "style" | "content" | "inline_edit",
     "original_text": "the text being corrected (if inline edit)",
     "feedback": "the user's comment or rewrite",
     "auto_classification": "style" | "content",
     "user_override": null or corrected classification
   }
   ```
5. The orchestrator presents the auto-classification to the user:
   "I classified this as a **style** correction (voice/framing preference). Correct? [yes / no, it's content]"
   If the user overrides, record the override in `user_override`. Over time, the classification model improves.
6. Route feedback:
   - Style feedback → spawn `r01-evolution` with the feedback file and target voice file path.
   - Content feedback → accumulate for the revision phase or re-dispatch to the appropriate writer.
   - Inline edits → apply directly to the draft if the user confirms.

## Agent Learnings Collection
After each subagent completes (any phase), check if the agent's output includes an `agent_learnings` JSON block. If present:
1. Extract the learnings.
2. Accumulate in `feedback/agent_learnings_{project}.json` (append-only, tagged with agent name and phase).
3. Route to `r01-evolution` during the evolution phase for pattern detection.

Do NOT spawn the evolution agent for each individual learning — batch them and process during the evolution phase.

# State Management
- Always read `state.json` before dispatching or transitioning phases.
- Write phase/task updates atomically in `state.json`.
- Append lifecycle events to `events.jsonl` (`spawned`, `completed`, `failed`, `checkpoint_wait`, `checkpoint_resumed`).
- Append per-agent cost entries to `cost.jsonl` after each subagent completion. Each entry must include: `timestamp`, `phase`, `agent` (skill name), `model`, `prompt_tokens`, `completion_tokens`, `cost_usd` (estimated from token counts), and `task_description`. If token counts are not available from the spawn result, record `null` and note in the event. The `cost.jsonl` should never be empty after any phase completes — at minimum, record a zero-cost entry for phases that use no subagents (e.g., init).
- Treat `events.jsonl` and `cost.jsonl` as append-only ledgers.

# Workspace Constraint
- All file operations are restricted to `~/Dropbox/AgentWorkspace/` and `~/.nanobot/workspace/`.
- Never access files outside these two roots.

# References
- `references/pipeline.md`
- `references/parallel_execution.md`
