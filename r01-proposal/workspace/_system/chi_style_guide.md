# CHI/CSCW/UIST/UbiComp Writing Conventions Guide
## HCI Paper Pipeline — Shared Reference

> **This file evolves — updated after each project based on reviewer feedback and accepted paper patterns.**
> All paper-writer and paper-reviewer skills must read this file before generating or evaluating any section.
> Do not override these conventions without explicit user instruction.

---

## 1. Voice and Tone

**Register:** Formal academic, but more accessible than NIH grant writing. HCI papers are read by a broad interdisciplinary audience — assume expertise in HCI methods but not in your specific application domain.

**Person:** First person plural ("We conducted," "We found," "Our system") is standard and expected. Third person is used only for self-citations during anonymous review (see Section 3).

**Active vs. Passive:** Active voice is strongly preferred. Passive is acceptable for describing study procedures where the agent is genuinely irrelevant ("Participants were recruited via..."). Never use passive to soften claims or obscure methodology choices.

**Hedging:** Use appropriate epistemic hedging for qualitative and exploratory findings. "Suggests," "may," "could," and "appears to" are correct for interview findings and design implications. Do not overclaim causality from correlational or qualitative data. Do not under-hedge quantitative results — report confidence intervals and effect sizes.

**Jargon Policy:** Define HCI-specific methods on first use (e.g., "contextual inquiry, a field research method in which..."). Define domain-specific terms from your application area. Do not assume reviewers share your subdomain.

**Tone Calibration by Section:**
- Introduction: Engaging, motivating, clear problem statement. Draw the reader in.
- Related Work: Authoritative, synthetic, critical. Not a list of summaries.
- Method: Precise, transparent, replicable. Justify every design choice.
- Findings: Grounded, evidence-rich, organized. Let the data speak.
- Discussion: Interpretive, honest about limitations, connected to prior work.
- Implications for Design: Concrete, actionable, grounded in findings.
- Conclusion: Crisp summary. No new claims.

---

## 2. ACM Citation Format

**Inline citations:** Use author-year format in parentheses: [Smith 2023] or [Smith and Jones 2023] or [Smith et al. 2023] for three or more authors. Place citations at the end of the relevant clause, before the period.

**Multiple citations:** List in chronological order, separated by semicolons: [Brown 2019; Smith 2021; Jones 2023].

**Reference list format:** Follow ACM Reference Format exactly. The acmart LaTeX template enforces this automatically. Key patterns:

