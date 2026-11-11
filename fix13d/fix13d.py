#!/usr/bin/env python3
"""Fix program #13d — staged-source edits (durable sources of truth).

Items (Audit #44 0 blocking / 4 minor; dry-run #16 2 blocking / 3 minor):
  S1  polish-pass SKILL.md (round2-skills/polish-pass/SKILL.md) — Harmony check
      is a second screen-distinctiveness executor (Audit M1 / dry-run B1,
      BLOCKING). Scope Harmony to code-level CONSISTENCY only + the
      missing-direction finding. Direction-application is browser-qa's job
      ALONE; the generic-template finding + Persona-fit cap route through
      browser-qa's verdict, never Harmony's own.
  S2  polish.md (reference/) — Step 2:4, Step 2:7, Step 3, Lenses preamble:
      same scoping (generic-template diagnosis = candidate evidence for
      browser-qa; FINDING exists only on browser-qa's verdict).
  S3  scoring.md (reference/) — Persona-fit cap + 3-tells overall cap route
      through browser-qa's verdict.
  S4  Hallmark (new-skills/design-taste-frontend/references/hallmark/
      references/) — gates.md §3 6-axis critique, hallmark-floor.md 6-axis
      section, review-hero.md, review-finish.md: template observations are
      candidate evidence for browser-qa, never independent verdicts
      (Audit M3 / dry-run M2, minor).
  S5  app-scaffold best-practices.md (rewritten-skills/app-scaffold/) — pin
      `npm install -D supabase` to supabase@3.1.0 (observation, one line).
  S6  hackathon-mode.mdc (new-rules/) — gan-style-harness parenthetical:
      precise truth (item 6, minor).
  S7  orchestrate SKILL.md (new-skills/orchestrate/SKILL.md) — step 5b
      re-verify sequencing (redesign from final polish re-verified by
      browser-qa before deploy); step 6 Specificity/finish-review template
      evidence routing; step-5 visual loop candidate-evidence input.
  S8  design-taste-frontend SKILL.md (new-skills/) :314 — hero-review
      invocation: ship/fix acts on craft findings; template observations are
      candidate evidence for browser-qa.

Two-phase: ALL anchors are verified count==1 across all files BEFORE any
write. On failure the script exits non-zero having written nothing. After
applying, the pre-existing build.sh (f) polish-pass patch anchors are
re-verified count==1 in the staged SKILL.md.
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (relative path, old text, new text, label)
SUBS = [
# ---------------------------------------------------------------- S1a
("round2-skills/polish-pass/SKILL.md",
 """Then, for each primary screen, check two things and record per-screen pass/fail in the report under "Harmony check": (1) **consistency** — tokens, type scale, color, radii, and spacing match the recorded direction, with no one-off values; (2) **direction-application** — the screen visibly traces to the named direction (its material, anchor, or theme is present and recognizable), rather than looking like a default template that could belong to any product. A screen that fails direction-application is a generic-template finding (see above): it routes to the design skill for a redesign, it is never restyled here, and it caps Persona fit per [reference/scoring.md](reference/scoring.md).""",
 """Then, for each primary screen, check **consistency** — tokens, type scale, color, radii, and spacing match the recorded direction, with no one-off values — and record per-screen pass/fail in the report under "Harmony check". Harmony checks consistency ONLY: it does NOT judge whether a screen reads as a default template — that is the distinctiveness bar, executed by `browser-qa` ONLY in the visual loop. If a screen's consistency check suggests the direction is not applied (tokens, type, or spacing do not trace to the recorded direction), record that as candidate evidence for `browser-qa` (screen + which tokens diverge), not a generic-template finding. A generic-template finding exists ONLY on `browser-qa`'s visual-loop verdict, and the Persona-fit cap in [reference/scoring.md](reference/scoring.md) applies only on that verdict, never on Harmony's own observation.""",
 "S1a harmony check: consistency only"),
