# HCI Paper Section Specifications
## Organized by Contribution Type

> This file defines required sections, word targets, quality criteria, and common pitfalls for each contribution type.
> The paper-outline and paper-writer skills read this file to generate appropriate section structures.
> The paper-reviewer skills use the quality criteria and pitfalls sections when evaluating drafts.

---

## How to Use This File

1. Find your `contribution_type` from `project.yaml`
2. Use the section structure as the default outline
3. Sections marked **Required** must be present; sections marked **Optional** can be omitted with justification
4. Word targets are for a standard 9,000-word full paper — scale proportionally for short papers
5. Quality criteria are the specific things reviewers check for that contribution type

---

## Contribution Type 1: Empirical

**Definition:** Papers whose primary contribution is new knowledge about people, practices, or phenomena, generated through systematic data collection and analysis. Includes qualitative studies (interviews, observations, diary studies, ethnography), quantitative studies (surveys, experiments, log analysis), and mixed-methods studies.

**Most common at:** CHI, CSCW, UbiComp/IMWUT, DIS

### Section Structure

| Section | Status | Word Target | Notes |
|---------|--------|-------------|-------|
| Abstract | Required | 150 | Include N=, method type, key finding |
| Introduction | Required | 1,200-1,500 | Problem, motivation, RQs, contribution list |
| Related Work | Required | 1,800-2,200 | Position against prior empirical work; end with gap |
| Method | Required | 2,000-2,500 | Study design, participants, procedure, analysis |
| Findings | Required | 2,200-2,800 | Organized by theme or RQ; evidence-rich |
| Discussion | Required | 1,200-1,500 | Interpret findings, connect to prior work |
| Implications for Design | Required | 700-900 | Grounded, specific, scoped |
| Limitations | Required | 400-600 | Honest scope; do not bury in Discussion |
| Conclusion | Required | 400-500 | Summary and future directions |
| Acknowledgments | Optional | 50-100 | Omit for anonymous review |
| References | Required | No limit | ACM format |

**Total body target:** 9,000 words (excluding abstract and references)

### Method Section Requirements

The Method section is the most scrutinized section for empirical papers. It must include:

- **Study design:** What type of study (interview, survey, experiment, deployment, diary study, etc.) and why this design fits the RQs
- **Participants:** N=, recruitment strategy, inclusion/exclusion criteria, demographics (age, gender, relevant expertise), compensation
- **Data collection:** Procedure, instruments used (interview guide, survey instrument, logging system), duration, setting (lab, remote, in-situ)
- **Data analysis:** Specific method (thematic analysis, grounded theory, statistical tests), who conducted analysis, inter-rater reliability if applicable, member checking if applicable
- **Ethical considerations:** IRB approval status, informed consent procedure, data handling

For qualitative studies, describe the analytic approach in enough detail that a reader could replicate it. "We conducted thematic analysis" is insufficient. Specify: initial coding, code refinement, theme development, and how disagreements were resolved.

For quantitative studies, report power analysis or justify sample size. Specify all statistical tests used and the alpha level.

### Findings Section Requirements

- Organize by theme, RQ, or phase — state the organizing principle at the start
- Every theme or finding must be supported by evidence (quotes for qualitative, statistics for quantitative)
- Quotes must include participant identifier (P1, P3, etc.) and enough context to be interpretable
- Report how many participants expressed each theme (e.g., "14 of 18 participants described...")
- Do not interpret in Findings — save interpretation for Discussion
- Use subheadings for each major theme or RQ

### Quality Criteria (Reviewer Checklist)

- [ ] RQs are stated explicitly and the method can answer them
- [ ] N= is reported for all participant groups
- [ ] Participant demographics are reported
- [ ] Analysis procedure is described in replicable detail
- [ ] Findings are grounded in evidence (quotes, counts, examples)
- [ ] Implications connect to specific findings (not generic)
- [ ] Limitations are honest and specific (not just "small sample size")
- [ ] Contribution is stated explicitly in introduction and abstract

### Common Pitfalls

**Pitfall 1: RQ-method mismatch.** Asking "why" questions but using a survey. Asking "how many" questions but using interviews. Reviewers will flag this immediately.

