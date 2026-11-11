#!/usr/bin/env python3
"""fix13-package.py — Fixer B (fix program #13): DESIGN-PACKAGE COMPONENTS.

Patches staged sources ONLY:
  - round2-skills/polish-pass/SKILL.md
  - round2-skills/polish-pass/reference/polish.md
  - round2-skills/polish-pass/reference/scoring.md
  - new-skills/design-taste-frontend/SKILL.md
  - ~/workspace/cursor-skills/less-flat-ui/SKILL.md  (durable source; build.sh
    copies it fresh into the plugin on every build)

Does NOT touch: orchestrate / orch-* / hackathon-mode.mdc / feature-expansion /
grill-me / hackathon-scope / dispatch-prompt.md (fixer A), build.sh, the repo,
the bundle. Does NOT edit any staged copy of ui-ux-pro-max (upstream-fetched);
its changes go ONLY as a runtime patch block, whose exact text lives in
MANIFEST-B.md for the coordinator to append LAST before STEP 5.

Every hunk asserts its anchor occurs exactly once in the target file. If an
anchor does not match, that hunk is SKIPPED and reported — never guessed.
Exit code is non-zero if any hunk failed.
"""
import sys
from pathlib import Path

HOME = Path.home()
PLUGIN = HOME / "workspace" / "hackathon-plugin"

results = []  # (hunk_id, target, ok, detail)


def sub(hunk_id, path, old, new):
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        results.append((hunk_id, str(path), False, "FILE NOT FOUND"))
        return
    n = text.count(old)
    if n != 1:
        results.append((hunk_id, str(path), False,
                        f"anchor count={n} (expected 1); hunk SKIPPED"))
        return
    path.write_text(text.replace(old, new), encoding="utf-8")
    results.append((hunk_id, str(path), True, "applied"))


POLISH_SKILL = PLUGIN / "round2-skills/polish-pass/SKILL.md"
POLISH_MD = PLUGIN / "round2-skills/polish-pass/reference/polish.md"
SCORING_MD = PLUGIN / "round2-skills/polish-pass/reference/scoring.md"
TASTE_SKILL = PLUGIN / "new-skills/design-taste-frontend/SKILL.md"
LESSFLAT_SKILL = HOME / "workspace/cursor-skills/less-flat-ui/SKILL.md"

# ---------------------------------------------------------------- polish-pass SKILL.md
# H1: generic-template diagnosis becomes a FINDING routed to the design skill.
# (Build.sh patch (f) anchors preserved verbatim: the "If the user asks..."
# sentence is untouched, as are the description line and the When-to-use row.)
sub("H1", POLISH_SKILL,
    """Apply the polish fixes that fit, then say so in the report under "Still short of 10/10" and name what a redesign would take.""",
    """Apply the polish fixes that fit, then record it as a generic-template FINDING in the report — per-screen evidence, which screens fail the harmony check and how — so the orchestrator routes it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps; it stays listed under "Still short of 10/10" until that redesign lands.""")

# H2: strengthen the Harmony rule in place — an invoked consistency check.
# (The build.sh patch (f) anchor sentence "The plugin already has
# `ui-ux-pro-max` and `less-flat-ui` for design direction and surface
# treatments. Those skills own the look." is NOT touched by this hunk: the
# new subsection is inserted after the "Never:" bullet, leaving that
# sentence intact so the build-time patch still applies.)
sub("H2", POLISH_SKILL,
    """- **Never:** change the color palette, typefaces, visual style, layout structure, or brand identity; invent a new direction; add decorative motion, new effects, or a "bolder" look.""",
    """- **Never:** change the color palette, typefaces, visual style, layout structure, or brand identity; invent a new direction; add decorative motion, new effects, or a "bolder" look.

### The harmony check — runs on every pass

The harmony rule is not a preamble: it is a check this skill executes on every pass, including small fixes and score-only passes. Read the recorded direction first — `docs/design-tokens.md` (its first lines carry the named direction) or `design-system/<project-slug>/MASTER.md`; if neither exists, infer the direction from the code and record it in the token file before judging (see Design system below). Then, for each primary screen, check two things and record per-screen pass/fail in the report under "Harmony check": (1) **consistency** — tokens, type scale, color, radii, and spacing match the recorded direction, with no one-off values; (2) **direction-application** — the screen visibly traces to the named direction (its material, anchor, or theme is present and recognizable), rather than looking like a default template that could belong to any product. A screen that fails direction-application is a generic-template finding (see above): it routes to the design skill for a redesign, it is never restyled here, and it caps Persona fit per [reference/scoring.md](reference/scoring.md). There is no standalone harmony skill: this rule, executed by the steps in [reference/polish.md](reference/polish.md), is the harmony check.""")

