# R01 Multi-Agent Proposal Auto-Generation System — Project Plan

> **Purpose**: This document is the single source of truth for any agent or developer continuing work on this system. It captures architecture decisions, what has been built, what remains, and all constraints. **Read this before doing anything.**

---

## 1. Project Goal

Build a **multiagent NIH R01 proposal auto-generation system** on top of nanobot that:

- Uses **14 specialized skills** (orchestrator, ideation, literature, 4 domain writers, 4 domain reviewers, reviser, figures, budget)
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
│       ├── reviewer_patterns.json   (71 lines — extracted reviewer feedback patterns)
│       ├── evolution_log.json       (44 lines — system self-evolution log)
│       └── r01_section_specs.md     (433 lines — detailed section specifications)

nanobot/skills/                      ← All 14 agent skills (built-in, distributed with package)
├── r01-orchestrator/
│   ├── SKILL.md                     (72 lines — state machine, parallel dispatch)
│   └── references/
│       ├── pipeline.md              (264 lines — all 10 phases detailed)
│       └── parallel_execution.md    (135 lines — parallel dispatch pseudocode)
├── r01-ideation/SKILL.md            (87 lines)
├── r01-literature/SKILL.md          (79 lines)
├── r01-writer-hci/SKILL.md          (72 lines)
├── r01-writer-healthcare/SKILL.md   (66 lines)
├── r01-writer-ai/SKILL.md           (65 lines)
├── r01-writer-integrator/SKILL.md   (60 lines)
├── r01-reviewer-hci/SKILL.md        (62 lines)
├── r01-reviewer-healthcare/SKILL.md (62 lines)
├── r01-reviewer-ai/SKILL.md         (63 lines)
├── r01-reviewer-panel/SKILL.md      (70 lines)
├── r01-reviser/SKILL.md             (61 lines)
├── r01-figures/SKILL.md             (73 lines)
└── r01-budget/SKILL.md              (66 lines)
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

All 14 skills created with proper YAML frontmatter (`name` + `description`) and substantive markdown bodies (60-87 lines each). Every skill is a complete instruction set — not a stub.

| Skill | Lines | Verified |
|-------|-------|----------|
| r01-orchestrator | 72 | Yes — state machine, parallel dispatch, user checkpoints |
| r01-orchestrator/references/pipeline.md | 264 | Yes — all 10 phases with entry/exit criteria |
| r01-orchestrator/references/parallel_execution.md | 135 | Yes — pseudocode for parallel writing + review |
| r01-ideation | 87 | Yes — tree-search, scoring rubric |
| r01-literature | 79 | Yes — PubMed/Semantic Scholar, 30-50 refs target |
| r01-writer-hci | 72 | Yes — HCI voice, CHI/CSCW venues |
| r01-writer-healthcare | 66 | Yes — clinical voice, NEJM/JAMA |
| r01-writer-ai | 65 | Yes — technical voice, NeurIPS/ICML |
| r01-writer-integrator | 60 | Yes — cross-domain merge, page budgets |
| r01-reviewer-hci | 62 | Yes — user study rigor, 1-9 scoring |
| r01-reviewer-healthcare | 62 | Yes — clinical feasibility, IRB |
| r01-reviewer-ai | 63 | Yes — technical soundness, baselines |
| r01-reviewer-panel | 70 | Yes — synthesis, impact score, proceed/revise |
| r01-reviser | 61 | Yes — targeted edits, feedback learning |
| r01-figures | 73 | Yes — matplotlib MVP, CONSORT diagrams |
| r01-budget | 66 | Yes — NIH budget format, justification |

### Phase C: End-to-End Test — IN PROGRESS

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

**Remaining**:
- [ ] Resume pipeline at literature phase and verify r01-literature subagent produces references.json + gaps.md
- [ ] Verify outline phase (r01-writer-integrator produces outline_v1.md)
- [ ] Verify parallel writer dispatch (Phase 5) spawns multiple subagents
- [ ] Verify parallel reviewer dispatch (Phase 7) works
- [ ] Verify revision loop (score < 5 → back to review)
- [ ] Fix any issues found during testing

### Phase D: Ideation Logic — NOT STARTED

**Goal**: Implement tree-search hypothesis generation (inspired by AI-Scientist v2 BFTS).