# ---------------------------------------------------------------- S1b
("round2-skills/polish-pass/SKILL.md",
 """Apply the polish fixes that fit, then record it as a generic-template FINDING in the report — per-screen evidence, which screens fail the harmony check and how — so the orchestrator routes it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps; it stays listed under "Still short of 10/10" until that redesign lands.""",
 """Apply the polish fixes that fit, then record the per-screen evidence as candidate evidence for `browser-qa` (which screens, what suggests the direction is not applied) — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps; it stays listed under "Still short of 10/10" until that redesign lands and is re-verified by `browser-qa` before deploy.""",
 "S1b diagnosis paragraph: evidence routing"),
# ---------------------------------------------------------------- S1c
("round2-skills/polish-pass/SKILL.md",
 """This is still a fix-only pass: it never restyles, and a look that itself is the problem is recorded as a generic-template finding for the orchestrator to route back to the design skill (and listed under "Still short of 10/10" until redesigned), not redesigned here.""",
 """This is still a fix-only pass: it never restyles, and a look that itself is the problem is recorded as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then does the orchestrator route it back to the design skill (and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy), not redesigned here.""",
 "S1c first-build final polish: evidence routing"),
# ---------------------------------------------------------------- S1d
("round2-skills/polish-pass/SKILL.md",
 """7. **Run the harmony check.** On every pass, run the harmony check (## The harmony rule): read the recorded direction, check each primary screen for consistency and direction-application, and record per-screen pass/fail in the report. A generic-template failure is a finding routed to the design skill, never a silent note.""",
 """7. **Run the harmony check.** On every pass, run the harmony check (## The harmony rule): read the recorded direction, check each primary screen for consistency only, and record per-screen pass/fail in the report. Harmony never verdicts screen distinctiveness — a screen whose consistency suggests the direction is not applied is recorded as candidate evidence for `browser-qa`, and a generic-template finding exists only on `browser-qa`'s visual-loop verdict; route it to the design skill then, never a silent note.""",
 "S1d non-negotiable 7: consistency only"),
# ---------------------------------------------------------------- S2a
("round2-skills/polish-pass/reference/polish.md",
 """Never apply a lens that picks a new visual direction — those are not in this skill; if the diagnosis calls for one, that is a redesign, recorded as a generic-template finding routed to the design skill and listed under "Still short of 10/10", not applied here.""",
 """Never apply a lens that picks a new visual direction — those are not in this skill; if the diagnosis calls for one, that is a redesign: record the per-screen evidence as candidate evidence for `browser-qa` — a generic-template finding exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill and listed under "Still short of 10/10" — not applied here.""",
 "S2a lenses preamble: evidence routing"),
# ---------------------------------------------------------------- S2b
("round2-skills/polish-pass/reference/polish.md",
 """A generic-template diagnosis (Level 2 template on [scoring.md](scoring.md), three or more vibe-code tells, or a Persona-fit cap from the generic look) is recorded as a generic-template FINDING with per-screen evidence — it routes to the design skill for a redesign (Step 3), not just a report note.""",
 """A generic-template diagnosis (Level 2 template on [scoring.md](scoring.md), three or more vibe-code tells, or a Persona-fit cap from the generic look) is recorded as candidate evidence for `browser-qa` with per-screen evidence — a generic-template FINDING exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (Step 3), not just a report note.""",
 "S2b Step 2:4: evidence routing"),
