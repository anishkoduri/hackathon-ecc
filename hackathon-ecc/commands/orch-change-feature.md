---
description: Orchestrate altering an existing, working feature to new desired behavior — update tests to the new spec, change impl, review, gated commit. Wrapper for the orch-change-feature skill.
---

# /orch-change-feature

Manually launch the **orch-change-feature** orchestrator: change behavior that
already works to a new desired spec, tests-first.

## Usage

```
/orch-change-feature <the new desired behavior>
```

Examples:

```
/orch-change-feature make nws-poller alert at 2 warnings instead of 3
/orch-change-feature instead of sorting by date, sort by priority
```

## What It Does

Invoke the `orch-change-feature` skill with `$ARGUMENTS` as the request. If `$ARGUMENTS` asks to remove a feature — including a one-prompt removal of a first-build feature — follow the skill's `Removing a feature` section instead of the change steps below: delete, verify no references remain, commit (or mark blocked and stop if the tests fail after deletion — never commit broken, see the skill), then re-deploy (push to `main` for the Vercel frontend + `railway up` for a split Railway backend), wait for the deploy to be ready (bounded wait, local-film fallback — never film a stale deployed URL), update `shots.json` before re-filming, re-film locally via `/demo --rebuild`, re-upload the video and update its link, update the docs, inventory, and pitch, and deliver the updated final report as the reply (the done signal for the removal). The skill
(via the shared `orch-pipeline` engine) will:

1. Classify size (default floor: small) and state the tier.
2. Light plan only if the new behavior needs research. → **GATE 1** (approve changed-test plan; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).
3. **Update the existing tests** to express the new behavior, then change the
   implementation until green. (Changing the tests first is what makes this a
   tweak, not a fix.)
4. `code-reviewer` (+ `security-reviewer` on a security trigger), then commit. → **GATE 2** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).

Honor both gates — do not write implementation before Gate 1, do not commit before Gate 2 — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting.

Use this only when the feature **works** but should behave differently — not for
bugs (`/orch-fix-defect`) or net-new capability (`/orch-add-feature`).

If `$ARGUMENTS` is empty, ask the user what behavior should change. — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you do NOT ask: proceed on `docs/decision-record.md` + `docs/scope.md` (or the raw prompt with a stated assumption if neither exists).
