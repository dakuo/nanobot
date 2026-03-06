# NIH R01 Writing Style Guide
## Human-Centered AI for Healthcare — Shared Reference

> **This file evolves — updated after each project based on user and reviewer feedback.**
> All writer and reviewer skills must read this file before generating or evaluating any section.
> Do not override these conventions without explicit user instruction.

---

## 1. Voice and Tone

**Register:** Formal academic. This is a scientific proposal reviewed by expert peers and NIH study section members. Every sentence must earn its place.

**Person:** Third person for describing the field, prior work, and the problem. First person plural ("We will," "Our team") is acceptable and preferred for describing the proposed work — NIH reviewers respond well to confident, direct ownership of the research plan.

**Active vs. Passive:** Active voice is strongly preferred. Passive voice is acceptable only when the agent is genuinely unknown or irrelevant (e.g., "Patients were enrolled between 2018–2022"). Never use passive to hedge or obscure responsibility.

**Hedging:** Avoid excessive hedging ("it may be possible that," "could potentially"). Use confident, precise language. Uncertainty should be acknowledged in Potential Pitfalls sections, not embedded throughout the prose.

**Jargon Policy:** Every technical term must be defined on first use. Acronyms must be spelled out on first use and used consistently thereafter. Do not assume reviewers share your exact subdomain — study sections are multidisciplinary.

**Explanatory Insertions:** When inline explanation is needed, use relative clauses (`which`, `who`) or parenthetical asides — never em-dash parentheticals that create long interrupting clauses. Avoid: "wearable sensing — passive continuous sensing via consumer wearables collecting accelerometry — no additional hardware." Prefer: "Wearable sensing collects accelerometry passively through consumer wearables (Fitbit or Apple Watch), which interface with standard health APIs."

**Tone Calibration by Section:**
- Specific Aims: Compelling, urgent, confident. This is the sales pitch.
- Significance: Authoritative, evidence-heavy, measured urgency.
- Innovation: Bold but grounded. Claim novelty explicitly; do not let reviewers infer it.
- Approach: Precise, methodologically rigorous, anticipatory of critique.
- Project Summary/Narrative: Plain, accessible, public-facing.

---

## 2. Claim-Evidence-Impact Pattern

Every substantive paragraph in Significance, Innovation, and Approach must follow this three-part structure:

1. **Claim / Assertion** — State the point directly in the first sentence. Do not bury the lead.
2. **Supporting Evidence / Citation** — Provide 1–4 citations that substantiate the claim. Prefer recent (≤5 years) high-impact sources. For foundational claims, seminal older works are appropriate.
3. **Impact / Significance** — Close the paragraph by connecting the evidence to the proposal's goals. Why does this matter for *this* project? What gap does it reveal or what opportunity does it create?

**Example (Significance):**
> Sepsis-associated acute kidney injury (SA-AKI) affects approximately 50% of ICU patients with sepsis and carries a 30-day mortality exceeding 40% [Smith et al., 2021; Jones et al., 2022]. Despite advances in sepsis management, early identification of patients at risk for SA-AKI remains unreliable using conventional clinical markers [Brown et al., 2020]. This gap creates a critical window for AI-driven early warning systems that could enable timely nephroprotective interventions and reduce preventable mortality.

**Anti-patterns to avoid:**
- Opening with background rather than a claim
- Citing without connecting evidence to the proposal
- Ending paragraphs without a "so what" statement
- Paragraphs longer than 150 words without a clear CEI structure

---

## 3. Citation Density

Citation density signals rigor and situates the work within the literature. Targets by section:

| Section | Target Citations per Paragraph | Notes |
|---|---|---|
| Specific Aims | 0–2 | Aims page is dense; cite only the most critical anchors |
| Significance | 2–4 | High density expected; reviewers will check literature coverage |
| Innovation | 1–3 | Cite prior work being surpassed; cite your own preliminary work |
| Approach | 1–2 | Cite methods sources, validation studies, and your own prior work |
| Project Summary | 0 | No citations in abstract |
| Project Narrative | 0 | No citations in plain-language summary |

**Citation format:** Follow the target journal/NIH format (typically numbered inline). Maintain a consistent bibliography. Do not cite preprints as primary evidence for clinical claims; preprints are acceptable for methods and computational approaches.

**Self-citation:** Cite your own prior work where directly relevant. Reviewers expect to see preliminary data and prior publications from the team. Do not over-cite self (>30% of citations from the same group is a red flag).

---

## 4. Transition Language

Transitions signal logical flow and prevent reviewers from losing the thread. Use bridging sentences at:

**Between major sections:**
- From Significance to Innovation: "Having established the critical gap in [X], we now describe how our approach represents a fundamental departure from existing methods."
- From Innovation to Approach: "The innovations described above are operationalized through the following research plan."
- From one Aim to the next: "Building on the [dataset/model/framework] established in Aim 1, Aim 2 extends this foundation to [next challenge]."

