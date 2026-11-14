# Polish Pass

Diagnoses the target, then applies only the Lenses that raise its Score, and verifies the result visually. It keeps the current look and identity. **It edits code.**

## Lenses

Each Lens has a playbook in `reference/lenses/`. Read a Lens's file before applying it. See SKILL.md for the table. Never apply a lens that picks a new visual direction — those are not in this skill; if the diagnosis calls for one, that is a redesign: append the per-screen evidence to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill and listed under "Still short of 10/10" — not applied here.

## Step 1: Context

1. Read the target's design system (SKILL.md → Design system): read `docs/design-tokens.md` when it exists (else `design-system/<project-slug>/MASTER.md`) as the token source of truth, plus the project's theme file and shared components, and who the product is for and what the target must do. If the project has no recorded tokens, infer the system from the code and proceed.
2. Read the target's source and its neighbors: shared components, tokens, and similar screens. **Before drawing or hand-styling any component, search the system for one with the same job** (component folders, Storybook, the UI library in `package.json`; search by role: `Tooltip`, `Chip`, `Avatar`, `IconButton`, `EmptyState`). Reuse or extend it. If none exists, say what you searched for in the report. Fix problems at the right level: a missing token goes into the system, a one-off becomes the shared component, a local bug gets fixed locally.
3. Read the matching pattern files: [patterns/forms.md](patterns/forms.md) whenever the target has an input, select, or submit action, [patterns/mobile-web.md](patterns/mobile-web.md) whenever a mobile cell exists, and always [patterns/vibe-code-tells.md](patterns/vibe-code-tells.md).

## Step 2: Baseline Capture + diagnosis

1. Run a **before** Capture across the Capture Matrix ([capture.md](capture.md)) with `--label before`.
2. Run the detector on the target's source: `node <skill dir>/scripts/detect.mjs <paths>`. Then run the Impeccable detector on the same paths: `npx impeccable@4.8.0 detect <paths> [--json]` (pinned; no API key, no LLM). It checks 62 rules ([impeccable-detector-rules.json](impeccable-detector-rules.json)) including rendered-page rules the static scan cannot see — run it against the running app's URL as well as the source when the app is running. Treat its findings the same way: evidence to verify, not verdicts. If the Impeccable detector cannot run (engine download failure, SHA mismatch, or no network on first run), record that and proceed on the static detector's findings — never block the pass on it. This step runs on every pass, including score-only passes and small fixes — no pass skips the detector runs by default. The only excuse is no source available for the target (record that in the report); a detector that cannot run is recorded and the pass proceeds on the other detector's findings.
3. Do a **quick internal score** using the Dimensions and calibration in [scoring.md](scoring.md): score each Dimension, list the gaps. Don't print a full report; keep it short. If any Dimension scores below 6, run the Impeccable critique playbook ([impeccable-critique.md](impeccable-critique.md)) — a scored review with persona testing and ranked fixes — and fold its Priority fixes into the Lens plan.
4. Note every vibe-code tell from [patterns/vibe-code-tells.md](patterns/vibe-code-tells.md); each one becomes a planned fix under its listed Lens (rows marked "report" go in the report as redesign items, not fixes). A generic-template observation (Level 2 template on [scoring.md](scoring.md), three or more vibe-code tells, or a Persona-fit cap from the generic look) is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa`, with per-screen evidence — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (Step 3), not just a report note.
5. If a score from this conversation exists for the same target, reuse its Priority fixes.
6. If the diagnosis is functional — a button or control does nothing when clicked, or leaves the UI in the wrong state — invoke `click-path-audit` for the state/click diagnosis instead of guessing a cosmetic fix. Polish fixes the states and feedback around the control; the click path itself belongs to `click-path-audit`.

7. Run the **harmony check** (SKILL.md → The harmony rule): read the recorded direction in `docs/design-tokens.md` (or `design-system/<project-slug>/MASTER.md`), then check each primary screen for consistency of tokens/type/color/spacing against that direction. Record per-screen consistency (consistent / diverges, with the tokens cited) for the report. Harmony does NOT judge whether a screen reads as a default template — that is the distinctiveness bar: pass/fail verdicts on rendered screens, executed by `browser-qa` ONLY, in the visual loop. A screen whose consistency check suggests the direction is not applied is appended to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` (which screen, which tokens diverge) — a **generic-template finding** exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (see Step 3); it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy. If neither file exists, do NOT infer a direction from the code — record a missing-direction finding (minor at least) routed to the design skill, and do not pass any screen on consistency against an unrecorded direction.

