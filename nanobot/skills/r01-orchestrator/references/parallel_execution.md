# Parallel Execution Reference

This document defines how `r01-orchestrator` runs parallel branches with nanobot subagents.

## Parallel Dispatch Model
- Orchestrator creates a task record per parallel unit in `state.json`.
- Orchestrator spawns multiple subagents in one dispatch wave.
- Orchestrator polls task state and updates status fields as results return.
- Orchestrator performs fan-in only when all required tasks are `complete`.

Nanobot execution assumption:
- The main agent has built-in subagent spawning capability.
- No custom API is introduced; orchestration uses the existing subagent mechanism.

## State Tracking Convention
Use two phase-level maps in `state.json`:

```json
{
  "writing_parallel": {
    "specific_aims": {"agent": "r01-writer-integrator", "status": "pending", "attempt": 0},
    "approach_aim1": {"agent": "r01-writer-hci", "status": "pending", "attempt": 0},
    "approach_aim2": {"agent": "r01-writer-ai", "status": "pending", "attempt": 0},
    "approach_aimN": "... populated dynamically from project.yaml aims[]"
  },
  "review_parallel": {
    "review_hci": {"agent": "r01-reviewer-hci", "status": "pending", "attempt": 0},
    "review_ai": {"agent": "r01-reviewer-ai", "status": "pending", "attempt": 0}
  }
}
```

Status values:
- `pending`: task defined, not started
- `running`: subagent spawned and in progress
- `complete`: output validated and accepted
- `failed`: subagent returned error or invalid output

## Pseudocode: Phase 3 Parallel Literature Dispatch
```python
state = read_json("state.json")
cfg = read_yaml("project.yaml")

domains = cfg["domain_tags"]  # ["hci", "healthcare", "ai"]

for domain in domains:
    state["literature_parallel"][domain] = {"agent": "r01-literature", "status": "pending", "attempt": 0}
write_json("state.json", state)

MAX_LITERATURE_RETRIES = 3  # hard cap — same broken strategy won't fix itself

for domain in domains:
    spawn_subagent(
        skill="r01-literature",
        task=(
            f"You are the {domain} literature agent. "
            f"Read the r01-literature skill and follow its instructions. "
            f"Your domain assignment is: {domain}. "
            f"Project path: ~/Dropbox/AgentWorkspace/PaperAutoGen/{{project}}/. "
            f"Find 10-18 references for the {domain} domain. "
            f"Write to literature/references_{domain}.json and literature/gaps_{domain}.md."
        ),
    )
    state["literature_parallel"][domain]["status"] = "running"
    state["literature_parallel"][domain]["attempt"] += 1
    write_json("state.json", state)
    append_event("state.json", {"event": "literature_spawn", "domain": domain, "attempt": state["literature_parallel"][domain]["attempt"]})

while not all_complete("literature_parallel"):
    update_from_results("literature_parallel")
    if any_failed("literature_parallel"):
        for domain, entry in state["literature_parallel"].items():
            if entry["status"] == "failed":
                if entry["attempt"] >= MAX_LITERATURE_RETRIES:
                    entry["status"] = "blocked"
                    append_event("state.json", {"event": "literature_blocked", "domain": domain, "attempt": entry["attempt"], "reason": "max retries exceeded"})
                else:
                    retry_failed("literature_parallel", domain)  # re-spawn only this domain
                    entry["attempt"] += 1
                    entry["status"] = "running"
                    append_event("state.json", {"event": "literature_retry", "domain": domain, "attempt": entry["attempt"]})
        write_json("state.json", state)
    if any_blocked("literature_parallel"):
        mark_phase("literature", "blocked")
        request_user_intervention("Literature agent(s) failed after max retries. Check events.jsonl for details.")
        break

# Merge phase: combine domain outputs
all_refs = []
for domain in domains:
    refs = read_json(f"literature/references_{domain}.json")
    all_refs.extend(refs)

# Deduplicate by DOI/URL
merged = deduplicate_by_doi_or_url(all_refs)
write_json("literature/references.json", merged)

# Merge gap analyses
gaps_parts = []
for domain in domains:
    gaps_parts.append(read_file(f"literature/gaps_{domain}.md"))
write_file("literature/gaps.md", merge_gap_sections(gaps_parts))
```

