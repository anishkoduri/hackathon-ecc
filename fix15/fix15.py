#!/usr/bin/env python3
"""Fix program #15: variety + theme-match rule, count-moving rules R1-R5,
fonts/text C1-C3, mandatory screenshot QA D1.

Applies the SPEC.md sections A-D rules to the plugin's staged sources, and
appends a build.sh patch block (LAST, before STEP 5) for the upstream files
that have no staged source (ui-ux-pro-max, make-interfaces-feel-better,
motion-foundations/patterns/advanced, orch-build-mvp).

Canonical rule block (SPEC section A) is VERBATIM identical in every target
file -- the same CANONICAL constant is used for staged edits and the build.sh
block, so audits can grep it everywhere.

Staged-source edits (direct, build.sh copies them verbatim):
  new-skills/design-taste-frontend/SKILL.md ......... A, R1, R2, R4, R5, C1, C2, C3, D1
  new-skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md .. A (Hallmark)
  new-skills/orchestrate/SKILL.md ................... A (design-package rule), R1 (5a), D1 (5, 6)
  round2-skills/polish-pass/SKILL.md ................ A, C3 (harmony), D1 (Capture/Verify)
  ~/workspace/cursor-skills/less-flat-ui/SKILL.md ... A, R3 (surface check)
Build.sh patch block (upstream, no staged source):
  skills/ui-ux-pro-max/SKILL.md ..................... A, C1 (type-scale step)
  skills/make-interfaces-feel-better/SKILL.md ....... A
  skills/motion-foundations/SKILL.md ................ A
  skills/motion-patterns/SKILL.md ................... A
  skills/motion-advanced/SKILL.md ................... A
  skills/orch-build-mvp/SKILL.md .................... A (design-package rule), R1 (step 6), D1 (step 6, step 9)

Hallmark placement note: references/hallmark/references/gates.md is staged
VERBATIM from upstream Nutlope/hallmark v2.0.0 -- it is NOT edited.
hallmark-floor.md is plugin-authored (condensed for this plugin from upstream
SKILL.md + gates.md section 3, per PROVENANCE.md), so the block goes there.

Every substitution asserts count==1. A preflight pass checks every anchor
before any file is written, so a bad anchor aborts before touching anything.
"""
import os
import shutil

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

TASTE = os.path.join(PLUGIN, "new-skills/design-taste-frontend/SKILL.md")
FLOOR = os.path.join(PLUGIN, "new-skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md")
ORCH = os.path.join(PLUGIN, "new-skills/orchestrate/SKILL.md")
POLISH = os.path.join(PLUGIN, "round2-skills/polish-pass/SKILL.md")
LESSFLAT = os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md")

CANONICAL = """**Element variety, all theme-matched.** Every build applies design elements across a wide variety of kinds — treatments, moments, effects, diagrams, components, motion, and type moments — never all of one kind: a build whose new elements are all one kind has not met this rule. Every element, of whatever kind, must match the dealt theme (its material, tokens, palette balance, and do-nots): theme-match is a precondition, not a preference — an element that clashes with the theme is not applied, and the reason is recorded in `docs/design-tokens.md` with the element. Every element application is recorded per surface in `docs/design-tokens.md` (surface → elements applied, kind, theme-fit)."""

D1_RULE = """**Screenshot QA at least once before finish (fix #15 D1).** Before the final report is written, the build runs a screenshot QA pass at least once: the rendered page/app is inspected in screenshots (desktop + mobile) for whitespace, sizing, spacing, alignment, overflow, and collisions. The pass counts toward the requirement from whichever existing tooling ran it (Taste shoot.mjs / check.mjs / consistency.mjs, polish-pass before/after verification, or browser-qa's visual loop) — do not run a duplicate pass to satisfy it; record the run (tool, screens, findings count) in the run ledger and the final report. A build that never ran a screenshot QA pass is incomplete and cannot be reported as finished. Findings feed the fix batch like other checks; browser-qa alone issues pass/fail verdicts on rendered screens."""

