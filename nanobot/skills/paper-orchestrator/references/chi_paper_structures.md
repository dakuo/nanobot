# CHI Paper Structures by Contribution Type

This reference defines canonical section structures for the 7 CHI contribution types. Use the structure matching your paper's `contribution_type` in `paper_project.yaml`. Word budgets assume a 10-page CHI paper (~7,500 words excluding references).

---

## 1. Empirical (User Study / Field Study / Experiment)

The most common CHI contribution type. Reports findings from studies with human participants.

**Canonical sections:**
| Section | Required | Word budget |
|---------|----------|-------------|
| Abstract | Yes | 150 |
| Introduction | Yes | 800 |
| Related Work | Yes | 1,200 |
| Method | Yes | 1,500 |
| Results / Findings | Yes | 2,000 |
| Discussion | Yes | 1,200 |
| Limitations | Yes | 300 |
| Conclusion | Yes | 350 |

**What reviewers expect:**
- Clear research questions or hypotheses stated in the introduction.
- Rigorous study design with justified participant count (power analysis for quantitative; saturation argument for qualitative).
- Transparent reporting of methods (replicability for quant; audit trail for qual).
- Results that directly address the stated research questions.
- Discussion that interprets findings, not just restates them.
- Honest limitations section that acknowledges threats to validity.

**Common mistakes:**
- Burying the research question deep in the introduction instead of stating it early and clearly.
- Conflating results and discussion. Keep findings separate from interpretation.
- Over-claiming generalizability from a small or homogeneous sample.
- Missing ethical considerations (IRB, informed consent, data handling).

---

## 2. Artifact (System / Tool / Prototype)

Second most common. Presents a novel interactive system, tool, or design.

**Canonical sections:**
| Section | Required | Word budget |
|---------|----------|-------------|
| Abstract | Yes | 150 |
| Introduction | Yes | 800 |
| Related Work | Yes | 1,000 |
| Design Goals / Requirements | Yes | 600 |
| System Description | Yes | 1,800 |
| Implementation | Optional | 500 |
| Evaluation | Yes | 1,500 |
| Discussion | Yes | 800 |
| Limitations & Future Work | Yes | 350 |
| Conclusion | Yes | 300 |

**What reviewers expect:**
- Clear articulation of the design space and why existing tools are insufficient.
- Design rationale tied to literature or formative studies.
- System description detailed enough to understand the key technical contributions.
- Evaluation that demonstrates the system works AND provides insight (not just "users liked it").
- Discussion of design trade-offs and lessons learned.

**Common mistakes:**
- All system description, no evaluation. CHI requires evaluation, not just a demo.
- Evaluation that only measures usability without assessing the core contribution.
- Missing design rationale: "we built X" without "because Y informed by Z".
- Over-engineering implementation details at the expense of design insight.

---

## 3. Methodological (New Research or Design Method)

Introduces a new method for studying or designing interactive systems.

**Canonical sections:**
| Section | Required | Word budget |
|---------|----------|-------------|
| Abstract | Yes | 150 |
| Introduction | Yes | 800 |
| Related Work / Background | Yes | 1,200 |
| Method Description | Yes | 2,000 |
| Validation / Application | Yes | 1,500 |
| Discussion | Yes | 1,000 |
| Guidance for Practitioners | Optional | 500 |
| Limitations | Yes | 300 |
| Conclusion | Yes | 300 |

**What reviewers expect:**
- Clear gap in existing methodological toolkit that justifies the new method.
- Detailed, reproducible method description that others can follow.
- Validation through application (at least one case study, ideally comparison with existing methods).
- Honest assessment of when the method works and when it does not.
- Practical guidance for adoption.

**Common mistakes:**
- Proposing a method without validating it. Theoretical description alone is insufficient.
- No comparison to existing alternatives. Reviewers want to know why this over established approaches.
- Overly abstract description. Need concrete steps and decision points.

---

## 4. Theoretical (Framework / Model / Concept)

Advances understanding through new conceptual frameworks, models, or theoretical contributions.

**Canonical sections:**
| Section | Required | Word budget |
|---------|----------|-------------|
| Abstract | Yes | 150 |
| Introduction | Yes | 900 |
| Background / Related Theory | Yes | 1,500 |
| Theoretical Framework | Yes | 2,200 |
| Application / Illustration | Yes | 1,200 |
| Discussion / Implications | Yes | 1,000 |
| Limitations | Yes | 300 |
| Conclusion | Yes | 300 |