**Within Approach (between subsections):**
- Rationale → Methods: "To address this rationale, we will employ the following experimental design."
- Methods → Expected Outcomes: "Successful completion of these experiments will yield [specific deliverable]."
- Expected Outcomes → Pitfalls: "While we anticipate [outcome], we have identified the following potential challenges and mitigation strategies."

**Aim interdependency language:**
- If aims are sequential: "Aim 2 is contingent on the [model/cohort/tool] developed in Aim 1; however, Aim 3 can proceed in parallel."
- If aims are independent: "Each aim is designed to be independently executable, ensuring the project remains viable if any single aim encounters delays."

**Avoid:** Starting consecutive paragraphs with the same word. Avoid "Furthermore," "Moreover," "Additionally" as the primary transition mechanism — these are weak. Use content-specific bridges instead.

---

## 5. NIH-Specific Conventions

### Rigor and Reproducibility
Every Approach section must explicitly address NIH's rigor and reproducibility requirements. Include a dedicated subsection or integrate throughout:
- **Scientific rigor:** Justify sample sizes with power calculations. Specify blinding procedures where applicable. Describe controls.
- **Reproducibility:** Describe how data, code, and models will be made available. Reference data sharing plans. Specify software versions and computational environments.
- **Biological variables:** Address sex as a biological variable. If the study involves human subjects, describe how sex and gender will be considered in analysis. If not applicable, explicitly state why.
- **Authentication of key resources:** Identify key biological, chemical, or computational resources and describe how they will be validated.

### Human Subjects Considerations
For clinical AI proposals (the primary domain of this system):
- Clearly distinguish between research involving human subjects and research using de-identified datasets.
- Address IRB status: existing approval, pending, or exempt with justification.
- For AI systems that will interact with patients or clinicians: address FDA regulatory pathway if applicable (SaMD — Software as a Medical Device).
- Address health equity explicitly: describe how the study population reflects diversity, and how the AI system will be evaluated for performance disparities across demographic groups.
- For EHR-based studies: address data governance, HIPAA compliance, and data use agreements.

### Innovation Framing
NIH reviewers score Innovation separately. Do not bury innovation claims in Significance or Approach. The Innovation section must:
- Use the word "novel" or "innovative" explicitly and justify it.
- Enumerate innovations (Innovation 1, Innovation 2, Innovation 3).
- Distinguish technical innovation (new methods), methodological innovation (new study designs), and conceptual innovation (new frameworks or theories).
- Cite the prior state of the art that is being surpassed.

### Rigor of Prior Research
When citing prior work (including your own), briefly note any limitations that your proposal addresses. This demonstrates awareness of the field and positions your work as a genuine advance.

---

## 6. Page Budget Enforcement

NIH R01 Research Strategy is limited to **12 pages** (standard R01). Budget carefully.

**Approximate word targets (at ~500 words/page):**

| Section | Pages | Word Target |
|---|---|---|
| Specific Aims | 1 | 450–500 |
| Significance | 2.5–3 | 1,250–1,500 |
| Innovation | 1.5–2 | 750–1,000 |
| Approach | 7–8 | 3,500–4,000 |
| **Total Research Strategy** | **12** | **~6,000** |

**Additional pages (not counted in 12-page limit):**
- Project Summary/Abstract: 30 lines (~250 words)
- Project Narrative: 2–3 sentences (~50 words)
- Bibliography: unlimited, not counted
- Specific Aims page: 1 page, separate from Research Strategy

**Enforcement rules:**
- If a section is running long, cut background — not methods or pitfalls.
- Figures count against page budget. Each figure typically costs 0.25–0.5 pages. Budget accordingly.
- Tables are efficient — use them for timelines, comparison of methods, and power calculations.
- Do not use font smaller than 11pt or margins smaller than 0.5 inches (NIH will reject).

---

## 7. Figure References

### Inline Reference Convention
- Reference figures parenthetically at the point of first relevance: "(Figure 1)" or "(Fig. 1A–B)"
- Do not say "the figure below" or "as shown above" — figures may reflow. Always use numbered references.
- Every figure must be referenced at least once in the text. Unreferenced figures will be questioned by reviewers.

### Figure Caption Conventions
Captions must be self-contained — a reviewer should understand the figure without reading the surrounding text.

Caption structure:
1. **Bold title** (1 sentence stating the main finding or content)
2. Brief description of what is shown (methods, conditions, data type)
3. Key result or takeaway (1 sentence)
4. Statistical notation if applicable (n=, p<, CI)