# --- staged-source appends: (path, old-anchor, addition) -------------------
# Addition is appended directly after the anchor (anchor kept verbatim).
STAGED_SUBS = [
    # -- Taste (design-taste-frontend) --
    (TASTE,
     "whose visual-loop verdict alone decides whether the hero passes the distinctiveness bar, even if every other check passes.",
     "\n\n" + CANONICAL),
    # R2: diagrams 0-2 -> 1-2 by default on software pages (first column only).
    (TASTE,
     "| Diagram cards (hub, lanes, pulses) | `assets/diagrams` | 0-2, pulsing | 0-2, pulsing | 0-1, still | - | `diagrams.md` |",
     ""),  # placeholder, replaced below (this is a replacement, not an append)
    # R1, step 4: every dealt moment applied or re-dealt.
    (TASTE,
     "The Hallmark Floor binds the page: read `references/hallmark/references/hallmark-floor.md` (16 non-waivable rules + the 6-axis pre-emit critique) and follow it; where it and this skill disagree, the stricter ban wins.",
     "\n\n   **Every dealt moment is applied or re-dealt (fix #15 R1 — baseline: iris-opens was dealt and never applied).** The build record in `docs/design-tokens.md` must list one application per dealt moment, or a re-deal log entry with reason. A dealt moment with neither is an incomplete build — a static check item in step 6 below, never a screen verdict."),
    # R5, step 4a: Range pattern's named lead element is its own element.
    (TASTE,
     "If the two diverge, this frozen landing system wins; do not re-derive a competing system.",
     " **Each Range pattern's named lead element is its own element (fix #15 R5 — baseline: the Bento lead tile's lone figure was folded into the tile, not counted).** When a theme Range pattern names a lead/hero element (e.g. Sticker's Bento \"the lead tile carries the lone figure\"), that element is recorded as its own type moment in `docs/design-tokens.md`, distinct from the surface carrying it."),
    # C1 + C2, step 4a Typography line: dealt faces only; self-host display faces.
    (TASTE,
     "**typography + type scale** (the dealt pairing and tokens, `system.md` Type);",
     " The dealt pairing is the ONLY permitted faces on the build — no other face is introduced — and the pairing + its source are recorded in `docs/design-tokens.md` (fix #15 C1). Display faces are self-hosted (bundled woff2 + `@font-face` in the built page) whenever the face's character matters — the closest installed font is a failure, not a fallback; body faces name their source (self-hosted or link) and fallback stack in `docs/design-tokens.md` (fix #15 C2). This is a required build step, not a recommendation; checkable: the built page contains `@font-face` for the display face, and the tokens file names the source."),
    # R4, step 5: dealt hero's loop implemented or waived.
    (TASTE,
     "Copy the hero's tile from `shoot.mjs` beside the page as `share.jpg`.",
     " **The dealt hero's loop is implemented or waived (fix #15 R4 — baseline: the centred-hero spec's loop inside the window was never applied).** The dealt hero's loop (or moment-inside-window) is implemented and recorded in `docs/design-tokens.md`, or waived with reason there."),
    # R1 step-6 static check + C3, step 6: copy + type checks recorded.
    (TASTE,
     "screenshot against the checklist.",
     " Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1). **Copy + type checks enforced and recorded (fix #15 C3).** Taste copy-voice rules apply to ALL copy; craft-floor type checks (body measure 65–75ch, obvious scale/weight steps, balanced headings, contrast 4.5:1 / 3:1 large) are verified per surface and recorded in `docs/design-tokens.md`'s Type list (surface → face/size/measure/contrast)."),
    # D1, step 6 -- a REPLACEMENT (see REPLACEMENTS below): the D1 rule goes
    # BEFORE the Hallmark sloplint paragraph, not after its heading.
    # -- Hallmark floor (plugin-authored; gates.md verbatim upstream, untouched) --
    (FLOOR,
     "count does not match v2.0.0.)",
     "\n\n" + CANONICAL),
    # -- orchestrate --
    (ORCH,
     "Small changes, one-prompt changes, redesigns, UI fixes, and removal flows that rebuild a surface are UI slices under this rule — they record the direction in the decision record / run ledger (the lightest-weight record that exists for that flow) and run the applicable package components. No UI slice builds on an unstated direction.",
     "\n\n" + CANONICAL),
    # D1, step 5 finish.
    (ORCH,
     "Record each Verification-stage check's outcome as one line (check name, findings count, fixed/blocked counts) in `docs/run-ledger-appendix.md`, with a one-line pointer (check count + file) in `.hackathon/run-ledger.md`, before proceeding to polish.",
     "\n\n   " + D1_RULE),
    # R1 static check, step 5a Verify.
    (ORCH,
     "   - **5a. Verify** — the Verification stage (expansion Phase 5 runs here: the expansion checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature, after the MVP is built).",
     " Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1)."),
    # D1, step 6 final report.
    (ORCH,
     "then write the final report — orchestrate owns it; see the concluding step at the end of this skill.",
     " The final report names the screenshot QA pass (tool, screens, findings count) — a build that never ran a screenshot QA pass is incomplete and cannot be reported as finished (fix #15 D1)."),
    # -- polish-pass --
    (POLISH,
     "## Lenses\n\nEach Lens has a playbook in `reference/lenses/`. Read a Lens's file before applying it.",
     "## Lenses\n\nEach Lens has a playbook in `reference/lenses/`. Read a Lens's file before applying it.\n\n" + CANONICAL),
    # C3: harmony check verifies the Type list (consistency only).
    (POLISH,
     "and record per-screen consistency (consistent / diverges, with the tokens cited) in the report under \"Harmony check\".",
     " The harmony check also verifies the Type list in `docs/design-tokens.md` (surface → face/size/measure/contrast): a surface whose type does not trace to the recorded pairing/scale is a harmony divergence, recorded as candidate evidence, never a verdict (fix #15 C3 — consistency only)."),
    # D1, Capture and verification -- a REPLACEMENT (see REPLACEMENTS below):
    # the D1 rule goes BEFORE the Capture sentence, not after it.
    # -- less-flat-ui (standalone source of truth) --
    # R3: two distinct treatment kinds per app screen.
    (LESSFLAT,
     "Never skip the check because a surface is small.",
     " On app/dashboard surfaces, at least TWO DISTINCT treatment kinds must be recorded per screen, or \"none — <reason>\" per untreated surface (fix #15 R3 — baseline: 2 treatment applications, both Soft Shadow, one kind). The second kind must be theme-matched (rule A governs the choice) — do not hard-code which kind, only that a second distinct kind is required."),
    (LESSFLAT,
     "never over the hero, dealt moments, or shader scenes. A flat-colour section IS part of the page system — do not texture it.",
     "\n\n" + CANONICAL),
]