**What reviewers expect:**
- Strong grounding in existing theory with clear identification of the gap.
- The framework must be more than a literature review; it must synthesize and generate new understanding.
- At least one concrete application or illustration showing the framework in use.
- Implications for both research and practice.
- Engagement with potential counter-arguments.

**Common mistakes:**
- Presenting a literature review as a theoretical contribution. Synthesis is required, not just aggregation.
- Framework too abstract to be actionable. Needs concrete dimensions, categories, or relationships.
- No illustration of application. Reviewers need to see how the framework works in practice.

---

## 5. Survey / Literature Review (Systematic Review)

Provides a comprehensive survey or systematic review of a research area.

**Canonical sections:**
| Section | Required | Word budget |
|---------|----------|-------------|
| Abstract | Yes | 150 |
| Introduction | Yes | 700 |
| Review Methodology | Yes | 1,000 |
| Results / Taxonomy | Yes | 3,000 |
| Discussion / Research Agenda | Yes | 1,500 |
| Limitations | Yes | 300 |
| Conclusion | Yes | 350 |

**What reviewers expect:**
- Rigorous, reproducible search methodology (databases, queries, inclusion/exclusion criteria, PRISMA flow).
- Complete coverage of the target area with quantified corpus statistics.
- Analytical synthesis: taxonomy, themes, or framework emerging from the review.
- Forward-looking research agenda identifying gaps and opportunities.
- The review must advance understanding beyond what individual papers provide.

**Common mistakes:**
- Incomplete search methodology: missing databases, date ranges, or exclusion criteria.
- Descriptive rather than analytical, listing papers without synthesizing themes.
- No research agenda. A review without forward-looking implications has limited value.
- Outdated corpus: missing recent key papers is a red flag.

---

## 6. Opinion / Argument (alt.CHI Style)

Presents a provocative argument, position, or critical analysis. Often submitted to the alt.CHI venue.

**Canonical sections:**
| Section | Required | Word budget |
|---------|----------|-------------|
| Abstract | Yes | 150 |
| Introduction / Provocation | Yes | 1,000 |
| Background / Context | Yes | 1,200 |
| Argument | Yes | 2,500 |
| Implications | Yes | 1,500 |
| Conclusion | Yes | 400 |

**What reviewers expect:**
- A clear, provocative thesis stated early.
- Well-grounded argument (not opinion without evidence).
- Engagement with opposing viewpoints, steel-man the counter-position.
- Concrete implications for the CHI community's research or practice.
- Compelling writing that holds the reader's attention.

**Common mistakes:**
- Provocation without substance, being controversial is not enough; the argument must be well-reasoned.
- Ignoring counter-arguments, one-sided arguments are easily dismissed.
- Too broad, focus on a specific, defensible claim rather than trying to critique an entire field.

---

## 7. Benchmark / Dataset

Introduces a new benchmark, evaluation set, or publicly released dataset for the HCI community.

**Canonical sections:**
| Section | Required | Word budget |
|---------|----------|-------------|
| Abstract | Yes | 150 |
| Introduction | Yes | 700 |
| Related Work / Existing Benchmarks | Yes | 800 |
| Dataset Description | Yes | 2,000 |
| Collection Methodology | Yes | 1,200 |
| Baseline Evaluations | Yes | 1,200 |
| Ethical Considerations | Yes | 400 |
| Discussion / Usage Guidelines | Yes | 600 |
| Conclusion | Yes | 300 |

**What reviewers expect:**
- Clear gap in existing benchmarks/datasets that justifies a new one.
- Transparent collection methodology with ethical review documentation.
- Sufficient scale and diversity to be useful to the community.
- Baseline evaluations demonstrating the dataset's utility and difficulty.
- Data availability plan (anonymized access, licensing, long-term hosting).
- Ethical considerations: consent, privacy, potential for misuse.

**Common mistakes:**
- Dataset too small or narrow to generalize, reviewers want community-scale resources.
- Missing baselines, a dataset without baseline results has limited immediate utility.
- Inadequate documentation, metadata, codebook, and usage guidelines are essential.
- No ethical review or consent documentation for human-generated data.
