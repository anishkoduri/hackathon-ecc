---
description: Run a generator/evaluator build loop for implementation tasks with bounded iterations and scoring.
---

Parse the following from $ARGUMENTS:
1. `brief` — the user's one-line description of what to build
2. `--max-iterations N` — (optional, default 15) maximum generator-evaluator cycles
3. `--pass-threshold N` — (optional, default 7.0) weighted score to pass
4. `--skip-planner` — (optional) skip planner, assume spec.md already exists
5. `--eval-mode MODE` — (optional, default "playwright") one of: playwright, screenshot, code-only

**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the planner, generator, and evaluator passes below run as factory drones per `gan-style-harness` — each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria (a rubric pass with a failed acceptance criterion is a fail). Fan-out is bounded by efficiency: N>3 justified in one line; drones carry minimal context.

## GAN-Style Harness Build

This command orchestrates a three-agent build loop inspired by the upstream multi-agent harness design paper.

### Phase 0: Setup
1. Create `gan-harness/` directory in project root
2. Create subdirectories: `gan-harness/feedback/`, `gan-harness/screenshots/`
3. Initialize git if not already initialized
4. Log start time and configuration

### Phase 1: Planning (Planner Agent)
Step 0 runs ALWAYS, including under `--skip-planner` — it is a direction check, not planner work; only steps 1–4 are skipped under `--skip-planner` (with `--skip-planner`, no rubric is written here — the existing `gan-harness/eval-rubric.md` is used as-is and is validated in Phase 2 before any scoring). On the `--skip-planner` path (including every `/orch-build-mvp` step-4 drive, which always passes `--skip-planner`), step 0 is the cold-start path: step 0 reads the decision record first and adopts its direction when one exists; only when neither the record nor the tokens file carries one does the design-lead generate the direction first and record it in `docs/design-tokens.md` — the first UI slice then writes its tokens FROM that recorded direction, never inventing one.
0. Design-direction check (cold start) — BEFORE launching the planner, read `docs/decision-record.md` FIRST: if the record carries a named direction, adopt it — it is the direction for this build, and `docs/design-tokens.md` carries it (write it into the tokens file if the tokens file lacks it or carries a different one). Only when the record carries no direction, check whether `docs/design-tokens.md` carries a direction recorded by the design-lead (model `grok-4.7-extra-high`). 'Carries a direction' means the file exists AND contains a named `Design direction:` line (the theme slug + axes/mood, or the named style + axes) with its tokens — an empty file, a heading-only file, or a file with no `Design direction:` line does NOT count. If it does, pass it to the planner as in step 1; if neither the record nor the tokens file carries a direction (cold start — no direction recorded yet), dispatch to the design skill for that surface — `design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface — on model `grok-4.7-extra-high`, first to generate the direction through the package skills (per the design-package rule) and record it in `docs/design-tokens.md` (the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief), then launch the planner with that recorded direction. Precedence on divergence: the decision record wins over `gan-harness/spec.md` — spec.md is translated from the record/scope before `/gan-build` runs, so a divergence means the translation drifted and the record is authoritative; the tokens file carries the record's direction. This is internal routing, never a user question — it never asks the user anything and never blocks the run. The planner still never generates or re-derives a direction on its own (see step 1).
1. Launch the `gan-planner` agent (`agents/ecc-gan-planner.md`) as a Cursor subagent with the user's brief, plus the design direction in `docs/design-tokens.md` (step 0 records it first on a cold start — from `docs/decision-record.md` when the record carries one, else from the design-lead; on any divergence between the record and the spec, the record wins) — the direction comes from step 0 BEFORE the loop; the planner records it in the spec and the loop executes under it, it does not generate or re-derive a direction on its own
2. Wait for it to produce `gan-harness/spec.md` and `gan-harness/eval-rubric.md`
3. Display the spec summary to the user
3a. Orchestrator checks the planner's spec against the brief before Phase 2 (on the `--skip-planner` path, against the existing `gan-harness/spec.md`): the spec's files, scope, and acceptance criteria must match the brief's goal, files in/out of scope, constraints, and acceptance criteria. If the spec fails the check, the planner is re-dispatched with a correction brief naming the failed criterion and the required correction, distinct from the original brief (at most two correction re-dispatches, per the plugin's 2-round fix-loop convention; if the spec still fails, stop and report the failure with evidence).
4. Proceed to Phase 2

### Phase 2: Generator-Evaluator Loop
```
iteration = 1
while iteration <= max_iterations:

    # GENERATE
    Launch the `gan-generator` agent as a Cursor subagent:
    - Read spec.md and `docs/design-tokens.md` (the tokens file carries the decision record's direction; on any divergence between spec.md and the tokens file, the record's direction — as carried in the tokens file — wins: spec.md is derived from the record/scope, so a divergence means the translation drifted and the record is authoritative; never re-derive a direction from spec.md alone)
    - Files out of scope: [named by the orchestrator from the spec before launch; `none` if genuinely none] — the generator touches only the spec's files.
    - If iteration > 1: read feedback/feedback-{iteration-1}.md
    - Build/improve the application — TDD: write the tests for the new/changed behaviour FIRST (`tdd-guide`: red → green → refactor) before implementing it; the tests live in the repo with the code, not in the harness
    - Ensure dev server is running
    - Commit changes
    - Verification steps: run the TDD tests you wrote plus the acceptance criteria from the spec — paste the test output; the build must pass and the acceptance criteria must hold before finishing.
    - Return format: Status first, then files changed, test output, concerns.

    # Wait for generator to finish

    # EVALUATE
    Launch the `gan-evaluator` agent as a Cursor subagent:
    - Read eval-rubric.md and spec.md
    - Validate `gan-harness/eval-rubric.md` before scoring: confirm the screen-distinctiveness scoping note is at its top; if it is missing, prepend the note (copied from the `gan-style-harness` SKILL.md rubric) to the rubric file, record the repair in the feedback file, and score the Design Quality / Originality rows on the recorded direction and its code-level application only — never score screen distinctiveness.
    - Test the live application (mode: playwright/screenshot/code-only)
    - Run the repo tests the generator wrote (`tdd-guide` tests) — a failing test caps the score below the pass threshold regardless of how the live app looks
    - Score against rubric
    - Write feedback to feedback/feedback-{iteration}.md

    # Wait for evaluator to finish

    # ORCHESTRATOR-CHECK
    After each evaluator pass, the orchestrator checks the generator's output against the brief's acceptance criteria (not just the rubric score — a rubric pass at or above 7.0 with a failed acceptance criterion is a fail) and re-checks the evaluator's pass/fail call against the same criteria. A rubric pass with a failed acceptance criterion is a fail: the generator is re-dispatched with a correction brief naming the failed criterion and the required correction, distinct from the original brief — the re-dispatch is the next iteration's GENERATE, consuming one iteration within max_iterations; skip CHECK SCORE and continue the loop. A rubric fail the orchestrator finds actually passes the criteria is a re-check, not a loop exit: the evaluator's call is corrected and the loop continues to CHECK SCORE.

    # CHECK SCORE — runs only after the orchestrator check above passes
    Read feedback/feedback-{iteration}.md
    Extract weighted total score

    if score >= pass_threshold:
        Log "PASSED at iteration {iteration} with score {score}"
        Break

    if iteration >= 3 and score has not improved in last 2 iterations:
        Log "PLATEAU detected — stopping early"
        Break

    iteration += 1
```

### Phase 3: Summary
1. Read all feedback files
2. Display final scores and iteration history
3. Show score progression: `iteration 1: 4.2 → iteration 2: 5.8 → ... → iteration N: 7.5`
4. List any remaining issues from the final evaluation
5. Report total time and estimated cost

### Output

```markdown
## GAN Harness Build Report

**Brief:** [original prompt]
**Result:** PASS/FAIL
**Iterations:** N / max
**Final Score:** X.X / 10

### Score Progression
| Iter | Design | Originality | Craft | Functionality | Total |
|------|--------|-------------|-------|---------------|-------|
| 1 | ... | ... | ... | ... | X.X |
| 2 | ... | ... | ... | ... | X.X |
| N | ... | ... | ... | ... | X.X |

### Remaining Issues
- [Any issues from final evaluation]

### Files Created
- gan-harness/spec.md
- gan-harness/eval-rubric.md
- gan-harness/feedback/feedback-001.md through feedback-NNN.md
- gan-harness/generator-state.md
- gan-harness/build-report.md
```

Write the full report to `gan-harness/build-report.md`.