# The R2 row is a REPLACEMENT (old -> new), not an append. Handle separately.
R2_OLD = "| Diagram cards (hub, lanes, pulses) | `assets/diagrams` | 0-2, pulsing | 0-2, pulsing | 0-1, still | - | `diagrams.md` |"
R2_NEW = "| Diagram cards (hub, lanes, pulses) | `assets/diagrams` | 1-2 by default, pulsing; 0 only with a recorded reason in the section plan | 0-2, pulsing | 0-1, still | - | `diagrams.md` |"

# Prepend-style replacements (old -> new, full text): the D1 rule goes BEFORE
# its anchor paragraph, so an append would put it after the anchor line
# (and, for polish-pass, duplicate the anchor sentence). These run before the
# appends in main().
REPLACEMENTS = [
    # D1, Taste step 6: before the Hallmark sloplint paragraph.
    (TASTE,
     "   **Hallmark sloplint.** Before the report, run the Hallmark gate checker on the built page:",
     "   " + D1_RULE + "\n\n   **Hallmark sloplint.** Before the report, run the Hallmark gate checker on the built page:"),
    # D1, polish-pass Capture and verification: before the Capture sentence.
    (POLISH,
     "## Capture and verification\n\nA **Capture** is screenshots across the **Capture Matrix**: {light, dark} × {desktop 1440×900, mobile 390×844}.",
     "## Capture and verification\n\n" + D1_RULE + "\n\nA **Capture** is screenshots across the **Capture Matrix**: {light, dark} × {desktop 1440×900, mobile 390×844}."),
]

