---
name: self-improvement
description: "Captures learnings, errors, and corrections to enable continuous self-improvement. Use when a command fails, the user corrects you, knowledge is outdated, or a better approach is discovered."
metadata: {"nanobot":{"emoji":"🧠"}}
---

# Self-Improvement

Log learnings and errors for continuous improvement. Important learnings get promoted to long-term memory.

Adapted from [openclaw/skills/self-improving-agent](https://github.com/openclaw/skills/tree/HEAD/skills/pskoett/self-improving-agent).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation fails | Log to `.learnings/ERRORS.md` |
| User corrects you | Log to `.learnings/LEARNINGS.md` (category: `correction`) |
| User wants missing feature | Log to `.learnings/FEATURE_REQUESTS.md` |
| API/external tool fails | Log to `.learnings/ERRORS.md` with integration details |
| Knowledge was outdated | Log to `.learnings/LEARNINGS.md` (category: `knowledge_gap`) |
| Found better approach | Log to `.learnings/LEARNINGS.md` (category: `best_practice`) |
| Broadly applicable learning | Promote to `memory/MEMORY.md` |

## When to Log (Detection Triggers)

**Corrections** (→ `LEARNINGS.md`, category `correction`):
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."

**Errors** (→ `ERRORS.md`):
- Command returns non-zero exit code
- Exception or stack trace
- Unexpected output or behavior

**Knowledge Gaps** (→ `LEARNINGS.md`, category `knowledge_gap`):
- User provides information you didn't know
- API behavior differs from your understanding

**Feature Requests** (→ `FEATURE_REQUESTS.md`):
- "Can you also..."
- "I wish you could..."
- "Is there a way to..."

## Entry Format

### Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-NNN] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- See Also: LRN-YYYYMMDD-NNN (if related to existing entry)
- Recurrence-Count: 1

---
```

### Error Entry

Append to `.learnings/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-NNN] command_or_tool_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
Brief description of what failed

### Error
```
Actual error message or output
```

### Context
- Command/operation attempted
- Input or parameters used

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-YYYYMMDD-NNN (if recurring)

---
```

### Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-NNN] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending

### Requested Capability
What the user wanted to do

### User Context
Why they needed it, what problem they're solving

### Suggested Implementation
How this could be built

---
```

## ID Format

`TYPE-YYYYMMDD-NNN` — e.g., `LRN-20260302-001`, `ERR-20260302-A3F`

## Promotion to Long-term Memory

When a learning proves broadly applicable, promote it to `memory/MEMORY.md`.

### Promotion Criteria (all must be true)

- `Recurrence-Count >= 3` (same issue appeared 3+ times)
- Occurred across 2+ distinct conversations
- Learning is not project-specific (useful across contexts)

### How to Promote

1. **Distill** the learning into a concise rule or fact
2. **Add** to the appropriate section in `memory/MEMORY.md`
3. **Update** the original entry: `**Status**: pending` → `**Status**: promoted`

### Example

**Verbose learning:**
> User corrected me three times about preferring pnpm over npm. The project uses pnpm workspaces.

**Promoted to MEMORY.md (concise):**
```markdown
## Preferences
- Package manager: pnpm (not npm)
```

## Recurring Pattern Detection

Before logging, search for similar existing entries:

```bash
grep -i "keyword" .learnings/LEARNINGS.md .learnings/ERRORS.md
```

If found:
1. **Link entries**: Add `See Also: ERR-YYYYMMDD-NNN` in metadata
2. **Bump priority** if the issue keeps recurring
3. **Increment Recurrence-Count** on the original entry
4. **Check promotion threshold**: If Recurrence-Count >= 3, promote to MEMORY.md

## Resolving Entries

When an issue is fixed, update:

```markdown
**Status**: resolved

### Resolution
- **Resolved**: ISO-8601 timestamp
- **Notes**: Brief description of what was done
```

## Periodic Review

Review `.learnings/` at natural breakpoints:
- Before starting a major task
- After completing a feature
- When working in an area with past learnings

Quick status check:
```bash
grep -h "Status\*\*: pending" .learnings/*.md | wc -l
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["
```

## Best Practices

1. **Log immediately** — context is freshest right after the issue
2. **Be specific** — include exact commands, inputs, error output
3. **Suggest concrete fixes** — not just "investigate"
4. **Link related entries** — builds a knowledge graph over time
5. **Promote aggressively** — if it's come up 3+ times, put it in MEMORY.md
6. **Keep MEMORY.md concise** — promoted rules should be short prevention rules, not incident write-ups
