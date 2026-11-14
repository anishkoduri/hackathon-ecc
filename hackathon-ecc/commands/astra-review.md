---
name: astra-review
description: "Deep, blind code review of a scoped change set by a fresh Grok deep-reasoner, followed by a fix cycle. (The Astra review backend was removed in fix #16; review now runs via Grok reviewers in Cursor.)"
---

# Deep Review

> The Astra review backend was removed in fix #16. Review now runs entirely in Cursor via Grok reviewers: a blind deep-reasoner pass for the review, fast-worker for fixes, deep-reasoner again for re-verification.

## Step 1: Scope

Scope the change set directly from git — no review tool needed:

```bash
git status --short
git diff --stat HEAD
git diff HEAD -- <paths>
```

Write down the scope: which files and hunks are in scope, which are out of scope, and the claim the change is making (what it is supposed to do).

## Step 2: Blind review (deep-reasoner)

Dispatch a blind review to the deep-reasoner as a **fresh subagent on Grok 4.7 High (`grok-4.7-high`)**, with no context from this conversation except the scope and the diff. The reviewer must not know who wrote the code or what the intended fix was beyond the claim:

- "Review this diff blind. For each finding: severity (blocker / major / minor), the exact file:line, what is wrong, and the concrete fix. Do not praise what works; list only findings. If a line is fine, say nothing about it."

The reviewer returns findings only — no code changes.

## Step 3: Fix cycle

- Fixes go to **fast-worker** (`cursor-grok-4.6-high-fast`) for mechanical fixes, or back to **deep-reasoner** (`grok-4.7-high`) for architectural ones.
- After fixes, run a **second blind deep-reasoner pass** over the fixed diff to re-verify (the second-pass pattern replaces any second-model peer review).
- Repeat until the second pass returns zero blockers.

## Verdict

```
Model: grok-4.7-high
Fixer: [fast-worker | deep-reasoner]
Scope: <files/hunks reviewed>
Blockers: <count>
Majors: <count>
Minors: <count>
Verdict: PASS | FAIL
```