# --- build.sh patch subs (against the BUILT tree): (rel, old, addition) ------
# All are appends: new = old + addition.
BUILD_SUBS = [
    ("skills/ui-ux-pro-max/SKILL.md",
     "Only `browser-qa`'s pass/fail verdict on the rendered screen decides whether the surface fails for having nothing memorable — this skill never states a screen pass/fail.",
     "\n\n" + CANONICAL),
    ("skills/ui-ux-pro-max/SKILL.md",
     "the same 10 items `design-taste-frontend` step 4a defines (that step is the canonical item list).",
     " The dealt pairing / type scale is the ONLY permitted faces on the build — no other face is introduced; record the pairing + its source in `docs/design-tokens.md` (fix #15 C1)."),
    ("skills/make-interfaces-feel-better/SKILL.md",
     "Source: salvaged from stale community PR #1659 by `linus707`.",
     "\n\n" + CANONICAL),
    ("skills/motion-foundations/SKILL.md",
     "Responsiveness always outranks smoothness. A 60 fps animation that causes\ninput delay is worse than no animation.",
     "\n\n" + CANONICAL),
    ("skills/motion-patterns/SKILL.md",
     "- `layout` is used only for small, isolated shifts. Large subtrees get explicit transforms.",
     "\n\n" + CANONICAL),
    ("skills/motion-advanced/SKILL.md",
     "- Motion values (`useMotionValue`, `useSpring`) are SSR-safe and do not cause hydration errors.",
     "\n\n" + CANONICAL),
    ("skills/orch-build-mvp/SKILL.md",
     "The GAN evaluator does NOT judge screen distinctiveness: its Design Quality / Originality rows defer to browser-qa (see `gan-style-harness`).",
     "\n\n" + CANONICAL),
    # D1, standalone step 6 Verify.
    ("skills/orch-build-mvp/SKILL.md",
     "expansion Phase 5 checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature, after the MVP is built.",
     " " + D1_RULE),
    # R1 static check, standalone step 6.
    ("skills/orch-build-mvp/SKILL.md",
     "Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on.",
     " Static check, not a screen verdict: every dealt moment has one application or a re-deal log entry in `docs/design-tokens.md` — a dealt moment with neither is an incomplete build (fix #15 R1)."),
    # D1, standalone step 9 final report.
    ("skills/orch-build-mvp/SKILL.md",
     "Write it to `docs/final-report.md` in the project AND deliver it as the reply.",
     " The final report names the screenshot QA pass (tool, screens, findings count) — a build that never ran a screenshot QA pass is incomplete and cannot be reported as finished (fix #15 D1)."),
]


def build_sh_block():
    """The fix15 patch block appended to build.sh (before STEP 5)."""
    lines = []
    lines.append("# --- fix15: variety + theme-match rule (SPEC section A), count-moving rules R1-R5, fonts/text C1-C3, screenshot QA D1 ---")
    lines.append("# (skills/ui-ux-pro-max, make-interfaces-feel-better, the motion-* skills and orch-build-mvp are upstream;")
    lines.append("#  they have no staged source and are patched here. The staged-source halves -- design-taste-frontend,")
    lines.append("#  orchestrate, polish-pass, less-flat-ui, hallmark-floor.md -- are applied by fix15/fix15.py to their")
    lines.append("#  sources. All anchors were verified count==1 against the post-fix14 built tree by fix15.py's preflight;")
    lines.append("#  the asserts below re-verify at build time and fail the build loudly on mismatch.)")
    lines.append("# Placement: LAST, just before STEP 5 (after the fix13j block).")
    lines.append("python3 - \"$PLUGIN_DIR\" <<'PYEOF'")
    lines.append("import os, sys")
    lines.append("base = sys.argv[1]")
    lines.append("")
    lines.append("CANONICAL = r'''" + CANONICAL + "'''")
    lines.append("")
    lines.append("D1_RULE = r'''" + D1_RULE + "'''")
    lines.append("")
    lines.append("subs = [")
    for rel, old, add in BUILD_SUBS:
        lines.append("  (%s," % (repr(rel),))
        lines.append("   r'''%s'''," % old)
        if add.startswith("\n\n"):
            lines.append("   \"\\n\\n\" + CANONICAL),")
        else:
            lines.append("   %s)," % repr(add))
    lines.append("]")
    lines.append("for rel, old, add in subs:")
    lines.append("    p = os.path.join(base, rel)")
    lines.append("    t = open(p).read()")
    lines.append("    n = t.count(old)")
    lines.append("    assert n == 1, f\"fix15 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})\"")
    lines.append("    open(p, \"w\").write(t.replace(old, old + add))")
    lines.append("print(\"fix15 upstream block applied\")")
    lines.append("PYEOF")
    lines.append("")
    return "\n".join(lines) + "\n"