# H3: first-build paragraph — finding routing, not just a report note.
sub("H3", POLISH_SKILL,
    """and a look that itself is the problem is reported under "Still short of 10/10", not redesigned here.""",
    """and a look that itself is the problem is recorded as a generic-template finding for the orchestrator to route back to the design skill (and listed under "Still short of 10/10" until redesigned), not redesigned here.""")

# H4: craft-floor reads required on every pass, not just before an edit.
sub("H4a", POLISH_SKILL,
    """Read [reference/craft-floor.md](reference/craft-floor.md) before any UI edit.""",
    """Read [reference/craft-floor.md](reference/craft-floor.md) before judging or editing on every pass — score-only passes and small fixes included, not just edit passes.""")
sub("H4b", POLISH_SKILL,
    """before the first edit: its bans are absolute""",
    """before judging or editing on every pass: its bans are absolute""")

# H5: detector runs required on every pass, including score-only + small fixes.
# The detector-failure fallback (record and proceed) is kept; only the
# silent skip is closed. No source available is the sole excuse, recorded.
sub("H5a", POLISH_SKILL,
    """5. **Run the detector** on edited or critiqued source files:""",
    """5. **Run the detector** on the target's source files on every pass — edit passes, score-only passes, and small fixes alike:""")
sub("H5b", POLISH_SKILL,
    """record that and proceed on the static detector's findings — never block the pass on it.""",
    """record that and proceed on the static detector's findings — never block the pass on it. The detector runs are attempted on every pass by default; the only excuse for not running one is that no source is available for the target (record that in the report). A detector that cannot run is recorded and the pass proceeds on the other detector's findings — never block, never silently skip.""")

# H6: score-only path no longer skips the detector + craft-floor reads.
sub("H6", POLISH_SKILL,
    """| Only an opinion or a rating, no edits | Score it with [reference/scoring.md](reference/scoring.md) and report; do not edit |""",
    """| Only an opinion or a rating, no edits | Score it with [reference/scoring.md](reference/scoring.md) and report; do not edit — but still run the harmony check and both detector reads (non-negotiables 4–5) when source is available, and record it when no source is available |""")

# H7: name the harmony check as a non-negotiable so it is executed, not loaded.
sub("H7", POLISH_SKILL,
    """6. **Be concrete.** Name the element, file, value, and fix. "Improve spacing" is not feedback; "Hero CTA sits 8px from the subhead; use `--space-6` (24px)" is.""",
    """6. **Be concrete.** Name the element, file, value, and fix. "Improve spacing" is not feedback; "Hero CTA sits 8px from the subhead; use `--space-6` (24px)" is.

7. **Run the harmony check.** On every pass, run the harmony check (## The harmony rule): read the recorded direction, check each primary screen for consistency and direction-application, and record per-screen pass/fail in the report. A generic-template failure is a finding routed to the design skill, never a silent note.""")