## Pseudocode: Phase 5 Parallel Writing Dispatch
```python
state = read_json("state.json")
cfg = read_yaml("project.yaml")
project_path = "~/Dropbox/AgentWorkspace/PaperAutoGen/{project}"

# --- Build aim map dynamically from project.yaml ---
aims = cfg["aims"]  # list of N aims (2-4 typically)
aim_map = {}
for i, aim in enumerate(aims, start=1):
    aim_map[f"aim{i}"] = aim["domain_tag"]  # e.g. {"aim1": "hci", "aim2": "ai", "aim3": "healthcare", "aim4": "hci"}

model_overrides = cfg["model_config"]["overrides"]

# --- Define batches: 1 integrator batch (A) + N aim batches + 1 assembly batch (E) ---

batch_a = {
    "label": "integrator-framing",
    "skill": "r01-writer-integrator",
    "sections": {
        "specific_aims":  {"word_target": 500,  "output": "docs/drafts/specific_aims_v1.md"},
        "significance":   {"word_target": 1500, "output": "docs/drafts/significance_v1.md"},
        "innovation":     {"word_target": 1000, "output": "docs/drafts/innovation_v1.md"},
    },
}

# Generate one batch per aim dynamically
aim_batches = []
for aim_key, domain in aim_map.items():
    aim_num = aim_key.replace("aim", "")
    page_budget = aims[int(aim_num) - 1].get("page_budget", 3)
    word_target = page_budget * cfg["word_count_targets"]["words_per_page"]
    aim_batches.append({
        "label": f"writer-{domain}-{aim_key}",
        "skill": f"r01-writer-{domain}",
        "sections": {
            f"approach_{aim_key}": {"word_target": word_target, "output": f"docs/drafts/approach_{aim_key}_v1.md"},
        },
    })

# --- Populate state.json with dynamic aim entries ---
for aim_key, domain in aim_map.items():
    state["writing_parallel"][f"approach_{aim_key}"] = {
        "agent": f"r01-writer-{domain}",
        "status": "pending",
        "attempt": 0,
        "word_count": 0,
        "draft_version": 0,
    }

# --- Mark all batch A + aim batches as running ---
all_parallel_batches = [batch_a] + aim_batches
for batch in all_parallel_batches:
    for section in batch["sections"]:
        state["writing_parallel"][section]["status"] = "running"
        state["writing_parallel"][section]["attempt"] += 1
write_json("state.json", state)

# --- Spawn batch A + all aim batches simultaneously ---
for batch in all_parallel_batches:
    skill_name = batch["skill"]
    skill_path = find_skill_path(skill_name)
    model = model_overrides.get(skill_name, cfg["model_config"]["default_model"])

    section_specs = "\n".join(
        f"  - {name}: {info['word_target']} words → {info['output']}"
        for name, info in batch["sections"].items()
    )

    spawn(
        label=batch["label"],
        max_iterations=30,
        model=model,
        task=f"""You are a writing subagent. Read the {skill_name} skill at {skill_path} and follow its instructions.

PROJECT: {project_path}
SECTIONS TO WRITE:
{section_specs}

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
4. Read 1-2 prior examples from PriorNIHR01Examples/ for NIH voice calibration.
5. Write each section to its output file. Use markdown with proper heading hierarchy.
6. Each section MUST meet its word target (±10%).
7. Cite references using [AuthorYear] format matching refs.json entries.
8. Do NOT modify state.json — the orchestrator handles tracking.""",
    )

# --- Wait for all parallel batches to complete ---
# The orchestrator receives completion notifications via message bus.
# On each notification, mark the batch's sections as "complete" in state.json.
# When all batches are complete, proceed to assembly.

# --- Spawn batch E: assembly (after all parallel batches complete) ---
for section in ["approach_timeline", "approach_crosscutting", "project_narrative", "project_summary"]:
    state["writing_parallel"][section]["status"] = "running"
    state["writing_parallel"][section]["attempt"] += 1
write_json("state.json", state)

integrator_model = model_overrides.get("r01-writer-integrator", cfg["model_config"]["default_model"])
integrator_skill_path = find_skill_path("r01-writer-integrator")

# Build dynamic aim list for assembly prompt
aim_file_list = ", ".join(f"approach_{aim_key}" for aim_key in aim_map)

spawn(
    label="integrator-assembly",
    max_iterations=30,
    model=integrator_model,
    task=f"""You are the integration writer. Read the r01-writer-integrator skill at {integrator_skill_path} and follow its instructions.

PROJECT: {project_path}

PHASE 1 — Write remaining sections:
- approach_timeline: 300 words → docs/drafts/approach_timeline_v1.md
- approach_crosscutting: 300 words → docs/drafts/approach_crosscutting_v1.md
- project_narrative: 1 sentence → docs/drafts/project_narrative_v1.md
- project_summary: 30 lines → docs/drafts/project_summary_v1.md

PHASE 2 — Merge all section drafts into a single document:
- Read ALL files in docs/drafts/ (specific_aims, significance, innovation, {aim_file_list}, timeline, crosscutting)
- Merge into docs/drafts/research_strategy_v1.md following NIH section order
- Resolve terminology conflicts across domain writers
- Ensure one coherent voice, no duplicated background text
- Verify total Research Strategy is within 15-page budget (~7500 words)

REQUIRED INPUTS:
- Project config: {project_path}/project.yaml
- Proposal outline: {project_path}/docs/outline.md
- All section drafts: {project_path}/docs/drafts/*.md
- Literature: {project_path}/literature/refs.json and {project_path}/literature/gaps.md
- Selected idea: {project_path}/ideas/ideas.json
- Style guide: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/style_guide.md
- Section specs: ~/Dropbox/AgentWorkspace/PaperAutoGen/_system/r01_section_specs.md

Do NOT modify state.json — the orchestrator handles tracking.""",
)

# On completion: mark all remaining sections + writing_integration as "complete"
```

