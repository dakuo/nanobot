# Personal Writing Voice Profile
## Generic — Applies to All Domains Unless Overridden

> **This file evolves.** Updated by `r01-evolution` after Draft Feedback Checkpoints and user corrections.
> Domain-specific voice files (`writing_voice_hci.md`, `writing_voice_healthcare.md`, `writing_voice_ai.md`) override specific dimensions below.
> Precedence: domain-specific voice > this file > `style_guide.md`.

---

## How This File Works

Each dimension below has:
- **Current calibration**: The active setting writers should follow.
- **Evidence**: Why this calibration exists (user feedback, reviewer comments, or default).
- **Examples**: Preferred vs. avoided phrasing.

When the evolution agent updates a dimension, it appends to Evidence and may revise Current calibration. Old calibrations are preserved as comments for traceability.

---

## Dimension 1: Argumentative Style

**Current calibration:** Problem-stakes-gaps-solution. The PI consistently structures arguments as: clinical problem with quantified burden → existing approaches and their limitations → specific gaps → proposed solution → expected impact. Never leads with the solution before establishing why it's needed.

**Evidence:** Observed consistently across all 3 prior proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery). Sepsis opens with survival benefit of early diagnosis; Cardiotoxicity opens with CVD incidence in breast cancer patients; Surgery opens with complication rates. All three pivot from burden to gaps to solution using "To address these challenges" or equivalent.

**Preferred:**
> "Early prediction and timely decision-making of acute diseases are critical to enabling early intervention and improving clinical outcomes (for example, a sepsis patient may benefit from a 4% higher chance of survival if diagnosed 1 hour earlier)." [2023Sepsis]

**Avoided:**
> In the field of critical care medicine, there has been growing recognition that acute kidney injury associated with sepsis represents a significant clinical challenge.

---

## Dimension 2: Technical Depth

**Current calibration:** Architecture-explicit with mathematical rigor. The PI names exact model architectures (Transformer, WCPH, LVLM, ECAPA-TDNN), writes actual mathematical formulas with all parameters defined, and specifies clinical scoring systems by name (qSOFA, MEWS, NEWS, SIRS, SOFA) without explanation. Sample sizes, train/val/test splits, and evaluation metrics are always stated precisely.

**Evidence:** Observed in all 3 proposals. Sepsis includes the full survival analysis formula: "f_w(x,t) = H_0(t)exp(β^T s(x^(i)))". Surgery specifies "n=24,755" and "70% training set, 10% validation set, 20% test set." This level of mathematical rigor is distinctive for R01 proposals and is a key voice trait.

**Preferred:**
> "The sepsis risk is defined as f_w(x,t) = H_0(t)exp(β^T s(x^(i))), a product of a baseline hazard function, H_0(t) = (ν/λ)(λt)^(ν-1), and the patient-specific sepsis risk which depends on the output of the transformer..." [2023Sepsis]

**Avoided:**
> We will apply advanced deep learning techniques to analyze the data.

---

## Dimension 3: Citation Philosophy

**Current calibration:** Superscript-integrated. The PI uses superscript numbered citations woven mid-sentence, not parenthetical [Author Year] format. Multiple sources per claim are standard, including ranges ("²,⁴²⁻⁴⁵"). Extensive self-citation establishes team credibility. Citations serve as evidence for specific performance metrics and epidemiological data, not as parenthetical afterthoughts.

**IMPORTANT NOTE FOR WRITERS:** The AI-generated Phase C drafts default to [Author Year] parenthetical format. This is wrong. The PI's actual style is superscript numbered (e.g., "can be lifesaving²,⁴²⁻⁴⁵ but are associated with high complication rates⁴⁶⁻⁴⁹"). All drafts must be converted to superscript format before review.

