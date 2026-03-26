# Media Coverage Writing Voice
## For university press, news blurbs, and public-facing summaries

> **This file is independent of academic writing voices.**
> Read by: any agent producing media coverage, press blurbs, or public-facing summaries.
> This file does NOT inherit from `writing_voice.md` — media writing is a different genre entirely.
> Updated by: `r01-evolution` or manually after media blurb feedback.

---

## Genre Definition

Media coverage writing translates academic research for university communications offices, news outlets, and general audiences. The goal is **impact and accessibility**, not comprehensiveness. Every sentence must earn its place.

Target formats: university news blurbs (150-250 words), research highlights, lab website summaries, social media threads, award announcements.

---

## Dimension 1: Structure

**Current calibration:** Three-block format.

1. **Hook paragraph** (3-4 sentences): Open with the real-world problem. Name the data challenge or clinical gap concretely. End with the open question or tension the research resolves.
2. **What they built** (2-3 sentences): Name the system/method. State what it does in one sentence. Give one concrete result from users or evaluation.
3. **PI quote** (2-3 sentences): First-person voice from PI. Frame why this matters broadly. Connect to the bigger picture (patient care, clinical workflow, societal impact).

**Evidence:** Derived from MIND paper media blurb (2026-03). Hook establishes the data overload problem → MIND system introduced → PI quote on clinical impact.

**Preferred:**
> Mental health treatment is complicated. Clinicians juggle two very different streams of patient data: clinical records generated during visits and self-tracked data from wearables and smartphones that patients generate between visits. Together, these sources could paint a far richer picture — but combining them into actionable clinical insights, rather than adding yet another flood of raw numbers, remains an open challenge.

**Avoided:**
> This paper presents MIND, a novel LLM-powered multimodal narrative dashboard for mental health clinicians. We conducted a co-design study with five participants... [academic abstract voice]

---

## Dimension 2: Voice & Person

**Current calibration:** Third person for description, first person only in PI quote.

- Body text: "these researchers," "the team," "[System Name]"
- PI quote: "we," "our," "this research matters because..."
- Never "we" in the body paragraphs (unlike academic writing)
- PI's title + name: "Khoury Associate Professor Dakuo Wang" or appropriate title at time of writing

**Preferred:**
> Through co-design with five mental health clinicians, these researchers developed an LLM-powered multimodal dashboard called MIND.

**Avoided:**
> We developed MIND through co-design sessions. [academic voice leaking into media]

---

## Dimension 3: Technical Depth

**Current calibration:** Zero jargon. One technical detail maximum per paragraph.

- System names are OK (MIND, UXAgent, etc.)
- One method phrase allowed if immediately explained: "LLM-powered" → acceptable because LLM is entering public vocabulary
- Never: architecture names, model specifications, evaluation metrics, mathematical formulas, sample sizes without context
- Translate method to outcome: not "co-design study with N=5" but "co-design with five mental health clinicians"
- Numbers: use only when they create impact ("30-40% complication rate"), not for method details ("n=24,755 EHR records")

**Evidence:** MIND blurb avoids all technical architecture detail. "LLM-powered" is the only technical term retained.

**Preferred:**
> MIND integrates both patient-generated wearable data and clinical records to surface insights through narrative text and complementary charts.

**Avoided:**
> MIND uses a RAG-enhanced LLM pipeline with multimodal embeddings to process EHR data alongside wearable sensor streams, generating narrative summaries via chain-of-thought prompting.

---

## Dimension 4: Emphasis Strategy

**Current calibration:** Lead with the "so what," not the "what." Every paragraph must answer: why should a non-researcher care?

Key emphasis patterns for the PI's research:
1. **Data integration** — combining different data types (EHR + wearable, clinical + patient-generated) is a recurring theme. Always name both data sources explicitly.
2. **Insight over information** — the value is not more data, but actionable understanding. Frame as "turning X into insights" not "presenting X."
3. **Clinician empowerment** — AI supports human expertise, never replaces it. Frame as tools that free up clinician time/attention.
4. **Real clinical workflows** — ground in specific clinical contexts (mental health, surgery, sepsis) rather than abstract "healthcare."

**Evidence:** User feedback on MIND blurb: "the key are two things: one to combine EHR and patient's self-generated wearable data; and the second is to provide insights rather than just raw and overloaded data."

