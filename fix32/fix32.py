#!/usr/bin/env python3
"""Fix #32 — demote ui-ux-pro-max to lookup-only.

Run by build.sh as a patch step (after the fix #32 restatement block,
before STEP 5):
    python3 "$PLUGIN_ROOT/fix32/fix32.py" "$PLUGIN_DIR"

The demotion is enforced by the plugin's routing, descriptions, and
triggers, never by editing the vendored skill itself: ui-ux-pro-max is
upstream-pinned (build.sh UIPRO_PIN) and has no staged source; its data
CSVs stay untouched and its own vendored SKILL.md still describes itself
as design intelligence (upstream content at a pinned commit — see
OWED-32-2).

This script operates on the BUILT tree only and does three things:

  1. Census (no writes): asserts the staged weave landed (row 10 routes
     every surface to design-taste-frontend; inventory §1 heading is
     lookup-only; hackathon-mode §2/§5 name Taste as lead for app
     surfaces; the type-scale, tokens-record, and no-landing-fallback
     rewordings); asserts the build.sh description patches landed
     (ui-ux-pro-max lookup-only, Taste leads every surface, polish-pass
     (f), frontend-design-direction note in build.sh — that skill is CUT
     by fix27, so no built copy exists to assert); asserts the fix #32
     restatement block landed (orch-* x5, gan x2, design-system, README
     bullet, less-flat-ui); runs the data census (styles 89/51, palettes
     192, fonts 74, guidelines 120, icons 105, charts 25, stacks 22,
     app-interface 32, landing 34, products 192, GSAP presets 17);
     checks each of the 11 pins is present in its owner home; asserts
     the fix30 pin census still holds exactly; asserts the trigger
     pre-state (49 keys, skill:ui-ux-pro-max present with the 4 dashboard
     phrases); asserts DESIGNPKG-AUTO + GLOBAL-ROUTING are byte-identical
     in orchestrate + hackathon-mode; asserts the glossary G1-G20
     citations still stand (vocabulary attribution, not lead).
  2. Writes: the trigger move (4 dashboard phrases from
     skill:ui-ux-pro-max to skill:design-taste-frontend; the
     skill:ui-ux-pro-max key deleted; coverage.withTriggers 49 -> 48,
     coverage.skills stays 72) + the fix #32 README provenance note.
  3. Post-assertions: re-census everything in (1) plus the trigger
     move, the README note, and the lead-language denylist + proximity
     scan (zero lead/ownership language for ui-ux-pro-max outside the
     allowlist: the vendored skills/ui-ux-pro-max/ subtree itself, plus
     historical/provenance notes explicitly marked as describing a past
     fix. Audit round 1 tightened the scan: a 3-line window with an
     ownership denylist — lead/leads/leading/led, "sets the design
     direction", "design lead", "owns", co-sourced "identity",
     "direction check" naming ui-ux-pro-max, "define the design system"
     as a ui-ux-pro-max attribution — and a shaped exemption that only
     covers a lookup marker attached to the ui-ux-pro-max mention or an
     explicit never/no-longer/not-the-design-lead denial, replacing the
     old blanket "lookup"-substring exemption. Audit round 2 hardened
     it further (DECISION-32-11): the lookup marker must sit within 25
     chars after the mention with no denylist verb between mention and
     lookup, and no denylist verb directly predicating the mention from
     the left (copula-joined, e.g. "the design lead is `ui-ux-pro-max`");
     a reverse "define the design system" pattern was added, excused
     only when the window attributes the defining to Taste
     (design-taste-frontend + defines). Audit round 3 redesigned it on
     subject attribution (DECISION-32-13), hardened in audit round 4 (DECISION-32-16): a 7-line window (mention
     line +/-3, widened from +/-2) with an authority denylist (lead words, "sets the
     design direction", "design lead", owns, decides, runs, controls,
     authors, drives, directs, governs, dictates, determines,
     prescribes, "identity", "direction check", "define(s) the design
     system"); each denylist verb is linked to a mention only in the
     same clause, then attributed by the subject in the 60 chars
     before it (or a passive "by <subject>" after it) — a verb
     attributed to another named skill is skipped, otherwise it
     flags; a denial excuses a verb only within 15 chars before it;
     "define(s) the design system" flags unless design-taste-frontend
     governs it within 60 chars; the lookup exemption is subordinate
     and can never excuse a flagged verb; no distance caps (the
     window bounds distance). Audit round 3 also fixed B1
     (DECISION-32-14): the executable body now lives in main() under
     `if __name__ == "__main__"`, so importing this module can never
     execute the census or overwrite the patch log. Audit round 4 hardened it further (DECISION-32-16): a 7-line window (mention line +/-3); denylist adds 'heads', 'steers', 'leadership of', 'is the authority on', 'is in charge of', generalized 'sets (the <word>) direction', and the passive 'set by ui-ux-pro-max'; attribution counts only the last skill-name occurrence before the verb, excluding parenthetical/bracketed names, 'by '/'with ' adjuncts, and appositive 'this skill'; a table row is one clause and adjacent sentences/bullets link; denial must have no other skill name between it and the verb; the design-lead phrase check looks both ways; every pattern carries a hyphenated-compound guard; the lookup exemption is REMOVED as dead code (DECISION-32-17).

Exits non-zero on any error so the build fails rather than shipping a
half-demoted tree.

SPEC fix32/SPEC.md. Decisions D32-1..D32-19. Counts: skills 72, agents
45, rules 48, commands 55, hooks 15, trigger keys 49 -> 48 only.
"""
import csv
import json
import os
import re
import sys

BASE = ""  # DECISION-32-15: set from sys.argv[1] inside main() only;
ROOT = ""  # importing this module must leave BASE '' and touch nothing.
CHANGES = []
ERRORS = []
OWED = []
DECISIONS = []

# Pin census from fix33 (must still hold exactly — the demotion adds no pin text).
# fix #30 retired: the orchestrator is unpinned (fix #33), so the built tree
# carries no orchestrator pin at all — old pin 0, new pin 0. The 2 OLD_PROSE
# are the strategic-compact keeps (factual model examples in "Grok 4.7 High"
# form — fix30's rename no longer runs, so they are never rewritten to Extra
# High; fix33/SPEC.md §1(b)). FAST is 72: 71 pre-existing (70 + 1 from the fix33 staged weave's
# orchestrate L93 picker note, D33-16) + 1 in the agent.schema.json description
# added by fix33.py (D33-17).
OLD_ID = "grok-4.7-high"
NEW_ID = "grok-4.7-extra-high"
OLD_PROSE = "Grok 4.7 High"
NEW_PROSE = "Grok 4.7 Extra High"
FAST_ID = "cursor-grok-4.6-high-fast"
FAST_BARE = "grok-4.6-high-fast"
EXPECT_PIN = {OLD_ID: 0, OLD_PROSE: 2, FAST_ID: 72,
              NEW_ID: 0, NEW_PROSE: 0}

# Data census (SPEC §5(f)): data rows excluding the header line.
EXPECT_DATA = {
    "styles.csv": 89, "colors.csv": 192, "typography.csv": 74,
    "ux-guidelines.csv": 120, "icons.csv": 105, "charts.csv": 25,
    "motion.csv": 17, "app-interface.csv": 32, "landing.csv": 34,
    "products.csv": 192,
}
EXPECT_STACKS = 22

# The 11 pins and the per-skill home that owns each (SPEC D32-4; the
# LIQGLASS/SHADERGRAD homes are design-taste-frontend — verified in-tree,
# the SPEC's parenthetical did not name them explicitly).
PIN_HOMES = [
    ("lenis@1.3.27", "skills/motion-foundations/SKILL.md"),
    ("gsap@3.15.1", "skills/gsap/SKILL.md"),
    ("vanta@0.5.24", "skills/design-taste-frontend/SKILL.md"),
    ("9d9c687", "skills/react-bits/SKILL.md"),
    ("@react-three/fiber@9.8.2", "skills/motion-foundations/SKILL.md"),
    ("78cb6cc", "skills/design-taste-frontend/SKILL.md"),
    ("@shadergradient/react@2.4.20", "skills/design-taste-frontend/SKILL.md"),
    ("689bb38", "skills/design-taste-frontend/SKILL.md"),
    ("particles.casberry.in", "skills/motion-foundations/SKILL.md"),
    ("OriginKit", "skills/motion-patterns/SKILL.md"),
    ("daisyui@5.7.50", "skills/design-system/SKILL.md"),
]
PIN_SUPPORT = [
    ("three@0.185.1", "skills/motion-foundations/SKILL.md"),
    ("three@0.134.0", "skills/design-taste-frontend/SKILL.md"),
]

# Old lead-language strings: must occur ZERO times in the built tree
# outside the vendored skills/ui-ux-pro-max/ subtree (checked in §3).
OLD_LEAD = [
    "a dashboard/app surface goes to `ui-ux-pro-max`",
    "at minimum a `ui-ux-pro-max` direction check",
    "`ui-ux-pro-max` (design lead)",
    "app: the `ui-ux-pro-max` direction",
    "the `ui-ux-pro-max` direction",
    "(the dealt pairing in Taste step 4a / the ui-ux-pro-max type scale)",
    "(the dealt display face in Taste step 4a / the ui-ux-pro-max type scale)",
    "the dealt pairing (Taste step 4a / ui-ux-pro-max type scale)",
    "`ui-ux-pro-max` sets the design direction",
    "`ui-ux-pro-max` is the general design intelligence",
    "It replaces `ui-ux-pro-max` as design lead",
    "dashboards and apps → `ui-ux-pro-max`",
    "(`ui-ux-pro-max` + `less-flat-ui` pairing, or `design-taste-frontend` on full landing/company pages)",
    "route that to `ui-ux-pro-max` instead",
    "`ui-ux-pro-max` for a dashboard/app surface",
    "(`ui-ux-pro-max` direction / `design-taste-frontend`",
    "ui-ux-pro-max leads dashboards/apps/components",
    "design-taste-frontend leads full landing-page builds, ui-ux-pro-max leads dashboards/apps/components",
    "a new look belongs to ui-ux-pro-max and less-flat-ui, not this skill.",
    "a new look belongs to `ui-ux-pro-max`, `less-flat-ui`, and `design-taste-frontend`",
    "A new look belongs to `ui-ux-pro-max`",
    "The plugin already has `ui-ux-pro-max` and `less-flat-ui` for design direction",
    "The plugin already has `ui-ux-pro-max`, `less-flat-ui`, and `design-taste-frontend` for design direction",
    "point them at `ui-ux-pro-max`.",
    "point them at `ui-ux-pro-max`, `less-flat-ui`, or `design-taste-frontend`.",
    "`ui-ux-pro-max` / `less-flat-ui` — not this skill",
    "`ui-ux-pro-max` / `less-flat-ui` / `design-taste-frontend` — not this skill",
    "the first UI slice (`ui-ux-pro-max`)",
    "the dashboard MASTER.md (`ui-ux-pro-max`)",
    "via `ui-ux-pro-max`) defines the design system",
    "via `ui-ux-pro-max`) writes `docs/design-tokens.md`",
    "`ui-ux-pro-max` supplies the design guidance that builds the direction",
    "(`ui-ux-pro-max`, or `design-taste-frontend` on a landing page)",
    "run `ui-ux-pro-max` for that.",
    "<`ui-ux-pro-max` | `design-taste-frontend`>",
    "(the named direction from `ui-ux-pro-max`, or the dealt Hallmark theme from `design-taste-frontend`)",
    "`ui-ux-pro-max` (design direction)",
    "(`design-taste-frontend`) leads full company/landing-page builds.",
    "goes through the full design package: `ui-ux-pro-max` and `less-flat-ui` together",
    "full design package: `ui-ux-pro-max` + `less-flat-ui` + Impeccable",
    "use `ui-ux-pro-max` and `less-flat-ui` together for it",
    "dashboard/app surface or component — `ui-ux-pro-max` + Impeccable",
    "landing: `design-taste-frontend` + dealt Hallmark theme + `ui-ux-pro-max` + Impeccable",
    "app/dashboard/components: `ui-ux-pro-max` + Impeccable via `polish-pass` + Harmony + `less-flat-ui` where dull/flat; landing:",
    "The design package's GSAP presets (17 ready snippets): `skills/ui-ux-pro-max/data/motion.csv`",
    "The fix #22 pin and stack scope: `skills/ui-ux-pro-max/SKILL.md` (§11, REACTBITS_F22)",
    "## 1. ui-ux-pro-max — design intelligence for dashboards, apps, components",
    "Choosing the app/dashboard direction; never",
    "Type decisions on app surfaces; re-dealt",
    "Pins + stack scope in `skills/ui-ux-pro-max/SKILL.md`; per-skill homes in",
    "App/dashboard decisions (see §1)",
    "| Any surface with a depth strategy |",
    "Colour decisions for an app surface; the palette balance comes from here |",
    "Any interaction, form, navigation, or feedback decision |",
    "Any data surface; the chart choice is a design decision, not a default",
    "App-surface structure; landing structure on app-led builds",
    "Motion on GSAP builds; ScrollTrigger is the scroll plugin (GSAP_F22). Usage skill: `skills/gsap/SKILL.md` (fix #31) |",
    # Audit round 1 (audit #100 B2-B4): the four authority lines SPEC §0
    # missed. They must occur ZERO times in the built tree.
    "that skill owns layout, type, and components",
    "system: `ui-ux-pro-max` (\"Define the design system before implementing UI\")",
    "`ui-ux-pro-max` owns spacing;",
    "(the dealt direction in Taste step 4a / the ui-ux-pro-max identity)",
]