**Evidence:** Superscript format confirmed in 2024Cardiotoxic and 2025PostSurgery. 2023Sepsis uses inline brackets [#] — superscript is the majority style across the two more recent proposals and should be treated as the default.

**Preferred:**
> "Complex gastrointestinal (GI) surgical procedures (e.g., pancreaticoduodenectomy) can be lifesaving²,⁴²⁻⁴⁵ but are associated with high complication (e.g., anastomotic leaks, surgical site infections) rates⁴⁶⁻⁴⁹ with an overall incidence of moderate-to-severe complications of 30–40%.¹,⁵⁰,⁵¹" [2025PostSurgery]

**Avoided:**
> Several studies have examined sepsis prediction (Wang 2022, Chen 2023, Patel 2023, Kim 2021, Lee 2022, Rivera 2023).

---

## Dimension 4: Hedging Tolerance

**Current calibration:** Low hedging overall. "Will" for all committed actions and proposed methods. "Hypothesize," "expect," or "has the potential to" reserved for uncertain outcomes — specifically speculative clinical benefits and outcome predictions. The PI is notably confident about technical feasibility and method choices; hedging appears only where genuine uncertainty exists.

**Evidence:** Observed across all 3 proposals. Certain: "We will develop a human-centered AI system..." / "We will recruit..." Uncertain: "We hypothesize that the onset of sepsis can be predicted before its clinical recognition." [2023Sepsis] / "This integrated, continuous dataset has the potential to enhance AI models and enable earlier, more accurate complication detection." [2025PostSurgery]

**Preferred:**
> "This method is expected to significantly improve the performance of sepsis onset prediction." [2023Sepsis — hedging reserved for outcome prediction, not method description]

**Avoided:**
> This model may potentially be able to help detect some early AKI biomarker patterns that could possibly precede clinical diagnosis.

**Calibration note:** Hedging is asymmetric. Technical claims ("we will train," "we will compare") use "will" without qualification. Clinical outcome claims ("has the potential to," "we expect") use cautious language. Never hedge both in the same sentence.

---

## Dimension 5: Narrative Voice

**Current calibration:** First-person-plural with named team. "We/our" for all proposed work. Team members are named with their specific expertise areas. Prior collaboration history is explicitly quantified. Aims are described as "co-designed" with clinical practitioners, not just informed by them.

**Evidence:** Consistent across 2023Sepsis and 2025PostSurgery. The PI names individuals and their roles rather than describing the team generically.

**Preferred:**
> "Our experienced interdisciplinary team (Table 1) from The Ohio State University (OSU) and Northeastern University (NEU) will meet at least twice a month to ensure progress. Synergy of investigator: PI Zhang, MPI Cao, and MPI Wang have worked together on developing human-centered AI systems for healthcare for more than three years." [2025PostSurgery]

Also preferred:
> "Our team includes experts on deep learning (Zhang), human-AI collaboration (Wang), data visualization (Padilla), emergency medicine (Caterino), and critical care medicine (Exline). All Aims are endorsed and co-designed by practicing physicians." [2023Sepsis]

**Avoided:**
> Contextual inquiry sessions will be conducted with ICU nurses to map current alert-response workflows.

---

## Dimension 6: Interdisciplinary Framing

**Current calibration:** Clinical-workflow-first. The PI always starts with the clinical workflow or clinical need, then identifies how AI addresses specific gaps in that workflow. AI is framed as supporting clinical expertise, never replacing it. "Human-Centered AI (HCAI)" is the PI's explicit design philosophy and is named as such. The connection between AI capability and clinical decision point is always made explicit.

**Evidence:** Observed in all 3 proposals. The Sepsis proposal grounds the entire AI design in a four-step physician decision-making workflow. The Surgery proposal maps each AI capability to a specific clinical need. The Cardiotoxicity proposal frames the system as "HCAI system to support explainable human-AI decision-making."

**Preferred:**
> "Guided by the HAIC design philosophy, we start with an examination of physician's sepsis decision-making workflow: despite the decision making of sepsis shares some commonalities with others (e.g., roughly following the four-step workflow in Figure 1), it also has some unique characteristics, which present novel challenges for physicians to make a decision..." [2023Sepsis]

**Avoided:**
> Results from Aim 1 will inform Aim 2.

---

## Dimension 7: Reader Model

**Current calibration:** Dual-literacy assumed. The PI explains clinical context and disease burden for non-expert reviewers (mortality rates, complication definitions, clinical significance) but assumes ML/AI expertise throughout. Transformer, WCPH, AUROC, AUPRC, and Shapley values are never explained. Novel concepts that are distinctive to this PI's approach — HCAI design philosophy, RAG integration, participatory design methodology — receive detailed explanation. Standard clinical scoring systems (qSOFA, SOFA, MEWS) get brief parenthetical definitions on first use.

**Evidence:** Observed in 2023Sepsis and 2025PostSurgery. Sepsis explains "Sepsis is typically caused by the acute overwhelming response of the body to a systematic infection" but does not explain Transformer architecture. Surgery explains "anastomotic leaks, surgical site infections" but does not explain AUROC.

**Preferred:**
> "A value embedding will be used to map the observed clinical variables into vectors, and a variable attention module is followed to generate a fixed-size vector for each collection. The sequence of attention results and the time embeddings are sent to Transformer to generate a patient state vector, denoted as s(x^(i)) at time t_i." [2023Sepsis — no explanation of embeddings or attention; assumes ML literacy]

**Avoided:**
> We will use SUS to assess usability. (undefined acronym, no context)

Also avoided:
> We will use a survey to assess whether users think the system is easy to use. (too informal, no validated instrument named)

---

## Cross-Cutting Preferences

### Paragraph Length
**Current calibration:** Mix of short (2-3 sentences in Significance) and long (8-12 sentences in Approach methods). Surgery proposal uses slightly longer paragraphs (4-8 sentences average) than Sepsis. Short paragraphs are used for high-stakes claims that need to stand alone; long paragraphs for multi-step method descriptions.

### Transition Patterns
**Current calibration:** Content-specific bridges preferred over generic connectors. Observed transitions from the PI's proposals: "To address these challenges," "Guided by," "In summary," "Notably," "Building on," "While there is growing interest," "As illustrated in Figure X," "Collectively, these limitations..." Avoid starting consecutive paragraphs with the same word.

### Lists vs. Prose
**Current calibration:** Numbered lists for challenges, shortcomings, and innovation points. Prose for motivation and methods narrative. Surgery proposal uses more lists than Sepsis (numbered lists for shortcomings, innovation points, aims, tasks, and evaluation criteria). Bulleted lists should be rare and only for genuinely parallel items.

### Emphasis Patterns
**Current calibration:** Bold for system names (SepsAI, REACH-AI), aim titles, and key terms on first definition. Italics sparingly for genuine emphasis. Key phrases are repeated for rhetorical emphasis ("human-AI collaboration" in Sepsis, "multimodal" in Surgery). Never use ALL CAPS.

### Explanatory Insertions
**Current calibration:** When an inline explanation is needed, prefer these structures (in order):
1. **Relative clauses** (`which`, `who`, `that`) — best for explanations integral to the sentence logic. Example: "PREP-AI integrates wearable sensing, which captures physiological signals passively during preparation."
2. **Parenthetical asides** — best for supplementary detail the reader could skip. Example: "consumer wearables (Fitbit Sense 2 or Apple Watch) collecting accelerometry and heart rate."
3. **Appositive phrases** (brief, single-noun clarifications) — acceptable when short. Example: "the Boston Bowel Preparation Scale (BBPS), a validated measure of preparation adequacy, was used."

**Avoided:** Em-dash parenthetical insertions that interrupt sentence flow with long explanatory clauses. This pattern creates run-on structures that are hard to parse:
> wearable sensing — passive continuous sensing via consumer wearables (Fitbit Sense 2 or Apple Watch) collecting accelerometry, heart rate, HRV, and sleep staging data through HealthKit/Google Health Connect APIs — no additional hardware burden.

**Preferred rewrite:**
> Wearable sensing collects accelerometry, heart rate, HRV, and sleep staging data passively through consumer wearables (Fitbit Sense 2 or Apple Watch), which interface with HealthKit and Google Health Connect APIs. This approach requires no additional hardware burden.

---

## Feedback History

*This section is populated automatically by the evolution agent after each Draft Feedback Checkpoint.*

| Date | Project | Dimension | Change | Source |
|------|---------|-----------|--------|--------|
| 2026-03-05 | All | All 7 dimensions | Seeded from 3 prior R01 proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery) | Proposal analysis |

---

*Last updated: 2026-03-05. Seeded from PI's prior R01 proposals. This file improves after every project through user feedback.*
