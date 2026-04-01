# HCI Domain Writing Voice
## Overrides for Human-Computer Interaction Sections

> **This file overrides `writing_voice.md` for HCI-domain content only.**
> Read by: `r01-writer-hci`, `r01-writer-integrator` (for HCI-specific aim framing).
> Precedence: this file > `writing_voice.md` > `style_guide.md`.
> Updated by: `r01-evolution` after Draft Feedback Checkpoints with HCI-domain corrections.

---

## Dimension Overrides

Only dimensions that differ from the generic voice are listed here. For all other dimensions, follow `writing_voice.md`.

### Dimension 1: Argumentative Style. Override

**Current calibration:** Problem-experience-first with co-design framing. Lead HCI paragraphs with the user's experience of the problem, not the technical gap. The PI frames HCI work as "co-design with stakeholders" and names specific stakeholder compositions. Transition from human experience to design response to evidence of effectiveness.

**Evidence:** Limited direct HCI-section quotes available from the 3 proposals; HCI appears primarily as participatory design components. The Surgery proposal names the advisory panel composition explicitly: "We will form an Advisory Panel of 6 stakeholders (2 GI surgeons, 2 GI nurse practitioners, 2 recent surgical patients) from OSUWMC." The Sepsis proposal states "All Aims are endorsed and co-designed by practicing physicians."

**Preferred:**
> "We will form an Advisory Panel of 6 stakeholders (2 GI surgeons, 2 GI nurse practitioners, 2 recent surgical patients) from OSUWMC. Notably, this builds on our prior interview study with 13 providers and 4 patients, which revealed challenges such as digital tool struggles and unreliable wound descriptions." [2025PostSurgery]

**Avoided:**
> Alert fatigue is a well-documented problem in ICU settings. Many studies have shown that nurses receive too many alerts.

### Dimension 2: Technical Depth. Override

**Current calibration:** Method-justified. For HCI methods, always explain *why* a specific method was chosen for this context, not just name it. Link method choice to the research question it answers.

**Preferred:**
> We selected contextual inquiry over laboratory usability testing because our research question requires understanding decision-making under real clinical time pressure, factors that cannot be reproduced in a controlled setting [Beyer & Holtzblatt, 1998].

**Avoided:**
> We will use contextual inquiry to study nurse workflows.

### Dimension 6: Interdisciplinary Framing. Override

**Current calibration:** Clinical-impact-anchor. Every HCI finding must be connected to a clinical outcome, not left as a standalone usability result. Reviewers from clinical study sections need to see why interaction design matters for patient care.

**Preferred:**
> The redesigned alert interface reduced critical alert response time from 4.2 to 1.8 minutes (p<0.01), which our clinical collaborators estimate would enable intervention within the 6-hour therapeutic window for sepsis-associated AKI in 73% of cases (vs. 41% with current workflows).

**Avoided:**
> The redesigned interface improved task completion time by 57% and received a SUS score of 82.

### Dimension 7: Reader Model. Override

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

*Note: Limited evidence from the 3 analyzed proposals, this pattern is inferred from the Surgery proposal's patient-centered design approach. Flag as "limited evidence" if used in a proposal that doesn't involve MCI populations.*

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
| 2026-03-05 | All | Dim 1 override updated with co-design framing and real quotes; PD Session Specification and MCI Adaptations conventions added | Seeded from 3 prior R01 proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery): limited HCI-specific data; patterns inferred from participatory design sections |

---

## HCI Paper Writing Style (Derived from 6 Highly-Cited Papers)

> **Source**: Deep style analysis of 6 of the PI's highly-cited HCI papers: *Human-AI Collaboration in Data Science* (CSCW 2019), *Mental-LLM* (IMWUT 2024), *How Data Science Workers Work with Data* (CHI 2019), *Brilliant AI Doctor in Rural Clinics* (CHI 2021), *Talk2Care* (IMWUT 2024), *StoryBuddy* (CHI 2022). These patterns override R01 voice when writing academic papers.

### Introduction Structure (MANDATORY for Paper Mode)

The PI's introductions follow a consistent 5-element arc across all 6 papers. Writers MUST follow this structure:

1. **Problem grounding** (¶1): Open with the domain activity and its importance. Ground in concrete evidence, statistics, scope, or specific stakeholder burden. Never lead with the technical solution. **Keep mitigation descriptions concise**: for each mitigation method (e.g., pilot studies, empathy-based methods), state its name, citation, ONE key limitation, and move on. Do NOT add a separate sentence explaining why the limitation matters. The paragraph should state the problem, name 2 mitigations with their limitations in a single compound sentence joined by semicolons, and close with the need statement. Total: 5-7 sentences for ¶1. Examples:
   - Talk2Care: "nearly 95% of older adults in the US have at least one chronic health condition"
   - Mental-LLM: "more than 20% of adults in the U.S. experience at least one mental disorder"
   - Brilliant AI Doctor: "hundreds of millions of Chinese still live in rural areas"
   - Human-AI: "organizations are struggling to recruit enough data scientists"