8. Run the **slop checklist** ([slop-checklist.md](slop-checklist.md), `SLOP_F22`) on the target's source and Capture: walk the 20 checks (C1–C20) plus the accent-sprawl check (`ACCENT_F22`) and the accent-hierarchy check (`ACCENTUATION_F22`). Each flagged instance is a static/code-level finding and candidate evidence for `browser-qa` — never a verdict. A flag is cleared only by a recorded D19 reason + theme-fit in `docs/design-tokens.md`; a flag with neither stays a finding and is fixed with its paired fix in [unslop-fixes.md](unslop-fixes.md) (`UNSLOP_F22`). Template-pattern instances (a whole screen built from the flagged defaults) go to `.hallmark/candidate-evidence.md` for `browser-qa`.

## Step 3: Plan the Lenses

- **Forced Lenses** (named by the user) always run. Also fix any P0 issue you see, and mention it.
- **Otherwise** pick the Lenses for every Dimension scoring below 9, ordered by impact. Usually 3–6 Lenses; **polish-details** always runs last. Structural fixes a Lens suggests follow the polish scope rule in [layout](lenses/layout.md): adjust within the existing structure, and report the rest as a redesign recommendation.
- Fix in this order: broken or blocked tasks and a11y blockers → missing states → hierarchy/layout/responsive → type/color/consistency → motion → cleanup.
- If the diagnosis shows systemic drift — the same value or pattern repeated in three or more places with no token, or tokens missing across screens — record it as a **design-system finding** routed to the `design-system` skill (tokens to `design-tokens.json`, 10-dimension score) via the orchestrator; polish-pass consolidates only the repeated pattern it was already fixing under extract, it does not run a design-system audit itself.

