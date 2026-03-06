# Healthcare Domain Writing Voice
## Overrides for Clinical / Healthcare Sections

> **This file overrides `writing_voice.md` for healthcare-domain content only.**
> Read by: `r01-writer-healthcare`, `r01-writer-integrator` (for healthcare-specific aim framing).
> Precedence: this file > `writing_voice.md` > `style_guide.md`.
> Updated by: `r01-evolution` after Draft Feedback Checkpoints with healthcare-domain corrections.

---

## Dimension Overrides

Only dimensions that differ from the generic voice are listed here. For all other dimensions, follow `writing_voice.md`.

### Dimension 1: Argumentative Style — Override

**Current calibration:** Burden-first with quantified stakes. Healthcare paragraphs always open with specific epidemiological data — mortality percentages, cost figures, incidence rates — before presenting any solution. The PI uses exact numbers, not approximations, and cites them immediately.

**Evidence:** Observed in all 3 proposals. Surgery opens with "30–40%" complication incidence. Cardiotoxicity opens with "up to 20% of breast cancer patients treated with these therapies will develop some form of serious cardiovascular disease." Sepsis cites "35% in-hospital deaths are caused by sepsis."

**Preferred:**
> "Complex gastrointestinal (GI) surgical procedures (e.g., pancreaticoduodenectomy) can be lifesaving²,⁴²⁻⁴⁵ but are associated with high complication (e.g., anastomotic leaks, surgical site infections) rates⁴⁶⁻⁴⁹ with an overall incidence of moderate-to-severe complications of 30–40%." [2025PostSurgery]

**Avoided:**
> Acute kidney injury is a significant complication in ICU patients and represents an important area for AI research.

### Dimension 2: Technical Depth — Override

**Current calibration:** Clinically-grounded specificity with ICD codes and scoring systems assumed. The PI names exact clinical scoring systems (SOFA, APACHE-II, NEWS-2, KDIGO, qSOFA, MEWS, SIRS, MACEs, CDR) and ICD codes (I21-I23, I50.9, etc.) without defining them for clinical reviewers. Drug classes, procedure types, and care settings are always named precisely.

**Evidence:** Observed in 2023Sepsis (qSOFA, MEWS, NEWS, SIRS named without definition) and 2025PostSurgery (pancreaticoduodenectomy, anastomotic leaks named as examples). ICD codes appear in the Cardiotoxicity proposal without explanation.

**Preferred:**
> "We will compare the proposed model with widely used warning scores (qSOFA, MEWS, NEWS, and SIRS) and DL-based risk prediction models on various metrics, including AUROC, AUPRC, sensitivity, and specificity with multiple prediction windows (i.e., to predict sepsis onset within n = 0,1,4,8,12 hours)." [2023Sepsis]

**Avoided:**
> We will identify sepsis patients in the ICU using standard clinical criteria.

### Dimension 4: Hedging Tolerance — Override

**Current calibration:** Asymmetric hedging. The PI is MORE cautious on clinical outcome predictions but LESS cautious on technical feasibility claims. "Has the potential to enhance AI models" for speculative clinical benefits; "we will develop" for technical deliverables. Never claim clinical efficacy before a properly powered trial.

**Evidence:** Observed in 2025PostSurgery: "This integrated, continuous dataset has the potential to enhance AI models and enable earlier, more accurate complication detection." Contrast with the same proposal's confident technical claims: "We will develop a human-centered AI system (REACH-AI)..." The asymmetry is consistent and intentional.

**Preferred:**
> "This integrated, continuous dataset has the potential to enhance AI models and enable earlier, more accurate complication detection." [2025PostSurgery — hedging on clinical benefit]

Also preferred:
> "We will develop a human-centered AI system (REACH-AI)..." [2025PostSurgery — no hedging on technical deliverable]

**Avoided:**
> Our model will detect AKI 6 hours early with 90% accuracy, saving lives.

