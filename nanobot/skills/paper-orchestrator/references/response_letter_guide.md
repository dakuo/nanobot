# Response Letter Guide (Revise & Resubmit)

Format, tone, and best practices for R&R response letters across ACM venues.

---

## Overall Structure

```
Dear Associate Chair and Reviewers,

Thank you for your thoughtful and constructive reviews. We have carefully
addressed all concerns. Below we summarize the major changes, followed by
point-by-point responses to each reviewer.

## Summary of Major Changes
- [1-paragraph summary of the most significant revisions]
- [Bullet list of 3-5 major changes with section references]

## Responses to Reviewer 1 (R1)
### R1.1: [Brief label for the comment]
> [Quoted reviewer comment — verbatim or faithfully summarized]

**Response:** [What action was taken] [Where in the paper the change appears]

[Repeat for each comment from R1]

## Responses to Reviewer 2 (R2)
[Same format]

## Responses to Reviewer 3 (R3)
[Same format]

## Responses to Associate Chair (AC)
[If the AC provided specific guidance, address it here]
```

---

## Per-Comment Response Format

For each reviewer comment, follow this 3-part structure:

1. **Quote** — Reproduce the reviewer's comment (use `>` blockquote). Verbatim is ideal; if summarizing, be faithful to the intent.
2. **Action** — State clearly what was done: "We revised Section 4.2 to...", "We added a new analysis in Section 5.3...", "We respectfully disagree because...".
3. **Location** — Point to the exact section, paragraph, or page where the change appears: "See Section 4.2, paragraph 3" or "See the new Table 3 in Section 5."

---

## Tone Guidelines

- **Professional and specific** — Avoid vague responses like "We have addressed this concern." State exactly what changed.
- **Grateful but not sycophantic** — "Thank you for this suggestion" is fine. "We are deeply grateful for your brilliant insight" is excessive.
- **Confident but not combative** — When disagreeing, provide evidence and reasoning. Never dismiss a reviewer's concern.
- **Concise** — Reviewers read many response letters. Respect their time with clear, direct responses.

---

## When to Push Back

It is acceptable (and sometimes necessary) to respectfully disagree with a reviewer when:

- **The reviewer misunderstood the paper** — Clarify the misunderstanding, then explain what you changed to prevent future confusion: "We appreciate this concern. We believe this may stem from unclear wording in Section 3. We have revised the paragraph to clarify that..."
- **The requested change is out of scope** — Acknowledge the suggestion's value but explain why it exceeds the paper's scope: "This is an excellent suggestion for future work. However, addressing it fully would require [X], which is beyond this paper's scope. We have added this to our Future Work discussion."
- **The reviewer's suggestion would weaken the paper** — Explain why with evidence: "We considered this alternative approach but found that [reasoning]. We have added a brief discussion of this trade-off in Section 5."
- **Conflicting reviewer requests** — When two reviewers want opposite changes, explain the conflict and your resolution: "R1 suggested expanding the related work while R2 suggested shortening it. We balanced both perspectives by restructuring the section to be more focused (addressing R2) while adding the specific references R1 requested."

Always frame pushback constructively — show you took the concern seriously even when not implementing the exact change requested.

---

## Latexdiff Usage

For venues that expect tracked changes (most ACM R&R processes):

- Generate a visual diff using `latexdiff old.tex new.tex > diff.tex`.
- Convention: **blue text** = added content, **red strikethrough** = deleted content.
- Submit the diff PDF alongside the clean revised paper.
- In the response letter, reference the diff: "Changes are highlighted in the accompanying diff document."
- If not using LaTeX, manually highlight changes in the revised PDF using colored text.

---

## Timeline Awareness

| Venue | R&R window | Rounds | Notes |
|-------|-----------|--------|-------|
| CHI | ~4-5 weeks | 1 round | No second revision; make it count |
| CSCW | ~6-8 weeks | 1-2 rounds | Journal model allows deeper revision |
| DIS | ~4 weeks | 1 round | Similar to CHI |
| UIST | N/A | No R&R | Accept/reject only; shepherding for minor issues |
| UbiComp/IMWUT | ~1-2 months | Multiple rounds | Rolling deadlines; major revisions get full re-review |

**CHI-specific note:** With only one R&R round, prioritize addressing all major concerns. Minor issues matter less than demonstrating you took the big feedback seriously.

**CSCW-specific note:** The multi-round process means you can address major structural issues in round 1 and polish in round 2. Communicate your revision plan clearly.

---

## Common Mistakes in Response Letters

1. **Being vague** — "We have revised the paper accordingly" without saying what changed. Always be specific.
2. **Ignoring minor comments** — Address every point, even small ones. A simple "Fixed, thank you" suffices for typos.
3. **Defensive tone** — Arguing with reviewers rather than engaging constructively. Even when pushing back, be collaborative.
4. **Inconsistent numbering** — Use consistent labels (R1.1, R1.2, R2.1...) that match the original review structure.
5. **Missing the meta-review** — If the AC wrote a meta-review with specific guidance, address it first and prominently.
6. **Not acknowledging limitations of changes** — If a requested study would take 6 months, say so honestly rather than pretending a minor edit addresses a major concern.
7. **Forgetting to update the paper** — Writing a great response letter but not actually making the changes in the manuscript.