# (staged_rel, built_rel, new anchors that must be present in the built
# copy, old anchors that must be absent from the built copy). The
# row-10 route anchor is written without the model pin so the fix30
# staged-vs-built pin rename does not trip it. Fix #33 updated the anchor
# tail: the unpin changed 'leads on model `grok-4.7-high`' to 'leads on the
# model selected in this chat' (D33-18) — the anchor now asserts the demotion
# AND the unpin.
STAGED_BUILT = [
    ("new-skills/orchestrate/SKILL.md", "skills/orchestrate/SKILL.md",
     ["a dashboard/app surface goes to `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` as its lookup inventory",
      "at minimum a design-package direction check + Harmony check",
      "**route to the design skill for that surface** — `design-taste-frontend` for every surface — landing page, dashboard/app surface, or component; the design skill leads on the model selected in this chat",
      "dashboard/app surface or component — `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + Impeccable",
      "app: the `design-taste-frontend` direction — theme/axes/mood, named, never \"modern clean\", with the `ui-ux-pro-max` lookup rows it used",
      "(the dealt pairing in Taste step 4a, with `data/typography.csv` as the lookup source for app-surface pairings)",
      "(the dealt display face in Taste step 4a, with `data/typography.csv` as the lookup source for app-surface pairings)",
      "`ui-ux-pro-max` styles / palettes / font pairings / UX guidelines as the lookup inventory for app/dashboard decisions",
      "the first UI slice (dashboard/app, led by `design-taste-frontend` with `ui-ux-pro-max` lookups) writes `docs/design-tokens.md`",
      "the dashboard system recorded in `design-system/<project-slug>/MASTER.md` (built on the `ui-ux-pro-max` lookup inventory) must conform to it",
      "app/dashboard: the `design-taste-frontend` direction (theme/axes/mood, named, never \"modern clean\", with the `ui-ux-pro-max` lookup rows it used)",
      "`ui-ux-pro-max` supplies the lookup inventory the direction draws on, never the verdict",
      # Audit round 1 (B4): the brand is generated through Taste's dealt
      # direction, with the ui-ux-pro-max lookup rows cited as lookups.
      "(the dealt direction in Taste step 4a, with the `ui-ux-pro-max` lookup rows it used: palette row, type-scale row)"],
     ["a dashboard/app surface goes to `ui-ux-pro-max`",
      "at minimum a `ui-ux-pro-max` direction check",
      "app: the `ui-ux-pro-max` direction",
      "(the dealt direction in Taste step 4a / the ui-ux-pro-max identity)"]),
    ("new-skills/orchestrate/references/design-inventory.md",
     "skills/orchestrate/references/design-inventory.md",
     ["## 1. ui-ux-pro-max — lookup-only inventory for dashboards, apps, components (fix #32: no longer the design lead)",
      "Owned by the gsap skill (fix #32, D32-5); the CSV stays the lookup source",
      "Every surface's depth strategy as a lookup (orchestrate step 3)",
      "owned by their per-skill homes, with the upstream vendored record in `skills/ui-ux-pro-max/SKILL.md` (§11/§15/§17)",
      "Owned by their per-skill homes — `skills/motion-foundations/SKILL.md` (Lenis, R3F, Casberry)",
      "App/dashboard lookups after Taste sets the direction (see §1)",
      "the rules are a lookup (DEPTH_F22), applied by the design-lead (Taste) at orchestrate step 3"],
     ["## 1. ui-ux-pro-max — design intelligence for dashboards, apps, components",
      "Pins + stack scope in `skills/ui-ux-pro-max/SKILL.md`; per-skill homes in"]),
    ("new-skills/orchestrate/references/dispatch-prompt.md",
     "skills/orchestrate/references/dispatch-prompt.md",
     ["dashboard/app surface or component — `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + Impeccable"],
     ["dashboard/app surface or component — `ui-ux-pro-max` + Impeccable"]),
    ("new-skills/design-taste-frontend/SKILL.md",
     "skills/design-taste-frontend/SKILL.md",
     ["the design package (`ui-ux-pro-max` (lookup), `less-flat-ui`",
      "the dashboard MASTER.md (built on the `ui-ux-pro-max` lookup inventory) must conform to it",
      "the first UI slice (led by `design-taste-frontend`, with `ui-ux-pro-max` lookups) writes the file instead",
      "the dealt pairing (Taste step 4a, with `data/typography.csv` as the lookup source for app-surface pairings)",
      # Audit round 1 (B4): same brand-identity rewording as orchestrate.
      "(the dealt direction in Taste step 4a, with the `ui-ux-pro-max` lookup rows it used: palette row, type-scale row)"],
     ["the first UI slice (`ui-ux-pro-max`)",
      "the dashboard MASTER.md (`ui-ux-pro-max`)",
      "(the dealt direction in Taste step 4a / the ui-ux-pro-max identity)"]),
    ("new-skills/feature-expansion/SKILL.md",
     "skills/feature-expansion/SKILL.md",
     ["`design-taste-frontend` (design lead for every surface) with `ui-ux-pro-max` lookups and `less-flat-ui` together",
      "full design package: `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + `less-flat-ui` + Impeccable"],
     ["goes through the full design package: `ui-ux-pro-max` and `less-flat-ui` together"]),
    ("new-skills/integration/SKILL.md", "skills/integration/SKILL.md",
     ["use `design-taste-frontend` (design lead for every surface) with `ui-ux-pro-max` lookups and `less-flat-ui` together for it"],
     ["use `ui-ux-pro-max` and `less-flat-ui` together for it"]),
    ("new-skills/gsap/SKILL.md", "skills/gsap/SKILL.md",
     ["The design package's GSAP presets (17 ready snippets), owned by this skill"],
     ["The design package's GSAP presets (17 ready snippets): `skills/ui-ux-pro-max/data/motion.csv`"]),
    ("new-skills/react-bits/SKILL.md", "skills/react-bits/SKILL.md",
     ["The fix #22 pin and stack scope: owned by this skill (commit `9d9c687…`)"],
     ["The fix #22 pin and stack scope: `skills/ui-ux-pro-max/SKILL.md` (§11, REACTBITS_F22)"]),
    ("new-rules/hackathon-mode.mdc", "rules/hackathon-mode.mdc",
     ["use `design-taste-frontend` (design lead for every surface) with `ui-ux-pro-max` lookups and `less-flat-ui` TOGETHER. `design-taste-frontend` sets the design direction, consulting `ui-ux-pro-max` only as a lookup inventory after the direction is set",
      "Every build — a full company or landing-page build, a dashboard/app surface, or a component — is led by `design-taste-frontend` (fix #32: the design lead for every surface). `ui-ux-pro-max` is the lookup inventory the lead consults after the direction is set; it never leads.",
      "`ui-ux-pro-max` is the lookup-only design inventory for dashboards and apps (fix #32)",
      "A new look belongs to `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` lookups) and `less-flat-ui` — never to `polish-pass`.",
      "every surface — a full landing/company page, dashboards, apps, components — → `design-taste-frontend` (design lead), with `ui-ux-pro-max` as its lookup inventory;"],
     ["`ui-ux-pro-max` sets the design direction",
      "`ui-ux-pro-max` is the general design intelligence",
      "It replaces `ui-ux-pro-max` as design lead",
      "dashboards and apps → `ui-ux-pro-max`"]),
    ("new-rules/ponytail.mdc", "rules/ponytail.mdc",
     ["the UI direction set by the hackathon-mode rule (`design-taste-frontend` leading every surface, with `ui-ux-pro-max` lookups and `less-flat-ui` texture)"],
     ["(`ui-ux-pro-max` + `less-flat-ui` pairing, or `design-taste-frontend` on full landing/company pages)"]),
    ("round2-skills/polish-pass/SKILL.md", "skills/polish-pass/SKILL.md",
     ["a new look belongs to design-taste-frontend (design lead for every surface, with ui-ux-pro-max lookups) and less-flat-ui, not this skill.",
      "The plugin already has `design-taste-frontend` for design direction on every surface (with `ui-ux-pro-max` as its lookup inventory) and `less-flat-ui` for surface treatments. Those skills own the look.",
      "route it back to the design skill (`design-taste-frontend`, the design lead for every surface) for a redesign within the existing caps",
      "If the user asks for a new look outright, that is not this skill: say so and point them at `design-taste-frontend`.",
      "| `design-taste-frontend` / `less-flat-ui` (with `ui-ux-pro-max` lookups) — not this skill |"],
     ["a new look belongs to ui-ux-pro-max and less-flat-ui, not this skill.",
      "The plugin already has `ui-ux-pro-max` and `less-flat-ui` for design direction",
      "route it back to the design skill (`ui-ux-pro-max`, or `design-taste-frontend` on a landing page)"]),
    ("round2-skills/polish-pass/reference/polish.md",
     "skills/polish-pass/reference/polish.md",
     ["routed to the design skill (`design-taste-frontend`, the design lead for every surface) for a redesign within the existing caps",
      "routed to <`design-taste-frontend`> for redesign",
      "run `design-taste-frontend` for that."],
     ["(`ui-ux-pro-max`, or `design-taste-frontend` on a landing page)",
      "run `ui-ux-pro-max` for that."]),
    # Audit round 1 (B3): unslop-fixes.md design-system + spacing rewordings.
    ("round2-skills/polish-pass/reference/unslop-fixes.md",
     "skills/polish-pass/reference/unslop-fixes.md",
     ["`design-taste-frontend` step 4a defines the design system before implementing UI",
      "Spacing comes from the craft floor (Impeccable/`polish-pass`) and `motion-foundations` tokens, with `ui-ux-pro-max` guidelines as a lookup only"],
     ["system: `ui-ux-pro-max` (\"Define the design system before implementing UI\")",
      "`ui-ux-pro-max` owns spacing;"]),
]

SKIP_DIRS = {"node_modules", ".git"}
UIPRO_MOVE = ["design the dashboard", "redesign the app ui",
              "dashboard design", "app interface design"]
FIX32_NOTE = ("- **Fix #32 ui-ux-pro-max demotion (Nov 17, 2026)** — ui-ux-pro-max is now lookup-only: "
              "design-taste-frontend leads every surface (landing, dashboard/app, component) with ui-ux-pro-max "
              "as its lookup inventory. Trigger keys 49 -> 48 (the dashboard phrases moved to "
              "design-taste-frontend; the skill:ui-ux-pro-max key is deleted). Skills stay 72. (`UIPROLOOKUP_F32`)")
FIX31_NOTE_START = "- **Fix #31 design libraries (Nov 17, 2026)**"


def p(rel):
    return os.path.join(BASE, rel)


def sp(rel):
    return os.path.join(ROOT, rel)


def exists(f):
    return os.path.exists(f)


def read(f):
    with open(f, encoding="utf-8") as fh:
        return fh.read()


def write(f, text):
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(text)


def _walk_files():
    for _root, _dirs, _files in os.walk(BASE):
        _dirs[:] = [d for d in _dirs if d not in SKIP_DIRS]
        for _name in sorted(_files):
            _path = os.path.join(_root, _name)
            try:
                with open(_path, encoding="utf-8") as _fh:
                    yield _path, _fh.read()
            except (UnicodeDecodeError, OSError):
                yield _path, None


def _block(text, marker):
    _i = text.find(marker)
    if _i < 0:
        return None
    _j = text.find("\n", _i)
    return text[_i:_j] if _j > _i else text[_i:]


