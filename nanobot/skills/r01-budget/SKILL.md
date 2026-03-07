---
name: r01-budget
description: "Budget generation agent for NIH R01 proposals. Creates modular budget table and detailed justification narrative. Triggers: invoked by orchestrator during budget phase."
---

# Mission
Generate a defensible NIH R01 budget package with transparent line items and justification aligned to aims, staffing, and operational requirements.

# Inputs
- Read all budget parameters from `project.yaml`.
- Read `project.yaml.investigators` for PI, co-investigator, and key personnel roster (names, roles, effort percentages, institutions). Use these to generate the personnel section with real names and roles rather than generic placeholders.
- Read `project.yaml.submission.budget_period_years` for the grant duration (default 5 years).
- Read `project.yaml.nih_context.foa.budget_ceiling` for the annual direct cost ceiling. If set, this is a **hard constraint** — annual direct costs MUST NOT exceed this value. If null, use the standard R01 modular budget ceiling of $500,000/year direct costs. Flag any budget that approaches within 5% of the ceiling.
- Read scope, milestones, and staffing assumptions from `docs/`.
- Read any existing budget artifacts in `budget/` before updating.

# Budget Structure
Produce modular categories:
- personnel
- equipment
- travel
- participant costs
- other direct costs
- indirect costs (F&A)

# Personnel Costing
- Map each role to aims and year-by-year effort.
- Use names and effort percentages from `project.yaml.investigators` when available. For each PI and co-investigator: use their actual name, institution, role, and effort_percent. For key_personnel: use their name and effort_percent.
- If investigator data is not available, use descriptive role titles (e.g., "PI", "Co-I, HCI Lead") and reasonable effort estimates.
- Include salary basis, effort fraction, and fringe assumptions.
- Distinguish key personnel from trainees and support staff.
- Explain role necessity in execution terms.

# Non-Personnel Costing
- Equipment: one-time items with utilization rationale.
- Travel: conferences, site coordination, and collaboration meetings.
- Participant costs: recruitment, compensation, retention support.
- Other direct: cloud compute, software, data access, compliance expenses.

# NIH Format Expectations
- Present annual and project-period totals.
- Keep direct and indirect calculations explicit.
- Use NIH-appropriate narrative tone in justifications.
- Avoid vague phrases like "general support".

# Output Contract
- Write table to `budget/budget_table.md`.
- Write narrative to `budget/budget_justification.md`.

`budget_table.md` should include:
- year columns (Year 1..Year N)
- category subtotals
- annual total direct, annual indirect, annual total cost
- cumulative project totals

`budget_justification.md` should include:
- personnel subsection by role
- non-personnel subsection by category
- alignment notes linking costs to aims and milestones
- assumption notes for pending values

# Validation Checklist
- Totals are arithmetically consistent.
- **Annual direct costs do not exceed `budget_ceiling` from project.yaml** (default $500K for standard R01). If they do, flag specific line items to reduce and provide alternatives.
- Costs align with proposed methods and timeline.
- Staffing levels match claimed workload.
- Participant and safety-related costs are not under-scoped.

# Quality Bar
- Budget is realistic for NIH R01 expectations.
- Justification is specific, necessity-based, and reviewer-ready.
- Outputs can be converted to institutional forms with minimal rework.
