---
description: Run a generator/evaluator design loop for frontend or visual work with bounded iterations and scoring.
---

Parse the following from $ARGUMENTS:
1. `brief` — the user's description of the design to create
2. `--max-iterations N` — (optional, default 10) maximum design-evaluate cycles
3. `--pass-threshold N` — (optional, default 7.5) weighted score to pass (higher default for design)

**Factory routing (fix #29, GLOBAL-ROUTING_F29):** the design-lead is invoked inline as the orchestrator in Setup step 0 (not spawned as a drone — a spawned execution must carry a director brief); the generator/evaluator loop below runs as factory drones per the `/gan-build` pointer, each with a director brief (goal, files in/out of scope, constraints, acceptance criteria, verification steps, what to return), no-guessing, and orchestrator verification against the brief's acceptance criteria.

## GAN-Style Design Harness

A two-agent loop (Generator + Evaluator) focused on frontend design quality. No planner — the brief IS the spec, and the brief RESTATES the design direction from `docs/decision-record.md` when the record carries one, else the direction recorded by the design-lead (model `grok-4.7-extra-high`) in `docs/design-tokens.md` (Setup step 0 records it first on a cold start) — the direction lives in the file, never in the brief alone; on any divergence between the record and the spec, the record wins — the direction comes from the design-lead BEFORE the loop; the loop executes under it and does not re-derive a direction on its own.

This mode was used for frontend design experiments, with creative breakthroughs like the 3D Dutch art museum with CSS perspective and doorway navigation.

### Setup
0. Design-direction check (cold start) — BEFORE writing the spec or rubric, read `docs/decision-record.md` FIRST: if the record carries a named direction, adopt it — it is the direction for this build, and `docs/design-tokens.md` carries it (write it into the tokens file if the tokens file lacks it or carries a different one). Only when the record carries no direction, check whether `docs/design-tokens.md` carries a direction recorded by the design-lead (model `grok-4.7-extra-high`). 'Carries a direction' means the file exists AND contains a named `Design direction:` line (the theme slug + axes/mood, or the named style + axes) with its tokens — an empty file, a heading-only file, or a file with no `Design direction:` line does NOT count. If it does, proceed as below; if neither the record nor the tokens file carries a direction (cold start — no direction recorded yet), dispatch to the design skill for that surface — `design-taste-frontend` for a landing page, `ui-ux-pro-max` for a dashboard/app surface — on model `grok-4.7-extra-high`, first to generate the direction through the package skills (per the design-package rule) and record it in `docs/design-tokens.md` (the design-lead is invoked inline as the orchestrator here, not spawned as a drone — a spawned execution must carry a director brief), then restate that recorded direction in the brief/spec and proceed. Precedence on divergence: the decision record wins over the spec — the spec is translated from the record/scope, so a divergence means the translation drifted and the record is authoritative; the tokens file carries the record's direction. This is internal routing, never a user question — it never asks the user anything and never blocks the run. The generator still never re-derives a direction (see Key Difference below).
1. Create `gan-harness/` directory
2. Write the brief directly as `gan-harness/spec.md`
3. Write a design-focused `gan-harness/eval-rubric.md` with extra weight on Design Quality and Originality — and include the screen-distinctiveness scoping note at its top (copy it from `gan-style-harness` SKILL.md's rubric: screen distinctiveness is NOT scored here; it is judged ONLY by `browser-qa` in the visual loop). Every rubric written on any path must carry that deferral. Validate it before the loop starts: re-read `gan-harness/eval-rubric.md` and confirm the scoping note is at its top; if it is missing, prepend it — never start the loop on a rubric without it.

### Design-Specific Eval Rubric
```markdown
### Design Quality (weight: 0.35)
### Originality (weight: 0.30)
### Craft (weight: 0.25)
### Functionality (weight: 0.10)
```

Note: Originality weight is higher (0.30 vs 0.20) to push for creative breakthroughs. Functionality weight is lower since design mode focuses on visual quality.

### Loop
Same as `/gan-build` Phase 2, but:
- Skip the planner
- Use the design-focused rubric
- Generator prompt emphasizes visual quality over feature completeness
- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?" — but screen distinctiveness is NOT judged here: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop; the evaluator scores against `eval-rubric.md` only after the Setup step-3 validation confirms it carries that deferral (a rubric without the deferral is repaired before scoring — see Setup step 3).

### Key Difference from gan-build
The Generator is told: "Your PRIMARY goal is visual excellence within the recorded direction. A stunning half-finished app beats a functional ugly one. Push for creative leaps — unusual layouts, custom animations, distinctive color work — inside the design-lead's direction, never by re-deriving a new direction."