# ---------------------------------------------------------------- S2c
("round2-skills/polish-pass/reference/polish.md",
 """7. Run the **harmony check** (SKILL.md → The harmony rule): read the recorded direction in `docs/design-tokens.md` (or `design-system/<project-slug>/MASTER.md`), then check each primary screen for (a) consistency of tokens/type/color/spacing against that direction and (b) direction-application — does the screen visibly trace to the named direction? Record per-screen pass/fail for the report. A screen that fails direction-application is a **generic-template finding**: record it with evidence (which screen, what makes it a default template) — it routes to the design skill for a redesign (see Step 3), it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned.""",
 """7. Run the **harmony check** (SKILL.md → The harmony rule): read the recorded direction in `docs/design-tokens.md` (or `design-system/<project-slug>/MASTER.md`), then check each primary screen for consistency of tokens/type/color/spacing against that direction. Record per-screen pass/fail for the report. Harmony does NOT judge whether a screen reads as a default template — that is the distinctiveness bar, executed by `browser-qa` ONLY in the visual loop. A screen whose consistency check suggests the direction is not applied is recorded as candidate evidence for `browser-qa` (which screen, which tokens diverge) — a **generic-template finding** exists only on `browser-qa`'s visual-loop verdict, and only then does it route to the design skill for a redesign (see Step 3); it is never restyled here, and it stays listed under "Still short of 10/10" until redesigned and re-verified by `browser-qa` before deploy.""",
 "S2c Step 2:7: consistency only"),
# ---------------------------------------------------------------- S2d
("round2-skills/polish-pass/reference/polish.md",
 """Still apply the Lenses, but record the generic-template diagnosis as a FINDING routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps — the orchestrator routes it; it also stays listed under "Still short of 10/10", naming the artifact or idea each weak section is missing, until that redesign lands.""",
 """Still apply the Lenses, but record the generic-template diagnosis as candidate evidence for `browser-qa` — a FINDING exists only on `browser-qa`'s visual-loop verdict, and only then is it routed to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page) for a redesign within the existing caps — the orchestrator routes it; it also stays listed under "Still short of 10/10", naming the artifact or idea each weak section is missing, until that redesign lands and is re-verified by `browser-qa` before deploy.""",
 "S2d Step 3: evidence routing"),
# ---------------------------------------------------------------- S3a
("round2-skills/polish-pass/reference/scoring.md",
 """- Generic "AI-template" look (the craft-floor slop tells) can't score above 6 on Persona fit for a Persuade surface. A generic-template diagnosis is a FINDING routed to the design skill for a redesign (polish.md Step 3), not only a score cap — record which screens fail and how.""",
 """- Generic "AI-template" look (the craft-floor slop tells) can't score above 6 on Persona fit for a Persuade surface — but only on `browser-qa`'s visual-loop verdict: a generic-template diagnosis exists ONLY when `browser-qa`'s verdict says so. Polish's own observation of an AI-template look is candidate evidence for `browser-qa` (record which screens and how), never the cap or the FINDING on its own. On `browser-qa`'s verdict the diagnosis is a FINDING routed to the design skill for a redesign (polish.md Step 3), not only a score cap — record which screens fail and how.""",
 "S3a Persona-fit cap routes through browser-qa"),
# ---------------------------------------------------------------- S3b
("round2-skills/polish-pass/reference/scoring.md",
 """- Each vibe-code tell ([patterns/vibe-code-tells.md](patterns/vibe-code-tells.md)) is a finding. Three or more tells cap the overall Score at 6.""",
 """- Each vibe-code tell ([patterns/vibe-code-tells.md](patterns/vibe-code-tells.md)) is a finding. Three or more tells are candidate evidence for `browser-qa` that the surface reads as a template; the overall Score cap at 6 for a template look applies only on `browser-qa`'s generic-template verdict, never on the tell count alone.""",
 "S3b three-tells cap routes through browser-qa"),
# ---------------------------------------------------------------- S4a
("new-skills/design-taste-frontend/references/hallmark/references/gates.md",
 """Before the sweep, score the planned page 1 to 5 on six axes; anything under 3 triggers a revision first.""",
 """Before the sweep, score the planned page 1 to 5 on six axes; anything under 3 triggers a revision first.

**Scope — this critique is a design input, not a distinctiveness verdict.** It judges the planned page's IDEA before the sweep (no screen exists yet at pre-emit time), and in Verify it scores the built page the same way. Its Specificity axis (3: fits the category; 5: could belong to no other product) is candidate evidence for `browser-qa`, never a verdict: a Specificity score under 3 is recorded (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar. The other five axes (Philosophy, Hierarchy, Execution, Restraint, Variety) are craft judgments and join the fix list as usual. A Specificity finding never joins the fix list as a verdict on its own.""",
 "S4a gates §3: Specificity is evidence, not verdict"),
