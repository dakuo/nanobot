---
name: reviewer-panel
description: "Study section panel synthesizer for simulated NIH review. Reads all domain reviewer reports, simulates multi-persona panel discussion, and produces per-dimension NIH scores, a revision priority matrix, and a findings memory entry. Triggers: invoked by orchestrator after all domain reviews complete."
---

# Document Type Awareness
Read `project.yaml.document_type` before starting. This skill operates in two modes:
- **R01 mode** (`document_type: "r01"`): NIH study section conventions. Score on NIH 1-9 scale.
- **Paper mode** (`document_type: "paper"`): Academic peer review conventions. Score on venue-appropriate scale. Read `project.yaml.venue` for the target venue.

Sections marked `### For R01 Proposals` apply ONLY in R01 mode. Sections marked `### For Academic Papers` apply ONLY in paper mode. Unmarked sections apply to BOTH modes.

# Mission
Simulate a full NIH study section discussion across three domain reviewers. Synthesize their reports into a defensible overall impact score, a revision priority matrix, and a structured findings memory entry. The panel does not average scores — it deliberates.

# Required Inputs
- `reviews/review_hci_r{N}.json` (must include `nih_dimensions` or `venue_dimensions`, `background_findings`, `review_confidence`)
- `reviews/review_healthcare_r{N}.json` (same fields)
- `reviews/review_ai_r{N}.json` (same fields)
- `ideas/findings_memory.json` (prior rounds, if round > 1)
- `project.yaml` → `investigators` section (PI track record, co-investigator expertise, effort allocations)
- Current proposal snapshot in `docs/` for conflict resolution

### For Academic Papers
Also read from `project.yaml`:
- `venue`: target venue (CHI, CSCW, UIST, UbiComp, DIS)
- `contribution_type`: declared contribution type (empirical, artifact, methodological, theoretical, survey, opinion, benchmark)

# Synthesis Workflow

## Step 1: Parse Domain Reviews
Read all three domain JSONs. Extract from each:
- Per-dimension scores (`nih_dimensions`: significance, investigator, innovation, approach, environment)
- Top strengths and weaknesses
- `background_findings` (what the reviewer found in literature)
- `review_confidence` (how certain the reviewer is)
- `reflection_rounds_used` (how many self-critique passes the reviewer ran)

## Step 2: Identify Convergence and Disagreement
- **Convergent strengths**: praised by 2+ reviewers with overlapping evidence
- **Convergent weaknesses**: flagged by 2+ reviewers, especially across different domains
- **Disagreements**: one reviewer praises what another flags; document the evidence basis for each side

## Step 3: Study Section Discussion Simulation
Use a `<THOUGHT>` scratchpad to simulate 3-4 panelist voices before writing any output. Only the `<OUTPUT>` block is parsed downstream.

### For R01 Proposals: NIH Panelists

**Panelist personas:**

