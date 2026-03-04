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
    "approach_aim1": {"agent": "r01-writer-hci", "status": "pending", "attempt": 0}
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
    mark_status("literature_parallel", domain, "running")

while not all_complete("literature_parallel"):
    update_from_results("literature_parallel")
    if any_failed("literature_parallel"):
        retry_failed("literature_parallel")

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

## Pseudocode: Phase 4 Parallel Writing Dispatch
```python
state = read_json("state.json")
cfg = read_yaml("project.yaml")

aim_map = cfg["aim_to_domain"]  # e.g., aim1->hci, aim2->ai, aim3->healthcare

tasks = {
    "specific_aims": "r01-writer-integrator",
    "significance": "r01-writer-integrator",
    "innovation": "r01-writer-integrator",
    "project_narrative": "r01-writer-integrator",
    "project_summary": "r01-writer-integrator",
    "approach_aim1": f"r01-writer-{aim_map['aim1']}",
    "approach_aim2": f"r01-writer-{aim_map['aim2']}",
    "approach_aim3": f"r01-writer-{aim_map['aim3']}",
    "approach_timeline": "r01-writer-integrator",
    "approach_crosscutting": "r01-writer-integrator",
}

for section, agent in tasks.items():
    state["writing_parallel"][section] = {"agent": agent, "status": "pending", "attempt": 0}
write_json("state.json", state)

for section, agent in tasks.items():
    spawn_subagent(
        skill=agent,
        task=(
            f"Read PriorNIHR01Examples/ for style, then write {section} "
            f"to docs/drafts/{section}_v{{N}}.md"
        ),
    )
    mark_status("writing_parallel", section, "running")

while not all_complete("writing_parallel"):
    update_from_results("writing_parallel")
    if any_failed("writing_parallel"):
        retry_failed("writing_parallel")

spawn_subagent(skill="r01-writer-integrator", task="Merge sections into docs/drafts/research_strategy_v1.md")
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
- If one writer/reviewer fails, keep successful outputs and statuses unchanged.
- Mark failed task `failed`, increment `attempt`, append structured failure event.
- Retry only failed task(s), not the entire parallel batch.
- If retries exceed configured limit, mark phase blocked and request user intervention.

## Cost Tracking During Parallel Execution
- Every subagent completion appends one line to `cost.jsonl` with `timestamp`, `phase`, `agent`, `task`, `attempt`, and `cost`.
- Costs are appended per task completion; do not wait for branch fan-in.
- Fan-in/phase transition still requires all required tasks to reach `complete`.