**Preferred:**
> ...combining them into actionable clinical insights, rather than adding yet another flood of raw numbers, remains an open challenge.

**Avoided:**
> Can the two be presented in conversation, so providers can spend less time interpreting data...? [vague, misses the key contributions]

---

## Dimension 5: Verb Strength

**Current calibration:** Active, confident verbs. No hedging in media writing.

| Weak | Strong |
|------|--------|
| suggest | developed, built, created |
| may help | enables, empowers |
| can potentially | allows, makes it possible |
| seeks to address | tackles, solves |
| is designed to | does, achieves |

**Evidence:** MIND blurb revision changed "suggest" → "developed" — these are built systems, not suggestions.

**Preferred:**
> These researchers developed an LLM-powered multimodal dashboard called MIND.

**Avoided:**
> These researchers suggest a LLM-powered multimodal dashboard called MIND. [passive, uncertain]

---

## Dimension 6: PI Quote Construction

**Current calibration:** Three-part structure within the quote:

1. **The problem** in accessible language (one sentence)
2. **Why this research matters** (one sentence, uses "this research")
3. **The bigger picture** connecting to human impact (one sentence)

The quote should be quotable standalone — a journalist should be able to pull it without surrounding context.

**Evidence:** MIND blurb quote structure: problem ("overwhelmed by sheer volume") → why it matters ("uses AI to turn overwhelming data into coherent narrative") → human impact ("focus energy on patient care rather than data processing").

**Preferred:**
> "Mental health clinicians are often overwhelmed by the sheer volume of data we can now collect from wearables and smartphones. This research matters because it uses AI to turn that overwhelming data into a coherent narrative that can be aligned with clinical notes, allowing mental health professionals to focus their energy on patient care rather than data processing."

---

## Anti-Patterns (NEVER in media writing)

- **Academic abstract voice**: "We present...", "This paper introduces...", "We conducted a study..."
- **Jargon dumping**: listing technical components without translating to impact
- **Passive constructions**: "A system was developed..." -> "These researchers developed..."
- **Citation references**: No "[1]", no "(Wang et al., 2025)", no superscripts
- **Evaluation metrics**: No AUROC, SUS scores, p-values, effect sizes
- **Sample size as method detail**: Say "five mental health clinicians" not "N=5 participants"
- **Footnotes or endnotes**: Everything must be self-contained
- **Acronym soup**: Define at most one acronym per blurb; prefer spelling out
- **Em-dash parenthetical insertions** (`— xxx —`): Never wedge clauses between em-dashes. BANNED: "MIND — an LLM-powered dashboard for mental health — integrates..." REWRITE: "MIND, an LLM-powered dashboard for mental health, integrates..."
- **Trailing participial phrases** (`, verb-ing xxx`): Never append dangling `-ing` clauses. BANNED: "The system combines both data sources, providing clinicians with insights." REWRITE: "The system combines both data sources and provides clinicians with insights."
- **Comma + gerund clauses** (`, having xxx` / `, being xxx`): Never insert subordinate gerund clauses. BANNED: "The team has extensive experience, having developed three clinical AI systems." REWRITE: "The team has extensive experience and has developed three clinical AI systems."

---

## Award Annotations

When the paper won an award, include it prominently after the title:

- Best Paper → "WINNER: Best Paper Award"
- Honorable Mention → "WINNER: Best Paper Honorable Mention"
- Place the award on its own line, before the author list
- Do not bury it in body text

---

## Length Calibration

| Format | Target | Hard limit |
|--------|--------|------------|
| University news blurb | 150-200 words (body) + PI quote | 300 words total |
| Research highlight | 100-150 words | 200 words |
| Social media (long) | 50-80 words | 100 words |
| Lab website summary | 200-300 words | 400 words |

Body word count excludes the PI quote paragraph.

---

## Feedback History

| Date | Project | Change | Source |
|------|---------|--------|--------|
| 2026-03-26 | MIND (CHI'25) | Initial creation from MIND media blurb revision; emphasis strategy calibrated to PI's data-integration + insight-over-raw-data framing | User feedback on draft blurb |

---

*Last updated: 2026-03-26. Seeded from MIND paper media coverage revision. This file improves with each media blurb produced.*
