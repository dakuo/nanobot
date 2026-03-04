# R01 Multi-Agent Proposal System — Setup Guide

A multiagent NIH R01 proposal auto-generation system built on [nanobot](https://github.com/HKUDS/nanobot). Uses 14 specialized AI agents with parallel domain writers and reviewers to generate complete R01 proposals for human-centered AI in healthcare research.

## Quick Setup

### 1. Install Skills

Copy the R01 skills into your nanobot workspace:

```bash
# From the repo root
cp -r r01-proposal/skills/r01-* ~/.nanobot/workspace/skills/
```

Verify they're discoverable:

```bash
nanobot status
# Should list all 14 r01-* skills
```

### 2. Set Up Shared Workspace

Create the shared workspace directory (default path — configurable per project):

```bash
# Create workspace structure
mkdir -p ~/Dropbox/AgentWorkspace/PaperAutoGen
mkdir -p ~/Dropbox/AgentWorkspace/PriorNIHR01Examples

# Copy templates and system files
cp -r r01-proposal/workspace/_templates ~/Dropbox/AgentWorkspace/PaperAutoGen/
cp -r r01-proposal/workspace/_system ~/Dropbox/AgentWorkspace/PaperAutoGen/
```

> **Custom paths**: If you don't use `~/Dropbox/AgentWorkspace/`, edit the paths in `project.yaml` — the system reads paths from config, not hardcoded.

### 3. Add Prior Examples (Optional but Recommended)

Place 2-3 of your prior R01 proposals in:

```
~/Dropbox/AgentWorkspace/PriorNIHR01Examples/
```

These are used by writers and ideation agents for style learning and inspiration. The system works without them but produces better output with examples.

### 4. Create a New Project

```bash
# Create project folder
mkdir -p ~/Dropbox/AgentWorkspace/PaperAutoGen/my-first-project

# Copy templates
cp ~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/project.yaml \
   ~/Dropbox/AgentWorkspace/PaperAutoGen/my-first-project/
cp ~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/state.json \
   ~/Dropbox/AgentWorkspace/PaperAutoGen/my-first-project/
cp ~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/cost.jsonl \
   ~/Dropbox/AgentWorkspace/PaperAutoGen/my-first-project/
cp ~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/events.jsonl \
   ~/Dropbox/AgentWorkspace/PaperAutoGen/my-first-project/

# Edit project.yaml with your research topic, aims, team info, etc.
```

### 5. Run the Pipeline

Tell nanobot to start (via CLI or Slack):

```
Start R01 pipeline for my-first-project
```

The orchestrator will guide the pipeline through all 10 phases.

## Architecture

```
14 Agents → 10 Pipeline Phases → 1 Complete R01 Proposal

Phase 1: init              → orchestrator sets up project
Phase 2: ideation          → tree-search hypothesis generation
Phase 3: literature        → PubMed + Semantic Scholar search
Phase 4: writing           → 4 writers IN PARALLEL (HCI, Healthcare, AI, Integrator)
Phase 5: outline_review    → user checkpoint
Phase 6: figures + budget  → figure generation + budget justification
Phase 7: review            → 3 reviewers IN PARALLEL → panel synthesis
Phase 8: revision          → targeted edits from feedback
Phase 9: export            → final assembly
Phase 10: (loop)           → back to review if score < 5
```

## Configuration

### project.yaml

Each project's `project.yaml` controls:

- **Research topic, title, aims** — the core content
- **Aim-to-domain mapping** — which domain writer leads each aim (hci, healthcare, ai)
- **Page budgets** — per-section page limits (default: 15 pages total for Research Strategy)
- **Model overrides** — use different LLMs for different agents
- **Parallel settings** — enable/disable parallel writing and review
- **Workspace paths** — shared workspace root, prior examples path

### Workspace Paths

Default paths (override in `project.yaml`):

| Path | Purpose |
|------|---------|
| `~/Dropbox/AgentWorkspace/PaperAutoGen/` | Shared workspace root |
| `~/Dropbox/AgentWorkspace/PriorNIHR01Examples/` | Prior proposals for few-shot learning |
| `~/.nanobot/workspace/skills/r01-*/` | Agent skills (installed in step 1) |

## Project Status

See [PLAN.md](./PLAN.md) for the full project plan, architecture decisions, and phase status.

**Completed**: Phase A (workspace schema) + Phase B (14 skills)
**Next**: Phase C (end-to-end test)

## Skills Reference

| Skill | Role |
|-------|------|
| `r01-orchestrator` | Central pipeline controller — state machine, parallel dispatch |
| `r01-ideation` | Tree-search hypothesis generation with scoring |
| `r01-literature` | PubMed + Semantic Scholar literature review |
| `r01-writer-hci` | HCI domain writer (CHI/CSCW voice) |
| `r01-writer-healthcare` | Healthcare domain writer (clinical/regulatory voice) |
| `r01-writer-ai` | AI/ML domain writer (NeurIPS/ICML voice) |
| `r01-writer-integrator` | Cross-domain synthesis + final assembly |
| `r01-reviewer-hci` | Simulated HCI reviewer (user study rigor) |
| `r01-reviewer-healthcare` | Simulated healthcare reviewer (clinical feasibility) |
| `r01-reviewer-ai` | Simulated AI/ML reviewer (technical soundness) |
| `r01-reviewer-panel` | Study section panel synthesizer (overall impact score) |
| `r01-reviser` | Targeted revision from reviewer/user feedback |
| `r01-figures` | Research-grade figure generation (matplotlib MVP) |
| `r01-budget` | NIH budget table + justification narrative |
