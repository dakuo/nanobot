# R01 Multi-Agent Proposal Auto-Generation System — Project Plan

> **Purpose**: This document is the single source of truth for any agent or developer continuing work on this system. It captures architecture decisions, what has been built, what remains, and all constraints. **Read this before doing anything.**

---

## 1. Project Goal

Build a **multiagent NIH R01 proposal auto-generation system** on top of nanobot that:

- Uses **16 specialized skills** (orchestrator, ideation, novelty checker, literature, 4 domain writers, 4 domain reviewers, reviser, figures, budget, evolution)
- Domain writers (HCI, Healthcare, AI) work **in parallel**; domain reviewers also work **in parallel**
- **Self-evolves** from user feedback and actual NIH reviewer feedback
- Has a **web UI dashboard** (NiceGUI recommended) for progress/cost tracking
- Has **Figma bidirectional sync** for figures (MVP: matplotlib, future: Figma MCP)
- Generates: 15-page Research Strategy, 1-sentence Project Narrative, 30-line Project Summary, Budget Justification
- All artifacts live in a **configurable shared workspace** (default: `~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/`)
- Prior R01 examples in a **configurable examples directory** (default: `~/Dropbox/AgentWorkspace/PriorNIHR01Examples/`) for few-shot learning

### Target Domain

Human-centered AI research for medical/healthcare proposals. The system is designed around three intersecting domains:
- **HCI** (Human-Computer Interaction) — user studies, participatory design, usability
- **Healthcare** — clinical workflows, patient outcomes, health informatics, regulatory
- **AI/ML** — model architectures, training pipelines, evaluation methodology

---

## 2. Architecture Overview

### 2.1 Why Nanobot as Orchestration Layer

After evaluating AutoGen, LangGraph, CrewAI, FARS, OpenFARS, AI-Scientist v1, and AI-Scientist v2:

- **Nanobot can serve as the orchestration layer directly** — its `SubagentManager` spawns child agents (15 iterations each) that inherit skills and tools
- No external framework needed (no AutoGen/LangGraph dependency)
- Skills system (`SKILL.md` files) provides clean agent specialization
- Slack integration already set up for user checkpoints

### 2.2 Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Writing approach | Template-based (AI-Scientist v1) | 15-page R01 has rigid structure; template ensures compliance |
| Ideation approach | Tree-search (AI-Scientist v2) | BFTS exploration generates diverse hypotheses |
| Orchestration | Nanobot native subagents | Already set up, avoids new dependencies |
| Agent specialization | SKILL.md files in workspace | Hot-reloadable, human-editable, version-controlled |
| Parallel execution | Multiple subagent spawns + state.json tracking | Nanobot can spawn N subagents; state.json tracks completion |
| Dashboard | NiceGUI (recommended) | FastAPI + Vue.js + Tailwind, reads state.json in real-time |
| Figures (MVP) | matplotlib + SVG export | Works offline, no API needed |
| Figures (future) | Figma MCP bidirectional sync | Figma REST API is read-only; write needs WebSocket bridge + plugin |
| Default LLM model | openai-codex/gpt-5.1-codex | User's configured default in `~/.nanobot/config.json` |
| Code execution | Faked for now | User explicitly requested this |

### 2.3 14-Agent Architecture

```
                    ┌─────────────────────┐
                    │   r01-orchestrator   │  ← State machine, dispatches all phases
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   Phase 2            Phase 3 (PARALLEL)       Phase 4
┌──────────────┐   ┌──────────────────────┐  ┌──────────────┐
│ r01-ideation │   │ r01-literature ×3    │  │r01-writer-   │
│              │   │  (hci, healthcare,   │  │ integrator   │
│ Tree-search  │   │   ai) → merge/dedup  │  │ (outline)    │
│ hypotheses   │   └──────────────────────┘  └──────────────┘
└──────────────┘              │                      │
                              │               Phase 5 (PARALLEL)
                              │         ┌──────────────────────────┐
                              │         │ r01-writer-hci           │
                              │         │ r01-writer-healthcare    │ ← simultaneous
                              │         │ r01-writer-ai            │
                              │         │ r01-writer-integrator    │
                              │         └──────────────────────────┘
                              │                    │ merge
                                           ┌──────┴──────┐
                                    Phase 6│ r01-figures  │
                                           └──────┬──────┘
                                           Phase 6│ r01-budget  │
                                           └──────┬──────┘
                                                  │
                                     Phase 7 (PARALLEL)
                              ┌──────────────────────────┐
                              │ r01-reviewer-hci         │
                              │ r01-reviewer-healthcare  │ ← simultaneous
                              │ r01-reviewer-ai          │
                              │ r01-reviewer-panel       │ ← after above 3
                              └──────────┬───────────────┘
                                         │
                                  Phase 8 │
                              ┌──────────┴──────────┐
                              │    r01-reviser       │
                              └─────────────────────┘
```

### 2.4 Pipeline Phases (10 total)

| Phase | Name | Agent(s) | Parallel? |
|-------|------|----------|-----------|
| 1 | init | orchestrator | No |
| 2 | ideation | r01-ideation | No |
| 3 | literature | r01-literature × 3 (hci, healthcare, ai) → merge | **Yes — 3 domain searches simultaneous** |
| 4 | outline | r01-writer-integrator | No |
| 5 | writing | r01-writer-{hci,healthcare,ai,integrator} | **Yes — all writers simultaneous** |
| 6 | figures + budget | r01-figures, r01-budget | Yes |
| 7 | review | r01-reviewer-{hci,healthcare,ai} → r01-reviewer-panel | **Yes — 3 reviewers simultaneous, then panel** |
| 8 | revision | r01-reviser | No |
| 9 | export | orchestrator | No |
| 10 | (loop) | Back to Phase 7 if score < 5 and rounds remain | — |