2. **Gap identification** (¶2-3): Explicitly name 2-3 research gaps or challenges with "However..." / "Despite..." / "there remains a lack of..." transitions. Weave gaps into prose paragraphs using inline numbering ("First, ... Second, ... Third, ...") or parenthetical numbering ("(1)...; (2)...; (3)...") within a single flowing paragraph. **ABSOLUTE BAN on standalone numbered/bulleted list items for gaps, requirements, or challenges.** The ONLY standalone list permitted in the Introduction is the final contribution list. Any `1. **Bold header.** Description` or `- **Bold header.** Description` format is a standalone list and is BANNED. Requirements/gaps must be woven into a prose paragraph where the numbering is inline within sentences, not on separate lines.

   **Evidence-per-challenge rule (MANDATORY):** Every individual challenge or gap MUST be backed by at least one citation or concrete evidence (statistic, prior finding, named system limitation). Challenges stated as bare assertions without evidence will be rejected. When listing numbered requirements/gaps inline, each numbered item needs its own supporting evidence, not a single citation cluster at the end of the list.
   - **Banned format (standalone list):**
     ```
     1. **Real-world operation.** Agents need to interact with live webpages [17, 19].
     2. **Reasoning depth.** Agents need to produce rich traces [61].
     3. **Real-time responsiveness.** Agents need to interact at human-like speed [38].
     ```
   - **Preferred format (inline within prose paragraph):**
      "Translating this promising approach into an actual practice is not easy, and existing systems cannot yet support it. First, the agent systems need to interact with live and dynamically changing webpages, because usability testing requires encountering the same page conditions that real participants would face [17, 19]. Many existing digital twin frameworks [33, 48, 51] can only operate in text-based or simulated sandbox environments (e.g., WebVoyager [19] and WebAgent [17]). Second, agents need to produce both rich cognitive data suitable for qualitative analysis and behavioral log data for quantitative analysis, since UX researchers rely on post-study interviews and think aloud to triage the study design flaws [59, 61]."

3. **"In this work" bridge** (¶4): Introduce the system/contribution using "In this work, we..." or "Building on [prior work / our formative investigation], we designed and developed [SystemName]..." This phrase appears in 5 of 6 papers.

4. **System components as inline enumeration**: When describing a multi-component system, enumerate components inline within a prose paragraph using "(1)... (2)... (3)..." numbering woven into the sentence, not as a standalone bulleted or numbered list. Example: "UXAgent comprises five components: (1) a UX Study Configuration Interface that...; (2) a Persona Generator that...; (3) an LLM Agent module with...; (4) a Universal Browser Connector that...; and (5) a Result Viewer Interface that..." **CRITICAL: The component count and names MUST exactly match the system as described in the outline, user input, or system design section. Do not omit components. Cross-check against `docs/outline.md` or `docs/user_input.md` before finalizing.**

5. **Contributions as standalone list** (final element): Always format contributions as a bulleted or numbered list, not inline prose. Each contribution gets its own line with 1-2 sentences. The list is introduced by "Our primary contributions are:" or "We make the following contributions:" or "This paper presents the following contributions:". Typical count: 3-4 items.

### Pre-Contribution Elements (between system description and contribution list)

- **Formative study mention**: 5 of 6 papers mention their empirical/formative study in the introduction. Include participant count and method: "we conducted interviews with N [role]" or "we conducted a user study with N [role]."
- **Results preview**: Include 1-2 sentences previewing key results before the contribution list: "Our results show/suggest that..."

### Related Work Structure (MANDATORY for Paper Mode)

1. **Preamble sentence**: 4 of 6 papers open Related Work with a 1-2 sentence overview: "We organize related work into three areas: [topic A] (Section 2.1), [topic B] (Section 2.2), and [topic C] (Section 2.3)."

2. **Thematic subsections**: The PI's 6 analyzed CHI/CSCW/IMWUT papers use exactly 3 RW subsections. However, 4 subsections are acceptable for UIST or other technically dense papers where the content genuinely requires it (e.g., when the paper has both a domain contribution and a distinct architecture contribution). Title may be "Related Work", "Background", or "Background and Related Work" depending on contribution type.