**Tasks**:
- [ ] Implement branching: generate 3-5 hypothesis branches per exploration
- [ ] Implement scoring: novelty (0-10), feasibility (0-10), NIH alignment (0-10)
- [ ] Read prior examples from PriorNIHR01Examples/ for inspiration
- [ ] Output to `ideas/ideas.json` with full scoring rubric
- [ ] Implement user checkpoint: present top ideas for selection

### Phase E: Literature Search — REDESIGNED (parallel, tool-level)

**Goal**: Three parallel domain literature agents (HCI, Healthcare, AI) using concrete web_search/web_fetch tool chains.

**Design Changes (implemented)**:
- [x] Rewrote `r01-literature` SKILL.md with concrete tool-level instructions (web_search, web_fetch, Semantic Scholar API)
- [x] Skill is now domain-parameterized — spawned per domain with `hci`, `healthcare`, or `ai` assignment
- [x] Added `literature_parallel` tracking to state.json (3 parallel entries)
- [x] Updated orchestrator to dispatch 3 literature agents simultaneously
- [x] Updated pipeline.md with parallel literature phase spec
- [x] Updated parallel_execution.md with literature dispatch pseudocode
- [x] Each agent writes `literature/references_{domain}.json` + `literature/gaps_{domain}.md`
- [x] Merge step combines into `literature/references.json` + `literature/gaps.md` with dedup

**Remaining**:
- [ ] Verify parallel literature dispatch works end-to-end
- [ ] Verify merge/dedup produces clean combined output
- [ ] Validate that 30-50 real references are collected across domains

### Phase F: Web Dashboard — COMPLETE (MVP)

**Goal**: NiceGUI-based dashboard for monitoring pipeline progress and costs.

**Completed**:
- [x] Set up NiceGUI app (`r01-proposal/dashboard/`)
- [x] `state_reader.py` — data layer reads state.json and cost.json
- [x] Pipeline progress view — phase status cards, circular progress, parallel task expansion
- [x] Cost tracking view — per-phase and per-agent tables
- [x] Event timeline — chronological event log with icons and color-coding
- [x] Real-time updates — 3-second polling timer with toggle switch
- [x] Multi-project support — left drawer lists all projects, click to switch
- [x] Dark theme with Material Design icons

**Run**: `python r01-proposal/dashboard/main.py` → http://localhost:8090

### Phase G: Figma Integration — NOT STARTED

**Goal**: Bidirectional figure sync (MVP: matplotlib only; future: Figma MCP).

**Tasks**:
- [ ] **Tier 1 (MVP)**: matplotlib figure generation from YAML specs
- [ ] Figure types: system architecture, CONSORT flowchart, data pipeline, conceptual framework
- [ ] Export to PNG + SVG in `figures/exports/`
- [ ] Auto-generate captions
- [ ] **Tier 2 (Future)**: Figma MCP read integration (pull design tokens)
- [ ] **Tier 3 (Future)**: Figma write bridge (WebSocket + plugin for pushing updates)

### Phase H: Self-Evolution — NOT STARTED

**Goal**: System learns from feedback and improves over time.

**Tasks**:
- [ ] After each project: r01-reviser extracts patterns into `_system/reviewer_patterns.json`
- [ ] User feedback (Slack or feedback files) → style_guide.md updates
- [ ] Real NIH reviewer feedback → reviewer_patterns.json + evolution_log.json
- [ ] Track what changed, why, which project triggered it
- [ ] Eventually: automated A/B testing of writing strategies

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
2. **Skills are built-in** — all 14 r01 skills are in `nanobot/skills/` and auto-discovered by SkillsLoader. No manual installation needed.
3. **Do NOT redo Phases A or B** — they are complete and verified
4. **Continue Phase C** — init, ideation, and state alignment are done. Resume at the literature phase for the `r01-older-adults-mci-home-ai` project.
5. **Respect the constraints** in Section 6 — especially workspace restrictions and parallel execution
6. **The skills are substantive** — read them; they contain detailed instructions for each agent role
7. **Check `state.json`** patterns in `workspace/_templates/state.json` — this is how the orchestrator tracks progress
8. **Parallel execution pseudocode** is in `nanobot/skills/r01-orchestrator/references/parallel_execution.md`
