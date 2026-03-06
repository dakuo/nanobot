# NIH R01 Section Specifications
## Human-Centered AI for Healthcare — Detailed Section Requirements

> All writer skills must read this file before drafting any section.
> All reviewer skills must use this file as the evaluation rubric.
> Cross-reference with `style_guide.md` for writing conventions.

---

## Overview: R01 Document Structure

```
Application Package
├── Project Summary / Abstract          (30 lines, ~250 words)
├── Project Narrative                   (2–3 sentences, ~50 words)
├── Specific Aims                       (1 page, separate from Research Strategy)
└── Research Strategy                   (12 pages total)
    ├── Significance                    (~2.5–3 pages)
    ├── Innovation                      (~1.5–2 pages)
    └── Approach                        (~7–8 pages)
        ├── Aim 1
        ├── Aim 2
        ├── Aim 3
        └── Aim 4 (if applicable; 2-4 aims typical)
```

---

## Section 1: Project Summary / Abstract

### Page Budget
- **Hard limit:** 30 lines of text (NIH enforces this)
- **Word target:** 220–260 words
- **Format:** Single paragraph or structured short paragraphs; no headers; no citations

### Purpose
The Project Summary is the first thing reviewers and program officers read. It must stand alone — a reader with no other context must understand what the project does, why it matters, and what it will produce.

### Required Elements (in order)
1. **Background / Problem Statement** (2–3 sentences): What clinical or scientific problem is being addressed? What is the burden?
2. **Gap / Opportunity** (1–2 sentences): What is missing from current knowledge or practice?
3. **Central Hypothesis** (1 sentence): The overarching scientific hypothesis the project will test.
4. **Specific Aims** (2–4 sentences): Brief description of each aim — what will be done, not just what will be studied.
5. **Methods / Approach** (2–3 sentences): Key methodological approaches. Name the AI/ML methods, clinical datasets, and study designs.
6. **Expected Outcomes** (1–2 sentences): What will be produced? (Models, tools, datasets, clinical evidence)
7. **Public Health Relevance** (1–2 sentences): How will this improve health outcomes? Be specific about the patient population and the expected benefit.

### Key Elements Checklist
- [ ] Clinical problem stated with epidemiological anchor (mortality, prevalence, cost)
- [ ] Gap clearly identified
- [ ] Central hypothesis stated as a testable proposition
- [ ] All aims mentioned (even briefly)
- [ ] Methods named (not just "AI" — specify the approach)
- [ ] Expected outcomes are concrete deliverables
- [ ] Public health relevance is explicit and specific
- [ ] No jargon without definition
- [ ] No citations
- [ ] Within 30-line limit

### Common Reviewer Complaints
- "The abstract reads like a background section — the proposed work is buried."
- "The hypothesis is not stated."
- "The aims are described as topics, not as research activities."
- "Public health relevance is vague — 'improve patient outcomes' is insufficient."

---

## Section 2: Project Narrative

### Page Budget
- **Hard limit:** 2–3 sentences
- **Word target:** 40–60 words
- **Audience:** General public, Congress, journalists — NOT scientists

### Purpose
The Project Narrative is the plain-language summary required by NIH for public accountability. It appears in NIH Reporter and may be read by non-scientists. It must be jargon-free and immediately comprehensible.

### Required Elements
1. **What the project does** (1 sentence, plain language)
2. **Why it matters** (1 sentence, patient/public benefit)
3. **Who benefits** (optional 3rd sentence if needed for clarity)

### Template
> This project will develop [plain-language description of the AI tool or study]. [Tool/study] has the potential to [specific clinical benefit] for [patient population]. Findings from this research will [broader impact on healthcare or public health].

### Key Elements Checklist
- [ ] Zero technical jargon (no "transformer," "EHR," "AUC," "multivariate")
- [ ] Mentions the disease or health condition in plain terms
- [ ] States a concrete patient benefit
- [ ] 2–3 sentences maximum
- [ ] Written at 8th-grade reading level

### Common Reviewer Complaints
- "This reads like a scientific abstract, not a plain-language summary."
- "The public benefit is not stated."

---

## Section 3: Specific Aims

### Page Budget
- **Hard limit:** 1 page (separate from 12-page Research Strategy)
- **Word target:** 450–500 words
- **Format:** Flowing prose with aim descriptions; may use bold for aim titles

### Purpose
The Specific Aims page is the most important page in the application. Many reviewers read only this page before scoring. It must: (1) establish the problem's importance, (2) position the team's approach as the right solution, (3) state a clear hypothesis, and (4) describe 2–4 aims that are logical, feasible, and impactful.

### Required Structure