# ---------------------------------------------------------------- S4b
("new-skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md",
 """— name the weakest axis + the fix taken; straight 5s name what was cut.""",
 """— name the weakest axis + the fix taken; straight 5s name what was cut.

**Scope:** the Specificity axis is candidate evidence for `browser-qa`, never a distinctiveness verdict (see gates.md §3); the other five axes join the fix list as craft judgments.""",
 "S4b hallmark-floor 6-axis scope"),
# ---------------------------------------------------------------- S4c-1
("new-skills/design-taste-frontend/references/hallmark/references/review-hero.md",
 """First line: `ship` or `fix`.""",
 """First line: `ship` or `fix`. The word rests on the craft questions below (headline, composition, visual, signature, type) — template observations are candidate evidence for `browser-qa` and never drive it.""",
 "S4c-1 hero review first line: craft only"),
# ---------------------------------------------------------------- S4c-2
("new-skills/design-taste-frontend/references/hallmark/references/review-hero.md",
 """- Does anything read as a template: a centred stack, a pill or a label above the headline, a gradient blob, an empty coloured box where a picture should be, a drawn illustration, a row of counting marks, two filled buttons side by side? A filled primary beside an outlined or text action that goes somewhere else is the control pair, and a sample of the product built in a slot is the product; neither is a finding. Grey bars or outline cards inside a slot are.""",
 """- Does anything read as a template: a centred stack, a pill or a label above the headline, a gradient blob, an empty coloured box where a picture should be, a drawn illustration, a row of counting marks, two filled buttons side by side? A filled primary beside an outlined or text action that goes somewhere else is the control pair, and a sample of the product built in a slot is the product; neither is a finding. Grey bars or outline cards inside a slot are. **Record what reads as a template as candidate evidence for `browser-qa` (screen + what it reads as) — it is not a finding of this review and does not drive its first word: `browser-qa` alone executes the distinctiveness bar in the visual loop.**""",
 "S4c-2 hero template question: evidence only"),
# ---------------------------------------------------------------- S4c-3
("new-skills/design-taste-frontend/references/hallmark/references/review-hero.md",
 """On a custom run (`theme: custom`) the composition is free: skip the centred, beside-the-text and 60% questions, and ask instead whether this screen is one you would expect a model to make for this prompt. If it is, say what gives it away.""",
 """On a custom run (`theme: custom`) the composition is free: skip the centred, beside-the-text and 60% questions, and ask instead whether this screen is one you would expect a model to make for this prompt. If it is, say what gives it away — as candidate evidence for `browser-qa`, not as a finding of this review: the distinctiveness verdict belongs to `browser-qa` alone.""",
 "S4c-3 hero custom run: evidence only"),
# ---------------------------------------------------------------- S4d-1
("new-skills/design-taste-frontend/references/hallmark/references/review-finish.md",
 """**Seen before:** the page, or a section, reads as a template, a catalog theme or a familiar site; name which and where.""",
 """**Seen before:** the page, or a section, reads as a template, a catalog theme or a familiar site; name which and where — as candidate evidence for `browser-qa`, not a finding of this review: the distinctiveness verdict belongs to `browser-qa` alone in the visual loop.""",
 "S4d-1 finish Seen before: evidence only"),
# ---------------------------------------------------------------- S4d-2
("new-skills/design-taste-frontend/references/hallmark/references/review-finish.md",
 """On a polish you get only the full pages at 1440, before and after: the layout was kept on purpose, so ask one thing, whether anything still reads as machine-made, in at most five findings.""",
 """On a polish you get only the full pages at 1440, before and after: the layout was kept on purpose, so ask one thing, whether anything still reads as machine-made, in at most five findings — recorded as candidate evidence for `browser-qa`, not as findings of this review.""",
 "S4d-2 finish polish variant: evidence only"),