**Note:** This is stricter than the generic voice's calibration for clinical outcome claims. Precision requires acknowledging uncertainty about patient outcomes even when technical confidence is high.

### Dimension 6: Interdisciplinary Framing — Override

**Current calibration:** Workflow-integration-anchor. Every AI or HCI component must be described in terms of how it fits into the clinical workflow. Name the specific clinical decision point, the care team member who acts on the information, and the time window for action. The PI explicitly maps each system capability to a clinical need — this is the HCAI design philosophy in practice.

**Evidence:** Observed in 2025PostSurgery: the system is designed to "(1) collect home-based multimodal patient data, (2) provide consolidated summaries and visualizations of multimodal data that clinicians can easily interpret and act upon, (3) generate transparent and explainable risk scores along with risk predictions, and (4) integrate the system seamlessly into clinical workflow through human-centered designs." Each capability maps to a clinical action.

**Preferred:**
> "To address these challenges, we will integrate postoperative multimodal data with EHRs into a HIPAA-compliant Human-Centered AI (HCAI) system, REACH-AI...designed to: (1) collect home-based multimodal patient data, (2) provide consolidated summaries and visualizations of multimodal data that clinicians can easily interpret and act upon..." [2025PostSurgery]

**Avoided:**
> The model's predictions will be integrated into clinical workflows.

---

## Healthcare-Specific Conventions

### Patient Population Specification
Every mention of a patient population must include:
- Disease/condition (with diagnostic criteria, e.g., Sepsis-3, KDIGO staging)
- Care setting (e.g., "adult medical ICU at a 750-bed academic medical center")
- Key inclusion/exclusion criteria
- Expected demographics (age range, sex distribution if known)

### Stakeholder Engagement Specification
Advisory panels and stakeholder groups must name their exact composition. The PI's pattern: "We will form an Advisory Panel of 6 stakeholders (2 GI surgeons, 2 GI nurse practitioners, 2 recent surgical patients) from OSUWMC." [2025PostSurgery] Generic descriptions ("a panel of clinical experts") are not acceptable.

### Data Specification
Name exact data sources, sample sizes, and time periods. The PI's pattern: "We will use large-scale complex GI surgical EHR data (n=24,755) from OSUWMC." [2025PostSurgery] Never describe data as "a large dataset from a major academic medical center."

### Clinical Actionability
Every AI output must be mapped to a specific clinical decision point in the workflow. The PI frames each system capability as enabling a specific clinical action — not as a general improvement to care. Ask: who acts on this output, when, and what do they do?

### Regulatory and Ethics Framing
For AI tools with clinical applications:
- Name the FDA regulatory pathway if applicable (SaMD classification, De Novo vs. 510(k))
- Address IRB status: approved, pending, or exempt with justification
- For EHR data: specify HIPAA compliance, data use agreements, de-identification method
- For prospective studies: address DSMB requirements, stopping rules, safety reporting

### Health Equity Requirements
NIH expects explicit equity attention. For every clinical study:
- Describe how the study population reflects demographic diversity
- Specify plans for subgroup analysis by race, ethnicity, sex, age, socioeconomic status
- Address potential bias in AI models (training data representativeness)
- Describe recruitment strategies to ensure diverse enrollment

### Clinical Endpoint Precision
- Primary endpoints must be clinically meaningful (not just statistical)
- Specify the clinical significance threshold (not just p-value)
- Name the validated outcome measure (e.g., "KDIGO stage 2+ AKI within 72 hours" not "kidney injury")
- Define the minimum clinically important difference

---

## Feedback History

| Date | Project | Change | Source |
|------|---------|--------|--------|
| 2026-03-05 | All | Dim 1, 2, 4, 6 overrides updated; Stakeholder Engagement, Data Specification, Clinical Actionability conventions added | Seeded from 3 prior R01 proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery) |

---

*Last updated: 2026-03-05. Seeded from PI's prior R01 proposals. Updated by evolution agent after healthcare-domain feedback.*
