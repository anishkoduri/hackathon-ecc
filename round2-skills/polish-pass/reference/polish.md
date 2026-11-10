# Polish Pass

Diagnoses the target, then applies only the Lenses that raise its Score, and verifies the result visually. It keeps the current look and identity. **It edits code.**

## Lenses

Each Lens has a playbook in `reference/lenses/`. Read a Lens's file before applying it. See SKILL.md for the table. Never apply a lens that picks a new visual direction — those are not in this skill; if the diagnosis calls for one, that is a redesign, reported under "Still short of 10/10", not applied here.

## Step 1: Context

1. Read the target's design system (SKILL.md → Design system): the project's tokens, theme file, and shared components, plus who the product is for and what the target must do. If the project has no recorded tokens, infer the system from the code and proceed.
2. Read the target's source and its neighbors: shared components, tokens, and similar screens. **Before drawing or hand-styling any component, search the system for one with the same job** (component folders, Storybook, the UI library in `package.json`; search by role: `Tooltip`, `Chip`, `Avatar`, `IconButton`, `EmptyState`). Reuse or extend it. If none exists, say what you searched for in the report. Fix problems at the right level: a missing token goes into the system, a one-off becomes the shared component, a local bug gets fixed locally.
3. Read the matching pattern files: [patterns/forms.md](patterns/forms.md) whenever the target has an input, select, or submit action, [patterns/mobile-web.md](patterns/mobile-web.md) whenever a mobile cell exists, and always [patterns/vibe-code-tells.md](patterns/vibe-code-tells.md).

## Step 2: Baseline Capture + diagnosis

1. Run a **before** Capture across the Capture Matrix ([capture.md](capture.md)) with `--label before`.
2. Run the detector on the target's source: `node <skill dir>/scripts/detect.mjs <paths>`.
3. Do a **quick internal score** using the Dimensions and calibration in [scoring.md](scoring.md): score each Dimension, list the gaps. Don't print a full report; keep it short.
4. Note every vibe-code tell from [patterns/vibe-code-tells.md](patterns/vibe-code-tells.md); each one becomes a planned fix under its listed Lens (rows marked "report" go in the report as redesign items, not fixes).
5. If a score from this conversation exists for the same target, reuse its Priority fixes.

## Step 3: Plan the Lenses

- **Forced Lenses** (named by the user) always run. Also fix any P0 issue you see, and mention it.
- **Otherwise** pick the Lenses for every Dimension scoring below 9, ordered by impact. Usually 3–6 Lenses; **polish-details** always runs last. Structural fixes a Lens suggests follow the polish scope rule in [layout](lenses/layout.md): adjust within the existing structure, and report the rest as a redesign recommendation.
- Fix in this order: broken or blocked tasks and a11y blockers → missing states → hierarchy/layout/responsive → type/color/consistency → motion → cleanup.

**Ask before proceeding only if** the plan would: change brand identity or the overall visual direction (that's a redesign; out of scope for this skill — report it instead), change factual copy or claims, add a dependency (font, library), or remove a feature. Otherwise proceed without asking; state the plan in one or two lines.

If the baseline sits below Level 6 (template) on [scoring.md](scoring.md), polish can't reach 10/10 on its own: it keeps the look, and a surface moves past 6 only through a product idea or a new direction that polish isn't allowed to invent. Still apply the Lenses, but recommend a redesign under "Still short of 10/10", naming the artifact or idea each weak section is missing.

## Step 4: Apply

1. Read [craft-floor.md](craft-floor.md) once before the first edit.
2. For each planned Lens, read its file in `reference/lenses/` and apply it to the target. When animate runs, build from [patterns/motion-recipes.md](patterns/motion-recipes.md); when harden runs on a data-driven component, test it against [patterns/worst-case-data.md](patterns/worst-case-data.md).
3. Use the project's tokens. If a needed value doesn't exist, add a token to the system (and to the token file) instead of hard-coding.
4. Keep changes scoped to the target and to the shared code it genuinely needs. No drive-by refactors.
   - **Check what's coupled to the geometry before changing it.** A spacing, indent, or size value may drive something else: connector lines in trees, timeline rails, avatar stacks, sticky offsets, scroll calculations, or canvas/SVG math. Search for the value and its token before proposing a change; if it's coupled, change both together or leave it.
5. Remove what you made obsolete: dead styles, unused imports, duplicate values, debug code.

## Step 5: Verify (one after-Capture)

1. Run the project's type-check/lint/build if they exist and are fast. Fix what you broke.
2. Re-run the detector on edited files. Fix real findings. Accept a flagged item only after you've verified it's safe, and record why in the report (e.g. `outline: none` is fine only when you confirmed a visible `:focus-visible` replacement such as a ring or border, in light and dark).
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

### Accepted detector findings
- <rule> at <file:line>: <why it's safe, and how you verified it> (omit if none)

### Still short of 10/10
- <remaining gaps, with what it would take: content, assets, or decisions only the user can make>
```

Keep it tight. If the look itself needs a new direction, end with: "The remaining gaps need a redesign (new direction), which is out of scope for a polish pass — run `ui-ux-pro-max` for that."