#### Opening Paragraph (~100 words)
- Hook: Start with the clinical/scientific problem and its burden (1–2 sentences with statistics)
- Current state: What exists now and why it is insufficient (1–2 sentences)
- Gap: The specific knowledge or technology gap this project addresses (1 sentence)
- Opportunity: Why now is the right time (1 sentence — new data, new methods, new clinical need)

#### Central Hypothesis (~50 words)
- State explicitly: "We hypothesize that..."
- The hypothesis must be testable and directly addressed by the aims
- Include the key mechanism or relationship being tested

#### Team Positioning (~30 words)
- 1–2 sentences establishing why this team is uniquely qualified
- Reference key preliminary data, datasets, or clinical partnerships

#### Specific Aims (2–4 aims, ~200 words total)
For each aim:
- **Aim [N]: [Bold title — action verb + object]** (e.g., "Aim 1: Develop and validate a multimodal AI model for early sepsis-AKI prediction")
- 2–3 sentences: what will be done, how, and what will be produced
- Do NOT describe methods in detail — save for Approach

#### Closing Impact Statement (~50 words)
- Restate the significance: what will this project enable?
- Connect to NIH mission and public health
- Optional: mention expected publications, tools, or datasets

### Template Outline

```
[Opening: Problem + Burden]
[Current State + Insufficiency]
[Gap]
[Opportunity / Why Now]

Central Hypothesis: We hypothesize that [X] will [Y] in [population], 
enabling [clinical outcome].

[Team positioning sentence]

Aim 1: [Action verb + specific deliverable]
[2–3 sentences: what, how, deliverable]

Aim 2: [Action verb + specific deliverable]
[2–3 sentences: what, how, deliverable]

Aim 3 (if applicable): [Action verb + specific deliverable]
  Aim 4 (if applicable): [Action verb + specific deliverable]
[2–3 sentences: what, how, deliverable]

[Closing: Impact on field + public health relevance]
```

### Key Elements Checklist
- [ ] Opens with clinical problem + epidemiological statistics
- [ ] Gap is specific (not "more research is needed")
- [ ] Central hypothesis is explicitly stated and testable
- [ ] Each aim has an action verb (Develop, Validate, Evaluate, Characterize, Determine)
- [ ] Aims are logically connected (sequential or parallel — state which)
- [ ] Closing impact statement connects to NIH mission
- [ ] No methods detail (save for Approach)
- [ ] No more than 500 words
- [ ] Fits on one page at 11pt font

### Common Reviewer Complaints
- "The hypothesis is not stated — I cannot evaluate whether the aims test it."
- "The aims are topics, not research activities. Use action verbs."
- "The opening paragraph is all background — the gap and opportunity are buried."
- "Three aims feel disconnected — the logical flow between them is unclear."
- "The closing paragraph is generic — it does not tell me what this project uniquely contributes."

---

## Section 4: Significance

### Page Budget
- **Target:** 2.5–3 pages of the 12-page Research Strategy
- **Word target:** 1,250–1,500 words
- **Citation density:** 2–4 citations per paragraph

### Purpose
Significance establishes that the problem is important, that the current state of knowledge is insufficient, and that this project addresses a genuine gap. It answers: "Why does this matter?" and "Why hasn't it been solved?"

### Required Structure

#### 4.1 Clinical / Scientific Problem (~300 words)
- Establish the disease burden: prevalence, incidence, mortality, morbidity, economic cost
- Use authoritative, recent statistics (CDC, CMS, AHRQ, high-impact journals)
- Describe the clinical context: who is affected, when, and how
- Establish urgency: why does this problem demand a solution now?

#### 4.2 Current State of Knowledge (~400 words)
- Describe existing approaches: clinical scores, prior AI/ML work, current standard of care
- Acknowledge what has been accomplished (do not dismiss prior work — reviewers may have done it)
- Identify the specific limitations of existing approaches:
  - Performance limitations (sensitivity, specificity, generalizability)
  - Implementation limitations (workflow integration, interpretability, equity)
  - Conceptual limitations (wrong framing, missing variables, inadequate theory)

#### 4.3 Gaps in Knowledge (~300 words)
- Enumerate gaps explicitly: "Gap 1: ...", "Gap 2: ...", "Gap 3: ..."
- Each gap should correspond to one aim
- Gaps must be specific — not "more research is needed" but "no validated model exists for [specific population] using [specific data type]"

#### 4.4 How This Project Addresses the Gaps (~300 words)
- Map each gap to the corresponding aim
- Establish "why now": new data availability, new methods, new clinical partnerships, new regulatory landscape
- Establish "why this team": unique datasets, clinical access, interdisciplinary expertise, preliminary data
- Do not describe methods in detail — that belongs in Approach

