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
| ideation | `r01-ideation` |
| literature | `r01-literature` |
| outline | `r01-writer-integrator` |
| writing | `r01-writer-integrator` + domain writers |
| figures | `r01-figures` |
| budget | `r01-budget` |
| review | `r01-reviewer-hci`, `r01-reviewer-healthcare`, `r01-reviewer-ai`, `r01-reviewer-panel` |
| revision | `r01-reviser` |
| export | orchestrator |

See `references/pipeline.md` for full phase contracts and transitions.

# Parallel Writing Dispatch (Phase 4)
1. Read `project.yaml` -> get aim-to-domain mapping.
2. Populate `state.json.writing_parallel` with domain leads from `project.yaml`.
3. Spawn all writers simultaneously using nanobot's subagent capability:
   - `r01-writer-integrator` for: `specific_aims`, `significance`, `innovation`, `project_narrative`, `project_summary`
   - `r01-writer-{aim.domain_lead}` for: `approach_aim1`, `approach_aim2`, `approach_aim3`
   - `r01-writer-integrator` for: `approach_timeline`, `approach_crosscutting`
4. Each writer reads prior examples from `PriorNIHR01Examples/` for style.
5. Each writer writes output to `docs/drafts/{section}_v{N}.md`.
6. Track completion by updating `state.json.writing_parallel.{task}.status`.
7. When all parallel tasks show status `complete`:
   - Spawn `r01-writer-integrator` for merge pass.
   - Output `docs/drafts/research_strategy_v1.md`.

# Parallel Review Dispatch (Phase 7)
1. Spawn 3 domain reviewers in parallel:
   - `r01-reviewer-hci`
   - `r01-reviewer-healthcare`
   - `r01-reviewer-ai`
2. Each reviews the full research strategy draft from their domain lens.
3. When all 3 complete, spawn `r01-reviewer-panel` to synthesize.
4. Panel produces overall impact score (1-9) and summary.
5. If score `< 5` and `review_round < max_review_rounds`, route to Phase 8 (revision).

# User Checkpoints
- After ideation, pause for user idea selection.
- After export, pause for final user review.
- At each checkpoint, post to Slack and wait for explicit user confirmation.

# State Management
- Always read `state.json` before dispatching or transitioning phases.
- Write phase/task updates atomically in `state.json`.
- Append lifecycle events to `events.jsonl` (`spawned`, `completed`, `failed`, `checkpoint_wait`, `checkpoint_resumed`).
- Append per-agent cost entries to `cost.jsonl` after each subagent completion.
- Treat `events.jsonl` and `cost.jsonl` as append-only ledgers.

# Workspace Constraint
- All file operations are restricted to `~/Dropbox/AgentWorkspace/` and `~/.nanobot/workspace/`.
- Never access files outside these two roots.

# References
- `references/pipeline.md`
- `references/parallel_execution.md`