**Pitfall 2: Thin method description.** "We conducted semi-structured interviews" with no detail on the guide, duration, or analysis. Reviewers cannot assess rigor without this information.

**Pitfall 3: Findings that are just summaries.** Reporting what participants said without synthesizing into themes or patterns. Findings should reveal something that wasn't obvious before the study.

**Pitfall 4: Generic implications.** "Systems should be easy to use" or "designers should consider user needs." Every implication must trace to a specific finding.

**Pitfall 5: Overclaiming from small samples.** "Users prefer X" from N=12 interviews. Scope claims appropriately: "Participants in our study described a preference for X."

**Pitfall 6: Burying limitations.** One sentence at the end of Discussion. Limitations deserve their own section and honest treatment.

---

## Contribution Type 2: Artifact

**Definition:** Papers whose primary contribution is a designed system, tool, prototype, technique, or design artifact. The artifact itself is the contribution; empirical evaluation demonstrates its value.

**Most common at:** CHI, UIST, UbiComp/IMWUT

### Section Structure

| Section | Status | Word Target | Notes |
|---------|--------|-------------|-------|
| Abstract | Required | 150 | Name the system, state what it enables, summarize evaluation |
| Introduction | Required | 1,200-1,500 | Problem, design space, system overview, contribution list |
| Related Work | Required | 1,500-2,000 | Prior systems, design space analysis, gap |
| Design | Required | 1,500-2,000 | Design goals, rationale, key design decisions |
| System / Implementation | Required | 1,500-2,000 | Architecture, key technical components, implementation details |
| Evaluation | Required | 1,800-2,200 | Study design, participants, results |
| Discussion | Required | 1,000-1,200 | Lessons learned, limitations, generalizability |
| Conclusion | Required | 400-500 | Summary and future work |
| Acknowledgments | Optional | 50-100 | Omit for anonymous review |
| References | Required | No limit | ACM format |

**Total body target:** 9,000 words (excluding abstract and references)

**Note on "Design" vs. "System" sections:** Some artifact papers combine these into one section; others separate design rationale from implementation details. Separate them when the design decisions are complex enough to warrant their own argument. Combine them for simpler systems where design and implementation are tightly coupled.

### Design Section Requirements

The Design section must articulate:

- **Design goals:** What properties should the system have? Derive these from the problem analysis, not from the system you built.
- **Design rationale:** Why did you make the key design decisions? What alternatives did you consider and reject?
- **Design process:** How did you arrive at the current design? (Formative study, design iterations, expert feedback, etc.)
- **Design space:** Where does this system sit relative to prior work? What design dimensions does it explore?

Do not describe what the system does in the Design section — that belongs in System/Implementation. The Design section explains why.

### System/Implementation Section Requirements

- Describe the system architecture at a level that allows replication or extension
- Include a system figure showing the architecture or key interface components
- Specify key technical components, algorithms, or data structures
- Report implementation details (platform, language, key libraries) if relevant to reproducibility
- Include a usage scenario or walkthrough that demonstrates the system in action

### Evaluation Section Requirements

Artifact papers must evaluate the system. Acceptable evaluation approaches (in rough order of strength):

1. **Controlled user study:** Participants complete tasks with the system; compare to baseline
2. **In-the-wild deployment:** Real users use the system over time; collect usage logs and interviews
3. **Expert evaluation:** Domain experts assess the system against criteria
4. **Technical evaluation:** Benchmark performance, accuracy, latency, resource usage
5. **Usage scenario + expert walkthrough:** Weakest; acceptable only for early-stage systems

For CHI and CSCW, user studies are expected. For UIST, technical evaluation plus a user study is standard. For UbiComp, deployment studies are preferred.

### Quality Criteria (Reviewer Checklist)

- [ ] Design goals are stated explicitly and derived from the problem
- [ ] Key design decisions are justified (not just described)
- [ ] System figure is included and legible
- [ ] Evaluation demonstrates the system works for real users or tasks
- [ ] Comparison to baseline or prior systems is included
- [ ] Limitations of the current implementation are acknowledged
- [ ] Contribution is clearly the system, not just the study findings

### Common Pitfalls

**Pitfall 1: System description without design rationale.** Describing what the system does without explaining why it was designed that way. Reviewers want to understand the design thinking, not just the output.