**Ask before proceeding only if** the plan would: change brand identity or the overall visual direction (that's a redesign; out of scope for this skill — report it instead), change factual copy or claims, add a dependency (font, library), or remove a feature. Otherwise proceed without asking; state the plan in one or two lines — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you proceed without waiting and record it as blocked in the final report if you cannot resolve it; never stop for a human decision mid-build. A plan item that would need asking is resolved by the safe option instead — leave copy, claims, and brand identity unchanged, add no dependency, remove nothing — or recorded as blocked.

If the baseline sits below Level 6 (template) on [scoring.md](scoring.md), polish can't reach 10/10 on its own: it keeps the look, and a surface moves past 6 only through a product idea or a new direction that polish isn't allowed to invent. Still apply the Lenses, but append the generic-template observation to `.hallmark/candidate-evidence.md` as candidate evidence for `browser-qa` — a FINDING exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps — the orchestrator routes it; it also stays listed under "Still short of 10/10", naming the artifact or idea each weak section is missing, until that redesign lands and is re-verified by `browser-qa` before deploy.

## Step 4: Apply

1. Read [craft-floor.md](craft-floor.md) once before the first edit, and the Impeccable craft floor ([impeccable-craft-floor.md](impeccable-craft-floor.md)) — its bans are absolute as static/code-level checks — a ban is design guidance / static-check evidence, never a pass/fail verdict on a rendered screen (that verdict is `browser-qa`'s alone); where the two floors disagree, the stricter ban wins — except page-level template patterns, which are candidate evidence for `browser-qa`, never a rewrite decided here. Also read the slop checklist ([slop-checklist.md](slop-checklist.md), `SLOP_F22`) and its fixes ([unslop-fixes.md](unslop-fixes.md), `UNSLOP_F22`) once before the first edit — a flag there is cleared only by a recorded D19 reason + theme-fit.
2. For each planned Lens, read its file in `reference/lenses/` and apply it to the target. When animate runs, build from [patterns/motion-recipes.md](patterns/motion-recipes.md); when harden runs on a data-driven component, test it against [patterns/worst-case-data.md](patterns/worst-case-data.md). When harden runs on a first-run, empty-state, or activation surface, also read [impeccable-onboard.md](impeccable-onboard.md) and apply its first-run/empty-state/activation guidance (fix-only: do not invent onboarding copy or product claims). When consistency finds the same pattern or value repeated in three or more places, consolidate it into the shared system following [impeccable-extract.md](impeccable-extract.md) (pull repeated patterns/tokens/components into the design system; never extract a one-off).
3. Use the project's tokens. If a needed value doesn't exist, add a token to the system (and to the token file) instead of hard-coding.
4. Keep changes scoped to the target and to the shared code it genuinely needs. No drive-by refactors.
   - **Check what's coupled to the geometry before changing it.** A spacing, indent, or size value may drive something else: connector lines in trees, timeline rails, avatar stacks, sticky offsets, scroll calculations, or canvas/SVG math. Search for the value and its token before proposing a change; if it's coupled, change both together or leave it.
5. Remove what you made obsolete: dead styles, unused imports, duplicate values, debug code.

## Step 5: Verify (one after-Capture)

1. Run the project's type-check/lint/build if they exist and are fast. Fix what you broke.
2. Re-run the detector on edited files. Fix real findings. Accept a flagged item only after you've verified it's safe, and record why in the report (e.g. `outline: none` is fine only when you confirmed a visible `:focus-visible` replacement such as a ring or border, in light and dark). Re-run the Impeccable detector too (`npx impeccable@4.8.0 detect <paths>`), and fix real findings the same way — EXCEPT a template-pattern finding (e.g. `icon-tile-stack`: a small rounded-square icon container above a heading is the universal AI feature-card template): append it to `.hallmark/candidate-evidence.md` (screen + what reads as a template) for `browser-qa`, and fix it only on `browser-qa`'s verdict — never rewrite a template pattern on the detector's say-so alone. If it cannot run here either, record that and proceed on the static detector's findings.
3. Run the project's tests that touch what you changed. New UI can break selectors: e.g. a search box inside a popup adds a second combobox, so tests must find each one by its accessible name, not by role alone. Update tests to be specific; never delete or skip them to pass.
4. Run an **after** Capture across the same cells (`--label after`), plus rest, hover, pressed, and focus-visible (and tooltip/menu states) for every control you changed. Confirm each dark cell really rendered dark ([capture.md](capture.md) → Step 3). Check for regressions in every cell, especially dark mode and mobile. Every cell's `rowMismatches` must be empty ([craft-floor.md](craft-floor.md) → Spacing and layout).
5. Fix what the Capture shows, then re-capture **once** to confirm. Don't loop on cosmetic churn; only the gate in step 9 adds further rounds.
6. **If you regenerated visual-test baselines, open and look at them.** A baseline clipped by the test viewport, or taken mid-animation, locks in a bug. Fix the test's viewport or wait condition, not just the image.
7. **"Done" includes the surrounding docs.** Update everything that describes what you changed: prose about motion, tokens, and components (token files, READMEs, Storybook/MDX docs, code comments), and visual baselines. A token that was renamed or retimed must match everywhere it's documented.
8. Re-score each Dimension honestly, applying the uncaptured-state caps from [scoring.md](scoring.md) → Calibration. In the report, say "verified" only for what was checked under the user's real conditions ([capture.md](capture.md) → Step 2).
9. **Independent re-score gate.** The builder doesn't grade its own work. Re-score the after-Capture in a fresh context: a sub-agent if the harness has one; otherwise re-read [scoring.md](scoring.md) and judge from the captures alone, ignoring what you meant to build. Give it the target, the project's tokens, and the capture paths, not your change list or intent. If its Overall is below 8, or below Level 8 for the mode, fix its Priority fixes that fit this pass (polish keeps the look), re-capture, and run a new fresh re-score. Stop after 2 rounds. The report's after-Score is the last independent re-score's score, not your own, and its open findings go under "Still short of 10/10".

## Step 6: Report

```markdown
## Polish pass: <target> (<url | screenshot | file | feature>; files: <edited files>)
Design context: <project tokens/components, or "none">
**Score: X/10 → Y/10** · Lenses: <applied> · Captured: <cells and states> (before/after paths) · Not captured: <states, or "none">

### Changes
| Before | After | Why (for the user) |
|---|---|---|
| `<file>`: `transition: all 300ms` | `transition: transform 160ms var(--ease-out)` | <Lens>: … |

One row per meaningful change, grouped by Lens. Use the real old and new values, not paraphrase.

### Dimension deltas
| Dimension | Before | After |
|---|---|---|

### Harmony check
| Screen | Consistency vs recorded direction | Result |
|---|---|---|
| <screen> | <consistent / inconsistent + evidence> | <consistent / diverges (tokens cited)> |

Direction-application is `browser-qa`'s verdict, cited not judged: record it here only if `browser-qa` has already rendered it on the screen, with the verdict cited; otherwise leave it out.

### Generic-template findings (only on `browser-qa`'s visual-loop verdict)
- <screen>: <`browser-qa`'s verdict + evidence> — routed to <`ui-ux-pro-max` | `design-taste-frontend`> for redesign (omit if no `browser-qa` verdict; candidate evidence alone is recorded under Harmony check / "Still short of 10/10", not here)

### Accepted detector findings
- <rule> at <file:line>: <why it's safe, and how you verified it> (omit if none)

List every real Impeccable detector finding here, fixed and left open, with its rule id and file:line — this section is the findings' durable record, not the detector's stdout.

### Slop-checklist findings (SLOP_F22)
- <check id, e.g. C6 / ACCENT_F22> on <screen>: <what was seen> — <fixed with D<fix> | cleared with D19 reason + theme-fit, reason cited> (omit if none; a flag with neither stays listed here as open)

### 10 highest-impact REMAINING improvements
1. <highest-impact remaining improvement, with impact/effort/risk>
2. …

Ranked by impact/effort/risk; this is the list orchestrate's final report consumes as highest-value next improvements.

### Still short of 10/10
- <remaining gaps, with what it would take: content, assets, or decisions only the user can make>
```

Keep it tight. If the look itself needs a new direction, end with: "The remaining gaps need a redesign (new direction), which is out of scope for a polish pass — run `ui-ux-pro-max` for that."
