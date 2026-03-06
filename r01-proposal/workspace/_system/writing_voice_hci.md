# HCI Domain Writing Voice
## Overrides for Human-Computer Interaction Sections

> **This file overrides `writing_voice.md` for HCI-domain content only.**
> Read by: `r01-writer-hci`, `r01-writer-integrator` (for HCI-specific aim framing).
> Precedence: this file > `writing_voice.md` > `style_guide.md`.
> Updated by: `r01-evolution` after Draft Feedback Checkpoints with HCI-domain corrections.

---

## Dimension Overrides

Only dimensions that differ from the generic voice are listed here. For all other dimensions, follow `writing_voice.md`.

### Dimension 1: Argumentative Style — Override

**Current calibration:** Problem-experience-first with co-design framing. Lead HCI paragraphs with the user's experience of the problem, not the technical gap. The PI frames HCI work as "co-design with stakeholders" and names specific stakeholder compositions. Transition from human experience to design response to evidence of effectiveness.

**Evidence:** Limited direct HCI-section quotes available from the 3 proposals; HCI appears primarily as participatory design components. The Surgery proposal names the advisory panel composition explicitly: "We will form an Advisory Panel of 6 stakeholders (2 GI surgeons, 2 GI nurse practitioners, 2 recent surgical patients) from OSUWMC." The Sepsis proposal states "All Aims are endorsed and co-designed by practicing physicians."

**Preferred:**
> "We will form an Advisory Panel of 6 stakeholders (2 GI surgeons, 2 GI nurse practitioners, 2 recent surgical patients) from OSUWMC. Notably, this builds on our prior interview study with 13 providers and 4 patients, which revealed challenges such as digital tool struggles and unreliable wound descriptions." [2025PostSurgery]

**Avoided:**
> Alert fatigue is a well-documented problem in ICU settings. Many studies have shown that nurses receive too many alerts.

### Dimension 2: Technical Depth — Override

**Current calibration:** Method-justified. For HCI methods, always explain *why* a specific method was chosen for this context, not just name it. Link method choice to the research question it answers.

**Preferred:**
> We selected contextual inquiry over laboratory usability testing because our research question requires understanding decision-making under real clinical time pressure — factors that cannot be reproduced in a controlled setting [Beyer & Holtzblatt, 1998].

**Avoided:**
> We will use contextual inquiry to study nurse workflows.

### Dimension 6: Interdisciplinary Framing — Override

**Current calibration:** Clinical-impact-anchor. Every HCI finding must be connected to a clinical outcome, not left as a standalone usability result. Reviewers from clinical study sections need to see why interaction design matters for patient care.

**Preferred:**
> The redesigned alert interface reduced critical alert response time from 4.2 to 1.8 minutes (p<0.01), which our clinical collaborators estimate would enable intervention within the 6-hour therapeutic window for sepsis-associated AKI in 73% of cases (vs. 41% with current workflows).

**Avoided:**
> The redesigned interface improved task completion time by 57% and received a SUS score of 82.

### Dimension 7: Reader Model — Override

**Current calibration:** Define all HCI-specific terms. Assume reviewers understand research methodology but not HCI vocabulary. Terms that need first-use definition include: contextual inquiry, think-aloud protocol, affinity diagramming, cognitive walkthrough, heuristic evaluation, SUS, NASA-TLX, PSSUQ, technology acceptance model (TAM), Wizard-of-Oz prototyping, design probe.

---

## HCI-Specific Conventions

### Participant Description Standard
Always specify for HCI studies:
- Role (e.g., "board-certified intensivists," not just "clinicians")
- Sample size with justification (n=5–8 formative, n=20+ summative, with citation for HCI sample size norms)
- Recruitment strategy and eligibility criteria
- Compensation and IRB status

### Participatory Design Session Specification
The PI conducts PD sessions via specific formats and this level of specificity should be maintained. Observed pattern from the proposals: sessions conducted via Zoom, approximately 60 minutes, structured as group interview followed by system presentation followed by structured feedback. Name the format, duration, platform, and structure. Generic descriptions ("we will conduct user studies") are not acceptable.

### MCI-Specific Adaptations (when applicable)
When the target population includes older adults or those with mild cognitive impairment (MCI), explicitly address:
- Extended session times to accommodate cognitive load
- Multi-modal instruction formats (verbal, written, demonstrated)
- Caregiver involvement in study design and sessions
- Simplified interface adaptations and their rationale

*Note: Limited evidence from the 3 analyzed proposals — this pattern is inferred from the Surgery proposal's patient-centered design approach. Flag as "limited evidence" if used in a proposal that doesn't involve MCI populations.*

### Design Rationale Traceability
Every design decision in Approach must trace back to either:
- User research finding from this project (Aim reference)
- Prior published evidence (citation)
- Established design heuristic (named, e.g., Nielsen's visibility of system status)

Never present a design choice without rationale. Reviewers will ask "why this design?"

### Evaluation Instrument Selection
When choosing evaluation instruments:
- Name the instrument and cite the validation study
- Justify why this instrument over alternatives
- Report psychometric properties (reliability coefficients) if known
- For custom instruments: describe development process and pilot validation plan

---

## Feedback History

| Date | Project | Change | Source |
|------|---------|--------|--------|
| 2026-03-05 | All | Dim 1 override updated with co-design framing and real quotes; PD Session Specification and MCI Adaptations conventions added | Seeded from 3 prior R01 proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery) — limited HCI-specific data; patterns inferred from participatory design sections |

---

*Last updated: 2026-03-05. Seeded from PI's prior R01 proposals. HCI data is limited — these proposals treat HCI as a secondary component (participatory design). Updated by evolution agent after HCI-domain feedback.*