**Pitfall 2: Weak evaluation.** A usage scenario with no user data. "We showed the system to 3 experts who thought it was interesting." This is insufficient for a full paper.

**Pitfall 3: Contribution confusion.** Is the contribution the system or the study findings? Artifact papers should foreground the system. If the study findings are the main contribution, reconsider the contribution type.

**Pitfall 4: Missing baseline.** Evaluating the system without comparing it to anything. "Users completed tasks in 45 seconds" means nothing without a comparison.

**Pitfall 5: Overpromising in design goals.** Setting design goals the system doesn't actually meet, then not acknowledging the gap in Discussion.

**Pitfall 6: Implementation details without architecture.** Listing technologies used without explaining how they fit together. Include a system architecture figure.

---

## Contribution Type 3: Methodological

**Definition:** Papers whose primary contribution is a new method, framework, measurement instrument, or research approach that other researchers can use. The method itself is the contribution; a demonstration study shows it works.

**Most common at:** CHI, CSCW, UbiComp/IMWUT

### Section Structure

| Section | Status | Word Target | Notes |
|---------|--------|-------------|-------|
| Abstract | Required | 150 | Name the method, state what it enables, summarize validation |
| Introduction | Required | 1,200-1,500 | Problem with existing methods, proposed approach, contribution |
| Related Work | Required | 1,500-2,000 | Prior methods, their limitations, gap |
| Method Description | Required | 2,000-2,500 | Detailed description of the new method |
| Validation / Demonstration | Required | 2,000-2,500 | Study showing the method works |
| Discussion | Required | 1,000-1,200 | When to use this method, limitations, comparison to alternatives |
| Conclusion | Required | 400-500 | Summary and future work |
| References | Required | No limit | ACM format |

**Total body target:** 9,000 words

### Method Description Requirements

- Describe the method in enough detail that another researcher could apply it
- Include a step-by-step procedure or protocol
- Specify required materials, expertise, or tools
- Describe how to analyze or interpret the outputs
- Include worked examples where helpful

### Validation Requirements

A methodological contribution must demonstrate that the method works. Acceptable approaches:

- **Comparative validation:** Apply the new method and an existing method to the same data; show the new method reveals something the old one missed
- **Reliability study:** Show the method produces consistent results across raters or applications
- **Sensitivity analysis:** Show the method can detect differences that matter
- **Application study:** Apply the method to a real research question and show it produces useful insights

### Quality Criteria (Reviewer Checklist)

- [ ] The method is described in replicable detail
- [ ] The problem with existing methods is clearly articulated
- [ ] Validation demonstrates the method works
- [ ] Limitations and appropriate use cases are discussed
- [ ] The method is accessible to the target audience (not just the authors)

### Common Pitfalls

**Pitfall 1: Method description without validation.** Proposing a method without showing it works. Even a small demonstration study is required.

**Pitfall 2: Reinventing existing methods.** Proposing a "new" method that is essentially an existing method with minor modifications, without acknowledging the prior work.

**Pitfall 3: Overly narrow applicability.** A method that only works for the specific study the authors conducted. Discuss generalizability explicitly.

---

## Contribution Type 4: Theoretical

**Definition:** Papers whose primary contribution is a conceptual framework, design theory, taxonomy, or theoretical lens that advances understanding of a phenomenon or design space. No empirical data collection required, but the framework must be grounded in prior work.

**Most common at:** CHI, CSCW, DIS

### Section Structure

| Section | Status | Word Target | Notes |
|---------|--------|-------------|-------|
| Abstract | Required | 150 | Name the framework/theory, state what it explains or enables |
| Introduction | Required | 1,200-1,500 | Problem, motivation, contribution |
| Related Work | Required | 2,000-2,500 | Extensive grounding in prior work; the framework synthesizes this |
| Framework / Theory | Required | 2,500-3,000 | The contribution itself; detailed and precise |
| Application / Demonstration | Required | 1,500-2,000 | Show the framework applied to examples or cases |
| Discussion | Required | 1,000-1,200 | Scope, limitations, relationship to prior frameworks |
| Conclusion | Required | 400-500 | Summary and future work |
| References | Required | No limit | ACM format |

**Total body target:** 9,000 words