# ---------------------------------------------------------------- S4d-3
("new-skills/design-taste-frontend/references/hallmark/references/review-finish.md",
 """First line: one of `recapture` (a screenshot is missing, blank or shows the wrong thing; list what to recapture and stop), `rebuild` (the first viewport fails the idea or the theme wholesale), `fix` (findings follow), `ship` (nothing owed).""",
 """First line: one of `recapture` (a screenshot is missing, blank or shows the wrong thing; list what to recapture and stop), `rebuild` (the first viewport fails the idea or the theme wholesale), `fix` (findings follow), `ship` (nothing owed). The first word rests on the gates, the plain defects, the copy, and the layout — template observations (`Seen before`, machine-made) are candidate evidence for `browser-qa` and never drive it.""",
 "S4d-3 finish first word: craft only"),
# ---------------------------------------------------------------- S5
("rewritten-skills/app-scaffold/reference/best-practices.md",
 """npm install -D supabase            # optional: pin the CLI per-project via npx""",
 """npm install -D supabase@3.1.0       # optional: CLI pinned per-project (3.1.0)""",
 "S5 pin supabase CLI 3.1.0"),
# ---------------------------------------------------------------- S6
("new-rules/hackathon-mode.mdc",
 """`gan-style-harness` (Claude Code only — it drives the `claude` CLI and does not run in Cursor, so it cannot lead design in a Cursor first build)""",
 """`gan-style-harness` (its upstream `claude -p` invocation path does not run in Cursor — the harness loop itself runs in Cursor through `/gan-build` + the `ecc-gan-*` agents as Cursor subagents — but the skill still cannot lead design in a Cursor first build: the design package owns direction and the GAN loop implements, it never directs design)""",
 "S6 hackathon-mode §5: GAN truth"),
# ---------------------------------------------------------------- S7a
("new-skills/orchestrate/SKILL.md",
 """and anything not implemented goes in the final report as highest-value next improvements. `polish-pass` fixes states, responsive issues, and consistency drift only — it never restyles.""",
 """and anything not implemented goes in the final report as highest-value next improvements. `polish-pass` fixes states, responsive issues, and consistency drift only — it never restyles. **Re-verify before deploy:** if final polish routes a redesign (a generic-template finding on `browser-qa`'s verdict, or any finding that needs a design skill), the design skill builds it and `browser-qa` re-runs the step-5 every-route visual loop on the redesigned screens BEFORE the 5c deploy — within the existing visual-loop caps; an unverified redesign never reaches deploy.""",
 "S7a step 5b: re-verify before deploy"),
# ---------------------------------------------------------------- S7b-1
("new-skills/orchestrate/SKILL.md",
 """Then the 6-axis pre-emit self-critique (`skills/design-taste-frontend/references/hallmark/references/gates.md` §3, condensed in `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md`): score the page 1–5 on Philosophy, Hierarchy, Execution, Specificity, Restraint, Variety; any axis under 3 joins the fix list with the rest of Verify's findings (same capped 2-round fix loop).""",
 """Then the 6-axis pre-emit self-critique (`skills/design-taste-frontend/references/hallmark/references/gates.md` §3, condensed in `skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md`): score the page 1–5 on Philosophy, Hierarchy, Execution, Specificity, Restraint, Variety; any axis under 3 joins the fix list with the rest of Verify's findings (same capped 2-round fix loop) — EXCEPT Specificity, which is candidate evidence for `browser-qa`, never a fix-list verdict on its own: record a Specificity score under 3 (screen + what reads as a template) for `browser-qa`'s visual loop, which alone executes the distinctiveness bar (see gates.md §3).""",
 "S7b-1 step 6: Specificity is evidence"),