3. **Subsection ordering, dependency check**: Before finalizing the RW outline, verify that no subsection references concepts or techniques that are only explained in a *later* subsection. If Section A discusses systems that use a technique explained in Section B, then B must come before A. The general flow should be: foundational/enabling technology → domain-specific applications → infrastructure/systems → architecture/method. When a "domain problem" section (e.g., usability testing challenges) needs to reference LLM-based tools, either (a) put the enabling technology section first, or (b) ensure the domain section's opening paragraphs cover only non-LLM content (human-conducted challenges) before pivoting to LLM-based approaches.

4. **Domain grounding paragraph**: When the RW includes a section on automated/AI-assisted approaches to a domain problem (e.g., "Automated Usability Evaluation"), that section MUST open with at least one paragraph (~150-200 words) covering the human-conducted challenges and existing non-AI approaches. This grounds the reader in *why* automation is needed before showing *how*. Do not jump straight into AI systems without establishing the domain context. However, keep this paragraph concise, it should not repeat the Introduction's problem statement verbatim; instead, focus on the specific methodological challenges (e.g., pilot study limitations, recruitment cost) that motivate the automated approaches discussed in subsequent paragraphs.

5. **Subsection closing = positioning**: Each subsection MUST end with 1-3 sentences positioning the current work relative to the reviewed literature. Use patterns like:
   - "Our work attempts to characterize..." (Human-AI)
   - "UXAgent addresses this gap by..." (UXAgent)
   - "In this work, we join the effort of..." (Brilliant AI Doctor)
   - "Compared with prior work, the key novel contributions are..." (StoryBuddy)
   Do NOT write full positioning paragraphs (5+ sentences) at subsection ends, compress to 1-3 sentences.

### Citation Patterns