### Framework/Theory Section Requirements

- Define all terms precisely
- Explain the relationships between components
- Distinguish from prior frameworks explicitly
- Include a figure illustrating the framework
- Explain what the framework predicts, explains, or enables

### Quality Criteria (Reviewer Checklist)

- [ ] The framework is grounded in extensive prior work
- [ ] All terms are defined precisely
- [ ] The framework is applied to concrete examples
- [ ] Relationship to prior frameworks is explicit
- [ ] The contribution is clear: what does this framework enable that prior frameworks don't?

### Common Pitfalls

**Pitfall 1: Framework without grounding.** A framework that appears to be invented rather than derived from prior work and evidence.

**Pitfall 2: Vague terms.** Using terms like "agency," "context," or "experience" without precise definitions. Reviewers will ask what these mean.

**Pitfall 3: No application.** Presenting a framework without showing how it applies to real cases. The application section is what makes the framework useful.

**Pitfall 4: Reinventing prior frameworks.** Proposing a framework that is essentially an existing framework with new names. Engage with prior frameworks explicitly.

---

## Contribution Type 5: Survey

**Definition:** Papers whose primary contribution is a systematic synthesis of prior work, revealing patterns, gaps, or trends across a body of literature. Includes systematic literature reviews, meta-analyses, and structured literature surveys.

**Most common at:** CHI, CSCW, UbiComp/IMWUT

### Section Structure

| Section | Status | Word Target | Notes |
|---------|--------|-------------|-------|
| Abstract | Required | 150 | Scope, N papers reviewed, key findings |
| Introduction | Required | 1,000-1,200 | Why this survey is needed now; scope |
| Survey Method | Required | 1,500-2,000 | Search strategy, inclusion/exclusion, coding scheme |
| Results | Required | 3,000-4,000 | Organized synthesis of findings |
| Discussion | Required | 1,500-2,000 | Patterns, gaps, future directions |
| Conclusion | Required | 400-500 | Summary |
| References | Required | No limit | ACM format |

**Total body target:** 9,000 words

### Survey Method Requirements

- Report the databases searched (ACM DL, IEEE Xplore, PubMed, etc.)
- Report search terms used
- Report inclusion and exclusion criteria
- Report the number of papers at each stage (initial results, after title/abstract screening, after full-text review)
- Include a PRISMA flow diagram or equivalent
- Describe the coding scheme and how codes were developed
- Report inter-rater reliability if multiple coders were used

### Quality Criteria (Reviewer Checklist)

- [ ] Search strategy is replicable
- [ ] Inclusion/exclusion criteria are explicit
- [ ] N papers is reported at each stage
- [ ] Coding scheme is described
- [ ] The synthesis reveals something not obvious from reading individual papers
- [ ] Gaps and future directions are specific and actionable

### Common Pitfalls

**Pitfall 1: Annotated bibliography instead of synthesis.** Summarizing each paper individually rather than synthesizing across papers. A survey should reveal patterns, not just list papers.

**Pitfall 2: Unclear scope.** Not defining what counts as "in scope" for the survey. Reviewers will question why certain papers were included or excluded.

**Pitfall 3: Outdated search.** Conducting the search more than 12 months before submission without updating it.

---

## Contribution Type 6: Opinion

**Definition:** Papers whose primary contribution is a perspective, provocation, or argument that advances discourse in the field. Also called "position papers," "provocations," or "perspectives." No empirical data required, but the argument must be well-supported.

**Most common at:** CHI (Papers Without Study track), DIS, CSCW

### Section Structure

| Section | Status | Word Target | Notes |
|---------|--------|-------------|-------|
| Abstract | Required | 150 | State the position clearly |
| Introduction | Required | 1,000-1,200 | State the argument; why it matters now |
| Background | Required | 1,500-2,000 | Ground the argument in prior work |
| Argument | Required | 3,000-4,000 | The core contribution; well-structured argument |
| Counterarguments | Required | 800-1,000 | Engage with opposing views honestly |
| Implications | Required | 800-1,000 | What should the community do differently? |
| Conclusion | Required | 400-500 | Summary |
| References | Required | No limit | ACM format |

**Total body target:** 8,000 words

### Quality Criteria (Reviewer Checklist)

