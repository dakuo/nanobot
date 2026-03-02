---
name: memory
description: Two-layer memory system with auto-recall and grep-based search.
always: true
---

# Memory

## Structure

- `memory/MEMORY.md` — Long-term facts (preferences, project context, relationships). Always loaded into your context.
- `memory/HISTORY.md` — Append-only event log. Each entry starts with [YYYY-MM-DD HH:MM].

## Auto-Recall

History entries relevant to the current message are **automatically retrieved** and included in your context under "Recalled History". You don't need to grep manually for most queries — the system extracts keywords from the user's message and searches HISTORY.md for matching entries.

You can still grep manually for more targeted searches:

```bash
grep -i "keyword" memory/HISTORY.md
```

Combine patterns: `grep -iE "meeting|deadline" memory/HISTORY.md`

## When to Update MEMORY.md

Write important facts immediately using `edit_file` or `write_file`:
- User preferences ("I prefer dark mode")
- Project context ("The API uses OAuth2")
- Relationships ("Alice is the project lead")

## Auto-consolidation

Old conversations are automatically summarized and appended to HISTORY.md when the session grows large. Long-term facts are extracted to MEMORY.md. You don't need to manage this.