# Scan (audit round 4, DECISION-32-16): SUBJECT ATTRIBUTION, tightened
# (audit #103 A-M1/A-M2/B-M1..B-M6). The block below is byte-identical in
# fix32.py and verify32.py check 15b — same helpers, same regexes, same
# tables — so the verifier cannot drift from the patcher. Auditors
# extract the helpers by AST and diff them; edit both files together.
#
# Rule, per denylist-verb occurrence in a 7-line window (mention line
# +/-3, lines joined with "\n" so line boundaries stay visible):
#   1. LINKAGE: the verb is a candidate only if some ui-ux-pro-max
#      mention in the window lies in the same clause. A table pipe
#      breaks linkage ONLY between non-adjacent cells (more than one
#      pipe between verb and mention — a table row is one clause) or
#      when the verb is not the first word of its cell (a verb
#      mid-cell, e.g. "where content and controls stay usable", does
#      not predicate the mention in the next cell; a verb that opens
#      its cell, e.g. "| `ui-ux-pro-max` | leads dashboards |", does).
#      A sentence terminator (". "/"! "/"? ") or a new bullet line
#      breaks linkage ONLY when another named skill sits between verb
#      and mention, and only across ADJACENT sentences/bullets (at
#      most one terminator and at most one bullet boundary between
#      them — a verb several sentences from the mention is not
#      adjacent, e.g. the README "Orchestration — /orchestrate runs"
#      line five sentences from the fix #32 bullet). A heading line
#      still breaks linkage. A plain newline continuation does NOT
#      break linkage. No forward/reverse distance cap: the window
#      bounds it. COMPOUND GUARD: every denylist pattern carries
#      (?<![\w]-) — a verb occurrence immediately preceded by a hyphen
#      is part of a hyphenated compound (package name
#      "camera-controls@3.1.2", adjective "app-led" / "type-led" /
#      "design-led") and never a finite verb predicated of
#      ui-ux-pro-max. A verb after a dash+space ("— leads") or a
#      bullet ("- leads") is unaffected: the char before it is a
#      space, not a hyphen.
#   2. ATTRIBUTION (the core): look up to 60 chars BEFORE the verb. A
#      skill name counts as the verb's attributable subject ONLY when
#      (a) it is the LAST skill-name occurrence before the verb (after
#      exclusions), (b) it is NOT inside (...) or [...] spans — unless
#      the verb lies inside the SAME span (the paren never closed
#      between subject and verb, e.g. the DESIGNPKG-AUTO skill list),
#      (c) it is NOT preceded within ~16 chars by "by " (passive
#      agent) or "with " (adjunct) with nothing but filler between,
#      and (d) no ui-ux-pro-max mention sits between it and the verb
#      (implied by (a)). A subject negated by a denial immediately
#      before it ("not Taste") does not count. "this skill" counts as
#      the file's own skill EXCEPT when it directly follows a
#      ui-ux-pro-max mention as a dash/comma appositive
#      ("`ui-ux-pro-max` — this skill leads"), where it refers to
#      ui-ux-pro-max itself (B-M1); the tree's own "This skill owns
#      texture" / "this skill leads the page system" lines rely on it
#      counting. A passive agent counts too: "led by <attributable
#      subject>" after the verb attributes it elsewhere; "led by
#      ui-ux-pro-max" does not. Otherwise the verb is unattributed
#      and the window FLAGS.
#   3. LOOKUP: REMOVED in round 4 (DECISION-32-17). _lookup_exempt was
#      dead code — _scan_window never called it — so it is deleted,
#      not widened. There is no lookup exemption path: a lookup marker
#      never excuses a verb; a line flags iff it contains an
#      unattributed denylist verb linked to a mention.
#   4. DENIAL: a denial word (never, no longer, not, doesn't/does not)
#      excuses a verb ONLY if it sits within 15 chars immediately
#      BEFORE that verb occurrence AND the text between the denial and
#      the verb contains no skill name other than the verb's
#      attributed subject ("`ui-ux-pro-max` — not Taste — leads"
#      flags: Taste sits between "not" and "leads"). A whole-window
#      denial excuses nothing.
#   5. REVERSE DEFINE: "define(s) the design system" flags UNLESS
#      "design-taste-frontend" governs it — within 60 chars before
#      the define occurrence (same sentence) or within 60 chars after
#      it as the instrument ("Define the design system with
#      design-taste-frontend step 4a"), same sentence. The 60-char
#      span (not ~30) is forced by the legitimate orchestrate line
#      "the FIRST UI slice ... led by design-taste-frontend with
#      ui-ux-pro-max lookups) defines the design system itself",
#      where Taste sits 53 chars before "defines".
#   6. DESIGN LEAD, EITHER SIDE (B-M5): a "design lead" phrase does
#      not flag when another named skill is positively identified as
#      its referent — named AFTER the phrase (copula, appositive, or
#      parenthetical naming it before any verb and before any
#      ui-ux-pro-max mention) or named BEFORE it (the nearest
#      attributable subject joined to the phrase only by connectors:
#      copula, "by", "as", articles, punctuation, parens). Flag only
#      when ui-ux-pro-max is the referent (nearest skill name to the
#      phrase) or no skill is named.
#   7. NOUN GUARDS (kept denylist items that are nouns in legitimate
#      lines): "lead" inside "design lead"/"design-lead" is the
#      design-lead pattern, not a lead verb; "the lead <verb>" ("the
#      lead consults") is a noun subject, not a verb; a "design lead"
#      phrase that is the subject of a following non-copula verb
#      ("the design-lead inventories...") is a role noun in use, and
#      a "design lead" phrase whose referent is not ui-ux-pro-max
#      ("whose design lead is the question") is not a claim about it;
#      "identity" followed by a noun ("identity tokens") is a
#      modifier, not a head claim.
# Synonym test (fixed tree, audit #102-B M3 + DECISION-32-13, extended
# audit #103 A-M2/B-M2 + DECISION-32-16): every synonym below was run
# against the fixed tree. "runs" and "prescribes" false-positived on
# legitimate lines ("the FIRST UI slice that runs", "no skill file ...
# prescribes it as an option", "the deliberate path ... runs through
# the named skill") and those three control lines were REWORDED
# meaning-preservingly instead of dropping the synonyms (see
# DECISION-32-13): runs -> executes, runs through -> goes through,
# prescribes -> recommends. Round-4 narrowings (each false-positive
# tested on the fixed tree, see DECISION-32-16): bare "leadership"
# flags the legitimate orchestrate row-10 line ("design leadership is
# the question"), so the entry is narrowed to "leadership of"; bare
# "set" flags the legitimate hackathon-mode §2 line ("the direction
# is set") and "skill set" noun lines, so "set" is covered ONLY by
# the "set by ui-ux-pro-max" passive-agent pattern. No synonym was
# dropped: "heads" (prescribed by audit #102-B M3, missed in round 3)
# is added, plus "steers", "is the authority on", "is in charge of",
# and the generalized "sets ... direction". Round 5 (audit #104-B O7 +
# DECISION-32-20): "oversees" and "is responsible for" are added — both
# pass with zero false positives on the fixed tree ("oversees" occurs
# nowhere in the tree; "is responsible for" matches nowhere — the
# tree's "responsible for" lines say "layer responsible for" /
# "remains responsible for", with no "is"). Round 5 (audit #104-B O1/O6
# + DECISION-32-20): bare "owned" was tested and DROPPED — it
# false-positives on legitimate D32-4/D32-5 inventory language
# (design-inventory.md:39 pins row "owned by their per-skill homes,
# with the upstream vendored record in `skills/ui-ux-pro-max/SKILL.md`"
# and :146 §9 row "Owned by their per-skill homes — ..."), so the
# passive "owned by `ui-ux-pro-max`" (O6) stays an observation per
# DECISION-32-18; the :568 line is fixed by rewording instead (build.sh
# patch, "The z-axis follows the depth rules (DEPTH_F22,
# `ui-ux-pro-max` depth rules as lookup)"). "responsible" joins
# _CLAUSE_VERB_RE only (it is the adjective in "is responsible for",
# not a verb stem for the "the lead <verb>" noun guard, so it does not
# join _NOUN_LEAD_VERBS); "oversees" joins both sibling tables.
_ATTRIB_SUBJECTS = [
    r"design-taste-frontend", r"\bTaste\b", r"design[ -]lead",
    r"less-flat-ui", r"polish-pass", r"motion-foundations",
    r"motion-patterns", r"design-system", r"\bgsap\b", r"react-bits",
    r"getlayers", r"hairline-create", r"hairline-adopt",
    r"make-interfaces-feel-better", r"motionsites-web-builder",
    r"this skill",
]
_SUBJ_RE = re.compile("|".join(f"(?:{s})" for s in _ATTRIB_SUBJECTS),
                      re.IGNORECASE)
_SUBJ_AFTER_RE = re.compile(
    r"^\s+by\s+[`'\"(]*(" + "|".join(_ATTRIB_SUBJECTS) + r")",
    re.IGNORECASE)
_DENIAL_WORD_RE = re.compile(
    r"\b(never|no longer|not|doesn'?t|does not)\b", re.IGNORECASE)
# (name, pattern). "lead" excludes the word inside "design lead" /
# "design-lead" (that is the design-lead pattern). "identity" and
# "direction check" are kept from the round-1/round-2 denylist: C4
# ("the ui-ux-pro-max identity defines the brand") and the
# brand-identity pre-fix site need "identity", and the gan-build /
# gan-design cold-start "direction check" step name needs the
# direction-check pattern to stay covered. Round 4 (DECISION-32-16):
# "sets-direction" is generalized to "sets? (the <word>) direction"
# (catches "sets the dashboard direction", "sets direction for
# dashboards"); "heads" (audit #102-B M3, missed in round 3),
# "steers", "leadership of" (narrowed from bare "leadership"),
# "is the authority on", "is in charge of", and the passive-agent
# "set by ui-ux-pro-max" are added (bare "set" is NOT added: it
# false-positives on legitimate lines — see the synonym test above).
# Round 5 (DECISION-32-20): "oversees" and "is responsible for" are
# added (audit #104-B O7, zero false positives — see the synonym test
# above). Bare "owned" is NOT added: it false-positives on legitimate
# D32-4/D32-5 inventory lines (see the synonym test above).
_VERB_RES = [
    ("lead", r"(?<!design[ -])\b(lead|leads|leading|led)\b"),
    ("sets-direction", r"\bsets?\s+(?:the\s+\w+\s+)?direction\b"),
    ("design-lead", r"design[ -]lead"),
    ("owns", r"\bowns\b"),
    ("decides", r"\bdecides\b"),
    ("runs", r"\bruns\b"),
    ("controls", r"\bcontrols\b"),
    ("authors", r"\bauthors\b"),
    ("drives", r"\bdrives\b"),
    ("directs", r"\bdirects\b"),
    ("governs", r"\bgoverns\b"),
    ("dictates", r"\bdictates\b"),
    ("determines", r"\bdetermines\b"),
    ("prescribes", r"\bprescribes\b"),
    ("heads", r"\bheads\b"),
    ("steers", r"\bsteers\b"),
    ("leadership", r"\bleadership of\b"),
    ("authority", r"\bis the authority on\b"),
    ("in-charge", r"\bis in charge of\b"),
    ("oversees", r"\boversees\b"),
    ("responsible-for", r"\bis responsible for\b"),
    ("set-by", r"\bset\s+by\s+(?:the\s+)?[`'\"(]*ui-ux-pro-max\b"),
    ("identity", r"\bidentity\b"),
    ("direction-check", r"direction[ -]check"),
    ("define-system", r"defines? the design system"),
]
# Every denylist pattern carries a compound guard (?<![\w]-): a verb
# occurrence immediately preceded by a hyphen is part of a hyphenated
# compound (a package name like "camera-controls@3.1.2", an adjective
# like "app-led" / "type-led" / "design-led") and never a finite verb
# predicated of ui-ux-pro-max (round 4, DECISION-32-16). A verb after
# a dash+space ("— leads") or a bullet ("- leads") is unaffected: the
# char before it is a space, not a hyphen.
_VERB_RES = [(n, re.compile(r"(?<![\w]-)" + p, re.IGNORECASE))
             for n, p in _VERB_RES]
_NOUN_LEAD_VERBS = (
    r"(?:consults|decides|sets|reads|selects|inventories|owns|defines"
    r"|chooses|applies|governs|directs|controls|runs|leads|determines"
    r"|dictates|authors|prescribes|heads|steers|oversees|names|routes|checks)")
_CLAUSE_VERB_RE = re.compile(
    r"(?<![\w]-)\b(?:leads?|led|owns|defines?|sets|decides|controls|runs|drives"
    r"|directs|governs|dictates|determines|authors|prescribes|heads"
    r"|steers|oversees|responsible|reads|selects|inventories|consults|names|routes|checks"
    r"|applies|chooses)\b",
    re.IGNORECASE)


def _clause_boundaries_between(_win, _a, _b, _vstart=None):
    """True when a clause boundary lies between offsets _a and _b
    (_a < _b). Round 4 (DECISION-32-16): a table pipe breaks linkage
    ONLY between non-adjacent cells (more than one pipe between verb
    and mention — a table row is one clause) or when the verb is not
    the first word of its cell (a verb mid-cell, e.g. "where content
    and controls stay usable", does not predicate the mention in the
    next cell; a verb that opens its cell, e.g. "| `ui-ux-pro-max` |
    leads dashboards |", does); a sentence terminator or a new bullet
    line breaks linkage ONLY when another named skill sits between
    verb and mention, and only across ADJACENT sentences/bullets (at
    most one terminator and at most one bullet boundary between
    them — a verb several sentences from the mention is not adjacent,
    e.g. the README "Orchestration — /orchestrate runs" line five
    sentences from the fix #32 bullet); a heading line still breaks
    linkage. A plain newline continuation does not count."""
    _seg = _win[_a:_b]
    if "|" in _seg:
        if _seg.count("|") > 1:
            return True
        if _vstart is not None:
            _cell = _win.rfind("|", 0, _vstart)
            _cell_text = _win[_cell + 1:_vstart] if _cell >= 0 \
                else _win[:_vstart]
            if not re.fullmatch(r"[\s\-*•\d.)]*", _cell_text):
                return True
    _terms = len(re.findall(r"[.!?]\s", _seg))
    _bullets = len(re.findall(r"\n\s*(?:[-*]|\d+\.)", _seg))
    if _terms or _bullets:
        if _terms > 1 or _bullets > 1:
            return True
        return bool(_SUBJ_RE.search(_seg))
    if re.search(r"\n\s*#{1,6}\s", _seg):
        return True
    return False


