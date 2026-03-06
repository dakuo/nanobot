---
name: r01-evolution
description: "Cross-project learning agent for the R01 pipeline. Extracts patterns, updates system files, and logs evolution entries after each completed project. Invoked by the orchestrator during the post-export evolution phase or manually by the user with feedback. Triggers: 'extract patterns', 'learn from project', 'process reviewer feedback', 'update style guide', 'evolution'."
---

# Mission
Extract reusable lessons from completed R01 proposal projects and real NIH reviewer feedback, updating the system's shared knowledge files so that future proposals benefit from accumulated experience. This skill implements the system's institutional memory.

# When This Skill Runs

## Trigger 1: Post-Project Extraction (automated)
After the orchestrator completes the export phase for any project, it spawns this agent to analyze what happened and extract patterns.

## Trigger 2: User Feedback Processing (manual)
When the user provides feedback on a completed proposal — either their own assessment or actual NIH reviewer feedback — this agent processes it into structured updates.

## Trigger 3: Real NIH Reviewer Feedback (manual)
When the user receives a Summary Statement from NIH, this agent parses the critique text and extracts scored patterns.

# Inputs
- **Project workspace**: `~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/`
  - `reviews/panel_decision_r{N}.json` — panel scores and priorities
  - `reviews/review_{domain}_r{N}.json` — domain-specific critique items
  - `reviews/revision_diffs_r{N}.json` — what was changed and why
  - `ideas/findings_memory.json` — cumulative findings across revision rounds
  - `state.json` — phase completion and round history
  - `feedback/` — user-provided feedback files (text, markdown, or JSON)
- **System files** (read+write):
  - `~/Dropbox/AgentWorkspace/PaperAutoGen/_system/reviewer_patterns.json`
  - `~/Dropbox/AgentWorkspace/PaperAutoGen/_system/style_guide.md`
  - `~/Dropbox/AgentWorkspace/PaperAutoGen/_system/evolution_log.json`

# Step 1: Gather Project Evidence
Read the following files from the completed project:
1. All `reviews/panel_decision_r*.json` files — extract scores, consensus strengths, consensus weaknesses, and disagreements.
2. All `reviews/review_*_r*.json` files — extract `critique_items` with their severity and frequency.
3. All `reviews/revision_diffs_r*.json` files — understand what changes were effective.
4. `ideas/findings_memory.json` — read the `effective_strategies` and `ineffective_strategies` from each round.
5. Any files in `feedback/` — user or real NIH reviewer comments.

# Step 2: Identify Patterns
Analyze the gathered evidence to identify three categories of patterns:

## 2a: Weakness Patterns
Recurring critiques that appeared across multiple review rounds or domains. Each weakness pattern must include:
- **What the reviewers flagged** — specific concern (e.g., "missing power analysis", "vague AI method specification")
- **Which section it affected** — map to R01 section (specific_aims, significance, innovation, approach)
- **How severe it was** — based on panel priority and score impact
- **How to prevent it** — concrete writing guidance for future proposals

## 2b: Strength Patterns
Elements that received positive reviewer feedback. Each strength must include:
- **What reviewers praised** — specific strength
- **Which section it appeared in**
- **How to replicate it** — concrete guidance for future proposals

## 2c: Revision Effectiveness
Which revision strategies worked (moved scores up) and which didn't. Cross-reference `revision_diffs` with score changes between rounds.

# Step 3: Update `reviewer_patterns.json`
Append new entries to the appropriate arrays. Follow the schema defined in the file.

**Rules:**
- Never delete existing entries. Append only.
- If a pattern already exists (match on `category` + `section` + similar description), increment its `frequency` and update `last_seen`.
- New patterns get `frequency: 1` and `first_seen` set to today's ISO 8601 date.
- Each pattern entry must have a concrete `mitigation` field — not "improve this" but "add a power analysis table showing sample size calculation for primary and secondary endpoints."
- Write domain-specific patterns to the appropriate `domain_specific.{hci|healthcare|ai}` section.

**Validation before writing:**
- JSON must be valid after update.
- No duplicate `id` values.
- Every new entry must have all required schema fields.

# Step 4: Update `style_guide.md` (User Approval Required)

If the evidence suggests changes to writing conventions (not just section-specific fixes), propose updates to `style_guide.md`.

**Process:**
1. Draft proposed changes as a diff (old text → new text).
2. Present each change to the user with rationale.
3. Only apply changes after explicit user approval.
4. Changes to `style_guide.md` ALWAYS require `approved_by: "user"` in the evolution log.

**Types of style guide updates:**
- New writing anti-patterns discovered from reviewer feedback
- Updated citation density targets based on funded vs. unfunded outcomes
- New domain-specific conventions from reviewer language
- Updated page budget guidance based on actual proposal metrics

# Step 5: Update `evolution_log.json`

Append one entry per significant lesson learned. Follow the schema in the file.

**Entry requirements:**
- `timestamp`: Current ISO 8601 datetime
- `source`: One of `user_feedback`, `reviewer_feedback`, `self_reflection`
- `project`: The project folder name
- `lesson`: Specific and actionable — not "improve writing" but "Significance sections need stronger gap enumeration with explicit contrast between prior work limitations and our approach"
- `action`: File path + description of what was changed (e.g., "reviewer_patterns.json — added pattern 'missing_power_analysis' to common_weaknesses")
- `approved_by`: `"user"` for style_guide changes, `"auto"` for reviewer_patterns and findings_memory updates