- **Density**: Very high. Nearly every factual claim backed by 2-6 citations. Citation-free sentences are limited to the PI's own interpretive claims.
- **Format**: Parenthetical (Author, Year) or bracketed [#] depending on venue template. Both are acceptable.
- **Multi-source claims**: Standard. Use ranges for closely related citations: "[33, 51]" or "[NEW-ArgyleEtAl2023, NEW-FreeLunchUX2025]".

### Transition Phrases (Preferred)

Use content-specific bridges, not generic connectors. Observed across all 6 papers:
- "In this work, we join..." / "Building on these insights, we..."
- "To address these challenges/limitations..." / "Despite consistent findings..."
- "In addition to..." / "Another related research area..."
- "In parallel to the development of..."
- "These advances/findings suggest..."

Avoid: "Furthermore," "Moreover," "Additionally," as standalone paragraph openers.

### Footnotes

Footnotes are acceptable in the Introduction for **terminological clarifications and scope notes** that would otherwise clutter the main argument. Use a footnote when the aside is >15 words and tangential to the paragraph's core claim. Use a short inline parenthetical only when the clarification is ≤15 words and tightly integrated with the sentence.

**Example (footnote preferred):** A long scope note like "The literature uses several overlapping terms... our findings are broadly applicable across these categories, though X is most closely related to Y" should be a footnote, not a bold inline parenthetical that interrupts the sentence.

**Example (inline OK):** A short clarification like "(e.g., web agents and GUI agents)" can stay inline.

### System Positioning Language (Paper Mode)

When describing a system's relationship to human participants or practitioners, use the PI's preferred framing:
- **"Collaborative tool"**: the system assists researchers, not replaces them.
- **"Digital twins of participants"**: when the system simulates user behavior, frame agents as digital twins that researchers can test with before involving real humans.
- **"Stress-test the study design"**: for pre-study validation tools.
- Avoid generic "automates" or "replaces" language. The PI consistently frames AI systems as augmenting human expertise.

### Key Conceptual Distinctions (MANDATORY for UXAgent and similar projects)

Writers MUST clearly differentiate and consistently use the following concepts throughout the paper. Conflating them confuses readers and undermines the paper's contribution framing.

#### 1. Feature/UI Design vs. Study Design

These are two distinct objects in usability testing:

- **Feature design (also: UI design, webpage design)**: The artifact being evaluated. This includes visual elements (color, layout, button size), interaction patterns, information architecture, and functional features on a webpage or application. This is the *target* of the usability test or user study. Example: "a newly designed product filter feature on an e-commerce website."
- **Study design (also: usability testing design, user study design)**: The research methodology used to evaluate the feature design. This includes task definitions, participant recruitment criteria, sample size, procedure, metrics, and analysis plan. Example: "a between-subjects study with 20 participants completing 3 shopping tasks, measured by task completion rate and SUS scores."

**UXAgent's contribution is about validating the study design**, not the feature design. The system helps researchers discover flaws in their study design (ambiguous tasks, overly narrow participant criteria, metrics that fail to capture the intended phenomena) *before* running the study with real participants. The feature design is the object being tested; the study design is what UXAgent helps validate. Writers MUST use precise language to distinguish these two concepts. When referring to what is being evaluated, say "feature design" or "UI design" or "webpage design." When referring to the methodology being validated, say "study design" or "usability testing design."

#### 2. LLM-Based Digital Twins vs. LLM-Based Autonomous Agents

These are two fundamentally different uses of LLMs as agents, and the paper MUST distinguish them clearly:

- **LLM-based digital twins (of human participants)**: Agents designed to *replicate a real human's multi-turn behavior and thinking trajectories*. The goal is behavioral fidelity to a specific human persona, not task completion. These agents require rich persona specifications (demographics, expertise, preferences, cognitive style) and produce behavior that approximates how a *specific type of person* would think and act. This is harder because the agent must maintain persona consistency across many interactions and produce human-like reasoning traces, not just correct actions. UXAgent uses this approach.
- **LLM-based autonomous agents (task-oriented)**: Agents designed to *complete a task automatically and efficiently*. The goal is task success (e.g., book a flight, fill out a form, write code). These agents optimize for correctness and speed. They do not need to replicate any particular human's behavior or thinking. Examples: Claude Computer Use, OpenClaw, OpenAI Operator, browser_use. These are sometimes called GUI agents, and the category is broad, encompassing web agents, computer-use agents, mobile agents, and code agents.

**Key distinction**: Digital twins aim for *behavioral fidelity to a human persona*; autonomous agents aim for *task completion efficiency*. UXAgent's agents are digital twins because they simulate how specific participant personas would experience and react to a website, producing think-aloud reasoning traces that UX researchers can analyze. This is fundamentally different from a GUI agent that navigates a website to complete a booking or purchase as fast as possible.

**Positioning UXAgent**: UXAgent's agents are most similar to web agents in that they interact with real webpages through a browser. However, they differ from conventional web agents (WebVoyager, WebAgent, browser_use, Operator, Claude Computer Use) in their *purpose*: web agents are task-oriented autonomous agents that optimize for task completion, while UXAgent's agents are digital twins that optimize for behavioral fidelity to human personas. This distinction should be made explicit whenever comparing UXAgent to existing agent systems.

### Hedging Asymmetry (Paper Mode)

- **Confident** about methods and system description: "we designed," "we conducted," "we developed"
- **Cautious** about generalizability and outcomes: "our results suggest," "may be most reliable for," "has the potential to"
- Never hedge both method and outcome in the same sentence.

### Paper Roadmap (BANNED after contribution list)

**Do NOT include a "remainder of this paper is organized as follows" paragraph after the contribution list.** This includes any variant that walks through sections sequentially: "Section 2 reviews... Section 3 describes... Section 4 presents..." The contribution list is the final element of the Introduction. The paper's structure should be self-evident from the section headings. If a brief roadmap is needed, it can appear as a single sentence *within* the last contribution item, not as a standalone paragraph.

### PI Copy-Edit Derived Patterns (Paper Mode — MANDATORY)

> **Source**: Sentence-by-sentence analysis of PI's hand-edited introduction_v14_copy vs. AI-generated introduction_v14 for the uist-uxagent project (2026-03-31). These patterns represent the PI's actual editing preferences when copy-editing AI-generated HCI paper prose. They apply to ALL HCI paper writing, not just UXAgent.

#### 1. Researcher-Agency Framing (MANDATORY)

When describing what a system does, center the **researcher** as the active agent and the system as the tool that follows researcher direction. The system acts *under researcher control*, not autonomously.

- **Preferred:** "a system that can follow UX researchers' configuration to automatically generate..."
- **Avoided:** "a system that generates..."
- **Preferred:** "from which researchers can collect behavioral and cognitive data"
- **Avoided:** "to collect behavioral data"
- **Preferred:** "from a UX researcher predefined demographic distribution"
- **Avoided:** "from a demographic distribution"

**Rule:** In every sentence describing system behavior in the Introduction and System Description, verify that the researcher's role is explicit. If the system is the grammatical subject performing an action, add a "following researcher's [configuration / specification / criteria]" clause.

#### 2. Body-of-Work as Subject (MANDATORY for literature paragraphs)

When introducing a body of research, make the **research works** the grammatical subject, not the technology itself. This is more scholarly and positions the author as surveying a literature, not promoting a technology.

- **Preferred:** "Recent works on Large Language Models (LLMs) as agents offer a promising path to evaluate the study design. Generally speaking, these works focus on two distinct uses..."
- **Avoided:** "Large Language Models (LLMs) offer a promising path toward scalable, low-cost study design validation, and a growing body of work explores two distinct uses..."

**Rule:** In paragraphs that survey related work or introduce a technology landscape, the subject of the opening sentence should be "Recent works on X" / "A growing body of research on X" / "Studies on X", NOT "X offers/enables/provides." The technology is the object being studied, not the actor.

#### 3. Structural Gap over Behavioral Observation

When describing a gap or problem, frame it as a **structural absence** (researchers lack a method/tool) rather than a **behavioral observation** (researchers rarely do X). Structural framing motivates the contribution more directly.

- **Preferred:** "researchers do not have a method to validate or iterate the study design itself before conducting the actual user study"
- **Avoided:** "researchers rarely validate the study design itself before conducting the user study"

**Why:** "Rarely validate" suggests researchers *could* but choose not to. "Do not have a method" identifies a structural gap that the paper fills. The contribution becomes the method, not a behavioral correction.

#### 4. Dual-Evaluation Framing (MANDATORY when applicable)

When a study evaluates two distinct objects (e.g., a feature design AND a study design; a system AND the data it produces), **name both evaluation targets explicitly** in every results sentence. Never collapse them into a single abstract term.

- **Preferred:** "form grounded evaluation of the new product filter feature design as well as the usability testing study design"
- **Avoided:** "form grounded assessments of both the simulation quality and their own study designs"

**Rule:** When the study has dual evaluation targets, use the pattern "[evaluation/assessment] of [target A] as well as [target B]" with the actual names of the targets, not abstract surrogates like "simulation quality."

#### 5. Practice-Lens Design Rationale

Ground every design decision in **disciplinary practice norms**, not computational convenience. When explaining why a specific number, method, or configuration was chosen, connect it to established practice in the field.

- **Preferred:** "We decided to create 20 LLM agents to align with the usability testing tradition [cite]"
- **Avoided:** "We chose 20 agents to keep the dataset at a scale amenable to close qualitative analysis"

**Preferred framing hierarchy:**
1. Disciplinary practice norm ("aligns with the usability testing tradition of N=20")
2. Methodological justification ("sufficient for thematic saturation per [cite]")
3. Practical constraint ("feasible within the IRB-approved timeline")

**Never use** as the primary rationale: "amenable to analysis," "manageable scale," "keeps the dataset tractable." These sound like excuses for not running more, not principled decisions.

#### 6. Concrete Method Details in Introduction

The Introduction's case study / evaluation paragraph should include **concrete procedural details** that ground the study in real-world research practice. Include:
- Session duration ("avg. 30 mins")
- Data collection instruments ("questionnaire about system usability and AI trustworthiness")
- Interview purpose ("interviewed each participant to see whether they were able to identify flaws in the study design")
- Scalability note when applicable ("it is easy to generate thousands of such agents")

**Why:** Concrete details make the study feel real and methodologically grounded, not hypothetical. Reviewers form first impressions of study rigor from the Introduction.

#### 7. Practice Analogues (Connect new to familiar)

When introducing an unfamiliar data type or process, immediately connect it to the **established equivalent** in the reader's discipline.

- **Preferred:** "Each of the 20 digital twins left a trace of their actions, reasoning, and observations, which replicate the session recordings of a real user study."
- **Avoided:** "Each agent produced action logs, reasoning traces, and observation records."

**Rule:** After introducing what agents produce, add a relative clause or sentence connecting it to the familiar equivalent ("which replicate [familiar concept]"). The reader should immediately understand what kind of data this is in terms they already know.

#### 8. Describe Capabilities, Not Limitations (for participant activities)

When describing what study participants can do with the system/data, **describe their capabilities positively** rather than justifying limitations defensively.

- **Preferred:** "Each of our UX researcher participant could examine action logs, reasoning traces, and post-study questionnaire responses; they can also conduct live interviews with the agent."
- **Avoided:** "This depth of engagement would be prohibitively time-consuming with hundreds of simulated sessions."

**Rule:** Replace defensive limitation sentences ("X would be too difficult/expensive/time-consuming for Y") with positive capability descriptions ("participants could do A, B, and C"). Let readers draw their own conclusions about scalability.

#### 9. Gap Paragraph: Consolidate Examples with Prior Work

When discussing which existing systems cannot satisfy requirements, **consolidate system examples with their categories** using parenthetical examples rather than dedicating separate sentences to each system.

- **Preferred:** "Many existing digital twin frameworks [33, 48, 51] can only operate in text-based or simulated sandbox environments (e.g., WebVoyager [19] and WebAgent [17]); SimUser [73] is one example that..."
- **Avoided:** "Existing digital twin frameworks [33, 48, 51] operate in text-based or simulated environments and lack the infrastructure for live webpage interaction. WebVoyager [19] and WebAgent [17] offer structured action traces yet operate on sandboxed environments. SimUser's traces center on task-completion metrics [73]."

**Why:** The avoided version uses 3 sentences to cover systems that can be consolidated into 1 compound sentence. Each system gets a parenthetical mention rather than a standalone sentence. The paragraph stays focused on the *gap* rather than becoming a system catalog.

#### 10. Soften Absolute Claims on Existing Systems

When characterizing existing systems' limitations, use **softened qualifiers** ("many," "can only") rather than absolute claims ("existing systems do not").

- **Preferred:** "**Many** existing digital twin frameworks... **can only** operate in..."
- **Avoided:** "Existing digital twin frameworks... operate in... and **lack** the infrastructure for..."

**Rule:** When stating that existing systems fail to do X, prefix with "Many" or "Most" and use "can only" instead of the bare limitation. This is both more accurate (there may be exceptions) and more defensible in peer review.

#### 11. Dual Data Types (Qualitative AND Quantitative)

When describing what data a system produces for analysis, explicitly name **both qualitative and quantitative** data types with their analysis purposes.

- **Preferred:** "produce both rich cognitive data suitable for qualitative analysis and behavioral log data for quantitative analysis"
- **Avoided:** "produce rich cognitive and behavioral traces suitable for qualitative analysis"

**Why:** The avoided version lumps all data under "qualitative analysis." The preferred version acknowledges that UX researchers use both qualitative and quantitative methods, and names each data type with its purpose. This is more precise and more credible to reviewers who value mixed-methods rigor.

#### 12. System Description: Detailed What-It-Does, Minimal How-It-Works

The Introduction's system component description should give each component a **substantive functional description** (what it does for the researcher and why it matters), while omitting low-level implementation details (specific algorithms, data representations, architecture internals). Save those for the System Design section. **Do NOT compress component descriptions into short labels.** Each component should get 1-2 full clauses describing its function, inputs, outputs, and user-facing purpose.

**Bold component names:** Every component name MUST be bolded on first mention in the system description paragraph: **Persona Generator**, **Universal Browser Connector**, **Result Viewer Interface**, etc. This formatting distinguishes component names from general prose and matches the PI's preferred style.

**Substantive "what it does" (CRITICAL — do not compress):** Each component gets a rich descriptive clause that conveys its functional purpose in enough detail that a reviewer can understand what it does without reading the System Design section. Include what the component takes as input, what it produces, for whom, and any distinguishing capability. A one-word or one-phrase summary (e.g., "drives behavior") is too compressed; aim for the detail level shown in the preferred examples below.

- **Preferred (target detail level):** "an **LLM Agent** module that generates persona-consistent actions and reasoning traces by grounding each decision in the assigned participant profile, browsing context, and task instructions"
- **Too compressed:** "an **LLM Agent** module that drives each digital twin's behavior"
- **Preferred:** "a **Universal Browser Connector** that enables agents to parse and act on real webpages; the connector translates the agent's intended actions into browser events and returns structured page observations for the next agent action cycle"
- **Too compressed:** "a **Universal Browser Connector** that translates actions into browser events"
- **Preferred:** "a **UX Study Configuration Interface** that allows researchers to specify study parameters, tasks, and evaluation criteria"
- **Too compressed:** "a **UX Study Configuration Interface** for defining study parameters"
- **Too technical (save for System Design):** "a browser connector that translates the agent's intended actions into browser events through accessibility-tree and DOM-based representations"

**Rule:** In the Introduction, each component gets a bolded name and a "what it does" description (1-2 full clauses, not compressed labels). The description should be detailed enough that a reviewer understands the component's role, but should omit low-level technical mechanisms (architecture, algorithms, specific representations like accessibility trees or DOM parsing). When in doubt, err toward MORE detail, not less.

#### 13. Stakeholder Specificity (MANDATORY)

Always use the most specific stakeholder term available. Generic "researchers" is too vague; the PI's prose consistently names the professional role.

- **Preferred:** "UX researchers", "usability practitioners", "study designers"
- **Avoided:** "researchers", "users", "practitioners" (generic)
- **Preferred:** "real participants" (when contrasting with simulated agents)
- **Avoided:** "human participants" (redundant in most UX contexts), "users" (ambiguous)

**Rule:** In every sentence referencing the people who use the system or conduct studies, use "UX researchers" (or the domain-appropriate equivalent from `project.yaml`). Reserve generic "researchers" only for sentences about the broader research community, not system users.

#### 14. Contribution Phrasing (MANDATORY)

Use the PI's preferred phrasing for the contribution list introduction:

- **Preferred:** "We make the following contributions:"
- **Acceptable:** "This paper presents the following contributions:"
- **Avoided:** "Our primary contributions are:" / "Our contributions include:"

**Why:** "We make" is active and direct. "Our primary contributions are" is passive and adds unnecessary qualifiers. The PI consistently uses "We make" across papers.

#### 15. Tense Conventions (Paper Mode)

Maintain consistent tense usage throughout the Introduction:

- **Present tense** (default) for the paper's contributions, system description, and general claims: "we present", "we design and develop", "our system generates", "UXAgent comprises"
- **Past tense** for citing prior work: "Smith et al. found [42]", "prior work showed that..."
- **Past tense** for describing specific completed studies, implementations, or data collection: "we conducted interviews with N participants", "we evaluated UXAgent through a case study", "we collected a questionnaire", "we designed and developed UXAgent" (when narrating what was concretely built/done)
- **Present tense** for describing ongoing research gaps and general truths: "UX researchers rely on...", "usability testing remains...", "there remains a lack of..."

**Nuance:** The "In this work, we..." bridge sentence and system capability descriptions use present tense ("we design and develop", "a system that generates"). But when the text shifts to narrating specific study procedures or concrete implementation steps, past tense is natural and correct ("we evaluated", "we collected", "we decided to create 20 agents"). Both are acceptable; the key is consistency within each paragraph's framing.

#### 16. Concrete Parenthetical Examples (MANDATORY for task descriptions)

When mentioning task types, completion criteria, or study activities, include a **concrete parenthetical example** grounded in a real-world scenario. Abstract descriptions lose reviewer attention.

- **Preferred:** "completing three purchase tasks (e.g., completing three purchase tasks on an e-commerce website)"
- **Preferred:** "form grounded evaluation of the new product filter feature design as well as the usability testing study design (e.g., completing three purchase tasks on an e-commerce website and then reflecting on the task clarity and metrics)"
- **Avoided:** "completing predefined tasks" / "performing evaluation tasks"

**Rule:** Every mention of "tasks" or "study activities" in the Introduction must include at least one concrete parenthetical example that names the domain, the action, and (optionally) the artifact being tested.

#### 17. Content Handling When Editing (MANDATORY)

When editing an existing draft, apply a two-tier preservation policy:

**Tier 1 — ALWAYS preserve (never silently drop):**
- **Citation placeholders**: `[NEW-BrowserUse2025]`, `[cite a chi paper]` → keep (or clean format to `[cite]`). These are the author's intentional markers.
- **Contextual details in citation examples**: "in a hospital [33]" — keep "in a hospital". The parenthetical max-2 rule applies to "(e.g., X, Y, Z)" constructions, NOT to descriptive phrases within the main clause.
- **Specific numbers and named entities**: participant counts, system names, accuracy figures.

**Tier 2 — MAY compress or cut (compression rules take priority):**
- **Scope-expanding asides** that broaden the problem beyond what the paper addresses (e.g., an aside about underrepresented groups when the paper evaluates a general-purpose tool). These expand scope without advancing the argument and should be cut.
- **Redundant elaboration**: When the source lists 3+ separate limitations for a single approach but the compression pattern says "1-2 sentences per approach", compress to the 1-2 most essential points and cut the rest. Conciseness over completeness.
- **Verbose phrases**: Trim filler words and extra modifiers (e.g., "analyze the user feedback" → "analyze feedback"; "for a software development company [51]" → "[51]" when the context is already clear).

**Precedence**: Compression rules (element 1 "5-7 sentences for ¶1", Compression pattern "1-2 sentences per approach") OVERRIDE content preservation. When a paragraph exceeds its sentence budget, cut Tier 2 content first.

**Minimize additions**: When editing, prefer tightening and restructuring over adding new words. If the source sentence is grammatically correct and conveys the right meaning, do not add filler words (e.g., do not add "and" before "not necessarily", do not add "use" to "The first is *LLM-based...*").

### Markdown Formatting Conventions (Paper Mode — MANDATORY)

These formatting rules apply to all generated paper prose. They reflect the PI's preferred emphasis patterns observed in the groundtruth introduction.

#### Bold (**text**) — Use for:
- **System component names** on first mention in the system description paragraph: **Persona Generator**, **UX Study Configuration Interface**, **Universal Browser Connector**, **Result Viewer Interface**. Subsequent mentions in the same paragraph do not need bold.
- **System name in the contribution list only**: Bold the system name when it appears as the lead item in the contribution list (e.g., "1. **UXAgent**, a system that..."). Do NOT bold the system name in running prose paragraphs (e.g., write "we designed and developed UXAgent", not "we designed and developed **UXAgent**").
- Do NOT bold generic terms, method names, or contribution item descriptions.

#### Italic (*text*) — Use for:
- **Type categories and taxonomies** when introducing a classification: *LLM-based autonomous agents*, *digital twins of human participants*, *task-oriented agents*. This signals to the reader that these are category labels within a taxonomy, not casual descriptions.
- **Venue or domain category names** on first mention: *usability testing*, *think-aloud protocols* (only when introducing as a category, not in passing use).
- **Foreign terms or terms of art** being defined.
- Do NOT italicize for generic emphasis or to stress a word.

#### Formatting in Context:
- **Preferred:** "Recent works on Large Language Models (LLMs) as agents offer a promising path... Generally speaking, these works focus on two distinct uses: *LLM-based autonomous agents* that complete tasks automatically (e.g., web agents, GUI agents), and *digital twins of human participants* that replicate human behavior..."
- **Avoided:** "Recent works on Large Language Models (LLMs) as agents offer a promising path... Generally speaking, these works focus on two distinct uses: LLM-based autonomous agents that complete tasks automatically, and digital twins of human participants that replicate human behavior..."

---

## Feedback History

| Date | Project | Change | Source |
|------|---------|--------|--------|
| 2026-03-05 | All | Dim 1 override updated with co-design framing and real quotes; PD Session Specification and MCI Adaptations conventions added | Seeded from 3 prior R01 proposals (2023Sepsis, 2024Cardiotoxic, 2025PostSurgery): limited HCI-specific data; patterns inferred from participatory design sections |
| 2026-03-26 | uist-uxagent | Added HCI Paper Writing Style section with Introduction Structure, RW Structure, Citation Patterns, Transition Phrases, Hedging Asymmetry, and Contribution Format rules | Deep analysis of 6 PI highly-cited HCI papers: Human-AI Data Science (CSCW), Mental-LLM (IMWUT), Data Science Workers (CHI), Brilliant AI Doctor (CHI), Talk2Care (IMWUT), StoryBuddy (CHI) |
| 2026-03-26 | uist-uxagent | Footnote rule revised: footnotes now OK in Intro for scope notes >15 words; added System Positioning Language section ("digital twins", "collaborative tool"); added CRITICAL cross-check rule for system component counts | User feedback on intro_v4: parenthetical too prominent, missing "digital twins" framing, wrong component count (4 vs 5) |
| 2026-03-26 | uist-uxagent | RW structure rules: (1) 4 subsections OK for UIST/technical papers; (2) added dependency-ordering check (enabling tech before domain applications); (3) added domain grounding paragraph rule (human challenges before AI approaches). Updated writer-integrator Pass 3 with dependency + grounding checks. | User feedback on RW structure proposal: §2.1 overlapped with §2.2, LLM-based UX tools referenced simulation concepts not yet introduced, missing generic usability testing challenges paragraph |
| 2026-03-26 | uist-uxagent | Added evidence-per-challenge rule to Gap Identification (element 2) in Introduction Structure. Each numbered gap/requirement MUST have its own citation or concrete evidence. Bare assertion lists banned. | User feedback on intro_v4: ¶3 requirements listed without per-item evidence, making claims unsubstantiated |
| 2026-03-27 | uist-uxagent | Gap identification: changed from "Use numbered items" to "Weave into prose with inline numbering." System components: changed from "numbered list" to "inline enumeration within prose paragraph." | User feedback on intro_v6: "avoid using bullet points as much as you can" |
| 2026-03-31 | uist-uxagent | Added 12 PI Copy-Edit Derived Patterns: researcher-agency, body-of-work subject, structural gap, dual-evaluation, practice-lens rationale, concrete method details, practice analogues, describe capabilities not limitations, consolidate examples, soften claims, dual data types, minimize intro tech detail. Updated gap identification example to match PI's preferred style. | Sentence-by-sentence analysis of PI's copy-edits on introduction_v14 vs introduction_v14_copy |
| 2026-03-31 | uist-uxagent | Refined rule #12 (detailed what-it-does with bold names). Added patterns #13-#16: stakeholder specificity ("UX researchers"), contribution phrasing ("We make"), tense conventions, concrete parenthetical examples. Added Markdown Formatting Conventions section (bold components, italic taxonomies). | Diff analysis of v16 vs groundtruth: 16 deviation points identified across formatting, phrasing, and content |

---

*Last updated: 2026-03-31. Added patterns #13-#16, Markdown Formatting Conventions, refined rule #12.*