def _linked_mention(_win, _vstart, _vend):
    """Nearest ui-ux-pro-max mention in the same clause as the verb
    occurrence [_vstart, _vend), or None when no mention is linked."""
    for _m in re.finditer(r"ui-ux-pro-max", _win):
        _ms = _m.start()
        if _ms >= _vend:
            if not _clause_boundaries_between(_win, _vend, _ms, _vstart):
                return _ms
        elif not _clause_boundaries_between(_win, _ms + 13, _vstart, _vstart):
            return _ms
    return None


def _paren_depth(_win, _pos):
    """Nesting depth of (...) / [...] spans at offset _pos."""
    _d = 0
    for _ch in _win[:_pos]:
        if _ch in "([":
            _d += 1
        elif _ch in ")]":
            _d = max(0, _d - 1)
    return _d


def _this_skill_appositive(_win, _pos):
    """True when a 'this skill' occurrence at _pos directly follows a
    ui-ux-pro-max mention as a dash/comma appositive ('`ui-ux-pro-max`
    — this skill ...'), i.e. it refers to ui-ux-pro-max itself rather
    than the file's own skill (B-M1). Only whitespace, commas, and
    dashes may intervene, and the gap is at most 10 chars."""
    for _m in re.finditer(r"ui-ux-pro-max", _win[:_pos]):
        _gap = _win[_m.end():_pos]
        if len(_gap) <= 10 and re.fullmatch(r"[\s,—–\-`'\"()\[\]]*", _gap):
            return True
    return False


def _attributed_before(_win, _vstart):
    """Attributable subject for the verb at _vstart, or None. A skill
    name counts ONLY when (a) it is the LAST skill-name occurrence
    before the verb (after exclusions), (b) it is NOT inside (...) or
    [...] spans — unless the verb lies inside the SAME span (the
    paren depth never drops below the subject's depth between subject
    and verb, e.g. the DESIGNPKG-AUTO skill list and the ponytail
    rule's "(design-taste-frontend leading every surface"), (c) it is
    NOT preceded within ~16 chars by "by " (passive agent) or "with "
    (adjunct) with nothing but filler between, and (d) no
    ui-ux-pro-max mention sits between it and the verb (implied by
    (a)). A subject negated by a denial immediately before it ("not
    Taste") does not count. "this skill" counts as the file's own
    skill EXCEPT when it directly follows a ui-ux-pro-max mention as
    a dash/comma appositive (see _this_skill_appositive)."""
    _span_start = max(0, _vstart - 60)
    _span = _win[_span_start:_vstart]
    _occs = []
    for _m in _SUBJ_RE.finditer(_span):
        _occs.append((_span_start + _m.start(), "subj", _m.group(0)))
    for _m in re.finditer(r"ui-ux-pro-max", _span):
        _occs.append((_span_start + _m.start(), "uipro", None))
    _occs.sort(key=lambda _t: _t[0])
    _cands = []
    for _pos, _kind, _txt in _occs:
        if _kind != "subj":
            continue
        if _txt.lower() == "this skill" \
                and _this_skill_appositive(_win, _pos):
            continue
        _pre = _win[max(0, _pos - 16):_pos]
        _bw = re.search(r"\b(by|with)\b", _pre, re.IGNORECASE)
        if _bw and not _SUBJ_RE.search(_pre[_bw.end():]) \
                and not re.search(r"[.!?]", _pre[_bw.end():]):
            continue
        if re.search(r"\b(never|no longer|not|doesn'?t|does not)\s+[`'\"(]*$",
                     _pre, re.IGNORECASE):
            continue
        _d = _paren_depth(_win, _pos)
        if _d > 0:
            _dd = _d
            _ok = True
            for _ch in _win[_pos:_vstart]:
                if _ch in "([":
                    _dd += 1
                elif _ch in ")]":
                    _dd -= 1
                    if _dd < _d:
                        _ok = False
                        break
            if not _ok:
                continue
        _cands.append((_pos, _txt))
    if not _cands:
        return None
    _last_pos, _last_txt = _cands[-1]
    if any(_pos > _last_pos for _pos, _kind, _t in _occs
           if _kind == "uipro"):
        return None
    return _last_txt


def _passive_attributed(_win, _vend):
    """Passive agent after the verb: "led by <attributable subject>"
    attributes the verb elsewhere. Backticks/quotes around the agent
    are allowed ("led by `design-taste-frontend`")."""
    return bool(_SUBJ_AFTER_RE.match(_win[_vend:_vend + 40]))


def _denied_before(_win, _vstart, _attr_subj=None):
    """A denial excuses a verb ONLY when a denial word sits within 15
    chars immediately before the verb AND the text between the denial
    and the verb contains no skill name other than the verb's
    attributed subject (B-M4: "`ui-ux-pro-max` — not Taste — leads"
    flags, because Taste sits between "not" and "leads"; "ui-ux-pro-max
    never leads dashboards" does not flag, because nothing sits
    between "never" and "leads")."""
    _span = _win[max(0, _vstart - 15):_vstart]
    _ms = list(_DENIAL_WORD_RE.finditer(_span))
    if not _ms:
        return False
    _m = _ms[-1]
    _between = _win[max(0, _vstart - 15) + _m.end():_vstart]
    for _s in _SUBJ_RE.finditer(_between):
        if _attr_subj is not None \
                and _s.group(0).lower() == _attr_subj.lower():
            continue
        return False
    if "ui-ux-pro-max" in _between:
        return False
    return True


def _define_governed(_win, _vstart, _vend):
    """M6: "define(s) the design system" is governed by Taste when
    design-taste-frontend sits within 60 chars before the define
    (same sentence) or within 60 chars after it as the instrument
    ("Define the design system with design-taste-frontend step 4a"),
    same sentence. A Taste mention in a LATER sentence does not
    govern (the M6 sprinkle case)."""
    _before = _win[max(0, _vstart - 60):_vstart]
    _before = re.split(r"[.!?]\s", _before)[-1]
    if "design-taste-frontend" in _before.lower():
        return True
    _after = re.split(r"[.!?]\s", _win[_vend:_vend + 60])[0]
    return "design-taste-frontend" in _after.lower()


def _design_lead_referent(_win, _vend):
    """For a "design lead" phrase: is ui-ux-pro-max its referent? Look
    at the clause after the phrase (to sentence end / pipe / bullet /
    ";"). The referent is ui-ux-pro-max when the first copula in the
    clause is followed by it ("the design lead is `ui-ux-pro-max`")
    or it appears before any other verb in the clause (appositive:
    "The design lead for dashboards, `ui-ux-pro-max`"). Otherwise
    the phrase refers to something else ("whose design lead is the
    question") and is not a claim about ui-ux-pro-max. A table pipe
    does not cut the clause (round 4: a table row is one clause)."""
    _clause = _win[_vend:_vend + 160]
    _m = re.search(r"[.!?]\s|\n\s*(?:[-*]|\d+\.|#{1,6}\s)|;", _clause)
    if _m:
        _clause = _clause[:_m.start()]
    _mu = re.search(r"ui-ux-pro-max", _clause)
    _mc = re.search(r"\b(is|are|was|were|be|been)\b", _clause)
    _mv = _CLAUSE_VERB_RE.search(_clause)
    if _mu and (_mc is None or _mu.start() < _mc.start()) \
            and (_mv is None or _mu.start() < _mv.start()):
        return True
    if _mc:
        _after = _clause[_mc.end():].lstrip(" \t`'\"")
        if _after.startswith("ui-ux-pro-max"):
            return True
    return False


def _design_lead_other_referent(_win, _vend):
    """True when the clause AFTER a "design lead" phrase positively
    names ANOTHER attributable subject as the referent — a copula,
    appositive, or parenthetical naming it before any verb in the
    clause and before any ui-ux-pro-max mention (B-M5: a
    positively-identified non-uipro referent must not fall back to
    the before-span flag)."""
    _clause = _win[_vend:_vend + 160]
    _m = re.search(r"[.!?]\s|\n\s*(?:[-*]|\d+\.|#{1,6}\s)|;", _clause)
    if _m:
        _clause = _clause[:_m.start()]
    _mu = re.search(r"ui-ux-pro-max", _clause)
    _mv = _CLAUSE_VERB_RE.search(_clause)
    for _s in _SUBJ_RE.finditer(_clause):
        if _mu and _s.start() > _mu.start():
            continue
        if _mv and _s.start() > _mv.start():
            continue
        return True
    return False


def _design_lead_before_referent(_win, _vstart):
    """True when an attributable subject is named as the design lead
    immediately BEFORE the phrase: the nearest attributable subject
    in the 60 chars before it, joined to the phrase only by
    connectors (copula, "by", "as", articles, punctuation, parens),
    with no ui-ux-pro-max mention between subject and phrase and no
    denial negating the subject (B-M5, either-side rule: "led by
    `design-taste-frontend` (design lead for every surface)" names
    Taste as the design lead)."""
    _span_start = max(0, _vstart - 60)
    _span = _win[_span_start:_vstart]
    _subs = list(_SUBJ_RE.finditer(_span))
    if not _subs:
        return False
    _m = _subs[-1]
    _abs = _span_start + _m.start()
    if _m.group(0).lower() == "this skill" \
            and _this_skill_appositive(_win, _abs):
        return False
    _between = _win[_span_start + _m.end():_vstart]
    if "ui-ux-pro-max" in _between:
        return False
    if re.search(r"\b(never|no longer|not|doesn'?t|does not)\s+[`'\"(]*$",
                 _win[max(0, _abs - 12):_abs], re.IGNORECASE):
        return False
    return bool(re.fullmatch(
        r"(?:[\s`'\"(),]|is|are|was|were|by|led|as|the|a|an|named|called)*",
        _between, re.IGNORECASE))


def _design_lead_is_subject(_win, _vend):
    """A "design lead" phrase that is the subject of a following
    non-copula verb ("the design-lead inventories/selects/reads...")
    is a role noun in use, not a claim about ui-ux-pro-max."""
    _after = _win[_vend:_vend + 40]
    _m = re.match(r"\s+(\w+)", _after)
    if not _m:
        return False
    _w = _m.group(1).lower()
    if _w in ("is", "are", "was", "were", "be", "been"):
        return False
    return bool(re.match(
        r"(?:inventor|select|read|decide|set|choose|appl|govern|lead"
        r"|own|defin|check|consult|name|rout)", _w))


def _scan_window(_win):
    """True when a 7-line window flags ui-ux-pro-max lead language:
    some denylist verb occurrence in the window is linked to a
    ui-ux-pro-max mention in the same clause, is not attributed
    elsewhere (before-span subject under the round-4 (a)-(d) rules,
    passive agent, Taste-governed define, design-lead referent /
    subject / either-side rules, identity-modifier rule, noun-"lead"
    rule), and is not denied immediately before it under the round-4
    denial rule. There is no lookup exemption (round 4,
    DECISION-32-17: _lookup_exempt was dead code and is deleted)."""
    _flagged = False
    for _name, _rx in _VERB_RES:
        for _m in _rx.finditer(_win):
            if _linked_mention(_win, _m.start(), _m.end()) is None:
                continue
            _attr = _attributed_before(_win, _m.start())
            if _name == "define-system":
                if _define_governed(_win, _m.start(), _m.end()):
                    continue
                if _denied_before(_win, _m.start(), _attr):
                    continue
                _flagged = True
                continue
            if _name == "identity":
                _after = _win[_m.end():_m.end() + 12]
                if re.match(r"\s+(tokens|system|row|rows|check|design)\b",
                            _after, re.IGNORECASE):
                    continue
                if _attr:
                    continue
                if _denied_before(_win, _m.start(), _attr):
                    continue
                _flagged = True
                continue
            if _name == "design-lead":
                if _design_lead_is_subject(_win, _m.end()):
                    continue
                if _attr:
                    continue
                if _design_lead_before_referent(_win, _m.start()):
                    continue
                if _design_lead_other_referent(_win, _m.end()):
                    continue
                if not _design_lead_referent(_win, _m.end()):
                    _span = _win[max(0, _m.start() - 60):_m.start()]
                    if "ui-ux-pro-max" not in _span:
                        continue
                if _denied_before(_win, _m.start(), _attr):
                    continue
                _flagged = True
                continue
            if _name == "lead":
                _seg = _win[max(0, _m.start() - 6):_m.start()]
                _mm = re.match(r"(lead|leads)\b\s+" + _NOUN_LEAD_VERBS
                               + r"\b", _win[_m.start():_m.start() + 30],
                               re.IGNORECASE)
                if _mm and re.search(r"\b(the|a|an)\s*$", _seg,
                                     re.IGNORECASE):
                    continue
            if _attr:
                continue
            if _passive_attributed(_win, _m.end()):
                continue
            if _denied_before(_win, _m.start(), _attr):
                continue
            _flagged = True
    if _flagged:
        return True
    return False