# ---------------------------------------------------------------- polish.md
# P1: detector step runs on every pass — close the score-only / small-fix skip.
sub("P1", POLISH_MD,
    """If the Impeccable detector cannot run (engine download failure, SHA mismatch, or no network on first run), record that and proceed on the static detector's findings — never block the pass on it.""",
    """If the Impeccable detector cannot run (engine download failure, SHA mismatch, or no network on first run), record that and proceed on the static detector's findings — never block the pass on it. This step runs on every pass, including score-only passes and small fixes — no pass skips the detector runs by default. The only excuse is no source available for the target (record that in the report); a detector that cannot run is recorded and the pass proceeds on the other detector's findings.""")

# P2: harmony check as an executed Step 2 item (per-screen pass/fail).
sub("P2", POLISH_MD,
    """the click path itself belongs to `click-path-audit`.""",
    """the click path itself belongs to `click-path-audit`.

7. Run the **harmony check** (SKILL.md → The harmony rule): read the recorded direction in `docs/design-tokens.md` (or `design-system/<project-slug>/MASTER.md`), then check each primary screen for (a) consistency of tokens/type/color/spacing against that direction and (b) direction-application — does the screen visibly trace to the named direction? Record per-screen pass/fail for the report. A screen that fails direction-application is a **generic-template finding**: record it with evidence (which screen, what makes it a default template) — it routes to the design skill for a redesign (see Step 3), it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned.""")

# P3: generic-template diagnosis is a FINDING, not just a report note.
sub("P3", POLISH_MD,
    """each one becomes a planned fix under its listed Lens (rows marked "report" go in the report as redesign items, not fixes).""",
    """each one becomes a planned fix under its listed Lens (rows marked "report" go in the report as redesign items, not fixes). A generic-template diagnosis (Level 2 template on [scoring.md](scoring.md), three or more vibe-code tells, or a Persona-fit cap from the generic look) is recorded as a generic-template FINDING with per-screen evidence — it routes to the design skill for a redesign (Step 3), not just a report note.""")

# P4: below-Level-6 baseline routes to the fix loop via a finding.
sub("P4", POLISH_MD,
    """Still apply the Lenses, but recommend a redesign under "Still short of 10/10", naming the artifact or idea each weak section is missing.""",
    """Still apply the Lenses, but record the generic-template diagnosis as a FINDING routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps — the orchestrator routes it; it also stays listed under "Still short of 10/10", naming the artifact or idea each weak section is missing, until that redesign lands.""")

# P5: systemic drift routes to the design-system skill as a finding.
sub("P5", POLISH_MD,
    """- Fix in this order: broken or blocked tasks and a11y blockers → missing states → hierarchy/layout/responsive → type/color/consistency → motion → cleanup.""",
    """- Fix in this order: broken or blocked tasks and a11y blockers → missing states → hierarchy/layout/responsive → type/color/consistency → motion → cleanup.
- If the diagnosis shows systemic drift — the same value or pattern repeated in three or more places with no token, or tokens missing across screens — record it as a **design-system finding** routed to the `design-system` skill (tokens to `design-tokens.json`, 10-dimension score) via the orchestrator; polish-pass consolidates only the repeated pattern it was already fixing under extract, it does not run a design-system audit itself.""")

# P6: report template gains Harmony check + Generic-template findings sections.
sub("P6", POLISH_MD,
    """### Accepted detector findings""",
    """### Harmony check
| Screen | Consistency vs recorded direction | Direction-application | Result |
|---|---|---|---|
| <screen> | <pass/fail + evidence> | <pass/fail + evidence> | <pass/fail> |

### Generic-template findings
- <screen>: <what makes it a default template> — routed to <`ui-ux-pro-max` | `design-taste-frontend`> for redesign (omit if none)

### Accepted detector findings""")

# P7: lenses intro — redesign is a routed finding, not just a report note.
sub("P7", POLISH_MD,
    """that is a redesign, reported under "Still short of 10/10", not applied here.""",
    """that is a redesign, recorded as a generic-template finding routed to the design skill and listed under "Still short of 10/10", not applied here.""")