### Key Elements Checklist
- [ ] Clinical burden established with specific statistics and citations
- [ ] Current state of knowledge is fair and accurate (not a strawman)
- [ ] Limitations of prior work are specific, not generic
- [ ] Gaps are enumerated and specific
- [ ] Each gap maps to an aim
- [ ] "Why now" is addressed
- [ ] "Why this team" is addressed (briefly — more in Approach)
- [ ] No methods detail
- [ ] 2–4 citations per paragraph
- [ ] Within word target

### Common Reviewer Complaints
- "The significance section reads like a literature review, not an argument for this project."
- "The gaps are vague — 'more research is needed' is not a gap."
- "The authors dismiss prior work without acknowledging its contributions."
- "I cannot see how the gaps connect to the specific aims."
- "The 'why now' is not addressed — why is this the right time for this project?"
- "Health equity is not mentioned despite the clinical AI focus."

---

## Section 5: Innovation

### Page Budget
- **Target:** 1.5–2 pages of the 12-page Research Strategy
- **Word target:** 750–1,000 words
- **Citation density:** 1–3 citations per paragraph (cite prior art being surpassed)

### Purpose
Innovation is scored separately by NIH reviewers. It must explicitly claim novelty and justify it. Do not let reviewers infer innovation — state it directly. The section answers: "What is genuinely new here, and why does it matter that it's new?"

### Required Structure

#### Opening Statement (~50 words)
- Explicitly state that the project is innovative
- Preview the categories of innovation (technical, methodological, conceptual)

#### Innovation 1: Technical Innovation (~200 words)
- What new AI/ML method, algorithm, architecture, or computational approach is being developed?
- How does it differ from prior approaches? (Cite the prior state of the art)
- What does this technical advance enable that was not previously possible?

#### Innovation 2: Methodological Innovation (~200 words)
- What new study design, data collection approach, or evaluation framework is being used?
- For HCI work: new participatory design methods, new usability evaluation frameworks
- For clinical AI: new validation approaches, new equity evaluation methods, new prospective study designs
- Why is this methodological advance significant?

#### Innovation 3: Conceptual Innovation (~200 words)
- What new theoretical framework, model of disease, or conceptual approach is being introduced?
- How does this reframe the problem in a way that opens new solution pathways?
- For human-centered AI: new frameworks for human-AI collaboration in clinical settings

#### Closing (~100 words)
- Summarize how the innovations together represent a step-change, not an incremental advance
- Connect innovations to expected impact on the field

### Key Elements Checklist
- [ ] "Novel" or "innovative" used explicitly and justified
- [ ] Innovations enumerated (Innovation 1, 2, 3)
- [ ] Prior state of the art cited for each innovation
- [ ] Technical, methodological, AND conceptual innovation addressed
- [ ] Each innovation connected to a specific aim
- [ ] No methods detail (save for Approach)
- [ ] Within word target

### Common Reviewer Complaints
- "The innovation section describes what will be done, not what is new about it."
- "The authors claim novelty but do not cite the prior work they are surpassing."
- "This is incremental, not innovative — the advance over prior work is marginal."
- "Only technical innovation is described — methodological and conceptual innovation are absent."
- "The innovation is in the application domain, not the science — this is not sufficient."

---

## Section 6: Approach

### Page Budget
- **Target:** 7–8 pages of the 12-page Research Strategy
- **Word target:** 3,500–4,000 words
- **Citation density:** 1–2 citations per paragraph
- **Figures:** At least 1 figure per aim; preliminary data figures strongly recommended

### Purpose
Approach is the most heavily weighted section. It must convince reviewers that the team has a rigorous, feasible, well-thought-out plan. It answers: "Can this team actually do this, and will it work?"

### Required Opening: Overall Strategy (~150 words)
Before the per-aim sections, include a brief overview:
- Restate the central hypothesis
- Describe the overall study design and how the aims fit together
- State whether aims are sequential, parallel, or mixed
- Include a timeline figure or table (strongly recommended)

### Per-Aim Structure

Each aim must contain all of the following subsections:

#### [Aim N]: [Title] (~800–1,200 words per aim)

**Rationale (~100 words)**
- Why is this aim necessary?
- What gap does it address?
- How does it connect to the preceding aim (if sequential)?

**Preliminary Data (~150–200 words + figure)**
- Present existing data that demonstrates feasibility
- For AI projects: preliminary model performance, dataset characteristics, pilot study results
- For HCI projects: formative study findings, prototype evaluation results
- Include a figure: "(Preliminary Data — Figure N)"
- Acknowledge limitations of preliminary data honestly