- Conference paper: Author(s). Year. Title. In *Proceedings of Conference Name (ACRONYM 'YY)*, pages. ACM. https://doi.org/...
- Journal article: Author(s). Year. Title. *Journal Name* Vol, Issue (Month Year), pages. https://doi.org/...
- Book: Author(s). Year. *Title*. Publisher, City.
- Thesis: Author. Year. *Title*. PhD Dissertation / Master's Thesis. Institution.

**DOIs:** Include DOIs for all references where available. Use the https://doi.org/ prefix.

**arXiv preprints:** Cite as: Author(s). Year. Title. *arXiv preprint arXiv:XXXX.XXXXX*. Acceptable for methods and systems work; avoid as primary evidence for empirical claims.

**Self-citation during anonymous review:** See Section 3.

---

## 3. Double-Blind Anonymization Rules

CHI, CSCW, UIST, DIS, and UbiComp/IMWUT all use double-blind review. Violations are grounds for desk rejection.

**What to anonymize:**
- Author names and affiliations everywhere in the paper body
- Acknowledgments section (omit entirely or write "Omitted for blind review")
- IRB protocol numbers that identify your institution
- System names that are publicly associated with your lab (use a generic name like "our system" or a pseudonym)
- GitHub/OSF/project URLs that identify the authors (use "https://anonymized.for.review" as placeholder)
- Funding acknowledgments (omit entirely)

**Self-citation rules:**
- Cite your own prior work in third person: "Smith et al. [2022] showed..." not "In our prior work [Smith 2022]..."
- Do not omit self-citations entirely — reviewers need to assess novelty relative to your prior work
- If a self-citation is essential but would reveal identity, write "[AUTHOR 20XX]" as a placeholder and note "citation anonymized for review" in a footnote
- Do not cite unpublished work from your lab that would identify you

**Supplementary materials:**
- Anonymize all supplementary files (study instruments, codebooks, video probes)
- Remove metadata from PDFs and videos (author fields, institution names)
- Use generic filenames (supplement_A.pdf, not smith_chi2027_codebook.pdf)

**Common violations to check before submission:**
- "As we showed in [Smith 2023]..." (first person self-citation)
- Acknowledgments left in
- System named after the lab ("The CMU HealthBot system")
- GitHub URL with username in path
- IRB number containing institution abbreviation

---

## 4. Contribution Statement Conventions

Every HCI paper must state its contribution explicitly. Reviewers score papers on contribution clarity.

**In the abstract:** State the contribution in the final 1-2 sentences. "We contribute X, which enables Y." Do not leave reviewers to infer the contribution.

**In the introduction:** Enumerate contributions explicitly, typically as a bulleted list near the end of the introduction. Standard framing:

> This paper makes the following contributions:
> - An empirical study of [N participants / context] revealing [key finding]
> - [System/framework/method name], a [type of artifact] that [what it does]
> - Design implications for [target design space]

**Contribution types and their standard phrasings:**
- Empirical: "An empirical study of...", "Findings from a [N]-participant [study type] revealing..."
- Artifact: "The design and implementation of [system name], a [type] that...", "An open-source [tool] for..."
- Methodological: "A [method/framework] for...", "A validated instrument for measuring..."
- Theoretical: "A conceptual framework for understanding...", "A taxonomy of..."
- Survey: "A systematic review of N papers on...", "A synthesis of..."

**Do not:** Describe contributions as "this paper presents" or "this paper explores" — these are process descriptions, not contribution claims. State what the reader gains.

---

## 5. Implications for Design Section Conventions

"Implications for Design" (sometimes titled "Design Implications" or "Design Guidelines") is a standard section at CHI and CSCW. It is frequently criticized in reviews. Follow these rules:

**Must connect to specific findings:** Every implication must trace back to a specific finding, quote, or observation from your study. Write the connection explicitly: "Drawing from our finding that participants [X], we suggest that systems should [Y]."

**Not speculative:** Do not write implications that could have been written without your study. "Systems should be easy to use" is not an implication — it's a truism. "Systems should surface [specific information] at [specific moment] because participants consistently [specific behavior]" is an implication.

**Scope appropriately:** Implications should be scoped to the design space your study actually informs. A study of 12 clinicians at one hospital does not generate implications for "all healthcare AI systems." Scope to "AI-assisted triage tools in emergency department settings."

**Format:** 3-6 implications is typical. Each should be 2-4 sentences: one sentence stating the implication, 1-2 sentences grounding it in findings, one sentence on how designers might act on it.

**Avoid:** Numbered lists of one-sentence implications with no grounding. Implications that are really just restatements of findings. Implications that contradict each other without acknowledging the tension.

---

## 6. Research Question Conventions

**State RQs explicitly:** HCI papers at CHI and CSCW are expected to state research questions explicitly, typically in the introduction or at the start of the method section. Do not leave reviewers to infer your RQs from the method.

**Number and scope:** 2-4 RQs is standard. One RQ is usually too narrow for a full paper; five or more suggests the paper is unfocused.

**Format:** "RQ1: [Question]?" Use consistent formatting. RQs should be answerable by your method — if your RQ asks "why" but your method is a survey, there's a mismatch.

**Alignment check:** Every RQ must be addressed in the Findings section. Every major finding should connect to at least one RQ. Reviewers will check this alignment.

**Avoid:** RQs that are too broad ("How do people use technology?"), too narrow to warrant a full paper ("What color do users prefer for the button?"), or that presuppose the answer ("How does our system improve outcomes?").

---

## 7. Hedging Language Norms

HCI papers must calibrate epistemic claims to the strength of evidence. Miscalibration — either overclaiming or underclaiming — is a common review criticism.

**For qualitative findings (interviews, observations, diary studies):**
- Use: "suggests," "indicates," "participants described," "we observed," "themes included"
- Avoid: "proves," "demonstrates," "shows that," "confirms"
- Correct: "Our findings suggest that clinicians may experience alert fatigue differently depending on their role."
- Incorrect: "Our findings show that alert fatigue is caused by role differences."

**For quantitative findings (controlled experiments, surveys with N>30):**
- Report effect sizes and confidence intervals, not just p-values
- Use: "significantly improved" (with statistics), "outperformed" (with comparison), "was associated with"
- Avoid: "dramatically," "substantially," "greatly" without quantification

**For design implications:**
- Use: "may benefit from," "could consider," "we suggest," "one approach would be"
- Avoid: "must," "should always," "will improve" (unless you have evidence)

**For generalizability:**
- Be explicit about scope: "within our study context," "for the population we studied," "in similar settings"
- Do not generalize beyond your sample without acknowledging the limitation

---

## 8. N= Reporting

Always report participant counts explicitly. Reviewers will flag missing N= values.

**In the abstract:** Include N= for the primary study. "We conducted semi-structured interviews with 18 emergency physicians."

**In the method section:** Report N= for every participant group. Report demographics (age range or mean, gender distribution, relevant expertise). For studies with multiple phases, report N= for each phase separately.

**In findings:** When reporting themes or patterns, indicate how many participants expressed them. "Most participants (14/18) described..." or "Several participants (n=5) noted..." Avoid vague quantifiers ("many," "some," "a few") without counts.

**For system evaluations:** Report N= for each condition. Report attrition and reasons. Report final N= used in analysis if different from recruited N=.

**Minimum sample size norms (approximate, venue-dependent):**
- Formative/exploratory interviews: 8-15 is acceptable; justify if fewer
- Summative usability study: 20+ for quantitative claims; 5-8 for qualitative usability
- Survey: 50+ for descriptive; 100+ for inferential statistics
- Controlled experiment: Power analysis required; typically 20+ per condition
- Longitudinal deployment: 5+ households or organizations; duration matters more than N

---

## 9. Figure Caption Conventions

Captions must be self-contained. A reviewer should understand the figure without reading the surrounding text.

**Caption structure:**
1. **Bold figure title** — one sentence stating what the figure shows or its main takeaway
2. Description of what is depicted (study context, system components, data type)
3. Key result or design rationale (one sentence)
4. Statistical notation if applicable (N=, p<, effect size)

**Example (study figure):**
> **Figure 2. Participants' reported workload increased significantly during the handoff phase.** NASA-TLX scores (0-100) across three workflow phases for 24 ICU nurses. Workload peaked during patient handoff (M=72.3, SD=11.4), significantly higher than documentation (M=48.1, p<0.001, d=1.8) and monitoring phases (M=51.6, p<0.01).

**Example (system figure):**
> **Figure 3. The dashboard surfaces patient risk scores alongside the clinical evidence driving each prediction.** The left panel shows the patient list sorted by predicted deterioration risk; the right panel shows the top contributing factors for the selected patient, drawn from the prior 24 hours of vitals and lab values. This design emerged from clinician feedback that unexplained scores were not actionable.

**Rules:**
- Every figure must be referenced in the text before it appears
- Do not say "the figure above/below" — use numbered references: "(Figure 3)"
- Screenshots must be legible at print resolution (300 DPI minimum)
- Redact any identifying information from screenshots (patient names, institution names)
- Use alt text for accessibility in the camera-ready submission

---

## 10. Signposting Conventions

HCI papers use explicit signposting to guide readers through the argument. This is expected, not considered redundant.

**Section openings:** Begin each major section with 1-2 sentences stating what the section covers and why. "In this section, we describe our study design, including participant recruitment, data collection procedures, and analysis approach."

**Subsection transitions:** End subsections with a brief forward pointer when the connection to the next subsection is not obvious. "Having established the study context, we now describe the analysis procedure."

**Findings organization:** State the organizing principle at the start of the Findings section. "We present findings organized around our three research questions. For each RQ, we describe the primary themes that emerged from analysis."

**Avoid:** Starting every paragraph with "Furthermore," "Moreover," or "Additionally." Use content-specific transitions that carry meaning.

---

## 11. Venue-Specific Notes

### CHI (ACM CHI Conference on Human Factors in Computing Systems)
- Broadest HCI venue. Values contribution diversity — empirical, artifact, theoretical, and methodological papers all have a home.
- Contribution statement must be explicit. Reviewers are instructed to score "contribution to HCI knowledge."
- "Implications for Design" section is expected for empirical papers.
- Papers Without Study (PWS) track accepts theoretical and opinion contributions without empirical data.
- Word limit: ~9,500 words for full papers (10 pages + references in the new format). Check the current CFP — limits change.
- Review criteria: Contribution, Rigor, Presentation, Significance.

### CSCW (ACM Conference on Computer-Supported Cooperative Work and Social Computing)
- Emphasizes social and organizational contexts of technology use. Values field studies, ethnography, and sociotechnical analysis.
- Stronger expectation for longitudinal or in-situ data compared to CHI.
- "Implications for Design" should address collaborative or organizational design, not just individual UX.
- Journal-style review process (rolling deadlines, multiple rounds).
- Word limit: ~9,500 words. Check current CFP.
- Review criteria: Contribution, Rigor, Presentation, Significance (same as CHI but with CSCW-specific rubric).

### UIST (ACM Symposium on User Interface Software and Technology)
- Systems and interaction techniques venue. Artifact contributions are primary.
- Technical novelty is the primary criterion. "What can users do now that they couldn't before?"
- Evaluation must demonstrate the system works, not just that users prefer it. Include performance benchmarks, task completion rates, or expert evaluation.
- Video figure is expected and heavily weighted. The video should demonstrate the system in use.
- Word limit: ~10 pages. Check current CFP.
- Review criteria: Technical contribution, System novelty, Evaluation quality.

### UbiComp/IMWUT (ACM International Joint Conference on Pervasive and Ubiquitous Computing / Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies)
- Emphasizes real-world deployment, sensing systems, and mobile/wearable computing.
- Deployment studies are valued over lab studies. "Did you deploy this in the real world?"
- Technical sensing contributions (new sensors, signal processing, inference methods) are primary.
- Evaluation should include real-world performance metrics (accuracy in the wild, battery life, latency).
- Journal-style review process (quarterly deadlines).
- Word limit: ~10 pages. Check current CFP.
- Review criteria: Technical contribution, Deployment/evaluation, Novelty.

### DIS (ACM Designing Interactive Systems)
- Values design quality, critical perspectives, and provocation alongside empirical rigor.
- "Provocation" and "pictorial" submission types are unique to DIS — these have different conventions.
- Critical and reflective framing is expected. "What does this design reveal about values, power, or assumptions?"
- Research through Design (RtD) is a legitimate methodology at DIS.
- Word limit: ~10 pages for full papers; pictorials have different format requirements.
- Review criteria: Design quality, Critical perspective, Contribution to design knowledge.

---

## 12. Word Count Guidelines

**Short papers (Notes, Late-Breaking Work, Extended Abstracts):**
- Word limit: 3,000-5,000 words (venue-dependent)
- Typically 4 pages in the ACM format
- Contribution scope is narrower — one focused finding or system feature
- "Implications for Design" is optional but appreciated
- Abstract: 150 words (same limit as full papers)

**Standard full papers:**
- Word limit: 7,000-10,000 words depending on venue and year (always check the current CFP)
- CHI 2025 moved to a page-limit format (10 pages + references); word count is approximate
- Target 9,000 words for the body; references are not counted
- Do not pad to hit the limit — reviewers notice

**Journal papers (IMWUT, CSCW journal track):**
- No strict word limit, but 10,000-14,000 words is typical
- More space for related work, method detail, and discussion
- Multiple study phases are expected to justify the length

---

## 13. Abstract Word Limit

**150 words is the hard limit for ACM metadata abstracts.** This is enforced by the ACM submission system. The abstract that appears in the ACM Digital Library and on the conference website must be 150 words or fewer.

The paper PDF may include a slightly longer abstract (some venues allow up to 250 words in the PDF), but the metadata abstract submitted to the system must be 150 words.

**Abstract structure (150 words):**
- 1-2 sentences: problem and motivation
- 1-2 sentences: approach or study design (include N=)
- 2-3 sentences: key findings or system capabilities
- 1-2 sentences: contribution and significance

Do not include citations in the abstract.

---

## 14. Section Formatting

**Template:** Use the official `acmart` LaTeX template. Download from ACM or the venue website. Do not use unofficial templates.

**Review submission (1-column):** Most venues require 1-column format for review to improve readability. The `acmart` template supports this with `\documentclass[manuscript,review,anonymous]{acmart}`.

**Camera-ready (2-column):** Final submissions use 2-column format: `\documentclass[sigconf]{acmart}`.

**Font and spacing:** Do not modify the default font (Linux Libertine), size (9pt body), or line spacing. ACM will reject papers that deviate from template defaults.

**Figures in 2-column:** Use `figure*` environment for full-width figures. Use `figure` for single-column figures. Place figures at the top or bottom of columns, not in the middle of text.

**Section hierarchy:** Use `\section`, `\subsection`, and `\subsubsection`. Avoid going deeper than three levels. If you need a fourth level, restructure.

**Anonymization in LaTeX:** The `anonymous` option in `acmart` automatically suppresses author information. Use it for review submissions.

---

*Last updated: System initialization. Update this file after each completed project with lessons learned from reviewer feedback.*
