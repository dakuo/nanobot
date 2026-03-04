---
name: r01-literature
description: "Conduct literature review for NIH R01 proposals using PubMed, Semantic Scholar, and web search. Builds annotated bibliography and identifies research gaps. Triggers: 'literature review', 'find papers', 'search references'."
---

# Mission
Build the evidence base for a human-centered AI R01 by collecting high-value references, annotating them for proposal use, and turning gaps into concrete Significance and Innovation arguments.

# Scope
- Work inside `~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/`.
- Cover HCI, healthcare, and AI literature, plus cross-domain translational work.
- Prefer peer-reviewed sources and authoritative preprints when necessary.

# Source Prioritization
1. PubMed for clinical evidence, outcomes, safety, and implementation.
2. Semantic Scholar for AI/ML and HCI breadth with citation context.
3. Web search for policy, standards, consortium reports, and recent updates.

# Query Strategy
- Start from selected hypothesis/aims in `ideas/ideas.json`.
- Build query packs by domain, then bridge queries that combine domains.
- Use Boolean templates with synonyms for population, intervention, and setting.
- Run iterative refinement: broad recall pass then precision pass.

# Volume and Recency Targets
- Collect 30-50 references total.
- Aim for majority published in the past 5 years.
- Keep foundational older papers only when they are field-defining.
- Balance domain coverage; avoid over-indexing one discipline.

# Annotation Standard
For each reference include:
- `id`
- `title`
- `authors`
- `year`
- `venue`
- `doi_or_url`
- `domain` (`hci`, `healthcare`, `ai`, `cross-domain`)
- `study_type` (trial, observational, systematic review, benchmark, methods)
- `key_findings` (1-3 sentences)
- `limitations` (1-2 sentences)
- `proposal_relevance` (1-2 sentences linked to aims)
- `priority` (`must-cite`, `supporting`, `optional`)

# Gap Identification Workflow
1. Group references by aim and domain.
2. Map evidence maturity: strong, mixed, sparse.
3. Identify methodological gaps (missing baselines, weak external validity, limited sample diversity).
4. Identify translational gaps (workflow mismatch, safety omissions, implementation barriers).
5. Identify measurement gaps (weak endpoints, short follow-up, absent user-centered metrics).

# Output Contract
- Write annotated bibliography to `literature/references.json`.
- Write ranked gap analysis to `literature/gaps.md`.

`gaps.md` structure:
1. `Top Gaps` (5-10 highest-impact gaps)
2. `HCI Gaps`
3. `Healthcare Gaps`
4. `AI Gaps`
5. `Cross-Domain Gaps`
6. `Implications for Aims`

# Evidence Rules
- Every claim in `gaps.md` must trace to one or more entries in `references.json`.
- Avoid uncited assertions and hype language.
- Flag contradictory findings explicitly for risk mitigation planning.

# Handoff to Writers
- Provide must-cite shortlist per aim.
- Mark references useful for Specific Aims page versus Approach detail.
- Highlight citation candidates for Significance and Innovation sections.

# Quality Bar
- 30-50 references achieved unless narrowly scoped by project constraints.
- Recent literature emphasis is clear and justified.
- Gaps are actionable and directly connected to proposal decisions.
- Outputs are clean JSON/Markdown and ready for orchestrator consumption.