- [ ] The position is stated clearly and early
- [ ] The argument is well-supported by evidence and prior work
- [ ] Counterarguments are engaged honestly, not dismissed
- [ ] Implications are specific and actionable
- [ ] The paper advances discourse rather than just summarizing existing views

### Common Pitfalls

**Pitfall 1: Argument without evidence.** Asserting a position without supporting it with evidence, examples, or prior work.

**Pitfall 2: Ignoring counterarguments.** Presenting only evidence that supports the position. Reviewers will raise counterarguments; address them proactively.

**Pitfall 3: Implications that are too vague.** "The community should think more carefully about X." What specifically should change?

---

## Contribution Type 7: Benchmark

**Definition:** Papers whose primary contribution is a dataset, evaluation framework, or set of baselines that enables systematic comparison of methods or systems. The benchmark itself is the contribution; a demonstration shows it is useful.

**Most common at:** CHI, UbiComp/IMWUT, and AI-adjacent HCI venues

### Section Structure

| Section | Status | Word Target | Notes |
|---------|--------|-------------|-------|
| Abstract | Required | 150 | Name the benchmark, scope, key statistics |
| Introduction | Required | 1,000-1,200 | Why this benchmark is needed; what it enables |
| Related Work | Required | 1,500-2,000 | Prior datasets/benchmarks and their limitations |
| Benchmark Design | Required | 2,000-2,500 | Collection methodology, annotation, quality control |
| Benchmark Statistics | Required | 1,000-1,500 | Descriptive statistics, distributions, coverage |
| Baseline Experiments | Required | 1,500-2,000 | Baseline methods evaluated on the benchmark |
| Discussion | Required | 800-1,000 | Limitations, appropriate use cases, future extensions |
| Conclusion | Required | 400-500 | Summary |
| References | Required | No limit | ACM format |

**Total body target:** 9,000 words

### Benchmark Design Requirements

- Describe the data collection procedure in replicable detail
- Report annotation guidelines and inter-annotator agreement
- Describe quality control procedures
- Report the license and access conditions for the dataset
- Provide a data statement (following Bender and Friedman 2018 or equivalent)

### Quality Criteria (Reviewer Checklist)

- [ ] Collection methodology is replicable
- [ ] Annotation quality is demonstrated (inter-annotator agreement)
- [ ] Baseline results are reported to enable comparison
- [ ] Dataset is publicly available or a clear access path is described
- [ ] Limitations and potential misuse cases are discussed
- [ ] The benchmark fills a gap not addressed by existing benchmarks

### Common Pitfalls

**Pitfall 1: Dataset without baselines.** Releasing a dataset without showing what performance looks like on it. Baselines are required so future work has something to compare against.

**Pitfall 2: No data statement.** Failing to document the provenance, limitations, and potential biases of the dataset.

**Pitfall 3: Restricted access.** Describing a benchmark that is not publicly available. If access is restricted, explain the access procedure clearly.

**Pitfall 4: Overlap with existing benchmarks.** Not demonstrating that the new benchmark covers a gap not addressed by existing ones.

---

## Cross-Cutting Quality Criteria (All Contribution Types)

These apply regardless of contribution type. Reviewers check these for every paper.

### Contribution Clarity
- The contribution is stated explicitly in the abstract and introduction
- The contribution is appropriate for the venue (CHI, CSCW, UIST, etc.)
- The contribution advances the field beyond prior work

### Related Work
- Prior work is cited accurately and fairly
- The gap motivating the paper is clearly articulated
- The paper is positioned relative to the most relevant prior work (not just tangentially related work)

### Writing Quality
- The paper is well-organized and easy to follow
- Signposting is used appropriately
- Figures are legible and captioned correctly
- Word count is appropriate (not padded, not truncated)

### Anonymization (for review submissions)
- No author names or affiliations in the paper body
- Self-citations use third person
- Acknowledgments are omitted
- System names do not identify the authors

### Ethics
- IRB approval or exemption is stated for studies involving human participants
- Participant privacy is protected (no identifying information in quotes or figures)
- Data handling and storage are described
- Potential harms of the research are acknowledged

---

*Last updated: System initialization. Update this file after each completed project with lessons learned from reviewer feedback.*