def _lead_scan():
    """SPEC §5(a), tightened in audit round 1 (audit #100 B-M2),
    hardened in audit round 2 (audit #101-B M1, DECISION-32-11), and
    redesigned on subject attribution in audit round 3 (audit #102-B,
    DECISION-32-13) and hardened in audit round 4 (audit #103-B M1-M5
    + #103-A M2, DECISION-32-16): a 7-line window (the ui-ux-pro-max
    line plus three lines either side, joined with "\\n" so line boundaries stay
    visible) around every ui-ux-pro-max mention, flagged when
    _scan_window finds an unattributed denylist verb linked to the
    mention in the same clause. No forward/reverse distance cap: the
    window bounds distance (M7). The lookup exemption is removed
    (DECISION-32-17). The vendored
    skills/ui-ux-pro-max/ subtree is the allowlisted upstream record.
    Returns the list of offending (file, line, window-text) hits.
    """
    _hits = []
    for _path, _text in _walk_files():
        if _text is None:
            continue
        _rel = os.path.relpath(_path, BASE)
        if _rel.startswith("skills/ui-ux-pro-max/"):
            continue
        _lines = _text.split("\n")
        for _i, _ln in enumerate(_lines):
            if "ui-ux-pro-max" not in _ln:
                continue
            _win = "\n".join(_lines[max(0, _i - 3):_i + 4])
            if _scan_window(_win):
                _hits.append((_rel, _i + 1, _win.strip()[:200]))
    return _hits


def _old_lead_hits():
    """Every OLD_LEAD string occurring anywhere in the built tree outside
    the vendored skills/ui-ux-pro-max/ subtree."""
    _hits = []
    for _path, _text in _walk_files():
        if _text is None:
            continue
        _rel = os.path.relpath(_path, BASE)
        if _rel.startswith("skills/ui-ux-pro-max/"):
            continue
        for _old in OLD_LEAD:
            if _old in _text:
                _hits.append((_rel, _old[:60]))
    return _hits



