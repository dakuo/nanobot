# NIH R01 Project Template

Copy this entire `_templates/` folder to create a new project:
```
cp -r _templates/ project-YYYYMMDD-shortname/
```

Then edit `project.yaml` with your proposal details.

## Folder Structure

```
{project-name}/
├── project.yaml              # Project config (edit this first)
├── state.json                # Pipeline state machine (auto-managed)
├── cost.jsonl                # LLM cost tracking (append-only)
├── events.jsonl              # Audit log (append-only)
│
├── ideas/                    # Phase 1: Ideation
│   ├── ideas.json            # Scored hypothesis tree
│   └── selected_idea.json    # User-chosen direction
│
├── literature/               # Phase 2: Literature Review
│   ├── references.json       # Annotated bibliography
│   ├── gaps.md               # Gap analysis
│   └── search_log.json       # Search queries and results
│
├── docs/                     # Phase 3-4: Written Sections
│   ├── drafts/               # Versioned drafts
│   │   ├── specific_aims_v1.md
│   │   ├── significance_v1.md
│   │   ├── innovation_v1.md
│   │   ├── approach_aim1_v1.md
│   │   ├── approach_aim2_v1.md
│   │   ├── approach_aim3_v1.md
│   │   ├── project_narrative_v1.md
│   │   └── project_summary_v1.md
│   └── final/                # Assembled final documents
│       ├── research_strategy.md
│       ├── project_narrative.md
│       └── project_summary.md
│
├── figures/                  # Phase 5: Figures
│   ├── specs/                # Figure description YAML files
│   └── exports/              # Rendered PNG/SVG
│
├── budget/                   # Phase 6: Budget
│   ├── budget.xlsx
│   └── budget_justification.md
│
├── reviews/                  # Phase 7-8: Review + Revision
│   ├── review_hci_r1.json
│   ├── review_healthcare_r1.json
│   ├── review_ai_r1.json
│   ├── panel_summary_r1.json
│   └── revision_plan_r1.md
│
└── feedback/                 # Learning (user + real reviewer)
    ├── user_feedback_001.md
    └── nih_reviewer_feedback.md
```

## Pipeline Phases

| # | Phase | Agent(s) | Parallel? | User Checkpoint? |
|---|-------|----------|-----------|------------------|
| 0 | Init | orchestrator | - | - |
| 1 | Ideation | r01-ideation | - | Yes: pick idea |
| 2 | Literature | r01-literature | - | - |
| 3 | Outline | orchestrator | - | - |
| 4 | Writing | writer-hci/ai/healthcare/integrator | **Yes** | - |
| 5 | Figures | r01-figures | - | - |
| 6 | Budget | r01-budget | - | - |
| 7 | Review | reviewer-hci/ai/healthcare/panel | **Yes** | - |
| 8 | Revision | r01-reviser | - | - |
| 9 | Export | orchestrator | - | Yes: final review |