## Pseudocode: Phase 7 Parallel Review Dispatch
```python
reviewers = {
    "review_hci": "r01-reviewer-hci",
    "review_healthcare": "r01-reviewer-healthcare",
    "review_ai": "r01-reviewer-ai",
}

for name, agent in reviewers.items():
    state["review_parallel"][name] = {"agent": agent, "status": "pending", "attempt": 0}
write_json("state.json", state)

for name, agent in reviewers.items():
    spawn_subagent(skill=agent, task="Review full research_strategy draft from domain lens")
    mark_status("review_parallel", name, "running")

while not all_complete("review_parallel"):
    update_from_results("review_parallel")
    if any_failed("review_parallel"):
        retry_failed("review_parallel")

spawn_subagent(skill="r01-reviewer-panel", task="Synthesize 3 domain reviews; output impact score 1-9")
panel = wait_for_panel_result()

if panel.score < 5 and state["review_round"] < state["max_review_rounds"]:
    route_to_phase("revision")
else:
    route_to_phase("export")
```

## Partial Failure Handling
- If one writer/reviewer/literature agent fails, keep successful outputs and statuses unchanged.
- Mark failed task `failed`, increment `attempt`, append structured failure event to `events` array in `state.json`.
- Retry only failed task(s), not the entire parallel batch.
- **Max retries per task: 3** (configurable via `MAX_LITERATURE_RETRIES`, `MAX_WRITING_RETRIES`, `MAX_REVIEW_RETRIES`). After 3 failed attempts with the same strategy, mark the task `blocked` and request user intervention — repeating the same approach will not produce a different result.
- If any task is `blocked`, mark the phase `blocked` and notify the user with the failure reason from `events`.

## Cost Tracking During Parallel Execution
- Every subagent completion appends one line to `cost.jsonl` with `timestamp`, `phase`, `agent`, `task`, `attempt`, and `cost`.
- Costs are appended per task completion; do not wait for branch fan-in.
- Fan-in/phase transition still requires all required tasks to reach `complete`.