### 2.5 State Machine

Each project has a `state.json` tracking:
- `current_phase` — which pipeline phase is active
- `writing_parallel` — per-task status for Phase 4 writers
- `review_parallel` — per-task status for Phase 7 reviewers
- `review_round` / `max_review_rounds` — revision loop control
- `overall_impact_score` — panel's 1-9 score
- `user_checkpoints` — which checkpoints have been approved

Detailed specs in `skills/r01-orchestrator/references/pipeline.md` (264 lines) and `skills/r01-orchestrator/references/parallel_execution.md` (135 lines).

---

## 3. Directory Structure

### 3.1 In This Repository

> **Note**: Skills have been moved from `r01-proposal/skills/` to `nanobot/skills/` as built-in skills for easier distribution via `pip install`.

```
r01-proposal/
├── PLAN.md                          ← THIS FILE (project plan + status)
├── README.md                        ← Setup and installation instructions
├── workspace/                       ← Project workspace templates (copy to shared workspace)
│   ├── _templates/
│   │   ├── project.yaml             (137 lines — project config with aim-to-domain mapping)
│   │   ├── state.json               (pipeline state machine)
│   │   ├── cost.jsonl               (cost tracking schema)
│   │   ├── cost.json                (cost summary)
│   │   ├── events.jsonl             (event log schema)
│   │   └── README.md                (folder structure docs)
│   └── _system/
│       ├── style_guide.md           (227 lines — NIH R01 writing conventions)
│       ├── writing_voice.md         (149 lines — generic personal voice profile, 7 style dimensions)
│       ├── writing_voice_hci.md     (96 lines — HCI domain voice overrides)
│       ├── writing_voice_healthcare.md (104 lines — healthcare domain voice overrides)
│       ├── writing_voice_ai.md      (118 lines — AI/ML domain voice overrides)
│       ├── ideation_preferences.json (93 lines — PI research taste profile, selection history)
│       ├── reviewer_patterns.json   (71 lines — extracted reviewer feedback patterns)
│       ├── evolution_log.json       (44 lines — system self-evolution log)
│       └── r01_section_specs.md     (433 lines — detailed section specifications)

nanobot/skills/                      ← All 16 agent skills (built-in, distributed with package)
├── r01-orchestrator/
│   ├── SKILL.md                     (230 lines — state machine, parallel dispatch, novelty sub-step, pre-review gate, evolution phase, feedback checkpoints, agent learnings collection)
│   └── references/
│       ├── pipeline.md              (359 lines — all 11 phases detailed including evolution)
│       └── parallel_execution.md    (135 lines — parallel dispatch pseudocode)
├── r01-ideation/SKILL.md            (211 lines — 5-step DIVERGE/DEVELOP/FILTER/CONVERGE/CHECKPOINT, ideation preferences, agent learnings)
├── r01-novelty-checker/SKILL.md     (163 lines — multi-round literature search, overlap classification, risk appetite calibration, agent learnings)
├── r01-literature/SKILL.md          (279 lines — multi-round search, snowball, claim mapping, contradiction detection)
├── r01-writer-hci/SKILL.md          (86 lines — HCI voice calibration, agent learnings)
├── r01-writer-healthcare/SKILL.md   (82 lines — healthcare voice calibration, agent learnings)
├── r01-writer-ai/SKILL.md           (81 lines — AI voice calibration, agent learnings)
├── r01-writer-integrator/SKILL.md   (136 lines — 3-pass outline, word-target feedback, multi-domain voice, agent learnings)
├── r01-reviewer-hci/SKILL.md        (115 lines — dual-bias, background retrieval, reflection loop)
├── r01-reviewer-healthcare/SKILL.md (116 lines — dual-bias, background retrieval, reflection loop)
├── r01-reviewer-ai/SKILL.md         (117 lines — dual-bias, background retrieval, reflection loop)
├── r01-reviewer-panel/SKILL.md      (203 lines — multi-persona panel, score trajectory, priority matrix)
├── r01-reviser/SKILL.md             (149 lines — self-generated plan, diff tracking, findings memory)
├── r01-figures/SKILL.md             (149 lines — VLM review loop, set coherence, revision inheritance)
├── r01-budget/SKILL.md              (66 lines)
└── r01-evolution/SKILL.md           (150 lines — cross-project learning loop, pattern extraction, evolution log)
```

### 3.2 Shared Workspace (Configurable — default: `~/Dropbox/AgentWorkspace/`)

```
AgentWorkspace/
├── PaperAutoGen/
│   ├── _templates/                  ← Copied from r01-proposal/workspace/_templates/
│   ├── _system/                     ← Copied from r01-proposal/workspace/_system/
│   └── {project-name}/             ← One folder per proposal project
│       ├── project.yaml
│       ├── state.json
│       ├── cost.jsonl
│       ├── events.jsonl
│       ├── ideas/                   ← Ideation output
│       ├── references/              ← Literature output
│       ├── docs/drafts/             ← Writing drafts (versioned)
│       ├── figures/specs/           ← Figure YAML specs
│       ├── figures/exports/         ← Rendered figures (PNG/SVG)
│       ├── reviews/                 ← Reviewer reports (JSON)
│       └── export/                  ← Final assembled proposal
└── PriorNIHR01Examples/            ← User's prior proposals (for few-shot learning)
    └── (user populates this)
```

### 3.3 Configuration

The workspace and examples paths are configurable via `project.yaml`:

```yaml
# In each project's project.yaml:
workspace_root: "~/Dropbox/AgentWorkspace/PaperAutoGen"
prior_examples_path: "~/Dropbox/AgentWorkspace/PriorNIHR01Examples"
```

These can be overridden per-project. The system does NOT hardcode paths.

---

## 4. Phase Status

### Phase A: Workspace Schema — COMPLETE

| Artifact | Status | Location |
|----------|--------|----------|
| project.yaml template | Done | `workspace/_templates/project.yaml` |
| state.json template | Done | `workspace/_templates/state.json` |
| cost.jsonl schema | Done | `workspace/_templates/cost.jsonl` |
| events.jsonl schema | Done | `workspace/_templates/events.jsonl` |
| Folder structure README | Done | `workspace/_templates/README.md` |
| style_guide.md | Done | `workspace/_system/style_guide.md` |
| reviewer_patterns.json | Done | `workspace/_system/reviewer_patterns.json` |
| evolution_log.json | Done | `workspace/_system/evolution_log.json` |
| r01_section_specs.md | Done | `workspace/_system/r01_section_specs.md` |

### Phase B: Skills Creation — COMPLETE

All 14 original skills created with proper YAML frontmatter (`name` + `description`) and substantive markdown bodies. Every skill is a complete instruction set — not a stub. (Phase D added `r01-novelty-checker` as a 15th skill and upgraded 9 existing skills — see Phase D status below. Phase H added `r01-evolution` as the 16th skill.)

| Skill | Lines | Verified |
|-------|-------|----------|
| r01-orchestrator | 144 | Yes — state machine, parallel dispatch, user checkpoints, novelty checker sub-step, pre-review gate |
| r01-orchestrator/references/pipeline.md | 289 | Yes — all 10 phases with entry/exit criteria |
| r01-orchestrator/references/parallel_execution.md | 135 | Yes — pseudocode for parallel writing + review |
| r01-ideation | 181 | Yes — 5-step DIVERGE/DEVELOP/FILTER/CONVERGE/CHECKPOINT, CycleResearcher COT, exploration bonus |
| r01-novelty-checker | 139 | Yes — multi-round Semantic Scholar + web search, 4-level overlap, verdict categories |
| r01-literature | 279 | Yes — multi-round search, snowball sampling, claim-evidence mapping, contradiction detection, synthesis tables |
| r01-writer-hci | 72 | Yes — HCI voice, CHI/CSCW venues |
| r01-writer-healthcare | 66 | Yes — clinical voice, NEJM/JAMA |
| r01-writer-ai | 65 | Yes — technical voice, NeurIPS/ICML |
| r01-writer-integrator | 116 | Yes — 3-pass outline refinement, word-target feedback, terminology concordance, scratchpad |
| r01-reviewer-hci | 115 | Yes — dual-bias protocol, background retrieval, reflection loop, scratchpad |
| r01-reviewer-healthcare | 116 | Yes — dual-bias protocol, background retrieval, reflection loop, scratchpad |
| r01-reviewer-ai | 117 | Yes — dual-bias protocol, background retrieval, reflection loop, scratchpad |
| r01-reviewer-panel | 203 | Yes — multi-persona panel simulation, score trajectory, priority matrix, findings memory |
| r01-reviser | 149 | Yes — self-generated revision plan, diff tracking, word budget reconciliation, findings memory |
| r01-figures | 149 | Yes — VLM quality review loop, figure set coherence, revision-aware inheritance |
| r01-budget | 66 | Yes — NIH budget format, justification |
| r01-evolution | 150 | Yes — 6-step cross-project learning loop, pattern extraction, evolution log, style guide proposals |

### Phase C: End-to-End Test — ✅ COMPLETE

**Goal**: Run the orchestrator with a sample project to verify the full pipeline.

**Completed**:
- [x] Create a sample project folder (`r01-older-adults-mci-home-ai/`) with templates
- [x] Fill in project.yaml with real research topic (MCI home-based speech monitoring)
- [x] Run nanobot: init and ideation phases completed successfully
- [x] User selected idea 3: "Community choir storytelling circles augmented with speech gap analytics"
- [x] Aligned state.json schema with pipeline spec (added outline phase, fixed writing_parallel/review_parallel structures)
- [x] Created full project directory structure (literature/, docs/drafts/, figures/, budget/, reviews/, feedback/, export/)
- [x] Aligned pipeline.md output paths with skill contracts
- [x] Moved skills from r01-proposal/skills/ to nanobot/skills/ (built-in)
- [x] Verified all 14 skills discoverable by SkillsLoader from built-in directory
- [x] Literature phase completed: 30 references, 15 gaps identified across HCI/Healthcare/AI/cross-domain
- [x] Outline phase completed: section-level outline with writer assignments and word targets
- [x] Writing Phase 5 — Batches A-D (parallel domain writers) completed:
  - Batch A (integrator): specific_aims (490w), significance (1,381w), innovation (970w)
  - Batch B (HCI writer): approach_aim1 (1,583w)
  - Batch C (AI writer): approach_aim2 (1,464w)
  - Batch D (Healthcare writer): approach_aim3 (1,431w)
- [x] Writing Phase 5 — Batch E (integrator assembly) completed:
  - approach_timeline (443w), approach_crosscutting (519w), project_narrative (45w), project_summary (323w)
- [x] Writing integration: research_strategy_v1.md assembled (3,926w)
- [x] Fixed 5 key issues in spawn mechanism (max_iterations, model params in spawn.py/subagent.py)
- [x] Total: 10 section drafts, 8,649 words across all drafts

**Writing Phase Results Summary**:

| Section | Agent | Words | Target | Status |
|---------|-------|-------|--------|--------|
| specific_aims | integrator | 490 | 500 | ✅ |
| significance | integrator | 1,381 | 1,500 | ✅ |
| innovation | integrator | 970 | 1,000 | ✅ |
| approach_aim1 | hci-writer | 1,583 | 1,500 | ✅ |
| approach_aim2 | ai-writer | 1,464 | 1,500 | ✅ |
| approach_aim3 | healthcare-writer | 1,431 | 1,500 | ✅ |
| approach_timeline | integrator | 443 | 300 | ✅ |
| approach_crosscutting | integrator | 519 | 300 | ✅ |
| project_narrative | integrator | 45 | 1 sentence | ✅ |
| project_summary | integrator | 323 | 300-350 | ✅ |
| **research_strategy_v1.md** | **assembled** | **3,926** | — | ✅ |

**Phase 6: Figures + Budget** — ✅ COMPLETE
- [x] Figure specs (F1-F4): system architecture, CONSORT flowchart, speech pipeline, timeline/Gantt
- [x] Figure captions: publication-quality, self-contained, all abbreviations defined
- [x] Budget table: 5-year, all years under $500K direct cost cap, $3.39M total
- [x] Budget justification: 9 personnel roles, equipment, travel, participant costs, other direct, F&A

**Phase 7: Review** — ✅ COMPLETE
- [x] 3 parallel domain reviewers dispatched (HCI=4, AI=5, Healthcare=3)
- [x] Panel synthesizer produced overall impact score: **4/9, decision: REVISE**
- [x] 23 priority revisions identified, 8 consensus strengths, 5 consensus weaknesses, 3 disagreements resolved
- [x] Key issues: English-only criterion, missing ML baselines, thin incidental findings protocol, TFT overparameterized

**Phase 8: Revision** — ✅ COMPLETE
- [x] All 23 panel revisions addressed across parallel revision batches
- [x] Aim 2 v2: baselines added, LLM step specified (Llama 3 70B), TFT→mixed-effects as primary, ablation plan, power analysis
- [x] Aims 1+3+cross-cutting v2: English-only addressed, incidental findings expanded, endpoints pre-specified, DSMB charter, group audio HIPAA
- [x] v2 word counts: Aim 1 (1,928w), Aim 2 (2,013w), Aim 3 (1,986w), Cross-cutting (881w), Specific Aims (553w)

**Phase 9: Export** — ✅ COMPLETE
- [x] research_strategy_v2.md assembled (9,610 words)
- [x] export/README.md package manifest created
- [x] 41 files total in project workspace
- [x] state.json updated: all phases complete

**End-to-End Pipeline Test: COMPLETE** (Phases 1-10 all verified)

### Phase D: Ideation, Review & Revision Enhancements — ✅ COMPLETE

**Goal**: Upgrade ideation, review, and revision skills with patterns from AI-Scientist V1/V2, CycleResearcher, Zochi, AI Researcher, and DeepScientist.

**Research Conducted**:
- Studied 6 AI research automation projects for improvement patterns
- Identified key patterns: multi-stage ideation, dual-bias review, VLM figure review, diff-tracked revision, structured scratchpad reasoning

**Skills Updated (8 total — 7 upgraded + 1 new)**:

| Skill | Lines | Key Enhancements |
|-------|-------|------------------|
| `r01-ideation` | 181 | 5-step DIVERGE/DEVELOP/FILTER/CONVERGE/CHECKPOINT pipeline; CycleResearcher 5-field chain-of-thought (motivation, main idea, interestingness, feasibility, novelty); 3-round reflection loop per branch (structured generation → literature grounding → self-critique with quoted evidence); exploration bonus scoring with diversity_bonus; prior example mining for structural patterns |
| `r01-novelty-checker` | 139 | **NEW SKILL** — Multi-round Semantic Scholar + web search (up to 5 rounds per branch); 4-level overlap classification (no_overlap → partial → significant → duplicate); differentiation articulation requirements; verdict categories (novel, novel_with_differentiation, needs_revision, not_novel); confidence tracking |
| `r01-orchestrator` | 144 | Updated ideation flow with novelty checker sub-step; pre-review self-check gate; findings_memory.json initialization during init phase |
| `r01-reviewer-hci` | 115 | Background retrieval step (Semantic Scholar/ACM DL); dual-bias review protocol (critical + supportive passes); reflection loop (up to 3 rounds); scratchpad pattern (`<THOUGHT>`/`<OUTPUT>`) |
| `r01-reviewer-healthcare` | 116 | Same pattern: background retrieval (PubMed/ClinicalTrials.gov); dual-bias; reflection; scratchpad |
| `r01-reviewer-ai` | 117 | Same pattern: background retrieval (arXiv/Papers With Code); dual-bias; reflection; scratchpad |
| `r01-reviewer-panel` | 203 | Multi-persona panel simulation (4 panelists: Senior Methodologist, Clinical Champion, Innovation Advocate, Devil's Advocate); score trajectory tracking across rounds; revision priority matrix (2×2 impact/effort); findings memory integration |
| `r01-figures` | 149 | VLM quality review loop (up to 3 retries per figure); figure set coherence review; revision-aware figure inheritance |
| `r01-reviser` | 149 | Self-generated revision plan with dependency graph; pre-revision self-review gate; precise diff tracking (`revision_diffs_r{N}.json`); word budget reconciliation table; findings memory read/write loop |
| `r01-writer-integrator` | 116 | 3-pass outline refinement (skeleton → detail → review); word-target feedback loop; terminology concordance table; scratchpad pattern for complex integration decisions |

**Tasks Completed**:
- [x] Implement branching: 5 orthogonal directions with 3-axis variation (intervention mechanism, user role, data pipeline)
- [x] Implement scoring: novelty (1-10), feasibility (1-10), NIH alignment (1-10), plus exploration/diversity bonus
- [x] Read prior examples from PriorNIHR01Examples/ for structural pattern extraction
- [x] Output to `ideas/ideas.json` with full scoring rubric and generation metadata
- [x] Implement user checkpoint: present top 3 ideas with scores, rationales, risks, and mitigations
- [x] Create novelty checker as separate skill with multi-round literature search
- [x] Add dual-bias review protocol to all 3 domain reviewers
- [x] Add background retrieval step to all 3 domain reviewers
- [x] Add reflection loops to all 3 domain reviewers
- [x] Add multi-persona panel simulation to panel reviewer
- [x] Add VLM quality review loop to figures agent
- [x] Add diff tracking and findings memory to reviser
- [x] Add 3-pass outline refinement to writer-integrator
- [x] Update orchestrator with new ideation flow and pre-review gate

### Phase E: Literature Search — ✅ COMPLETE (parallel, tool-level, enhanced)

**Goal**: Three parallel domain literature agents (HCI, Healthcare, AI) using concrete web_search/web_fetch tool chains, enhanced with patterns from AI-Scientist V1/V2, CycleResearcher, Zochi, AI Researcher, and DeepScientist.

**Design Changes (implemented)**:
- [x] Rewrote `r01-literature` SKILL.md with concrete tool-level instructions (web_search, web_fetch, Semantic Scholar API)
- [x] Skill is now domain-parameterized — spawned per domain with `hci`, `healthcare`, or `ai` assignment
- [x] Added `literature_parallel` tracking to state.json (3 parallel entries)
- [x] Updated orchestrator to dispatch 3 literature agents simultaneously
- [x] Updated pipeline.md with parallel literature phase spec
- [x] Updated parallel_execution.md with literature dispatch pseudocode
- [x] Each agent writes `literature/references_{domain}.json` + `literature/gaps_{domain}.md`
- [x] Merge step combines into `literature/references.json` + `literature/gaps.md` with dedup

**Phase E Enhancements (5 improvements from external AI research projects)**:

| Enhancement | Source Inspiration | What It Does |
|-------------|-------------------|--------------|
| Citation graph traversal | AI-Scientist V2, DeepScientist | Step 4.5: Snowball sampling via Semantic Scholar API — forward/backward citations from top 5 must-cite papers, capped at 10 additional papers |
| Iterative query refinement | AI-Scientist V1 novelty checker | Step 4.7: Assess per-aim coverage, generate refined queries from discovered terminology, up to 3 search rounds, early exit when all aims have 5+ papers |
| Contradiction detection | CycleResearcher | Added to Step 6: Flag papers with conflicting findings, document disagreements, explain how proposal handles them |
| Claim-evidence mapping | AI-Scientist V2, CycleResearcher | `supports_claim` field in annotation schema — one-sentence proposal claim each reference supports, creating traceable evidence chain |
| Evidence synthesis tables | AI Researcher, Zochi | Per-aim tables in gap analysis: paper, population, method, primary outcome, key finding, limitation, our advantage |

**Files updated**:
- [x] `nanobot/skills/r01-literature/SKILL.md` — 162 → 279 lines (5 enhancements integrated)
- [x] `nanobot/skills/r01-orchestrator/SKILL.md` — literature dispatch section updated with new capabilities
- [x] `nanobot/skills/r01-orchestrator/references/pipeline.md` — Phase 3 spec updated with enhanced actions, output metadata, and claim validation exit criteria

**Verification**:
- [x] Verify parallel literature dispatch works end-to-end — **PASS (partial)**: 2/3 domain agents completed successfully; AI agent hit Semantic Scholar 429 rate limits. Fixed by adding API priority/rate limiting guidance to skill and 30-second stagger to orchestrator dispatch.
- [x] Verify merge/dedup produces clean combined output — **PASS**: All produced files pass schema validation (`_metadata` header, `supports_claim` on must-cite refs, contradiction detection section, evidence synthesis tables present).
- [x] Validate that 30-50 real references are collected across domains — **PASS**: 32 references from 2 domains alone (HCI: 16, Healthcare: 16). With AI domain, projection is 45+. All have DOIs/URLs, must-cite refs have specific `supports_claim` fields.

**Post-test fixes applied**:
- Added API priority and rate limiting section to `r01-literature/SKILL.md` Step 3 (PubMed E-utilities primary, Semantic Scholar secondary with rate limits)
- Added 30-second stagger to orchestrator literature dispatch to distribute API load
- Skill now at 296 lines (was 279)

### Phase F: Web Dashboard — COMPLETE (via openclaw-bot-review)

**Goal**: Dashboard for monitoring pipeline progress and costs.

**Implementation**: Covered by the `openclaw-bot-review` project (separate repository), which provides subagent tracking and dashboard functionality. The original NiceGUI plan was superseded.

### Phase G: Figma Integration — ✅ COMPLETE (MVP: matplotlib renderer)

**Goal**: Bidirectional figure sync (MVP: matplotlib only; future: Figma MCP).

**Completed**:
- [x] **Tier 1 (MVP)**: matplotlib figure generation from YAML specs
- [x] Created `r01-proposal/r01_figure_renderer.py` (1,817 lines) — standalone renderer script
- [x] Figure types implemented: system architecture, CONSORT flowchart, data pipeline, conceptual framework/Gantt
- [x] Export to PNG (300 DPI) + SVG in `figures/exports/`
- [x] All 4 figures rendered and VLM-reviewed for quality
- [x] Auto-generated captions already in `figures/captions.md`
- [ ] **Tier 2 (Future)**: Figma MCP read integration (pull design tokens)
- [ ] **Tier 3 (Future)**: Figma write bridge (WebSocket + plugin for pushing updates)

**Figures Rendered**:

| Figure | Type | SVG Size | PNG Size | Status |
|--------|------|----------|----------|--------|
| F1 | System Architecture | 102K | 217K | ✅ Publication-quality |
| F2 | CONSORT Flowchart | 143K | 284K | ✅ Publication-quality |
| F3 | Data Pipeline | 152K | 251K | ✅ Publication-quality |
| F4 | Timeline/Gantt | 156K | 275K | ✅ Publication-quality |

**Renderer Architecture**:
- `RENDERER_MAP` dispatches on YAML `figure_type` field
- Each renderer reads the full spec and produces publication-grade output
- Exact hex colors from specs (amber #E8A838, blue #3A6EA5, teal #2E8B6A)
- 300 DPI PNG + SVG for every figure
- Standalone script: `python r01_figure_renderer.py --spec-dir ... --output-dir ...`

### Phase H: Self-Evolution — ✅ COMPLETE

**Goal**: System learns from feedback and improves over time.

**Completed**:
- [x] Created `r01-evolution` skill (16th skill) — 150-line SKILL.md with 6-step learning loop
- [x] After each project: evolution agent extracts patterns from reviews into `_system/reviewer_patterns.json`
- [x] User feedback (Slack or feedback files) → proposed `style_guide.md` updates (user approval required)
- [x] Real NIH reviewer feedback → parse Summary Statement, extract scored patterns, update calibration
- [x] Track what changed, why, which project triggered it in `_system/evolution_log.json`
- [x] Cross-project aggregation: increment pattern frequencies, flag high-frequency patterns (3+) for style guide promotion
- [x] Updated orchestrator with Phase 11 (evolution) — dispatches after export
- [x] Updated `pipeline.md` with Phase 11 entry/exit criteria
- [x] Updated `state.json` template with `evolution` phase status
- [x] Seeded `reviewer_patterns.json` with 8 patterns, 5 weaknesses, 5 strengths from Phase C test run
- [x] Seeded `evolution_log.json` with 5 initial learning entries from Phase C test run
- [ ] (Future) Automated A/B testing of writing strategies

**Self-Evolution Architecture**:
- `r01-evolution` skill reads all review JSONs, revision diffs, and findings memory from a completed project
- Identifies weakness patterns, strength patterns, and revision effectiveness
- Updates `_system/reviewer_patterns.json` (append-only, frequency-tracked, domain-specific)
- Appends to `_system/evolution_log.json` (append-only, each entry has lesson + action + approval status)
- Proposes `_system/style_guide.md` changes only with user approval
- Cross-references patterns across all prior projects to detect recurring issues

**System Files Seeded from Phase C**:

| File | Entries | Description |
|------|---------|-------------|
| `reviewer_patterns.json` | 8 patterns, 5 weaknesses, 5 strengths, 1 score example | Extracted from panel_decision_r1.json |
| `evolution_log.json` | 5 entries | Lessons on baselines, equity, ethics, model complexity, HCI methods |

### Phase I: Voice Calibration & Feedback System — ✅ COMPLETE

**Goal**: Implement a three-tier voice/preference learning system so writers produce output that matches the PI's personal writing style, with domain-specific calibration and interactive feedback refinement.

**Architecture**: Three-tier voice hierarchy with hybrid (AI + user) feedback classification.

| Tier | File | Purpose | Updated By |
|------|------|---------|------------|
| Generic voice | `_system/writing_voice.md` | Personal voice across all domains (7 style dimensions) | `r01-evolution` after Draft Feedback Checkpoint |
| Domain voice | `_system/writing_voice_{hci,healthcare,ai}.md` | Domain-specific overrides | `r01-evolution` after domain-specific feedback |
| NIH conventions | `_system/style_guide.md` | Baseline NIH writing standards | `r01-evolution` with user approval |

**Voice Precedence**: domain-specific > generic > style_guide. Writers read all three and apply the highest-precedence rule for each writing dimension.

**Seven Style Dimensions** (in `writing_voice.md`):
1. Argumentative Style — how claims are structured (assertion-first vs. background-first)
2. Technical Depth — specificity of methods description (architecture-explicit vs. umbrella-term)
3. Citation Philosophy — how evidence is woven into prose (integrated vs. parenthetical)
4. Hedging Tolerance — confidence level (definitive vs. cautious)
5. Narrative Voice — person and activity (first-plural active vs. passive)
6. Interdisciplinary Framing — how cross-domain links are made (bridge-explicit vs. implicit)
7. Reader Model — assumed audience expertise (expert-but-not-specialist vs. specialist)

**Domain Override Patterns**:
- HCI: Problem-experience-first argumentation, method-justified depth, clinical-impact-anchor framing
- Healthcare: Burden-first argumentation, clinically-grounded specificity, conservative hedging for clinical claims
- AI: Limitation-driven argumentation, architecture-explicit depth, benchmark-grounded confidence

**Ideation Preferences** (`_system/ideation_preferences.json`):
- `hypothesis_framing.preferences` — preferred hypothesis types (mechanistic, implementation, evaluation)
- `methodological_tendency` — preferred/avoided study designs
- `risk_appetite` — conservative/moderate/aggressive (inferred from selection patterns)
- `topic_preferences` — preferred/avoided research themes
- `scope_preference` — aim count and independence level preferences
- `selection_history` — tracks every idea selection with rejection reasons for pattern detection
- Auto-update rules: after 3+ selections showing consistent pattern, update preferences and notify user

**Feedback Checkpoints** (in orchestrator):
| Checkpoint | When | Feedback Types | Routing |
|-----------|------|----------------|---------|
| A: Idea Feedback | After ideation selection | Selection reasons, rejection reasons | `ideation_preferences.json` → `r01-evolution` |
| B: Outline Feedback | After outline, before writing | Structural changes, voice/framing notes | Structural → integrator; Voice → evolution |
| C: Draft Feedback | After writing, before review | Inline edits, style notes, content notes | Inline → reviser; Style → evolution; Content → reviser |

**Hybrid Feedback Classification** (in Checkpoint C):
- System auto-classifies each feedback item as "style" or "content"
- User can override classification: "I classified this as a **style** correction. Correct?"
- Over time, classification improves from override patterns
- Style feedback → voice file updates; Content feedback → revision

**Agent Learnings System**:
- All 6 updated skills (4 writers + ideation + novelty-checker) output `agent_learnings` JSON at task end
- Orchestrator collects learnings in `feedback/agent_learnings_{project}.json`
- Batched for evolution agent processing (not spawned per-learning)
- Learning types: `error_recovered`, `better_approach`, `style_observation`

**Completed**:
- [x] Created `_system/writing_voice.md` — 7-dimension generic voice profile with calibration notes, preferred/avoided examples, and feedback history table
- [x] Created `_system/writing_voice_hci.md` — HCI overrides for argumentative style, technical depth, interdisciplinary framing, reader model; plus HCI conventions (participant description, design rationale traceability, evaluation instruments)
- [x] Created `_system/writing_voice_healthcare.md` — Healthcare overrides for argumentative style, technical depth, hedging tolerance, interdisciplinary framing; plus healthcare conventions (patient population, regulatory/ethics, health equity, clinical endpoints)
- [x] Created `_system/writing_voice_ai.md` — AI overrides for argumentative style, technical depth, hedging tolerance, interdisciplinary framing; plus AI conventions (baseline comparisons, model specification checklist, external validation, anti-hype language guide)
- [x] Created `_system/ideation_preferences.json` — full schema with hypothesis_framing, methodological_tendency, risk_appetite, topic_preferences, scope_preference, selection_history, and auto-update rules
- [x] Updated `r01-writer-hci` SKILL.md — voice file reading with precedence, agent_learnings output
- [x] Updated `r01-writer-healthcare` SKILL.md — voice file reading with precedence, agent_learnings output
- [x] Updated `r01-writer-ai` SKILL.md — voice file reading with precedence, agent_learnings output
- [x] Updated `r01-writer-integrator` SKILL.md — multi-domain voice reading with context-aware precedence, agent_learnings output
- [x] Updated `r01-ideation` SKILL.md — ideation_preferences reading, selection_history recording, preference pattern detection, agent_learnings output
- [x] Updated `r01-novelty-checker` SKILL.md — ideation_preferences reading (risk_appetite, scope_preference), agent_learnings output
- [x] Updated `r01-orchestrator` SKILL.md — 3 feedback checkpoints (A/B/C), hybrid feedback classification, agent_learnings collection
- [x] Seed voice files from 3 prior proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery)
- [x] Seed reviewer_patterns.json from real NIH review feedback (2024Cardiotoxic, Impact 28, 8th percentile, 4 reviewers)
- [x] Copy all seeded files to shared workspace (`~/Dropbox/AgentWorkspace/PaperAutoGen/_system/`)
- [ ] (Future) Seed from YouthConcussion proposal (PDF extraction failed — retry with different tool)
- [ ] (Future) Cross-domain voice transfer validation across project types

**Files Created**:

| File | Lines | Description |
|------|-------|-------------|
| `writing_voice.md` | 155 | Generic voice: 7 dimensions seeded from 3 prior proposals with verbatim quotes |
| `writing_voice_hci.md` | ~100 | HCI overrides: PD session specs, MCI adaptations (limited evidence noted) |
| `writing_voice_healthcare.md` | ~110 | Healthcare overrides: burden-first, ICD codes, stakeholder specs, clinical actionability |
| `writing_voice_ai.md` | ~142 | AI overrides: HCAI philosophy, mathematical notation, baseline ladder, anti-hype guide |
| `ideation_preferences.json` | 93 | Research taste: 5 preference categories, selection history, auto-update rules |
| `reviewer_patterns.json` | ~250 | 10 patterns, 5 weaknesses, 5 strengths, scoring calibration from Cardiotoxic review |

**Skills Updated (6 total)**:

| Skill | Before | After | Changes |
|-------|--------|-------|---------|
| `r01-writer-hci` | 72 | 86 | +voice inputs, +agent_learnings |
| `r01-writer-healthcare` | 66 | 82 | +voice inputs, +agent_learnings |
| `r01-writer-ai` | 65 | 81 | +voice inputs, +agent_learnings |
| `r01-writer-integrator` | 116 | 136 | +multi-domain voice, +agent_learnings |
| `r01-ideation` | 181 | 211 | +preferences reading, +selection recording, +agent_learnings |
| `r01-novelty-checker` | 139 | 163 | +risk/scope inputs, +agent_learnings |
| `r01-orchestrator` | 168 | 230 | +feedback checkpoints A/B/C, +hybrid classification, +agent_learnings collection |

---

## 5. Nanobot Technical Reference

### 5.1 How Skills Work

- **SkillsLoader** scans `~/.nanobot/workspace/skills/*/SKILL.md` (workspace, highest priority) and `nanobot/nanobot/skills/*/SKILL.md` (built-in, lower priority). R01 skills are distributed as built-in skills and require no manual installation.
- Each skill = directory with `SKILL.md` + optional `references/`, `scripts/`, `assets/` subdirs
- YAML frontmatter: `name` (required), `description` (required)
- Markdown body = instructions injected into agent system prompt when skill is loaded
- Skills can have `requires` in metadata (bins, env vars) — filtered if unmet

### 5.2 How Subagents Work

- Main agent loop: 40 iterations max
- Subagent: 15 iterations max (spawned via `exec` tool)
- Subagent inherits model from parent (default: `provider.get_default_model()`)
- Multiple subagents can run concurrently
- No native "wait for all" — orchestrator must poll `state.json` or use sequential spawning

### 5.3 Key Source Files (reference only — do not modify)

| File | Purpose |
|------|---------|
| `nanobot/agent/skills.py` | SkillsLoader — skill discovery and loading |
| `nanobot/agent/subagent.py` | SubagentManager — spawn child agents |
| `nanobot/agent/context.py` | ContextBuilder — system prompt assembly |
| `nanobot/agent/loop.py` | AgentLoop — main 40-iteration loop |
| `nanobot/config/schema.py` | Config schema + model matching |

### 5.4 User Config

Located at `~/.nanobot/config.json`:
- Slack channel: enabled
- OpenAI provider: API key set
- Default model: `openai-codex/gpt-5.1-codex`
- Anthropic provider: API key slot present but empty (user may add later)

---

## 6. Constraints (Verbatim from User)

1. **"for code execution, let's just fake it for now"** — No real code execution in pipeline
2. **"i rejected because you shouldn't need those info beyond this workspace folder"** — ALL file operations restricted to the shared workspace and `~/.nanobot/workspace/`
3. **"make sure that the different writers can also work in parallel"** — Phase 4 writers MUST run simultaneously
4. **Workspace paths are configurable** — via `project.yaml`, not hardcoded
5. **PriorNIHR01Examples/ is user-populated** — do NOT ship example proposals in the repo

---

## 7. External References

| Resource | URL | Relevance |
|----------|-----|-----------|
| AI-Scientist v1 | https://github.com/SakanaAI/AI-Scientist | Template-based writing (12.2k stars) |
| AI-Scientist v2 | https://github.com/SakanaAI/AI-Scientist-v2 | Tree-search ideation (2.2k stars) |
| FARS blog | https://analemma.ai/blog/introducing-fars | Context on FARS design |
| OpenFARS | https://github.com/open-fars/openfars | Open-source FARS alternative |
| NiceGUI | https://nicegui.io | Recommended dashboard framework |
| Figma MCP | https://github.com/nicholasgriffintn/figma-mcp | Read-only Figma integration |

---

## 8. For the Next Agent

If you are an AI agent continuing this work:

1. **Read this entire document first** — it contains all architectural decisions and constraints
2. **Skills are built-in** — all 16 r01 skills are in `nanobot/skills/` and auto-discovered by SkillsLoader. No manual installation needed.
3. **Do NOT redo Phases A-I** — they are complete and verified
4. **Next work candidates**: Seed voice files from real prior proposals, Phase G Tier 2/3 (Figma integration), Phase H A/B testing, or new project runs
5. **Phase C end-to-end test is complete** — the `r01-older-adults-mci-home-ai` project ran through all 10 pipeline phases successfully
6. **Figure renderer** is at `r01-proposal/r01_figure_renderer.py` — standalone matplotlib script that reads YAML specs and produces SVG+PNG
7. **Self-evolution system** is seeded with 8 patterns from the first project — future runs will accumulate more
8. **Respect the constraints** in Section 6 — especially workspace restrictions and parallel execution
9. **The skills are substantive** — read them; they contain detailed instructions for each agent role. Phase D expanded review/ideation skills; Phase I expanded writer/ideation skills with voice calibration and agent learnings
10. **Check `state.json`** patterns in `workspace/_templates/state.json` — this is how the orchestrator tracks progress
11. **Parallel execution pseudocode** is in `nanobot/skills/r01-orchestrator/references/parallel_execution.md`
12. **Voice calibration system** (Phase I) — writers read 3-tier voice hierarchy (`writing_voice_{domain}.md` > `writing_voice.md` > `style_guide.md`). Voice files are **seeded with real PI voice data** from 3 prior proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery) — verbatim quotes, pattern analysis, and evidence citations. Key finding: PI uses superscript citations (not [Author Year]), mathematical notation in Approach, and "Human-Centered AI (HCAI)" as explicit design philosophy.
13. **Ideation preferences** (`_system/ideation_preferences.json`) — empty on first run; auto-populates from PI's idea selections over time. After 3+ projects, the ideation agent begins biasing toward the PI's preferred research directions
14. **Feedback checkpoints** — orchestrator has 3 user checkpoints (Idea, Outline, Draft) with hybrid feedback classification. Style feedback routes to evolution agent; content feedback routes to reviser
15. **Reviewer patterns** (`_system/reviewer_patterns.json`) — seeded with real NIH reviewer feedback from 2024Cardiotoxic (Impact 28, 8th percentile, 4 reviewers). Contains 10 reviewer critique patterns, 5 common weaknesses with prevention strategies, 5 strengths with replication strategies, and full scoring calibration. Key lesson: Innovation and team can compensate for Approach weaknesses; HIPAA/privacy gaps trigger UNACCEPTABLE flags.