**Methods (~400–600 words)**
- Describe the experimental design in sufficient detail for a knowledgeable reviewer to evaluate feasibility
- For AI/ML: specify model architecture, training procedure, hyperparameter selection, cross-validation strategy, evaluation metrics
- For clinical studies: specify patient population, inclusion/exclusion criteria, sample size with power calculation, data collection procedures
- For HCI studies: specify participant recruitment, study protocol, instruments, analysis approach
- Address rigor and reproducibility explicitly (see style_guide.md Section 5)
- Address sex as a biological variable

**Expected Outcomes (~100 words)**
- What specific deliverables will this aim produce?
- What performance thresholds define success? (e.g., "We expect AUC ≥ 0.85 on external validation")
- How will outcomes from this aim feed into the next aim?

**Potential Pitfalls and Alternative Approaches (~150 words)**
- Identify 2–3 realistic risks (not catastrophic failures — reviewers know you've thought about those)
- For each pitfall: describe the mitigation strategy or alternative approach
- Demonstrate that you have thought carefully about what could go wrong
- Do NOT say "we do not anticipate any problems" — this is a red flag

**Figure Placeholder**
- Every aim should reference at least one figure
- Preliminary data figures: "(Preliminary Data — Figure N: [description])"
- Conceptual figures: "(Figure N: Study design schematic for Aim N)"

### Timeline
- Include a Gantt chart or timeline table (typically at the end of Approach)
- Show all aims across the project period (typically 5 years for R01)
- Mark key milestones: dataset acquisition, model development, validation, dissemination
- Show that aims are feasible within the project period

### Rigor and Reproducibility Subsection
- Include a dedicated subsection (or integrate throughout) addressing:
  - Power and sample size justification
  - Blinding and randomization (where applicable)
  - Data sharing and code availability
  - Computational reproducibility (software versions, containerization)
  - Equity analysis plan

### Key Elements Checklist
- [ ] Overall strategy section present before per-aim sections
- [ ] Each aim has: Rationale, Preliminary Data, Methods, Expected Outcomes, Pitfalls
- [ ] Preliminary data figure included for each aim
- [ ] Power calculations included for clinical/statistical aims
- [ ] Sex as biological variable addressed
- [ ] Rigor and reproducibility addressed
- [ ] Pitfalls are realistic and mitigations are specific
- [ ] Timeline figure or table included
- [ ] Expected outcomes include measurable success criteria
- [ ] Within word target

### Common Reviewer Complaints
- "The preliminary data is insufficient to support the feasibility of this approach."
- "No power calculation is provided — I cannot evaluate whether the sample size is adequate."
- "The pitfalls section is superficial — the authors say they will 'consult with experts' without specifics."
- "The methods are too vague — I cannot evaluate whether this approach will work."
- "The timeline is unrealistic — Aim 3 cannot be completed in Year 5 given the dependencies."
- "Sex as a biological variable is not addressed."
- "There is no plan for external validation — the model may not generalize."
- "The expected outcomes do not include measurable success criteria."
- "The aims are described as independent but clearly depend on each other — this is not acknowledged."

---

## Cross-Section Consistency Requirements

These elements must be consistent across ALL sections:

| Element | Must Match Across |
|---|---|
| Aim titles | Specific Aims, Approach headers, Project Summary |
| Hypothesis | Specific Aims, Approach opening |
| Team members | Significance ("why this team"), Approach (who does what) |
| Dataset names | Significance, Approach, Preliminary Data |
| Performance metrics | Innovation (claimed), Approach (expected outcomes) |
| Timeline | Approach timeline, Project Summary |

**Consistency check:** Before finalizing, verify that aim titles in the Specific Aims page exactly match the aim headers in the Approach section. Mismatches are a red flag for reviewers.

---

## NIH Scoring Criteria Reference

Reviewers score each criterion 1–9 (1 = exceptional, 9 = poor):

| Criterion | Weight | Key Question |
|---|---|---|
| Significance | High | Does this address an important problem? |
| Investigator(s) | High | Is the team qualified? |
| Innovation | Medium | Is this genuinely new? |
| Approach | Very High | Is the plan rigorous and feasible? |
| Environment | Medium | Does the institution support this work? |

**Overall Impact Score** is a holistic judgment, not an average. A fatal flaw in Approach can sink an otherwise strong application.

**Fatal flaws (automatic poor score):**
- No preliminary data for a high-risk aim
- No power calculation for a clinical study
- Hypothesis not testable by the proposed aims
- Team lacks expertise in a critical area with no collaborator named
- Budget does not match the scope of work

---

*Last updated: System initialization. Update after each completed project with lessons from reviewer feedback.*