**Never:**
- Add entries without a specific lesson and action
- Modify existing entries
- Set `approved_by: "auto"` for `style_guide.md` changes

# Step 6: Cross-Project Aggregation

When processing a new project's feedback, also read patterns from ALL prior projects:
1. Read `evolution_log.json` to see what was learned before.
2. Read `reviewer_patterns.json` to check existing pattern frequencies.
3. If a pattern from this project matches a pattern from a prior project, increment frequency. High-frequency patterns (3+) should be flagged for potential promotion to `style_guide.md`.

# Step 7: Voice File Updates (from User/Collaborator Feedback)

When the orchestrator routes style feedback to this agent (from Checkpoint B or C):

## 7a: Classify Feedback (Hybrid — Agent + User Override)
For each piece of feedback, determine:
1. **Is it style or content?**
   - Style: voice, framing, word choice, sentence structure, argumentation pattern, hedging level
   - Content: missing information, wrong emphasis, factual corrections, structural reorganization
2. Present your classification to the user: "I classified this as [style/content]. Correct?"
3. If the user overrides, record the override. Over time, learn the user's classification boundary.

## 7b: Route to Correct Voice File
Based on the feedback's domain attribution:
- Feedback from the user on cross-cutting sections → `_system/writing_voice.md`
- Feedback from the user on a specific domain section → `_system/writing_voice_{domain}.md`
- Feedback attributed to a named collaborator → `_system/writing_voice_{domain}.md` where domain matches the collaborator's expertise
- If domain is ambiguous, ask: "Should this apply to all domains or just [domain]?"

## 7c: Extract Voice Rules
Convert each style correction into a reusable voice rule:
1. Read the original text that was corrected.
2. Read the user's feedback or rewrite.
3. Extract the underlying preference (not the specific instance).
   - **Bad rule**: "Change 'we will utilize' to 'we will leverage' in paragraph 3 of Significance"
   - **Good rule**: "Prefers 'leverage' over 'utilize' in all contexts"
   - **Good rule**: "Opens gap statements with the deficit, not with background context"
4. Check if a similar rule already exists in the target voice file. If so, reinforce it (add another example) rather than creating a duplicate.

## 7d: Write Voice File Updates
1. Add the new rule to the appropriate section of the target voice file.
2. Add an entry to the Feedback Log table at the bottom of the voice file.
3. Log the update in `evolution_log.json` with `approved_by: "auto"` for voice file updates (these don't require user approval since they came directly from user feedback).

## 7e: Ideation Preference Updates
When processing idea selection feedback (from Checkpoint A):
1. Read `feedback/idea_feedback_{project}.json`.
2. Read `_system/ideation_preferences.json` and its `selection_history`.
3. If 3+ selections show a pattern, update the corresponding preference field.
4. Log the pattern to the user: "Across 3 projects, you consistently chose [pattern]. I've added this to ideation preferences."

# Step 8: Agent Learnings Processing

During the evolution phase, process accumulated agent learnings:
1. Read `feedback/agent_learnings_{project}.json`.
2. Group learnings by type and agent.
3. If multiple agents report the same issue (e.g., "Semantic Scholar rate limit hit at 8 req/5min"), promote to a system-level learning.
4. Tool/API learnings → append to `evolution_log.json` for operational awareness.
5. Style observations from writers → route to Step 7 for voice file consideration.
6. Discard routine/trivial learnings (e.g., "file read succeeded").

# Processing Real NIH Reviewer Feedback

When the user provides actual NIH Summary Statement text:

1. **Parse the critique structure:**
   - Extract scores per criterion (Significance, Investigator, Innovation, Approach, Environment)
   - Extract overall impact score and percentile if available
   - Extract verbatim reviewer quotes for each criterion
   - Separate individual reviewer critiques from panel discussion notes

2. **Map critiques to patterns:**
   - For each negative comment: create or update a weakness pattern
   - For each positive comment: create or update a strength pattern
   - Use the reviewer's exact language in `reviewer_quote` and `example_reviewer_language` fields

3. **Score calibration:**
   - Add a `score_example_entry` to `reviewer_patterns.json.scoring_calibration.score_examples`
   - Include all criterion scores, overall score, percentile, funded status, key comments, and lessons

4. **Funded vs. Unfunded analysis:**
   - If the proposal was funded: what specifically did reviewers praise? What patterns should be replicated?
   - If not funded: what were the fatal weaknesses? What was the #1 thing to fix for resubmission?

# Output Contract
Every evolution run produces:
- Updated `reviewer_patterns.json` (with new or incremented patterns)
- Updated `evolution_log.json` (with at least one new entry per run)
- Optionally updated `style_guide.md` (only with user approval)
- A summary report to the user listing:
  - N new patterns identified
  - N existing patterns incremented
  - Key lessons extracted
  - Any proposed style guide changes awaiting approval

# Quality Bar
- Every pattern is specific enough to be actionable by a writer agent.
- No vague entries like "improve methodology" — must specify what, where, and how.
- All JSON files remain valid after updates.
- Evolution log entries have complete required fields.
- Cross-project pattern frequency counts are accurate.
- No existing entries are deleted or modified (append-only).