Example:
> **Figure 2. AI-ECG model outperforms cardiologist baseline on cardiotoxicity detection.** ROC curves comparing model performance (AUC=0.91, 95% CI 0.87–0.95) against cardiologist consensus (AUC=0.76) on held-out test set (n=1,240 patients). The model achieves clinically actionable sensitivity (87%) at a specificity of 82%, enabling earlier intervention in chemotherapy-treated patients.

### Preliminary Data Figures
- Label preliminary data figures clearly: "Preliminary Data — Figure X"
- Preliminary figures should demonstrate feasibility, not final results. Reviewers understand these are early-stage.
- Include error bars, confidence intervals, or uncertainty estimates wherever possible.

### Figure Placement
- Place figures as close as possible to their first text reference.
- Do not cluster all figures at the end of a section.
- Aim for at least one figure per Aim in the Approach section.

---

## 8. Domain-Specific Notes

### 8.1 HCI (Human-Computer Interaction) Writing Conventions

**Framing:** HCI work in NIH proposals must be framed in terms of clinical outcomes and patient/provider impact — not usability metrics alone. Reviewers from clinical study sections may not value "task completion time" unless connected to patient safety or care quality.

**Key terms to use:** Usability, user-centered design, participatory design, cognitive load, workflow integration, alert fatigue, human factors, implementation science.

**Key terms to define:** Do not assume reviewers know HCI-specific terms like "think-aloud protocol," "contextual inquiry," or "affinity diagramming." Define briefly on first use.

**Evaluation standards:** HCI studies must specify: participant recruitment (clinicians, patients, or both), sample size justification for usability studies (typically n=5–8 for formative, n=20+ for summative), and validated instruments (e.g., SUS, NASA-TLX, PSSUQ).

**Common reviewer concern:** "Is this just a usability study?" — Preempt by connecting every HCI finding to a clinical outcome hypothesis. Usability improvements must be linked to error reduction, adoption rates, or measurable care quality metrics.

**Interdisciplinary positioning:** Explicitly acknowledge the interdisciplinary nature. Name the HCI methods and the clinical science methods separately, then explain how they integrate.

### 8.2 Healthcare / Clinical Science Writing Conventions

**Clinical significance first:** Lead with the clinical problem and its burden (mortality, morbidity, cost, quality of life). Epidemiological statistics must be current (≤3 years) and from authoritative sources (CDC, CMS, peer-reviewed epidemiology journals).

**Clinical workflow integration:** Any AI or technology intervention must describe how it fits into existing clinical workflows. Reviewers will ask: "Will clinicians actually use this?" Address adoption barriers proactively.

**Regulatory awareness:** For AI tools intended for clinical use, address FDA SaMD classification. For diagnostic AI, address sensitivity/specificity tradeoffs in clinical context (not just AUC). For therapeutic decision support, address liability and clinician override.

**Patient population specificity:** Be precise about the patient population. "ICU patients" is too broad. "Adult ICU patients with sepsis-3 criteria admitted to academic medical centers" is appropriate. Specify inclusion/exclusion criteria in Approach.

**Health equity:** NIH expects explicit attention to health disparities. For AI systems: evaluate performance across race, ethnicity, sex, age, and socioeconomic status. For clinical studies: describe recruitment strategies to ensure diverse enrollment.

**Common reviewer concern:** "Is the clinical team adequately represented?" — Ensure the team includes clinical co-investigators (MDs, APRNs, or PhDs with clinical expertise). Name them and their roles explicitly.

### 8.3 AI / Machine Learning Writing Conventions

**Avoid hype:** Do not use "revolutionary," "unprecedented," or "game-changing." NIH reviewers are skeptical of AI hype. Use precise, measured language: "achieves state-of-the-art performance on [benchmark]," "reduces prediction error by X% compared to [baseline]."

**Specify the model:** Do not say "we will use deep learning." Say "we will train a transformer-based sequence model (specifically, a temporal fusion transformer) on longitudinal EHR data." Reviewers expect methodological specificity.

**Baseline comparisons:** Every AI method must be compared against a clinically relevant baseline (e.g., existing clinical scores like SOFA, APACHE-II, or NEWS) and a statistical baseline (logistic regression). Outperforming only other deep learning models is insufficient.

**Generalizability:** Address external validation explicitly. A model trained and tested on one institution's data will receive poor Innovation and Approach scores. Describe multi-site validation or prospective validation plans.

**Interpretability:** For clinical AI, address model interpretability. Specify whether the model produces explanations (SHAP values, attention maps, saliency maps) and how clinicians will interact with these explanations.

**Data:** Specify dataset size, class balance, missingness rates, and preprocessing pipeline. Reviewers will scrutinize whether the dataset is adequate for the proposed model complexity.

**Common reviewer concern:** "Will this generalize beyond the training institution?" — Address prospective validation, external cohort validation, or federated learning approaches.

---

*Last updated: System initialization. Update this file after each completed project with lessons learned.*