# ---------------------------------------------------------------- main
# Audit #102-B B1: the whole executable body below lives in main(),
# guarded by `if __name__ == "__main__"`. Importing this module
# (as audit #102-A did) must never execute the census, write the
# patch log, or exit: the build runs it as a script, so build
# behavior is unchanged.
def main():
    global BASE, ROOT  # DECISION-32-15: sys.argv is read here, never at
    BASE = sys.argv[1] if len(sys.argv) > 1 else ""  # import time.
    ROOT = os.path.dirname(BASE.rstrip("/")) if BASE else ""
    # ---------------------------------------------------------------- 1. Census (no writes)
    # 1a. Staged weave landed: new anchors present, old anchors absent, in
    #     each built copy. The staged files themselves are read for the
    #     existence check (they must contain the new anchors too).
    for _staged, _built, _new, _old in STAGED_BUILT:
        if not exists(sp(_staged)):
            ERRORS.append(f"census: staged source {sp(_staged)} missing")
            continue
        if not exists(p(_built)):
            ERRORS.append(f"census: built copy {_built} missing")
            continue
        _st = read(sp(_staged))
        _bt = read(p(_built))
        for _a in _new:
            if _a not in _st:
                ERRORS.append(f"census: staged {_staged} lacks new anchor {_a[:50]!r}")
            if _a not in _bt:
                ERRORS.append(f"census: built {_built} lacks new anchor {_a[:50]!r}")
        for _a in _old:
            if _a in _bt:
                ERRORS.append(f"census: built {_built} still carries old text {_a[:50]!r}")
    if not ERRORS:
        CHANGES.append(f"census: staged weave landed in all {len(STAGED_BUILT)} built copies "
                       "(new anchors present, old anchors absent)")

    # 1b. Description patches (build.sh) landed in the built tree.
    _uipro_desc = read(p("skills/ui-ux-pro-max/SKILL.md")).split("---", 2)[1]
    if "LOOKUP ONLY (fix #32)" not in _uipro_desc \
            or "never the design lead" not in _uipro_desc:
        ERRORS.append("census: ui-ux-pro-max description is not the lookup-only rewrite")
    _dtf_desc = read(p("skills/design-taste-frontend/SKILL.md")).split("---", 2)[1]
    if "Use for EVERY surface" not in _dtf_desc \
            or "with ui-ux-pro-max as its lookup inventory" not in _dtf_desc:
        ERRORS.append("census: design-taste-frontend description does not say Taste leads every surface")
    if "Do NOT use for dashboards, apps, components" in _dtf_desc:
        ERRORS.append("census: design-taste-frontend description still bans dashboards/apps")
    _pol = read(p("skills/polish-pass/SKILL.md"))
    if "New motion/interaction-feel design belongs to make-interfaces-feel-better; fixing broken feedback motion is in scope here." not in _pol:
        ERRORS.append("census: polish-pass description lost the (f) motion sentence")
    # frontend-design-direction is CUT (fix27): no built copy exists. Assert
    # the build.sh note instead (3 occurrences: (h) note + audit_patch old + new).
    _bs = read(os.path.join(ROOT, "build.sh"))
    _FDD_NEW = ("design-taste-frontend leads every surface (landing pages, dashboards, apps, components), "
                "with ui-ux-pro-max as its lookup inventory, and polish-pass fixes existing UI.")
    if _bs.count(_FDD_NEW) != 3:
        ERRORS.append(f"census: frontend-design-direction new note occurs {_bs.count(_FDD_NEW)}x in build.sh, expected 3x")
    if "ui-ux-pro-max leads dashboards/apps/components" in _bs:
        ERRORS.append("census: old frontend-design-direction phrase still in build.sh")
    if not ERRORS:
        CHANGES.append("census: description patches landed (uipro lookup-only, Taste leads every surface, "
                       "polish-pass (f) motion sentence, fdd note 3x in build.sh)")

    # 1c. Restatement block landed (orch-* x5, gan x2, design-system, README, less-flat-ui).
    _rest = [
        ("skills/orch-add-feature/SKILL.md",
         "app/dashboard/components: `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + Impeccable"),
        ("skills/orch-build-mvp/SKILL.md",
         "landing: `design-taste-frontend` + dealt Hallmark theme + `ui-ux-pro-max` (lookup) + Impeccable"),
        ("skills/orch-change-feature/SKILL.md",
         "route that to `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` lookups) instead."),
        ("skills/orch-fix-defect/SKILL.md",
         "app/dashboard/components: `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + Impeccable"),
        ("skills/orch-refine-code/SKILL.md",
         "app/dashboard/components: `design-taste-frontend` (design lead for every surface) + `ui-ux-pro-max` lookups + Impeccable"),
        ("commands/gan-build.md",
         "dispatch to the design skill for that surface — `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` lookups) —"),
        ("commands/gan-design.md",
         "dispatch to the design skill for that surface — `design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` lookups) —"),
        ("skills/design-system/SKILL.md",
         "(`design-taste-frontend` direction for every surface, with `ui-ux-pro-max` lookups / dealt Hallmark theme)"),
        ("skills/less-flat-ui/SKILL.md",
         "the named direction from `design-taste-frontend` — the Taste direction with `ui-ux-pro-max` lookups"),
        # Audit round 1 (B2): less-flat-ui L579 — Taste owns layout, type, and
        # components; ui-ux-pro-max is the lookup inventory.
        ("skills/less-flat-ui/SKILL.md",
         "`design-taste-frontend` (Taste) is the design lead that owns layout, type, and components"),
        # Audit round 5 (B-O1, DECISION-32-20): less-flat-ui :568 — the
        # z-axis follows the depth rules (DEPTH_F22, ui-ux-pro-max depth
        # rules as lookup), not "owned by the depth rules".
        ("skills/less-flat-ui/SKILL.md",
         "The z-axis follows the depth rules (DEPTH_F22, `ui-ux-pro-max` depth rules as lookup)"),
        ("README.md",
         "`design-taste-frontend` (design lead for every surface, with `ui-ux-pro-max` lookups)"),
    ]
    for _f, _a in _rest:
        if _a not in read(p(_f)):
            ERRORS.append(f"census: restatement missing in {_f}: {_a[:50]!r}")
    if not ERRORS:
        CHANGES.append("census: fix #32 restatement block landed (orch-* x5, gan x2, design-system, README, less-flat-ui)")

    # 1d. Data census (SPEC §5(f)).
    _data_dir = p("skills/ui-ux-pro-max/data")
    for _fn, _want in EXPECT_DATA.items():
        _fp = os.path.join(_data_dir, _fn)
        if not exists(_fp):
            ERRORS.append(f"census: data file {_fn} missing")
            continue
        with open(_fp, newline="", encoding="utf-8") as _fh:
            _n = sum(1 for _ in csv.reader(_fh)) - 1
        if _n != _want:
            ERRORS.append(f"census: {_fn} has {_n} data rows, expected {_want}")
    _stacks = [x for x in os.listdir(os.path.join(_data_dir, "stacks"))
               if x.endswith(".csv")] if exists(os.path.join(_data_dir, "stacks")) else []
    if len(_stacks) != EXPECT_STACKS:
        ERRORS.append(f"census: stacks dir has {len(_stacks)} csv files, expected {EXPECT_STACKS}")
    _uux = read(p("skills/ui-ux-pro-max/SKILL.md"))
    if "51 active" not in _uux:
        ERRORS.append("census: ui-ux-pro-max SKILL.md no longer claims 51 active styles")
    if not ERRORS:
        CHANGES.append("census: data exact (styles 89/51, palettes 192, fonts 74, guidelines 120, "
                       "icons 105, charts 25, stacks 22, app-interface 32, landing 34, products 192, GSAP presets 17)")

    # 1e. The 11 pins present in their owner homes (SPEC D32-4).
    for _pin, _home in PIN_HOMES + PIN_SUPPORT:
        if _pin not in read(p(_home)):
            ERRORS.append(f"census: pin {_pin!r} missing from owner home {_home}")
    if not ERRORS:
        CHANGES.append("census: all 11 pins present in their owner homes (GSAP in gsap, React Bits in react-bits, "
                       "Lenis/R3F/Casberry in motion-foundations, React Bits/R3F/OriginKit/Casberry in motion-patterns, "
                       "daisyUI in design-system, Vanta/liquid-glass/ShaderGradient/liquid-logo in design-taste-frontend)")

    # 1f. Pin census still exact (the demotion adds no pin text).
    _totals = {k: 0 for k in EXPECT_PIN}
    _totals["bare_fast"] = 0
    for _path, _text in _walk_files():
        if _text is None:
            continue
        for _k in EXPECT_PIN:
            _totals[_k] += _text.count(_k)
        _i = 0
        while True:
            _i = _text.find(FAST_BARE, _i)
            if _i < 0:
                break
            if not _text[max(0, _i - 7):_i].endswith("cursor-"):
                _totals["bare_fast"] += 1
            _i += len(FAST_BARE)
    for _k, _want in EXPECT_PIN.items():
        if _totals[_k] != _want:
            ERRORS.append(f"census: pin {_k} found {_totals[_k]}x, expected {_want}x")
    if _totals["bare_fast"] != 0:
        ERRORS.append(f"census: bare {FAST_BARE} found {_totals['bare_fast']}x, expected 0x")
    if not ERRORS:
        CHANGES.append(
            f"census: pin census holds ({NEW_ID} x{_totals[NEW_ID]}, {NEW_PROSE!r} "
            f"x{_totals[NEW_PROSE]}, {FAST_ID} x{_totals[FAST_ID]}, {OLD_ID} x0, "
            f"{OLD_PROSE!r} x0)")

    # 1g. Trigger pre-state (49 keys, uipro key present with the 4 phrases).
    _tf = p("manifests/context-packs/skill-triggers@1.json")
    _trig = json.load(open(_tf, encoding="utf-8"))
    if _trig["coverage"]["skills"] != 72 or _trig["coverage"]["withTriggers"] != 49:
        ERRORS.append(f"census: trigger coverage pre-state is {_trig['coverage']}, expected skills 72 / withTriggers 49")
    if len(_trig["triggers"]) != 49:
        ERRORS.append(f"census: trigger keys pre-state is {len(_trig['triggers'])}, expected 49")
    if _trig["triggers"].get("skill:ui-ux-pro-max") != UIPRO_MOVE:
        ERRORS.append(f"census: skill:ui-ux-pro-max key is not exactly the 4 dashboard phrases: {_trig['triggers'].get('skill:ui-ux-pro-max')!r}")
    _taste_pre = _trig["triggers"].get("skill:design-taste-frontend")
    if _taste_pre != ["design a landing page", "redesign the landing page",
                     "landing page design", "company page design"]:
        ERRORS.append(f"census: skill:design-taste-frontend pre-state phrases unexpected: {_taste_pre!r}")
    if not ERRORS:
        CHANGES.append("census: trigger pre-state 49 keys; skill:ui-ux-pro-max holds exactly the 4 dashboard phrases")

    # 1h. DESIGNPKG-AUTO + GLOBAL-ROUTING byte-identical in orchestrate + hackathon-mode.
    _orch = read(p("skills/orchestrate/SKILL.md"))
    _hm = read(p("rules/hackathon-mode.mdc"))
    _b1 = _block(_orch, "**DESIGNPKG-AUTO")
    _b2 = _block(_hm, "**DESIGNPKG-AUTO")
    if _b1 is None or _b1 != _b2:
        ERRORS.append("census: DESIGNPKG-AUTO block differs between orchestrate and hackathon-mode")
    _g1 = _block(_orch, "**GLOBAL-ROUTING")
    _g2 = _block(_hm, "**GLOBAL-ROUTING")
    if _g1 is None or _g1 != _g2:
        ERRORS.append("census: GLOBAL-ROUTING block differs between orchestrate and hackathon-mode")
    if not ERRORS:
        CHANGES.append("census: DESIGNPKG-AUTO + GLOBAL-ROUTING blocks byte-identical in orchestrate + hackathon-mode")

    # 1i. Glossary G1-G20 citations stay (SPEC D32-10).
    _gloss = read(p("skills/design-taste-frontend/references/design-glossary.md"))
    if _gloss.count("ui-ux-pro-max") != 17:
        ERRORS.append(f"census: design-glossary cites ui-ux-pro-max {_gloss.count('ui-ux-pro-max')}x, expected 17x")
    if "| G1 Kerning |" not in _gloss or "| G20 " not in _gloss:
        ERRORS.append("census: design-glossary G1/G20 rows missing")
    if not ERRORS:
        CHANGES.append("census: design-glossary G1-G20 citations intact (ui-ux-pro-max 17x)")

    # 1j. README pre-state (count line + fix31 note present, fix32 note absent).
    _readme = read(p("README.md"))
    if "72 skills, 45 agents, 48 rules, and 55 commands in total" not in _readme:
        ERRORS.append("census: README count line does not show 72 skills (pre-patch state unexpected)")
    if FIX31_NOTE_START not in _readme:
        ERRORS.append("census: README fix31 note line not found for fix32 note insert")
    if "UIPROLOOKUP_F32" in _readme:
        ERRORS.append("census: README fix32 note already present (double run?)")
    if ERRORS:
        _log_lines = ["# fix32 run log", "",
                      f"## Errors ({len(ERRORS)})"]
        _log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
        _log_lines += ["", "## Changes (0)", "- none", "",
                       "## Command decisions (0)", "- none", "",
                       "## OWED (0)", "- none"]
        _log_dir = os.path.join(ROOT, "fix32")
        os.makedirs(_log_dir, exist_ok=True)
        with open(os.path.join(_log_dir, "fix32-patch-log.md"), "w",
                  encoding="utf-8") as _fh:
            _fh.write("\n".join(_log_lines) + "\n")
        print(f"fix32: {len(ERRORS)} ERROR(S) in census — no files written",
              file=sys.stderr)
        for e in ERRORS:
            print(f"  ! {e}", file=sys.stderr)
        sys.exit(1)

    # ---------------------------------------------------------------- 2. Writes: trigger move + README note
    with open(_tf, encoding="utf-8") as _fh:
        _trig = json.load(_fh)
    _taste = _trig["triggers"]["skill:design-taste-frontend"]
    for _ph in UIPRO_MOVE:
        if _ph not in _taste:
            _taste.append(_ph)
    del _trig["triggers"]["skill:ui-ux-pro-max"]
    _trig["coverage"]["skills"] = 72
    _trig["coverage"]["withTriggers"] = len(_trig["triggers"])
    with open(_tf, "w", encoding="utf-8") as _fh:
        json.dump(_trig, _fh, indent=1, ensure_ascii=True)
        _fh.write("\n")
    CHANGES.append("trigger: 4 dashboard phrases moved to skill:design-taste-frontend; "
                   "skill:ui-ux-pro-max key deleted; coverage 72/49 -> 72/48")

    _lines = read(p("README.md")).split("\n")
    _idx = next((i for i, _ln in enumerate(_lines)
                 if _ln.startswith(FIX31_NOTE_START)), None)
    if _idx is None:
        ERRORS.append("README: fix31 note line not found for fix32 note insert")
    else:
        _lines.insert(_idx + 1, FIX32_NOTE)
        write(p("README.md"), "\n".join(_lines))
        CHANGES.append("README: fix32 provenance note added after the fix31 note line")

    # ---------------------------------------------------------------- 3. Post-assertions
    _trig = json.load(open(_tf, encoding="utf-8"))
    if len(_trig["triggers"]) != 48:
        ERRORS.append(f"post: trigger keys are {len(_trig['triggers'])}, expected 48")
    if "skill:ui-ux-pro-max" in _trig["triggers"]:
        ERRORS.append("post: skill:ui-ux-pro-max key still present in the trigger manifest")
    if _trig["coverage"]["skills"] != 72 or _trig["coverage"]["withTriggers"] != 48:
        ERRORS.append(f"post: trigger coverage is {_trig['coverage']}, expected skills 72 / withTriggers 48")
    _taste_post = _trig["triggers"].get("skill:design-taste-frontend", [])
    for _ph in UIPRO_MOVE:
        if _ph not in _taste_post:
            ERRORS.append(f"post: phrase {_ph!r} missing from skill:design-taste-frontend")
    if len(_taste_post) != 8:
        ERRORS.append(f"post: skill:design-taste-frontend has {len(_taste_post)} phrases, expected 8")
    if not ERRORS:
        CHANGES.append("post: trigger manifest 48 keys, uipro key gone, 4 dashboard phrases under design-taste-frontend (8 total)")
    _readme = read(p("README.md"))
    if "UIPROLOOKUP_F32" not in _readme:
        ERRORS.append("post: README fix32 note missing")
    if "72 skills, 45 agents, 48 rules, and 55 commands in total" not in _readme:
        ERRORS.append("post: README count line disturbed")
    if "144 skills, 69 agents, 121 rules, 94 commands" not in _readme:
        ERRORS.append("post: README stock-ECC line (144 skills ...) was disturbed")
    # Lead-language denylist + proximity scan (SPEC §5(a)).
    _old_hits = _old_lead_hits()
    if _old_hits:
        for _f, _s in _old_hits[:10]:
            ERRORS.append(f"post: old lead text in {_f}: {_s!r}")
        if len(_old_hits) > 10:
            ERRORS.append(f"post: ... and {len(_old_hits) - 10} more old-lead hits")
    _lead_hits = _lead_scan()
    if _lead_hits:
        for _f, _ln, _tx in _lead_hits[:10]:
            ERRORS.append(f"post: lead-language proximity hit {_f}:{_ln}: {_tx!r}")
        if len(_lead_hits) > 10:
            ERRORS.append(f"post: ... and {len(_lead_hits) - 10} more proximity hits")
    if not ERRORS:
        CHANGES.append("post: zero old lead strings and zero lead-language proximity hits outside the vendored ui-ux-pro-max/ subtree")
    # DESIGNPKG-AUTO + GLOBAL-ROUTING guards (post).
    _b1 = _block(read(p("skills/orchestrate/SKILL.md")), "**DESIGNPKG-AUTO")
    _b2 = _block(read(p("rules/hackathon-mode.mdc")), "**DESIGNPKG-AUTO")
    if _b1 is None or _b1 != _b2:
        ERRORS.append("post: DESIGNPKG-AUTO block no longer byte-identical in orchestrate + hackathon-mode")
    _g1 = _block(read(p("skills/orchestrate/SKILL.md")), "**GLOBAL-ROUTING")
    _g2 = _block(read(p("rules/hackathon-mode.mdc")), "**GLOBAL-ROUTING")
    if _g1 is None or _g1 != _g2:
        ERRORS.append("post: GLOBAL-ROUTING block no longer byte-identical in orchestrate + hackathon-mode")
    if not ERRORS:
        CHANGES.append("post: DESIGNPKG-AUTO + GLOBAL-ROUTING blocks byte-identical")

    # ---------------------------------------------------------------- Decisions + OWED
    DECISIONS = [
        "DECISION-32-1 (SPEC scope): Taste (design-taste-frontend) leads every surface — landing, dashboard/app, component — with ui-ux-pro-max as its lookup inventory after the direction is set. No skill added or removed (72/45/48/55/15); only trigger keys 49 -> 48 (the 4 dashboard phrases move to Taste; the skill:ui-ux-pro-max key is deleted).",
        "DECISION-32-2 (pins, D32-4): all 11 pins verified present in their owner homes, so no pin had to be added. Homes: Lenis/R3F/Casberry in motion-foundations; React Bits/R3F/OriginKit/Casberry in motion-patterns; daisyUI in design-system; Vanta/liquid-glass (78cb6cc)/ShaderGradient/liquid-logo in design-taste-frontend; GSAP in gsap; React Bits in react-bits. The SPEC's parenthetical did not name homes for liquid-glass-js and ShaderGradient — in-tree both live in design-taste-frontend, which is their owner home.",
        "DECISION-32-3 (frontend-design-direction, D32-11): the skill is CUT (fix27) — there is no built copy. Its two demotion sites are both in build.sh: the (h) routing note and the audit_patch old/new pair. fix32.py asserts the new phrase 3x in build.sh instead of in the built tree. This corrects SPEC §0's '2 copies in built tree' (the skill is cut before fix32.py runs).",
        "DECISION-32-4 (polish-pass (f)): subs 2-4 are identity guards — the staged copy now carries the demoted wording, so the patch only guards the lines and keeps staged == built. Sub 1 keeps the description motion-sentence append (that sentence lives only in the built description).",
        "DECISION-32-5 (restatement mechanism): the orch-*/gan/design-system/less-flat-ui restatements live in a new fix32 build.sh block patching final built text, NOT as edits to the fix13-era blocks — those blocks' new texts are further rewritten downstream by fix27/fix29/fix30, so editing them would break downstream anchors. The block runs before fix32.py so its census covers the restatements.",
        "DECISION-32-6 (extra sites found in-tree, beyond SPEC §3): the README UI-skills bullet (generated heredoc in build.sh), the less-flat-ui record-the-treatments line (built copy patched; the global source is read-only and untouched), and round2-skills/polish-pass/reference/polish.md :37/:86/:106 (staged reference file, edited as staged). All three carried lead language for ui-ux-pro-max and are demoted the same way.",
        "DECISION-32-7 (staged/built identity, SPEC §5(h)): asserted per edited anchor, not per whole file — full-file identity does not hold by design for files the build patches (Taste/feature-expansion/polish-pass descriptions, the fix30 pin rename in orchestrate/hackathon-mode), the same precedent as verify31 check 7e.",
        "DECISION-32-8 (audit round 1, B2-B4 — four authority lines SPEC §0 missed): less-flat-ui:579 'that skill owns layout, type, and components' reworded via the build.sh fix32 block (global source ~/workspace/cursor-skills/less-flat-ui is read-only and untouched): ui-ux-pro-max is the lookup inventory (palettes, type scale, guidelines) consulted after the design lead sets the direction; design-taste-frontend (Taste) is the design lead that owns layout, type, and components. unslop-fixes.md:110 reworded in the staged source: the design system is defined by design-taste-frontend step 4a, with ui-ux-pro-max as the lookup source for the system's palette and type rows. unslop-fixes.md:158 reworded in the staged source: spacing comes from the craft floor (Impeccable/polish-pass) and motion-foundations tokens, with ui-ux-pro-max guidelines as a lookup only. orchestrate:171 + design-taste-frontend:444 reworded in both staged files: the brand is generated through Taste's dealt direction (Taste step 4a), with the ui-ux-pro-max lookup rows it used (palette row, type-scale row) cited as lookups, never as the identity source. The whole unslop-fixes.md and the rest of round2-skills/polish-pass/reference/ were checked for other ui-ux-pro-max ownership attributions — the remaining mentions are plain rule citations (Points at / type / spacing-scale pointers), and the tightened scan finds none. (Round 2 correction, DECISION-32-12: the spacing line was cited as :157 in round 1; the :110 edit added a line, so it is :158 — the pointer, not the fix, was stale.)",
        "DECISION-32-9 (scan tightening, audit #100 B-M2): the §5(a) lead scan is now a 3-line window (ui-ux-pro-max line ±1) with an ownership denylist (lead/leads/leading/led, 'sets the design direction', 'design lead', 'owns', co-sourced 'identity', 'direction check' naming ui-ux-pro-max, 'define the design system' as a ui-ux-pro-max attribution) and a shaped exemption (lookup marker attached to the ui-ux-pro-max mention, or a never/no-longer/not-the-design-lead denial) replacing the blanket 'lookup' substring exemption. No reverse pattern for 'identity' or 'define the design system': those would flag the correct Taste-attributed rewordings, where the phrase precedes the lookup mention. The four old B2-B4 strings are added to OLD_LEAD. Prototype scan over the run2 built tree flagged exactly the 5 sites (B2 x1, B3 x2, B4 x2) and zero false positives; the tightened scan must pass 0 hits on the fixed tree, and any legitimate lookup it flags is reworded, never exempted by widening.",
        "DECISION-32-10 (staged/built byte-identity, SPEC §5(h) — verified per file, correct mapping new-skills/new-rules/round2-skills → hackathon-ecc/skills|rules): 6 of 12 staged files are byte-identical; the other 6 differ and EVERY differing line is a known build patch, verified by hunk-identity against HEAD 26b487f (no unexplained line, no real finding): orchestrate 34 lines = 14 fix30 pin-rename pairs (grok-4.7-high → grok-4.7-extra-high) + 3 fix27 agent-rewrite pairs (code-reviewer/security-reviewer → agent (agents/ecc-*.md)); design-taste-frontend 10 lines = 5 pairs, the fix32 D32-11 replace_desc_line description rewrite (the build rewrites the description; staged frontmatter is not the shipped text); feature-expansion 22 lines = 11 pairs (1 build.sh description note, 8 fix27 agent rewrites, 2 ECC-process rewrites); integration 2 lines = 1 pair, build.sh description rewrite (build.sh:594); hackathon-mode 6 lines = 3 pairs (fix16 'claude -p' → 'CLI-subprocess' scrub + 2 fix30 pin renames); polish-pass 6 lines = 3 pairs (build.sh (f) motion-sentence append + 2 Vercel-checklist insertions VERCEL-02/03). NOTE: the brief said '5 of 12' differ; the true count is 6 of 12 (audit #100-A said '5' but listed 6). Polish-pass at HEAD differed in 5 hunks; fix32's staged demotion edit closed 3 of them (15/27/34).",
        "DECISION-32-11 (scan hardening, audit #101-B M1 — the round-1 shaped lookup exemption was still gameable): the exemption now requires the lookup marker to sit within 25 chars AFTER the end of the ui-ux-pro-max mention, with no denylist verb between the mention and the lookup, and no denylist verb directly predicating the mention from the left (nearest denylist verb within 60 chars before the mention joined to it only by a copula/article or bare punctuation, e.g. 'the design lead is `ui-ux-pro-max`'). The reverse 'define the design system' pattern was added (define the design system.{0,40}ui-ux-pro-max); it is excused ONLY when the window attributes the defining to Taste (design-taste-frontend + defines present, as in the correct unslop-fixes.md:110 rewording) and it is the window's sole denylist match — this supersedes DECISION-32-9's 'no reverse pattern for define the design system' rationale, which audit #101-B showed was unforced (the correct rewording says 'defines', which the literal pattern does not match, and sits ~130 chars from the mention). The scan helpers (_lookup_exempt + _scan_window, same regex literals) are byte-identical in fix32.py and verify32.py check 15b. PROOF (test script /tmp/scan32-r2-test.py, run Nov 17, 2026 — ALL PASS): (a) all 4 audit #101-B hypotheticals now flagged — C1 '`ui-ux-pro-max` leads dashboards, using lookups', C2 'The design lead is `ui-ux-pro-max`; consult its lookup inventory afterwards', C3 'Define the design system with `ui-ux-pro-max` before building UI', C5 '`ui-ux-pro-max` owns spacing; see the lookup inventory' (plus C4/C6/C7 controls and 4 extra gaming variants, all flagged); (b) regression — the 4 old B2-B4 strings flagged as bare lines, the 2 round-1 lead strings covered ('`ui-ux-pro-max` (design lead)' flagged by the scan; 'a dashboard/app surface goes to `ui-ux-pro-max`' is caught by the OLD_LEAD substring denylist, not a scan verb, by design), and the 5 pre-fix sites re-inserted at their real sites flag exactly 1 hit each at exactly the right site (less-flat-ui:579, unslop-fixes:110, unslop-fixes:158, orchestrate:171, design-taste-frontend:444); (c) fixed tree 0 hits outside the allowlist — no legitimate lookup reworded; (d) controls not flagged — the Taste-attributed :110 rewording, adjacent-lookup phrasings, and denial lines. verify32.py gains 4 new checks (15b2a-15b2d) running the same _scan_window over the hypotheticals, the old strings, the real :110 window, and adjacent-lookup probes.",
        "DECISION-32-12 (stale pointers, audit #101-B M2): the spacing line is unslop-fixes.md:158, not :157 — the :110 edit replaced 3 lines with 4 (+1 line), shifting everything below it down by one. Corrected in all three places: the SPEC round-1 amendment, patch-log DECISION-32-8, and fix32.py DECISION-32-8. Checked for other stale round-1 pointers in the SPEC, patch log, and fix32.py: none other stale — the other amendment pointers verify (:110, less-flat-ui:579, orchestrate:171, design-taste-frontend:444) and DECISION-32-6's polish.md :37/:86/:106 lines are the reworded lines in the current staged file.",
        "DECISION-32-13 (scan redesign, audit #102-B M1-M7 — subject attribution, not proximity exemptions): the §5(a) lead scan is redesigned, identically in fix32.py and verify32.py check 15b (same helpers, same regexes, same tables, verified by AST comparison). Window: mention line +/-2 (5 lines, joined with newline so line boundaries stay visible). Denylist: lead/leads/leading/led, 'sets the design direction', 'design lead', owns, decides, runs, controls, authors, drives, directs, governs, dictates, determines, prescribes, plus 'identity', 'direction check', and 'define(s) the design system' (kept from rounds 1-2: C4 and the brand-identity pre-fix site need 'identity'). Attribution rule (the core): for each denylist verb occurrence in the window, look at up to 60 chars BEFORE the verb; if that span contains an attributable subject — design-taste-frontend, Taste, design-lead/design lead, less-flat-ui, polish-pass, motion-foundations, motion-patterns, design-system, gsap, react-bits, getlayers, hairline-*, make-interfaces-feel-better, motionsites-web-builder, or 'this skill' (self-reference to the file's own skill) — that appears CLOSER to the verb than any ui-ux-pro-max mention in the span, the verb is attributed elsewhere and skipped; a passive agent counts too ('led by design-taste-frontend' after the verb attributes it elsewhere; 'led by ui-ux-pro-max' does not). Otherwise the verb FLAGS. A verb is a candidate only when linked to a mention in the same clause (no sentence terminator, table pipe, or new bullet/heading line between them; a plain newline continuation does not break linkage, so M4 split-across-lines flags). Lookup exemption is subordinate: it excuses a window only when there is NO unattributed denylist verb in it AND the lookup phrase sits within 25 chars after a mention — it can never excuse a flagged verb (M1). Denial excuses a verb only when the denial word (never, no longer, not, doesn't/does not) sits within 15 chars immediately BEFORE that verb (M5). Reverse define: 'define(s) the design system' flags UNLESS design-taste-frontend governs it within 60 chars before the define (same sentence) or within 60 chars after it as the instrument ('Define the design system with design-taste-frontend step 4a'); the 60-char span (not ~30) is forced by the legitimate orchestrate line where Taste sits 53 chars before 'defines' (M6). Distance caps are DROPPED; the 5-line window bounds distance (M7). Noun guards: 'lead' inside 'design lead'/'design-lead' is the design-lead pattern, not a lead verb; 'the lead <verb>' ('the lead consults') is a noun subject; a 'design lead' phrase that is the subject of a following non-copula verb ('the design-lead inventories...') is a role noun in use, and a 'design lead' phrase whose referent is not ui-ux-pro-max ('whose design lead is the question') is not a claim about it — the referent is ui-ux-pro-max only when the first copula after the phrase is followed by it or it appears before any other verb in the clause (appositive); 'identity' followed by a noun ('identity tokens') is a modifier. Synonym test: every synonym was run against the fixed tree. 'runs' and 'prescribes' false-positived on legitimate lines, so those three control lines were REWORDED meaning-preservingly instead of dropping the synonyms: orchestrate 'the FIRST UI slice that runs' -> 'the FIRST UI slice that executes' (staged new-skills/orchestrate/SKILL.md); vercel-checklist 'the deliberate path for each flagged item runs through the named skill' -> 'goes through the named skill' (staged round2-skills/polish-pass/reference/vercel-checklist.md); design-taste-frontend 'no skill file names it, depicts it, or prescribes it as an option' -> 'or recommends it as an option' (staged new-skills/design-taste-frontend/SKILL.md). No synonym was dropped. PROOF (test script fix32/scan32-r3-test.py, run Nov 17, 2026 — ALL PASS): all 14 audit #102-B M1-M7 hypotheticals flag, all of C1-C7 flag, all 5 pre-fix sites flag exactly 1 hit each at exactly the right site, the fixed tree scans 0 hits, and the legitimate controls do not flag (DESIGNPKG-AUTO paragraph incl. 'the design-lead deciding which leads', fixed :110/:158/brand-identity/less-flat-ui lines, glossary G1-G20 citations incl. G9 'Leading', Taste step 4a lines, the reworded runs/prescribes lines). verify32.py gains 7 new checks (15b3a-15b3f round-3 scan proof + a fix32.py __main__-guard check), 453 -> 460 checks.",
        "DECISION-32-14 (audit #102-B B1 — patch log clobbered + missing import guard): fix32.py had NO `if __name__ == \"__main__\":` guard, so audit #102-A's module import executed main(), its pre-state census failed against the already-fixed tree, and it overwrote scratch-repo/fix32/fix32-patch-log.md with an error stub (Errors 5, Changes 0). The canonical copy fix32/fix32-patch-log.md was INTACT (Errors 0, Changes 14) and was restored into the scratch repo. Fix: the whole executable body of fix32.py now lives in main() under the `if __name__ == \"__main__\":` guard (BASE/ROOT assignments are guarded so import never touches sys.argv), and importing it was proven in /tmp to write nothing and leave the log untouched; the build runs it as a script, so build behavior is unchanged. verify32.py gains a guard check (15b3g).",
        "DECISION-32-15 (audit #103-A M1 / #103-B M6 - BASE/ROOT import guard incomplete): DECISION-32-14 overstated the fix: the executable body moved into main(), but fix32.py:89-90 still read sys.argv at module top level, so importing the module set BASE='SOMEARG' and contradicted the 'guarded so import never touches sys.argv' claim. Fix: module level now assigns BASE = '' and ROOT = ''; main() sets them from sys.argv[1] with a global declaration, so an import leaves BASE '' and touches nothing. DECISION-32-14's text is left intact as history; this decision corrects the record. verify32.py check 15b3g is rewritten as a PROPERTY check (it previously asserted only that the BASE line existed, and would have FAILED if the line were correctly moved): it copies fix32.py to /tmp, imports it with sys.argv=['x','SOMEARG'], and asserts BASE == '', no patch log is written under the temp dir, and the real patch log's md5/mtime are unchanged, plus a static assert that no top-level 'BASE = sys.argv' line exists. PROOF (run Nov 17, 2026 in /tmp/guardproof): BASE '' and ROOT '' after import with argv ['x','SOMEARG']; patch-log md5 af1b1b9f54a0306efa1e21b06fc9a21d unchanged; mtime_ns 1794952991649215775 unchanged; no log written under the temp dir.",
        "DECISION-32-16 (scan round-4 hardening, audit #103-B M1-M5 + #103-A M2): the section 5(a) scan is hardened identically in fix32.py and verify32.py check 15b (same helpers, same regexes, same tables, verified by AST comparison). Window widened from mention +/-2 to +/-3 (7 lines). Denylist additions: 'heads', 'steers', 'leadership of' (bare 'leadership' was tested and DROPPED - it false-positives on the legitimate orchestrate:135 'design leadership is the question'; bare 'set' was likewise dropped - it false-positives on hackathon-mode:18 'the direction is set'), 'is the authority on', 'is in charge of', generalized 'sets (the <word>) direction' (catches 'sets the dashboard direction' and 'sets direction for dashboards'), and the passive-agent rule (a denylist verb whose 'by <subject>' agent is ui-ux-pro-max flags, e.g. 'the direction was set by the ui-ux-pro-max tables'). Attribution tightened (B-M1): a skill name counts as the verb's attributable subject ONLY if (a) it is the LAST skill-name occurrence before the verb, (b) it is NOT inside (...) or [...] spans unless the verb lies in the SAME span, (c) it is NOT preceded within ~16 chars by 'by ' (passive agent) or 'with ' (adjunct) with nothing but filler between, and (d) no ui-ux-pro-max mention sits between it and the verb; a denial-negated subject does not count. 'this skill' counts as the file's own skill EXCEPT when it directly follows a ui-ux-pro-max mention as a dash/comma appositive ('`ui-ux-pro-max` - this skill leads'), where it refers to ui-ux-pro-max itself - the tree's own 'This skill owns texture' (less-flat-ui:568/:579) and 'this skill leads the page system' (design-taste-frontend:10) lines rely on it counting. Clause/window boundaries (B-M3): a table row is ONE clause - pipes break linkage only between non-adjacent cells (>1 pipe) or when the verb is not the first word of its cell ('| `ui-ux-pro-max` | leads dashboards |' flags; 'where content and controls stay usable' mid-cell does not predicate the next cell's mention); a sentence terminator or bullet boundary breaks linkage only when another named skill sits between verb and mention AND only across ADJACENT sentences/bullets (at most one terminator and at most one bullet boundary - a verb several sentences from the mention, e.g. README 'Orchestration - /orchestrate runs' five sentences from the fix #32 bullet, does not link). Denial (B-M4): a denial excuses a verb ONLY within 15 chars immediately before it AND with no skill name other than the verb's attributed subject between denial and verb ('`ui-ux-pro-max` - not Taste - leads' flags; 'ui-ux-pro-max never leads dashboards' does not). Design-lead phrase (B-M5): the check looks BOTH ways - if design-taste-frontend (or another named skill) is named as the design lead in the same window on EITHER side of the phrase, no flag; flag only when ui-ux-pro-max is the referent or no skill is named. Compound guard: every denylist pattern carries (?<![\\w]-), so a verb immediately preceded by a hyphen is part of a hyphenated compound (package name 'camera-controls@3.1.2', adjective 'app-led'/'type-led'/'design-led') and never a finite verb; a verb after a dash+space or a bullet is unaffected. PROOF (test script fix32/scan32-r4-test.py, run Nov 17, 2026 - ALL PASS, 76 checks): all round-4 hypotheticals flag (B-M1a-d, B-M2a-h, B-M3a-d, B-M4a) and all round-4 must-not-flag controls pass (B-M1 legit, B-M4b, B-M5a/b), all round-3 suites still pass, all 5 pre-fix sites flag exactly 1 hit each, fixed tree 0 hits. verify32.py gains 15b4 checks mirroring the round-4 hypotheticals and controls.",
        "DECISION-32-17 (dead code, audit #103-B observation): _lookup_exempt is removed from fix32.py and verify32.py check 15b (and the test file no longer calls it) - _scan_window never called it, so no behavior changes; the scan block stays byte-identical across the three files. There is no lookup exemption path: a lookup marker never excuses a verb; a line flags iff it contains an unattributed denylist verb linked to a mention. Scan scope stays the built tree: the build.sh scan (40 hits with the round-4 scan, old-side patch literals and historical comments) is out of scope by design and is not asserted.",
        "DECISION-32-18 (closed scan acceptance suite, Nov 17, 2026 - coordinator decision): the scan is a regression net, not a proof against arbitrary adversarial prose. Its acceptance suite is the enumerated set - C1-C7, M1-M7 (round 2), B's M1-M5 (round 3), A's M2 (round 3), B's M1-M6 (round 4) - plus the 5 pre-fix sites and the legitimate-controls list. The scan must flag every item in the suite and 0 hits on the fixed tree. New hypotheticals beyond the suite are OBSERVATIONS, not audit findings, unless they demonstrate a realized miss in the tree. The audit loop judges the demotion + the scan against this suite. This is the ceiling on scan-hardening: further rounds would only churn new hypotheticals. Recorded in the SPEC amendment and the MANIFEST.",
        "DECISION-32-19 (audit #103-A M3 - MANIFEST build-env sentence + run-5 exit evidence): the MANIFEST section 0 build-env sentence said /tmp/ecc-repo-clean and /tmp/ecc-dev-install are both symlinks - false for the second: /tmp/ecc-repo-clean IS a symlink to ~/workspace/hackathon-plugin/fix26/scratch-clones/ecc-repo-clean, but /tmp/ecc-dev-install is a REAL directory (containing .cursor/ and the nested symlink .ecc-dev-install -> ~/workspace/hackathon-plugin/fix32/.ecc-dev-install); the sentence is corrected to the true layout, verified with ls -la. build-log-run5.txt lacks the 'BUILD EXIT: 0' trailer runs 1-4 carry because build.sh contains no 'BUILD EXIT' string - the trailer comes from the wrapper echo, and run 5's log was captured without it; the run-5 log is NOT edited after the fact. Honest resolution: run 6 is re-run with the trailer-appending invocation so its log carries the trailer, and the MANIFEST/SPEC state what run 5's log actually evidences (fix32 OK + the coordinator's verify re-run).",
        "DECISION-32-20 (audit round 5, audit #104-A B1 + audit #104-B O1/O6/O7/O8): (a) BUILD GATE WINDOW (B1, blocking): DECISION-32-16 widened the scan window from mention +/-2 to +/-3 (7 lines) in verify32.py check 15b and the scan test, but fix32.py _lead_scan — the build-time gate main() enforces — still sliced _lines[max(0, _i - 2):_i + 3] (5 lines), contradicting its own docstring. Fix: the slice is now _lines[max(0, _i - 3):_i + 4] in fix32.py, so the gate matches the verifier and the test. CORRECTION to the 'hardened identically' claim (SPEC round-4 amendment, MANIFEST §3): the AST comparison covered the shared helpers only — the window is built by the CALLER (_lead_scan in fix32.py, the §15b walk in verify32.py, scan_text in the test), so a caller-side slicing difference was invisible to it; the claim now covers the caller window too, and the slicing is identical in all three files (modulo variable names: _lines / _lines32 / lines). Proof gap closed by verify32.py check 15b5a, which exercises fix32.py's OWN _lead_scan slicing (static assert on the _i - 3 / _i + 4 slice + a dynamic import-from-/tmp run: a tree containing the closed-suite B-M3b construction — verb 3 lines above the mention — flags through _lead_scan, a verb-2-lines-above case flags as a regression, and a clean lookup-only file does not flag), and by scan32-r5-test.py section (l) running the same cases. (b) O1 ADJUDICATION (coordinator decision: FIX): less-flat-ui:568 'The z-axis is owned by the depth rules (`ui-ux-pro-max` depth rules, DEPTH_F22)' is reworded via a third tuple in the build.sh fix32 less-flat-ui patch to 'The z-axis follows the depth rules (DEPTH_F22, `ui-ux-pro-max` depth rules as lookup)' — D32-3 keeps DEPTH_F22 as the referenced rules the design-lead (Taste) cites as lookup, so 'owned by the depth rules' contradicts the framing; the global source ~/workspace/cursor-skills/less-flat-ui is read-only and untouched. fix32.py census section 1c gains the reworded line as an anchor, and verify32.py 15j asserts it. (c) 'OWNED' DROPPED: bare 'owned' (\\bowned\\b) was tested against the fixed tree in /tmp (probe32a) and FALSE-POSITIVES on legitimate D32-4/D32-5 inventory language — design-inventory.md:39 pins row 'owned by their per-skill homes, with the upstream vendored record in `skills/ui-ux-pro-max/SKILL.md` (§11/§15/§17)' and :146 §9 row 'Owned by their per-skill homes — `skills/motion-foundations/SKILL.md` (Lenis, R3F, Casberry), ...' (the :34 GSAP row 'Owned by the gsap skill (fix #32, D32-5)' does NOT flag in isolation — the table-cell rule blocks linkage). Bare 'owned' is therefore NOT added to the denylist in any of the three files; the O6 passive cases ('the dashboard design is owned by `ui-ux-pro-max`', 'dashboard design, owned by `ui-ux-pro-max`, ships first') remain OBSERVATIONS per DECISION-32-18, recorded as must-not-flag cases in scan32-r5-test.py section (m) and verify32.py 15b5c. Tested-but-NOT-applied option for the coordinator: a narrowed 'owned-by' pattern mirroring 'set-by' (\\bowned\\s+by\\s+(?:the\\s+)?[`'\"(]*ui-ux-pro-max\\b) gives 0 hits on the fixed tree and flags both O6 cases (probe32c2) but does not catch the :568 line (its agent is 'the depth rules', not ui-ux-pro-max directly) — the :568 rewording is the fix for that line either way. (d) O7 ADDED: 'oversees' and 'is responsible for' are added to the denylist in all three files (probe32b: 0 hits on the fixed tree; both flag their hypotheticals; the tree's 'responsible for' lines — 'Keep the backend layer responsible for choosing ...', 'the team remains responsible for all claims' — lack 'is' and do not flag). Sibling tables: 'oversees' joins _NOUN_LEAD_VERBS and _CLAUSE_VERB_RE; 'responsible' joins _CLAUSE_VERB_RE only (adjective, not a verb stem for the 'the lead <verb>' noun guard). (e) O8 PROSE: the scan-block comment said the README 'Orchestration — /orchestrate runs' line is 'four sentences' from the fix #32 bullet — verified by counting [.!?]\\s terminators between the line-30 mention and the line-32 'runs': 5, so the word is corrected to 'five' in all three files (scan block comment + _clause_boundaries_between docstring + DECISION-32-16 text). Immaterial to the mechanism (either count exceeds the >1 bound). (f) Housekeeping: scratch-repo/fix32/__pycache__/ (created by a coordinator import test) is removed; all import tests run from /tmp copies, never with the scratch-repo fix32/ on sys.path. PROOF (test script fix32/scan32-r5-test.py, run Nov 17, 2026 - ALL PASS, 100 checks): the full round-4 suite still passes (76 checks), plus (l) the _lead_scan own-slicing cases (static slice + guard proof + B-M3b/2-line/clean through fix32.py's own _lead_scan), (m) the O1/O6 'owned'-dropped record (O6 cases + old :568 line do not flag, reworded :568 line does not flag, real built :568 line carries the new wording, the :39/:146 FP lines do not flag), (n) the O7 additions flag with legitimate 'responsible for' controls not flagging, and (o) the B-M5 design-lead controls re-run (must not flag). verify32.py gains 15b5 checks (15b5a _lead_scan own-slicing, 15b5b O7, 15b5c 'owned' drop + :568 rewording, 15b5d B-M5 re-run) + 1 restatement anchor in 15j, 468 -> 473 checks.",
    ]
    OWED = [
        "OWED-32-1 (call map): the call map is generator-owned and NOT regenerated by the build — fix32.py does not assert it. The worker regenerates it after the build (fix28/callmap/generate_call_map.py, EXPECTED triggers 49 -> 48) and rebuilds so the staged copy flows into the built tree; verify32.py asserts the regenerated map. This also closes OWED-31-3.",
        "OWED-32-2 (vendored self-description): the vendored skills/ui-ux-pro-max/SKILL.md still describes itself as design intelligence for dashboards/apps in its own body text (upstream at UIPRO_PIN, uneditable). Enforcement is the plugin's routing, descriptions, and triggers. If Cursor ever surfaces the skill's own body text as a lead claim in a build, that is a live-test observation, not a fix32 defect.",
        "OWED-32-3 (lead-scan allowlist, redesigned audit round 3 - DECISION-32-13, hardened audit round 4 - DECISION-32-16): the section 5(a) scan is a 7-line window (mention +/-3) with an authority denylist (lead words, 'sets (the <word>) direction', 'design lead', owns, decides, runs, controls, authors, drives, directs, governs, dictates, determines, prescribes, 'heads', 'steers', 'leadership of', 'is the authority on', 'is in charge of', the passive 'set by ui-ux-pro-max', 'identity', 'direction check', 'define(s) the design system', 'oversees', 'is responsible for' (round 5, DECISION-32-20; bare 'owned' tested and DROPPED in round 5 — it false-positives on the legitimate design-inventory :39/:146 'owned by their per-skill homes' lines, so the passive 'owned by ui-ux-pro-max' stays an observation)); each denylist verb is attributed by the subject in the 60 chars before it (or a passive 'by <subject>' after it) and flags unless attributed elsewhere, denied within 15 chars before it, or (for define) governed by design-taste-frontend within 60 chars; attribution counts only the LAST skill-name occurrence before the verb, excluding parenthetical/bracketed names, 'by '/'with ' adjuncts, and appositive 'this skill'; a table row is one clause and adjacent sentences/bullets link; the lookup exemption is REMOVED (dead code, DECISION-32-17); no distance caps. A line that names ui-ux-pro-max as a lead or owner WITHOUT attribution fails the build.",
    ]

    # ---------------------------------------------------------------- main / run log
    _log_lines = ["# fix32 run log", "",
                  f"## Errors ({len(ERRORS)})"]
    _log_lines += [f"- {e}" for e in ERRORS] or ["- none"]
    _log_lines += ["", f"## Changes ({len(CHANGES)})"]
    _log_lines += [f"- {c}" for c in CHANGES] or ["- none"]
    _log_lines += ["", f"## Command decisions ({len(DECISIONS)})"]
    _log_lines += [f"- {d}" for d in DECISIONS] or ["- none"]
    _log_lines += ["", f"## OWED ({len(OWED)})"]
    _log_lines += [f"- {o}" for o in OWED] or ["- none"]
    _log_dir = os.path.join(ROOT, "fix32")
    os.makedirs(_log_dir, exist_ok=True)
    with open(os.path.join(_log_dir, "fix32-patch-log.md"), "w",
              encoding="utf-8") as _fh:
        _fh.write("\n".join(_log_lines) + "\n")
    print(f"fix32: {len(CHANGES)} change(s)")
    for c in CHANGES:
        print(f"  - {c}")
    print(f"fix32: {len(OWED)} OWED item(s) recorded in the patch log")
    if ERRORS:
        print(f"fix32: {len(ERRORS)} ERROR(S)", file=sys.stderr)
        for e in ERRORS:
            print(f"  ! {e}", file=sys.stderr)
        sys.exit(1)
    print("fix32: OK")



if __name__ == "__main__":
    main()