- **Panelist A (Senior Methodologist)**: Focuses on rigor, reproducibility, statistical power, and whether the approach section holds up to scrutiny. Skeptical of underpowered designs and vague operationalization.
- **Panelist B (Clinical Champion)**: Focuses on patient impact, translational potential, and whether the intervention could realistically reach a clinical setting. Asks "who benefits and when?"
- **Panelist C (Innovation Advocate)**: Focuses on novelty and scientific significance. Asks whether this advances the field or repackages existing work. Champions paradigm-shifting ideas even when methods are imperfect.
- **Panelist D (Devil's Advocate, optional)**: Challenges assumptions that the other panelists accept. Probes for hidden weaknesses, conflicts of interest in the framing, or gaps the proposal glosses over.

### For Academic Papers: Peer Review Panelists

**Panelist personas:**

- **Panelist A (Domain Expert)**: Evaluates technical depth and domain contribution. Asks whether the paper advances domain knowledge and whether the claims are supported by the evidence. Checks that the contribution is positioned correctly against prior work.
- **Panelist B (Methodology Expert)**: Evaluates research design rigor and validity. Checks statistical methods, study design, threat-to-validity analysis, and whether conclusions follow from the data. For AI papers, checks baselines and ablations. For qualitative papers, checks coding rigor.
- **Panelist C (Presentation Expert)**: Evaluates writing quality, clarity, figure quality, and overall readability. Checks whether the paper tells a coherent story, whether figures are informative and well-designed, and whether the structure matches venue conventions.
- **Panelist D (Impact Advocate)**: Evaluates broader significance and novelty. Asks whether this work will influence future research or practice, whether the contribution is timely, and whether the implications are clearly articulated.

Each panelist contributes 2-3 sentences of perspective. The panel then converges on a consensus score through discussion, not arithmetic. If panelists disagree on a dimension, the discussion must resolve it explicitly before a score is assigned.

**Scratchpad format:**
```
<THOUGHT>
Panelist A: [2-3 sentences on rigor and approach]
Panelist B: [2-3 sentences on clinical impact]
Panelist C: [2-3 sentences on innovation and significance]
Panelist D: [2-3 sentences challenging assumptions, if warranted]

Panel convergence: [1-2 sentences on how the discussion resolved disagreements and landed on a score]
</THOUGHT>
```

### For R01 Proposals: NIH Dimensions

## Step 4: Score Each NIH Dimension
After the discussion, assign a score (1-9, lower is better) to each dimension:
- **Significance**: Does the problem matter? Is the gap real?
- **Investigator**: Does the team have the track record and expertise? Read `project.yaml.investigators` for PI and co-investigator details (name, institution, expertise, scholar_id). If investigator data is available, evaluate: (a) does the PI have prior publications in this domain? (b) do co-investigators cover all required disciplines (HCI, clinical, AI)? (c) are effort allocations realistic for the proposed work? If investigator data is missing, score based solely on what the proposal narrative claims about the team, and note this limitation.
- **Innovation**: Does this advance beyond current approaches?
- **Approach**: Is the design rigorous, feasible, and well-powered?
- **Environment**: Does the setting support the work?

These are not averaged into the overall impact score. They inform it.

### For Academic Papers: Venue Dimensions

## Step 4: Score Each Venue Dimension
After the discussion, assign a score (1-5, where 5 is best) to each dimension:
- **Significance**: Does this meaningfully advance the field? Is the problem important?
- **Originality**: Is the approach novel relative to prior work?
- **Research Quality**: Are methods sound, well-executed, and appropriately validated?
- **Presentation**: Is the paper well-written, well-organized, with clear figures?
- **Prior Work**: Does the related work section adequately position this contribution?

**Contribution-type-specific weighting** — weight dimensions according to the declared `contribution_type`:
- **Empirical**: Research Quality weighted highest (rigorous study design and analysis are paramount)
- **Artifact**: Originality and Significance weighted highest (novel system with clear value)
- **Methodological**: Originality and Research Quality weighted highest (new method must be validated)
- **Theoretical**: Originality and Significance weighted highest (conceptual clarity and grounding)
- **Survey**: Prior Work and Presentation weighted highest (comprehensive coverage, clear synthesis)
- **Benchmark**: Research Quality and Significance weighted highest (reproducible, meaningful comparisons)

These weights influence the overall recommendation but do not override it mechanically.

### For R01 Proposals

## Step 5: Overall Impact Score
The overall impact score (1-9) reflects holistic panel judgment. Rules:
- A critical flaw in any single domain (especially Approach) can pull the score down regardless of other dimension scores.
- A proposal with strong Significance and Innovation but weak Approach should not score better than 3.
- Provide a narrative rationale of 3-5 sentences explaining the score, not just restating the dimensions.

### For Academic Papers: Overall Recommendation

## Step 5: Overall Recommendation
Use the recommendation scale: **Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject / Strong Reject**

Decision logic:
- **`accept`**: Strengths are clear, no critical flaws, recommendation is Accept or stronger. Paper makes a solid contribution to the venue.
- **`minor_revision`**: Minor issues only, recommendation is Weak Accept, issues are fixable in camera-ready. No fundamental problems with the contribution.
- **`major_revision`**: Significant issues but paper has merit, recommendation is Borderline or Weak Reject, R&R (revise and resubmit) is appropriate. Core contribution is sound but execution needs work.
- **`reject`**: Fundamental problems, recommendation is Reject or stronger. Contribution is unclear, methods are flawed, or paper is not ready for the venue.

Provide a narrative rationale of 3-5 sentences explaining the recommendation, referencing specific dimension scores and panelist perspectives.

## Step 6: Score Trajectory (Round > 1)
If this is round 2 or later, compare to the prior round's score from `ideas/findings_memory.json`:
- Note the score change (improved, declined, unchanged)
- Identify what specifically drove the change
- Flag any recurring issues that were not addressed

## Step 7: Revision Priority Matrix
Classify each recommended revision into a 2x2 matrix:
- **Impact**: high (would materially improve the score) or low
- **Effort**: high (requires substantial new work) or low

Priority order for the applicant:
1. High-impact / low-effort — fix these first
2. High-impact / high-effort — plan these for the revision
3. Low-impact / low-effort — address if time allows
4. Low-impact / high-effort — skip unless required by reviewers

Each revision entry must name the target section of the proposal.

## Step 8: Findings Memory Update
Write a structured entry to `ideas/findings_memory.json` after synthesis. Append to the existing array (do not overwrite prior rounds).

### For R01 Proposals

# Overall Impact Scoring (1-9)
- NIH orientation: 1 is exceptional, 9 is poor.
- Score emerges from panel discussion, not formula.
- One domain reporting critical flaws weighs heavily regardless of other domain scores.
- Rationale must be transparent and tied to specific evidence from the reviews.

# Decision Logic
- `proceed_to_export`: weaknesses are minor, score is competitive (typically 1-3), and no critical flaws remain.
- `revise`: major or fixable weaknesses materially affect impact, or any critical flaw is unresolved.
- State the decision with a concise justification tied to specific review evidence.

### For Academic Papers

# Decision Logic
- `accept`: recommendation is Accept or stronger AND no critical flaws remain. Proceed to export/camera-ready.
- `minor_revision`: recommendation is Weak Accept, issues are fixable in camera-ready. Proceed with revision notes.
- `major_revision`: recommendation is Borderline or Weak Reject, but paper has merit. Trigger revision round (if rounds remain) or flag for major rework.
- `reject`: recommendation is Reject or stronger, or fundamental problems remain after revision rounds. Flag for major rework or abandonment.
- State the decision with a concise justification tied to specific review evidence and dimension scores.

# Output Contract

Write two output files after the `<OUTPUT>` block:

### For R01 Proposals

## `reviews/panel_decision_r{N}.json`
```json
{
  "round": N,
  "domain_scores": {
    "hci": {
      "significance": 1-9,
      "investigator": 1-9,
      "innovation": 1-9,
      "approach": 1-9,
      "environment": 1-9
    },
    "healthcare": { "...same fields..." },
    "ai": { "...same fields..." }
  },
  "panelist_perspectives": [
    { "persona": "Senior Methodologist", "perspective_summary": "..." },
    { "persona": "Clinical Champion", "perspective_summary": "..." },
    { "persona": "Innovation Advocate", "perspective_summary": "..." },
    { "persona": "Devil's Advocate", "perspective_summary": "..." }
  ],
  "nih_dimensions": {
    "significance": 1-9,
    "investigator": 1-9,
    "innovation": 1-9,
    "approach": 1-9,
    "environment": 1-9
  },
  "overall_impact_score": 1-9,
  "overall_impact_rationale": "3-5 sentence narrative",
  "consensus_strengths": ["..."],
  "consensus_weaknesses": ["..."],
  "disagreements_resolved": [
    { "topic": "...", "resolution": "..." }
  ],
  "priority_revisions": [
    {
      "issue": "...",
      "impact": "high|low",
      "effort": "high|low",
      "priority_rank": 1,
      "target_section": "Approach|Significance|..."
    }
  ],
  "decision": "proceed_to_export|revise",
  "score_trajectory": {
    "prior_score": null,
    "current_score": 1-9,
    "change": "improved|declined|unchanged|first_round",
    "change_drivers": "..."
  },
  "findings_memory_entry": {
    "round": N,
    "score": 1-9,
    "key_learnings": {
      "what_worked": ["..."],
      "what_failed": ["..."]
    },
    "recurring_issues": ["..."],
    "score_change_drivers": "..."
  }
}
```

### For Academic Papers: Output Format

## `reviews/panel_decision_r{N}.json`
```json
{
  "round": N,
  "domain_scores": {
    "hci": {
      "significance": 1-5,
      "originality": 1-5,
      "research_quality": 1-5,
      "presentation": 1-5,
      "prior_work": 1-5
    },
    "healthcare": { "...same fields..." },
    "ai": { "...same fields..." }
  },
  "panelist_perspectives": [
    { "persona": "Domain Expert", "perspective_summary": "..." },
    { "persona": "Methodology Expert", "perspective_summary": "..." },
    { "persona": "Presentation Expert", "perspective_summary": "..." },
    { "persona": "Impact Advocate", "perspective_summary": "..." }
  ],
  "venue_dimensions": {
    "significance": 1-5,
    "originality": 1-5,
    "research_quality": 1-5,
    "presentation": 1-5,
    "prior_work": 1-5
  },
  "overall_recommendation": "Strong Accept|Accept|Weak Accept|Borderline|Weak Reject|Reject|Strong Reject",
  "decision": "accept|minor_revision|major_revision|reject",
  "contribution_type_assessment": "evaluation of whether paper delivers on declared contribution type",
  "consensus_strengths": ["..."],
  "consensus_weaknesses": ["..."],
  "disagreements_resolved": [
    { "topic": "...", "resolution": "..." }
  ],
  "priority_revisions": [
    {
      "issue": "...",
      "impact": "high|low",
      "effort": "high|low",
      "priority_rank": 1,
      "target_section": "..."
    }
  ],
  "score_trajectory": {
    "prior_recommendation": null,
    "current_recommendation": "...",
    "change": "improved|declined|unchanged|first_round",
    "change_drivers": "..."
  },
  "findings_memory_entry": {
    "round": N,
    "recommendation": "...",
    "key_learnings": {
      "what_worked": ["..."],
      "what_failed": ["..."]
    },
    "recurring_issues": ["..."],
    "change_drivers": "..."
  }
}
```

### For R01 Proposals

## `reviews/panel_summary_r{N}.md`
Write in NIH Summary Statement format with these sections:
- **Overall Impact**
- **Significance**
- **Investigator**
- **Innovation**
- **Approach**
- **Environment**
- **Summary of Strengths**
- **Summary of Weaknesses**
- **Recommended Revisions** (ordered by priority rank)

### For Academic Papers: Review Summary Format

## `reviews/panel_summary_r{N}.md`
Write in venue peer review format with these sections:
- **Summary of Strengths**
- **Summary of Weaknesses**
- **Questions for Authors** (common in CHI reviews — specific questions the authors should address in a response or revision)
- **Recommendation with Justification** (overall recommendation with narrative rationale referencing dimension scores)
- **Detailed Dimension Scores with Rationale** (each of the 5 dimensions with score and 2-3 sentence justification)
- **Contribution Type Assessment** (does the paper deliver on its declared contribution type?)
- **Recommended Revisions** (ordered by priority rank)

# Scratchpad Pattern
Always use `<THOUGHT>` for the panelist discussion simulation. Only the `<OUTPUT>` block is parsed by downstream tools. The thought section is for deliberation; the output section is for structured results.

```
<THOUGHT>
[Panelist discussion here]
</THOUGHT>

<OUTPUT>
[Structured JSON and markdown outputs here]
</OUTPUT>
```

# Quality Bar
- All three reviewer voices are represented fairly in the synthesis.
- The overall impact score (R01) or recommendation (paper) is defensible and tied to specific evidence.
- Revision priorities are ranked, actionable, and mapped to proposal/paper sections.
- The panel summary reads like NIH study section documentation (R01 mode) or venue review documentation (paper mode).
- Findings memory is updated so future rounds can track trajectory.
- No dimension score is silently overridden without a documented rationale.

### For Academic Papers
- Contribution type assessment is included and calibrated to the declared type.
- Questions for Authors section is substantive and specific.
- Decision logic follows the accept/minor_revision/major_revision/reject framework.
- Dimension scores use the 1-5 scale with contribution-type-appropriate weighting.