# ---------------------------------------------------------------- S7b-2
("new-skills/orchestrate/SKILL.md",
 """Act on its first word (`recapture` / `rebuild` / `fix` / `ship`); findings join the fix batch.""",
 """Act on its first word (`recapture` / `rebuild` / `fix` / `ship`) for the gates, plain defects, copy, and layout findings; findings join the fix batch — EXCEPT template observations (`Seen before`, machine-made), which are candidate evidence for `browser-qa`, never fix-batch verdicts: route them to `browser-qa`, which re-inspects the affected screens in the step-5 visual loop (within the existing caps) before polish/deploy, and only its verdict decides whether a fix is owed.""",
 "S7b-2 step 6: finish template evidence routes to browser-qa"),
# ---------------------------------------------------------------- S7c
("new-skills/orchestrate/SKILL.md",
 """The finding routes to the fix loop within the existing caps (max 3 rounds total, at most 2 fix rounds per problem list), not a pass.""",
 """The finding routes to the fix loop within the existing caps (max 3 rounds total, at most 2 fix rounds per problem list), not a pass. **Candidate evidence in:** if `.hallmark/hero-review.md` exists, its template observations are input to your verdict (look where they point); step-6 template observations reach you the same way on re-inspection. Evidence never overrides your verdict — you make the call.""",
 "S7c step-5 visual loop: hero-review evidence input"),
# ---------------------------------------------------------------- S8
("new-skills/design-taste-frontend/SKILL.md",
 """Act on its first word (`ship` / `fix`); findings join the fix batch.""",
 """Act on its first word (`ship` / `fix`) for the craft findings; findings join the fix batch — EXCEPT template observations (anything that reads as a template, or that a model would be expected to make for this prompt), which are candidate evidence for `browser-qa`, never fix-batch verdicts: record them in `.hallmark/hero-review.md` with the screen and what reads as a template, for `browser-qa`'s visual loop to judge.""",
 "S8 Taste step 6: hero template evidence to browser-qa"),
]

# Pre-existing build.sh (f) polish-pass patch anchors — must still be count==1
# in the staged SKILL.md after the edits above.
F_ANCHORS = [
    "a new look belongs to ui-ux-pro-max and less-flat-ui, not this skill.",
    "The plugin already has `ui-ux-pro-max` and `less-flat-ui` for design direction and surface treatments. Those skills own the look.",
    "If the user asks for a new look outright, that is not this skill: say so and point them at `ui-ux-pro-max`.",
    "| A new look, direction, or visual style (\"redesign\", \"revamp\", \"make it look different\") | `ui-ux-pro-max` / `less-flat-ui` — not this skill |",
]


def main():
    texts = {}
    # Phase 1 — verify every anchor before writing anything.
    for rel, old, new, label in SUBS:
        p = os.path.join(PLUGIN_ROOT, rel)
        if p not in texts:
            with open(p, encoding="utf-8") as f:
                texts[p] = f.read()
        n = texts[p].count(old)
        assert n == 1, f"VERIFY {label}: anchor count={n} (expected 1) in {rel}: {old[:80]!r}"
        print(f"verify OK: {label}")
    # Phase 2 — apply.
    for rel, old, new, label in SUBS:
        p = os.path.join(PLUGIN_ROOT, rel)
        texts[p] = texts[p].replace(old, new, 1)
    for p, t in texts.items():
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
    # Phase 3 — re-verify build.sh (f) anchors in the staged polish SKILL.md.
    staged = os.path.join(PLUGIN_ROOT, "round2-skills/polish-pass/SKILL.md")
    t = open(staged, encoding="utf-8").read()
    for a in F_ANCHORS:
        n = t.count(a)
        assert n == 1, f"(f) anchor count={n} (expected 1) after edits: {a[:60]!r}"
        print(f"(f) anchor OK: {a[:50]!r}")
    print(f"fix13d staged edits applied ({len(SUBS)} substitutions)")


if __name__ == "__main__":
    main()