# ---------------------------------------------------------------- scoring.md
# S1: generic-template diagnosis is a routed FINDING, not only a score cap.
# The cap itself (Persuade Persona fit ≤ 6) is unchanged.
sub("S1", SCORING_MD,
    """Generic "AI-template" look (the craft-floor slop tells) can't score above 6 on Persona fit for a Persuade surface.""",
    """Generic "AI-template" look (the craft-floor slop tells) can't score above 6 on Persona fit for a Persuade surface. A generic-template diagnosis is a FINDING routed to the design skill for a redesign (polish.md Step 3), not only a score cap — record which screens fail and how.""")

# ---------------------------------------------------------------- design-taste-frontend SKILL.md
# T1: motion beyond the page system's own entrance/moments routes to
# make-interfaces-feel-better (feel/timing) then the motion-* skills
# (React/Next implementation). Taste keeps its own motion.md for the page
# system itself; this line covers only app-frame / React motion beyond it.
# No other Taste change: the Hallmark theme deal + log, the tokens writer,
# sloplint, and the hero/finish reviews are all verified present.
sub("T1", TASTE_SKILL,
    """**motion / micro-interactions** (hero entrance, hover/press, the dealt moments — house rule 5, `motion.md`)""",
    """**motion / micro-interactions** (hero entrance, hover/press, the dealt moments — house rule 5, `motion.md`; for motion beyond the page system's own entrance and moments — for example interactive app-frame widgets in React/Next.js — decide feel and timing with `make-interfaces-feel-better` first, then implement with the motion-* skills (`motion-foundations`, `motion-patterns`, `motion-advanced`))""")

# ---------------------------------------------------------------- less-flat-ui SKILL.md
# L1: check every surface on every UI build/change; a fitting treatment is
# REQUIRED where a surface is dull/flat and text stays readable.
sub("L1", LESSFLAT_SKILL,
    """Apply treatments when the UI looks flat or dull: heroes, landing pages, empty states, cards, buttons, dividers, headings, modals. Apply EVERY treatment that fits the project's mood, not just one. The picker table below is a menu, not a single choice.""",
    """Apply treatments when the UI looks flat or dull: heroes, landing pages, empty states, cards, buttons, dividers, headings, modals. Apply EVERY treatment that fits the project's mood, not just one. The picker table below is a menu, not a single choice.

**Check every surface, on every UI build or change.** First build, one-prompt change, redesign, small component, UI fix, or removal flow that rebuilds a surface — for each surface, ask: is it dull or flat, and would a treatment keep text readable (4.5:1)? If yes, a fitting treatment is REQUIRED, not optional. A surface is left flat only when it fits one of the Do NOT cases below (dense dashboard, form, or data table; strong brand background; photo-led design; treatment fights the content) — and then say so in one line. Never skip the check because a surface is small.""")

# L2: ADD the recording rule (verified absent: zero "record" hits in this
# file before this patch — the brief's ":72 recording rule" does not exist).
sub("L2", LESSFLAT_SKILL,
    """## Tailwind notes""",
    """## Record what you applied

Record every treatment applied, per surface, in `docs/design-tokens.md`: append a Treatments list (surface → treatments applied, or "none — <Do NOT reason>" for a surface deliberately left flat), so the polish-pass harmony check can verify the texture layer against the recorded direction. Never rewrite the direction line at the top of `docs/design-tokens.md` (the named direction from `ui-ux-pro-max`, or the dealt Hallmark theme from `design-taste-frontend`) — treatments are recorded under it, not instead of it.

## Tailwind notes""")

# ---------------------------------------------------------------- summary
failed = [r for r in results if not r[2]]
for hunk_id, target, ok, detail in results:
    print(f"{'OK  ' if ok else 'FAIL'} {hunk_id} {target} — {detail}")
print(f"\n{len(results) - len(failed)}/{len(results)} hunks applied.")
if failed:
    print("FAILED HUNKS (skipped, not guessed):")
    for hunk_id, target, _, detail in failed:
        print(f"  - {hunk_id}: {target} — {detail}")
    sys.exit(1)
print("All hunks applied.")