def preflight():
    """Check every anchor count==1 before writing anything."""
    # Staged-source anchors.
    grouped = {}
    for path, old, add in STAGED_SUBS:
        if add == "":
            continue  # R2 placeholder, checked separately
        grouped.setdefault(path, []).append(old)
    grouped.setdefault(TASTE, []).append(R2_OLD)
    for path, old, new in REPLACEMENTS:
        grouped.setdefault(path, []).append(old)
    for path, olds in grouped.items():
        text = open(path, encoding="utf-8").read()
        for old in olds:
            n = text.count(old)
            assert n == 1, f"PREFLIGHT {path}: anchor count={n}: {old[:70]!r}"
    # Build-sh patch anchors against the current built tree.
    for rel, old, add in BUILD_SUBS:
        p = os.path.join(BUILT, rel)
        text = open(p, encoding="utf-8").read()
        n = text.count(old)
        assert n == 1, f"PREFLIGHT built {rel}: anchor count={n}: {old[:70]!r}"
    # Build.sh insertion anchor.
    btext = open(BUILD_SH, encoding="utf-8").read()
    assert btext.count("# STEP 5 — Counts") == 1, "PREFLIGHT build.sh: STEP 5 anchor"
    assert "fix15 upstream block applied" not in btext, "PREFLIGHT build.sh: fix15 block already present"
    print(f"preflight OK: {sum(len(v) for v in grouped.values())} staged anchors + "
          f"{len(BUILD_SUBS)} built-tree anchors + build.sh insertion anchor")


def main():
    preflight()

    # 1. Staged-source edits (R2 replacement + prepend replacements first, then appends).
    by_path = {}
    for path, old, add in STAGED_SUBS:
        if add == "":
            continue
        by_path.setdefault(path, []).append((old, add))
    # R2 replacement on TASTE.
    text = open(TASTE, encoding="utf-8").read()
    assert text.count(R2_OLD) == 1
    text = text.replace(R2_OLD, R2_NEW)
    open(TASTE, "w", encoding="utf-8").write(text)
    print("Taste: R2 diagram row 0-2 -> 1-2 by default (software column)")
    # Prepend-style replacements (D1 before its anchor paragraph).
    for path, old, new in REPLACEMENTS:
        text = open(path, encoding="utf-8").read()
        assert text.count(old) == 1, f"{path}: replacement anchor not found exactly once: {old[:70]!r}"
        open(path, "w", encoding="utf-8").write(text.replace(old, new))
        print(f"{os.path.relpath(path, PLUGIN) if path.startswith(PLUGIN) else path}: D1 prepend replacement applied")
    for path, subs in by_path.items():
        text = open(path, encoding="utf-8").read()
        for old, add in subs:
            assert text.count(old) == 1, f"{path}: anchor not found exactly once: {old[:70]!r}"
            text = text.replace(old, old + add)
        open(path, "w", encoding="utf-8").write(text)
        print(f"{os.path.relpath(path, PLUGIN) if path.startswith(PLUGIN) else path}: {len(subs)} substitutions applied")

    # 2. Backup build.sh (keep the first pre-fix15 copy).
    backup = os.path.join(PLUGIN, "build.sh.before-fix15")
    if not os.path.exists(backup):
        shutil.copy2(BUILD_SH, backup)
        print("build.sh backup saved to build.sh.before-fix15")
    else:
        print("build.sh.before-fix15 already exists, kept")

    # 3. Append the fix15 block to build.sh before STEP 5.
    btext = open(BUILD_SH, encoding="utf-8").read()
    block = build_sh_block()
    assert btext.count("# STEP 5 — Counts") == 1
    btext = btext.replace("# STEP 5 — Counts", block + "# STEP 5 — Counts", 1)
    open(BUILD_SH, "w", encoding="utf-8").write(btext)
    print(f"build.sh: fix15 block appended ({len(BUILD_SUBS)} upstream subs, "
          f"{len(block.splitlines())} lines)")


if __name__ == "__main__":
    main()
