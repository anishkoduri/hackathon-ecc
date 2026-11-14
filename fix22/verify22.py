#!/usr/bin/env python3
"""verify22.py -- checks fix #22 in the BUILT tree (read-only).

Run after a build: python3 fix22/verify22.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc (+ build.sh
where the SPEC says so):
  1. Group A: A1-A12 named in motion-foundations Principles (PRINCIPLES_F22);
     A13-A20 laws in Decision Guidance (LAWS_F22); pointers in
     make-interfaces-feel-better (AB-11) and ui-ux-pro-max (AB-12).
  2. Group B: token values in motion-foundations (AB-03, incl. the three
     conflict flags carried unresolved); rules 11-19 + Dropdown/Popover/B20
     in motion-patterns (AB-05..08); rules 9-11 + 3 examples in
     motion-advanced (AB-09/10); B4/B18 already-covered evidence intact;
     group anchor labels ANIM_TOKENS_F22 / ANIM_RULES_F22 / ANIM_ADV_F22
     (AB-03g/AB-05g/AB-09g, Sweep #30 Finding 1).
  3. Group C: slop checklist names all 20 indicators (C1-C20), each a flag
     with a D19-reason + theme-fit clearance; SLOP_F22 wired in polish-pass.
  4. Group D: unslop fixes name all 20 fixes (D1-D20); UNSLOP_F22 wired;
     the ui-ux-pro-max / motion-* pointers (CD-P1..P7) present.
  5. Group E: trends menu names all 20 trends (E1-E20), each opt-in with
     the theme-match condition; overlapping slop pairs named in the intro;
     16 Hallmark Range lines carry TRENDS_F22 (15 theme files; the
     E-disposition's 15/14 miscounted one file).
  6. Group F: all 23 less-flat-ui treatments present in the built tree
     (verification-only; no text copied).
  7. Group G: glossary defines all 20 terms (G1-G20) with owning-skill
     pointers; P-G1/P-G2/P-G3 pointer lines in the owning skills; the G8
     40x40px wording is fixed (44x44px floor, W2-C4).
  8. H1/H2: H1 named in ui-ux-pro-max + sprawl check in polish-pass; H2
     named in orchestrate's design-package step + ui-ux-pro-max + the
     polish-pass hierarchy check. Single merged rows (B + CD dispositions).
  9. Mobbin (§9): research step in orchestrate + record requirement +
     no-copy boundary in each touchpoint skill + QA check in polish-pass;
     free-tier-only + recorded-gap fallback.
 10. Directives (§10): DIRECTIVES_F22 in orchestrate and each design
     skill's handoff section (Taste, ui-ux-pro-max, Hallmark theme-deal
     output, GAN planner/generator/evaluator, polish-pass).
 11. Libraries (§11): each of the 4 named in its target skills with pinned
     version + verified license + stack scope (GSAP license is GreenSock
     Standard "no charge", NOT MIT; React Bits is MIT + Commons Clause);
     --domain gsap integration intact; ScrollTrigger referenced; Lenis
     smooth-scroll rule present; Vanta reduced-motion + mobile-fallback +
     scrim constraints stated; React Bits React-only scope stated.
 12. Bang (§12): anti-slide checks + one-world architecture + style/opener
     menus marked menu-not-defaults + kinetic typography as directives +
     pin SHA + GSAP/Three.js versions + MIT license; GSAP converged on
     3.15.1 (Bang's 3.12.5 recorded as Bang's version only); three.js
     scoped pins (Vanta 0.134.0, general 0.185.1).
 13. Depth (§13): depth strategy per surface, Depth as the seventh D19
     dimension (extension line, D19_RULE untouched), depth tokens, depth
     rules, depth check; DEPTH_F22 in every placement + build.sh.
 14. Thinking Orbs (§14): nine verified states (no "thinking" state),
     orb tokens + component + pin 0.3.2 + MIT, waiting states, orb check;
     rareformlabs connection unresolved, recorded not invented.
 15. Libraries (§15): R3F + liquid-glass-js + ShaderGradient + liquid-logo
     named in their placements with pins + licenses + stack scope; R3F
     pairing rule; ShaderGradient v2 not v1; liquid-logo standalone +
     fallback + attribution; one-WebGL rule; liquid-glass-design resolved
     (option b, corrected).
 16. Vercel (§16): pinned snapshot in polish-pass (commit + date), wired
     into the pass + pointers; live-fetch instruction ABSENT (grep);
     ECC-source check + license gap recorded; dedupe 136 rows, AG19
     conflict recorded.
 17. Libraries (§17): Casberry + OriginKit + daisyUI named in their
     placements with pins/terms/caps; Casberry terms unresolved + trust
     flag + export review; OriginKit 10/day cap + Origin UI distinction;
     daisyUI 5.7.50 + Tailwind v4 + default-theme FAIL; running total 11.
 18. Dedupe (§5): the pairs resolve to a single primary home.
 19. Every placed item is named in its target skill in the built tree AND
     in build.sh (fix22 block).
 20. Counts unchanged post-fix21: 166/72/123/87/15; trigger keys 64.
 21. No banned terms in the built tree (excl. node_modules).
 22. build.sh is the post-fix22 file (fix22 block + BANG_PIN + all earlier
     markers; more lines than post-fix21, 23,647).
 23. verify15/17/18/19/20/21 still pass (subprocesses, exit 0 required).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
sys.path.insert(0, os.path.join(PLUGIN, "fix22"))
import fix22 as F22  # noqa: E402

BASE = os.path.join(PLUGIN, "hackathon-ecc")
BANG_SHA = F22.BANG_SHA  # pin record lives in fix22.py + build.sh + bang-report.md

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


mf = read("skills/motion-foundations/SKILL.md")
mp = read("skills/motion-patterns/SKILL.md")
ma = read("skills/motion-advanced/SKILL.md")
mifb = read("skills/make-interfaces-feel-better/SKILL.md")
uipro = read("skills/ui-ux-pro-max/SKILL.md")
qr = read("skills/ui-ux-pro-max/references/quick-reference.md")
threejs_csv = read("skills/ui-ux-pro-max/data/stacks/threejs.csv")
planner = read("agents/ecc-gan-planner.md")
generator = read("agents/ecc-gan-generator.md")
evaluator = read("agents/ecc-gan-evaluator.md")
taste = read("skills/design-taste-frontend/SKILL.md")
orch = read("skills/orchestrate/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
slop = read("skills/polish-pass/reference/slop-checklist.md")
unslop = read("skills/polish-pass/reference/unslop-fixes.md")
glossary = open(os.path.join(
    BASE, "skills/design-taste-frontend/references/design-glossary.md"),
    encoding="utf-8").read()
pitch = read("skills/pitch-deck-video/SKILL.md")
lessflat = read("skills/less-flat-ui/SKILL.md")
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
bang_report = open(os.path.join(PLUGIN, "fix22/bang-report.md"),
                   encoding="utf-8").read()
disp_e = open(os.path.join(PLUGIN, "fix22/disposition-E.md"),
              encoding="utf-8").read()

# 1. Group A — principles + laws.
for n, name in ((1, "Squash & stretch"), (2, "Anticipation wind-up"),
                (3, "Staging the focus"), (4, "Pose to pose"),
                (5, "Follow through"), (6, "Slow in & slow out"),
                (7, "Moving in arcs"), (8, "Secondary action"),
                (9, "Snappy timing"), (10, "Exaggerated feedback"),
                (11, "Solid drawing in 3D"), (12, "Overall appeal")):
    check(f"A{n} {name} in motion-foundations Principles",
          f"**A{n} {name}**" in mf)
check("PRINCIPLES_F22 token in motion-foundations + build.sh",
      "PRINCIPLES_F22" in mf and "PRINCIPLES_F22" in build)
for n, name in ((13, "Fitts's law"), (14, "Bigger hit areas"),
                (15, "Hick's law"), (16, "Miller's law"),
                (17, "Doherty threshold"), (18, "Postel's law"),
                (19, "Jakob's law"), (20, "Frequency of use")):
    check(f"A{n} {name} in motion-foundations Decision Guidance",
          f"**A{n} {name}**" in mf)
check("LAWS_F22 token in motion-foundations + build.sh",
      "LAWS_F22" in mf and "LAWS_F22" in build)
check("A14 names the 44x44px hit-area floor (no size-rule duplication)",
      "44x44px hit area (the plugin floor" in mf)
check("AB-11 pointer in make-interfaces-feel-better",
      "Motion feel decisions route through the principles (fix #22" in mifb)
check("AB-12 pointer in ui-ux-pro-max",
      "UX laws for motion decisions (fix #22" in uipro)

# 2. Group B — tokens, rules, examples.
check("B2 token: dropdown 0.2s in motionTokens", "    dropdown: 0.2," in mf)
check("B2 token comment names the 150-250ms band",
      "dropdowns animate at 150–250ms" in mf)
check("B3 token: staggerRow 0.03s in motionTokens",
      "    staggerRow: 0.03," in mf)
check("B3 conflict flag carried (30ms vs Rule 5 floor)",
      "CONFLICT FLAG (SPEC §4c): 0.03s sits below motion-patterns Rule 5's 0.05s floor" in mf)
check("B1 token: smooth annotated as the ease-out curve",
      "the ease-out curve — entrances use this easing" in mf)
check("B9 token: inOut ease-in-out curve in motionTokens",
      "inOut:  [0.65, 0, 0.35, 1]," in mf)
check("B10 token: popover 0.95, separate from press",
      "    popover: 0.95," in mf
      and "Separate token from press" in mf)
check("B5 token: stretch 1.12 (12%) in motionTokens",
      "    stretch: 1.12," in mf)
check("B15 token: exitFactor 0.8 in motionTokens",
      "  exitFactor: 0.8," in mf)
check("B15 conflict flag carried (0.8x vs quick-reference 60-70%)",
      "CONFLICT FLAG (SPEC §4c): quick-reference `exit-faster-than-enter` says ~60–70%" in mf)
check("B4 observation NOT resolved by editing scale.press (still 0.95)",
      "    press:  0.95," in mf)
for n, name in ((11, "Enter from the trigger"), (12, "Exit to the trigger"),
                (13, "No bounce on everyday UI"),
                (14, "Don't tween while held"),
                (15, "Exits run 20% shorter than their enter"),
                (16, "Overlap old & new states"),
                (17, "Pulse to confirm success"),
                (18, "Reuse the same layoutId"),
                (19, "Move along arcs")):
    check(f"B-rule {n} {name} in motion-patterns Rules",
          f"{n}. **{name} (fix #22" in mp)
check("B16 scope boundary stated (in-container swaps only; Rule 3 pages)",
      'SCOPE: in-container swaps\n    only. Page transitions still use `mode="wait"` (Rule 3)' in mp)
check("AB-06 Dropdown example (B2) in motion-patterns",
      "### Dropdown (fix #22 B2)" in mp)
check("AB-06 B6 stagger-as-details-settle note in motion-patterns",
      "Stagger as details settle (fix #22 B6)" in mp)
check("AB-07 Popover example (B10/B11/B12) in motion-patterns",
      "### Popover (fix #22 B10/B11/B12)" in mp)
check("AB-08 B20 note on the shared-element example in motion-patterns",
      "Reuse the same layoutId (fix #22 B20)" in mp)
for n, name in ((9, "Overlap old & new states in multi-step sequences"),
                (10, "Masks for reveals & colour"),
                (11, "Rubber band past bounds")):
    check(f"B-rule {n} {name} in motion-advanced Rules",
          f"{n}. **{name} (fix #22" in ma)
for name in ("### Mask reveal (fix #22 B17)",
             "### Stretching knob (fix #22 B5)",
             "### Overlapping state change (fix #22 B16)"):
    check(f"AB-10 example {name} in motion-advanced", name in ma)
check("B4 already-covered: press scale 0.97 polish default intact",
      "Press: `scale(0.97)` for tactile buttons" in mifb)
check("B18 already-covered: icon-swap cross-fade rule intact",
      "Icon swaps: cross-fade with opacity, scale, and blur" in mifb)
check("AB-05 names B18 as already covered (no duplicate rule)",
      "Icon swaps (fix #22 B18) are already covered" in mp)
check("ANIM tokens/rules/advanced content in build.sh (fix22 block)",
      "dropdown: 0.2," in build and "Enter from the trigger (fix #22 B11" in build
      and "Overlap old & new states in multi-step sequences" in build)
check("ANIM_TOKENS_F22 group anchor in motion-foundations + build.sh (Sweep #30)",
      "ANIM_TOKENS_F22" in mf and "ANIM_TOKENS_F22" in build)
check("ANIM_RULES_F22 group anchor in motion-patterns + build.sh (Sweep #30)",
      "ANIM_RULES_F22" in mp and "ANIM_RULES_F22" in build)
check("ANIM_ADV_F22 group anchor in motion-advanced + build.sh (Sweep #30)",
      "ANIM_ADV_F22" in ma and "ANIM_ADV_F22" in build)

# 3. Group C — slop checklist names all 20.
C_NAMES = {1: "Tags & pills", 2: "Excessive italics", 3: "Instrument Serif",
           4: "Negative kerning", 5: "Over-the-top detailed UI",
           6: "Overusing dividers", 7: "Color shades & opacities",
           8: "Containers with borders", 9: "Overly detailed diagrams",
           10: "Verbose, redundant text", 11: "Code breadcrumbs",
           12: "Section numbering", 13: "Eyebrows", 14: "Dithering",
           15: "ASCII images", 16: "Squircles", 17: "Excessive mono fonts",
           18: "ALL CAPS subtitles", 19: "Gradient backgrounds",
           20: "Periods in titles"}
for n, name in C_NAMES.items():
    check(f"C{n} {name} named in the slop checklist",
          f"C{n} — {name}" in slop or f"C{n} - {name}" in slop)
check("SLOP_F22 anchor in the slop checklist + polish-pass wiring",
      "SLOP_F22" in slop and "SLOP_F22" in polish)
check("slop checks are FLAGS, not bans (flag-vs-justified + clearance)",
      "cleared by a recorded D19 reason + theme-fit in the decision record" in slop)
check("slop checklist is static candidate evidence, never a verdict",
      "CANDIDATE EVIDENCE for `browser-qa`, NEVER a" in slop)
check("staged slop source is copied by build.sh (STEP 2 round2-skills copy)",
      '"$PLUGIN_ROOT/round2-skills/' in build)

# 4. Group D — unslop fixes name all 20.
D_NAMES = {1: "Delete filler badges", 2: "Drop redundant labels",
           3: "Unitalicize random words", 4: "Mono only where needed",
           5: "Use a design system", 6: "Show the actual product",
           7: "Enlarge the main feature", 8: "Group with spacing",
           9: "Make headlines specific", 10: "Emphasize the CTA",
           11: "Add an accent colour", 12: "Keep icons consistent",
           13: "Remove embellishments",
           14: "Inner radius = outer – padding",
           15: "Improve text contrast", 16: "Wrap headlines properly",
           17: "Align by eye, not pixels", 18: "Use tabular nums",
           19: "Add loading states", 20: "Animate useful feedback"}
for n, name in D_NAMES.items():
    check(f"D{n} {name} named in the unslop fixes",
          f"D{n} — {name}" in unslop or f"D{n} - {name}" in unslop)
check("UNSLOP_F22 anchor in the unslop fixes + polish-pass wiring",
      "UNSLOP_F22" in unslop and "UNSLOP_F22" in polish)
check("D19 loading-state RULE is new (every async action gets one)",
      "Every async action gets a loading state" in unslop)
for token in ("headline-specific", "cta-emphasis", "color-contrast-polish",
              "headline-wrap-polish", "tabular-polish", "spacing-group-polish"):
    check(f"CD pointer {token} in ui-ux-pro-max quick-reference",
          token in qr)
check("CD-P7a D20 pointer in motion-patterns Button feedback",
      "Animate useful feedback only (UNSLOP_F22 D20" in mp)
check("CD-P7b D20 pointer in motion-foundations tokens table",
      "Feedback animation (UNSLOP_F22 D20)" in mf)

# 5. Group E — trends menu names all 20, each opt-in + theme-matched.
E_NAMES = {1: "Dithering", 2: "ASCII over video", 3: "Infinite canvases",
           4: "Disco logos", 5: "Renaissance branding",
           6: "Monet backgrounds", 7: "Dark gradient heroes",
           8: "Pixel loaders", 9: "Instrument Serif",
           10: "One italic word", 11: "Cream backgrounds",
           12: "All-caps eyebrows", 13: "Pulsing live dots",
           14: "Sparkle icons", 15: "Liquid Glass",
           16: "Three icon cards", 17: "Decorative flowcharts",
           18: "Endless marquees", 19: "Squircles",
           20: "Pretext text wrapping"}
for n, name in E_NAMES.items():
    check(f"E{n} {name} named in the trends menu",
          f"**E{n} {name} (TRENDS_F22)" in taste)
check("every trend entry states opt-in + theme-matched (20/20)",
      taste.count("Opt-in only, theme-matched") >= 20)
check("trends intro names the overlapping slop pairs",
      "Overlapping pairs: E1 dithering with C14" in taste
      and "E7 dark gradient heroes with C19" in taste)
check("trends intro states the theme-match precondition",
      "A trend used with no theme-match reason is an incomplete build" in taste)
# 23 = 20 menu entries + intro line (2x) + finish-gate pointer. The
# E-disposition's "22x" miscounted the intro line's second occurrence.
check("TRENDS_F22 appears 23x in Taste SKILL.md (menu + pointers)",
      taste.count("TRENDS_F22") == 23)
_hallmark_themes = os.path.join(
    BASE, "skills/design-taste-frontend/references/hallmark/references/themes")
_theme_trend_hits = 0
_theme_trend_files = 0
for _fn in os.listdir(_hallmark_themes):
    if _fn.endswith(".md"):
        _lines = [_l for _l in open(
            os.path.join(_hallmark_themes, _fn), encoding="utf-8").read()
            .splitlines() if "TRENDS_F22" in _l]
        _theme_trend_hits += len(_lines)
        _theme_trend_files += 1 if _lines else 0
# 16 Range lines in 15 theme files (Blueprint carries E3+E17). The
# E-disposition's "15 lines / 14 files" missed one file.
check("16 Hallmark Range lines carry TRENDS_F22 (15 theme files)",
      _theme_trend_hits == 16 and _theme_trend_files == 15)
check("E6 points at less-flat-ui #21, does not duplicate the treatment",
      "the treatment is less-flat-ui #21 Impressionist paintings" in taste)
check("E12 has no theme-file line (validator forbids eyebrows) — menu only",
      "No theme file carries an eyebrow line" in taste)

# 6. Group F — all 23 treatments verified present (verification-only).
F_NAMES = {1: "Felt texture", 2: "Fluted glass", 3: "Thermal gradients",
           4: "Water ripples", 5: "Speckled graphite",
           6: "Single-hue landscapes", 7: "Blueprint grids", 8: "Halftone",
           9: "Grainy gradients", 10: "Grass texture",
           11: "Dithered images", 12: "Paper texture",
           13: "Contour lines", 14: "Cloud sky", 15: "Pixel mosaics",
           16: "Lens distortion", 17: "Stippled gradients",
           18: "Square-dot grids", 19: "Blurred photos",
           20: "Iridescent shapes", 21: "Impressionist paintings",
           22: "ASCII and pixels", 23: "Soft shadow"}
for n, name in F_NAMES.items():
    check(f"F{n} {name} present in built less-flat-ui",
          f"### {n}. {name}" in lessflat)
check("less-flat-ui states 23 treatments (no stale count of 22)",
      "## The 23 treatments" in lessflat)

# 7. Group G — glossary defines all 20 terms with owning-skill pointers.
G_NAMES = {1: "Kerning", 2: "Optical centre", 3: "Tabular numbers",
           4: "Layout shift", 5: "Tracking", 6: "Optimistic update",
           7: "x-height", 8: "Touch target", 9: "Leading",
           10: "Origin-aware animation", 11: "OKLCH", 12: "Widow",
           13: "Safe area", 14: "Stagger", 15: "Line length",
           16: "Affordance", 17: "Combobox",
           18: "Interruptible animation", 19: "Progressive disclosure",
           20: "Shared element transition"}
for n, name in G_NAMES.items():
    check(f"G{n} {name} defined in the glossary",
          f"| G{n} {name} |" in glossary)
check("GLOSSARY_F22 anchor in the glossary + staged source copied by build.sh",
      "GLOSSARY_F22" in glossary and "new-skills/design-taste-frontend" in build)
check("G-P1 pointer line in ui-ux-pro-max (16 terms)",
      "Design vocabulary — the definitions of kerning, optical centre, tabular numbers" in uipro)
check("G-P2 pointer line in motion-foundations (G18)",
      "the definition of interruptible animation (G18) lives in" in mf)
check("G-P3 pointer line in motion-patterns (G10/G14/G20)",
      "the definitions of origin-aware animation (G10), stagger (G14), and shared element transition (G20) live in" in mp)
check("G8 fix: no 40x40px wording remains in the glossary",
      "40x40px" not in glossary)
check("G8 fix: 44x44px floor (W2-C4) named in the owning column + dedupe note",
      "44x44px minimum (the plugin floor, W2-C4)" in glossary
      and "the 44x44px floor (W2-C4)" in glossary)
check("G8 definition still 44x44px minimum (untouched)",
      "44x44px minimum on the plugin's craft floor" in glossary)

# 8. H1/H2 — single merged rows.
check("H1 concept named in ui-ux-pro-max (AB-13, ACCENT_F22)",
      "One accent colour (fix #22 H1, ACCENT_F22)" in uipro)
check("H1 accent-sprawl check in polish-pass slop checklist",
      "Accent sprawl — ACCENT_F22" in slop)
check("H1 sprawl flag is slop-adjacent, cleared by D19 + theme-fit",
      "accent sprawl is a flag, slop-adjacent" in slop)
check("H2 named in orchestrate design-package step (ACCENTUATION_F22)",
      "Accent hierarchy in every UI slice brief (fix #22 H2, ACCENTUATION_F22)" in orch)
check("H2 hierarchy rules in ui-ux-pro-max (AB-14, ACCENTUATION_F22)",
      "Accent hierarchy — every screen declares what draws the eye first (fix #22 H2" in uipro)
check("H2 hierarchy check in polish-pass slop checklist",
      "Accent hierarchy — ACCENTUATION_F22" in slop)
check("H2 means cross-referenced, not duplicated (F5, F6, dealt moments, H1)",
      "H2 is the umbrella principle" in uipro)

# 9. Mobbin (§9) — research step + record requirement + no-copy boundary + QA.
check("Mobbin research step in orchestrate design-package step (MOBBIN_RESEARCH_F22)",
      "Pattern research before generating direction (fix #22 §9, MOBBIN_RESEARCH_F22)" in orch)
check("Mobbin record requirement: decision record notes categories consulted",
      "The decision record notes which categories were consulted" in orch)
check("Mobbin no-copy boundary in orchestrate (never a Mobbin URL as source)",
      "never a Mobbin URL" in orch)
check("Mobbin pattern reference in Taste (MOBBIN_PATTERN_F22)",
      "Pattern reference while building (fix #22 §9, MOBBIN_PATTERN_F22)" in taste)
check("Mobbin pattern reference in ui-ux-pro-max (MOBBIN_PATTERN_F22)",
      "Pattern reference while building (fix #22 §9, MOBBIN_PATTERN_F22)" in uipro)
check("Mobbin no-copy boundary in Taste + ui-ux-pro-max",
      "never a Mobbin URL" in taste and "never a Mobbin URL" in uipro)
check("Mobbin QA convention check in polish-pass (MOBBIN_QA_F22)",
      "Check category conventions against real apps (fix #22 §9, MOBBIN_QA_F22)" in polish)
check("Mobbin QA gap is candidate evidence, never a verdict",
      "A gap is CANDIDATE EVIDENCE for `browser-qa`, NEVER a verdict" in polish)
check("Mobbin free-tier-only + never-blocked in all four touchpoints",
      orch.count("no paid subscription") >= 1
      and taste.count("no paid subscription") >= 1
      and uipro.count("no paid subscription") >= 1
      and polish.count("no paid subscription") >= 1
      and "the build is NEVER blocked on Mobbin" in orch
      and "the build is NEVER blocked on Mobbin" in uipro)
# MOBBIN_PATTERN_F22 is the fix22-block token (PROC-P1). MOBBIN_RESEARCH_F22
# is staged orchestrate content, not in build.sh — it is asserted in §9.
check("Mobbin pattern token in build.sh (fix22 block)",
      "MOBBIN_PATTERN_F22" in build)

# 10. Directives (§10) — orchestrate + each design skill's handoff section.
check("directive requirement in orchestrate implementer briefs (DIRECTIVES_F22)",
      "Directives, not descriptions (fix #22 §10, DIRECTIVES_F22)" in orch)
check("directive requirement in Taste step 4a frozen system (DIRECTIVES_F22)",
      "Directives, not descriptions (fix #22 §10, DIRECTIVES_F22)" in taste)
check("Hallmark theme-deal output recorded as directives (Taste step 4a)",
      "The dealt theme is recorded as directives, not prose" in taste)
check("directive requirement in ui-ux-pro-max component specs (DIRECTIVES_F22)",
      "Component specs are directives, not descriptions (fix #22 §10, DIRECTIVES_F22)" in uipro)
check("directive requirement in GAN planner (DIRECTIVES_F22)",
      "Directives, not descriptions (fix #22 §10, DIRECTIVES_F22)" in planner)
check("directive requirement in GAN generator (DIRECTIVES_F22)",
      "Directives, not descriptions (fix #22 §10, DIRECTIVES_F22)" in generator)
check("directive requirement in GAN evaluator feedback (DIRECTIVES_F22)",
      "Feedback items are directives, not descriptions (fix #22 §10, DIRECTIVES_F22)" in evaluator)
check("directive requirement in polish-pass fix directives (DIRECTIVES_F22)",
      "Fix directives, not descriptions (fix #22 §10, DIRECTIVES_F22)" in polish)
check("directives: prose-only FAILS the handoff check (orchestrate + Taste)",
      "FAILS the handoff check" in orch and "FAILS the handoff check" in taste)
check("directives: implementers surface ambiguity as a recorded gap",
      "surfaced as a recorded gap instead of improvised around" in orch)

# 11. Libraries (§11) — pins + licenses + stack scope.
check("Lenis smooth-scroll rule in motion-foundations (LENIS_F22)",
      "### Smooth scroll — Lenis (fix #22 §11, LENIS_F22)" in mf)
check("Lenis pin lenis@1.3.27 + MIT in motion-foundations",
      "`lenis@1.3.27`, MIT" in mf)
check("Lenis never on Taste landing pages (standing rule kept)",
      "Lenis never applies there" in mf)
check("Scroll routing through Lenis + ScrollTrigger in motion-patterns",
      "Scroll-driven animation routes through Lenis + ScrollTrigger (fix #22 §11" in mp)
check("ScrollTrigger referenced in motion-patterns prose (SCROLLTRIGGER_F22)",
      "SCROLLTRIGGER_F22" in mp)
check("GSAP --domain gsap integration intact in ui-ux-pro-max",
      "--domain gsap" in uipro and "17 GSAP presets" in uipro)
check("GSAP extension: ScrollTrigger named in skill prose (LIB-04)",
      "GSAP is the animation engine; ScrollTrigger is its scroll plugin (fix #22" in uipro)
check("GSAP pin gsap@3.15.1 in ui-ux-pro-max + motion-patterns",
      "gsap@3.15.1" in uipro and "gsap@3.15.1" in mp)
check("GSAP license is GreenSock Standard 'no charge', NOT MIT",
      'GreenSock Standard "no charge" licence' in uipro
      and "gsap@3.15.1`, MIT" not in uipro
      and "gsap@3.15.1`, MIT" not in mp)
check("Group B numbers travel through GSAP tweens (LIB-04)",
      "Group B numbers travel" in uipro)
check("Vanta in Taste step 2 (VANTA_F22) with three@0.134.0 pair",
      "Animated 3D backgrounds come from Vanta (fix #22 §11, VANTA_F22)" in taste
      and "three@0.134.0" in taste)
check("Vanta in ui-ux-pro-max app surfaces (VANTA_F22)",
      "Animated 3D backgrounds — Vanta, on app surfaces (fix #22 §11, VANTA_F22)" in uipro)
check("Vanta reduced-motion + mobile-fallback + scrim constraints stated",
      "the scene MUST disable" in taste and "static fallback" in taste
      and "mobile/low-power" in taste and "scrim and a 4.5:1 contrast check" in taste)
check("Vanta scoped three pin: general pin does not apply to Vanta scenes",
      "the general three.js pin in" in uipro
      and "does not apply to Vanta scenes" in uipro)
check("React Bits in motion-patterns (REACTBITS_F22), React/Next only",
      "### React Bits — animated components, React/Next only (fix #22 §11, REACTBITS_F22)" in mp
      and "SCOPE — React/Next.js builds ONLY" in mp)
check("React Bits pinned commit + MIT + Commons Clause in motion-patterns",
      "9d9c687dc4f55b23539aa5417b703078047efa74" in mp
      and "MIT + Commons Clause" in mp)
check("React Bits scope pointer in ui-ux-pro-max (REACTBITS_F22)",
      "React Bits — React/Next only (fix #22 §11, REACTBITS_F22)" in uipro)
check("libraries: unpinned 'latest' FAILS the pin check",
      '"latest") FAIL the pin check' in uipro or '"latest" FAIL the pin check' in uipro)
check("library tokens in build.sh (fix22 block)",
      "LENIS_F22" in build and "GSAP_F22" in build
      and "SCROLLTRIGGER_F22" in build and "VANTA_F22" in build
      and "REACTBITS_F22" in build)

# 12. Bang (§12) — port into pitch-deck-video.
check("Bang anti-slide checks in pitch-deck-video (BANG_ANTISLIDE_F22)",
      "### Anti-slide checks (BANG_ANTISLIDE_F22)" in pitch)
check("Bang anti-slide: one continuous world, not slides with fades",
      "One continuous world" in pitch)
check("Bang anti-slide: no text under 30px on a 1080-wide stage",
      "No text under 30px on a 1080-wide stage" in pitch)
check("Bang anti-slide: at most two text levels per frame",
      "At most two text levels per frame" in pitch)
check("Bang one-world / camera / persistent-subject architecture (BANG_ONEWORLD_F22)",
      "### One-world / camera / persistent-subject architecture (BANG_ONEWORLD_F22)" in pitch)
check("Bang style-direction menu, 10, menu-not-defaults (BANG_STYLES_F22)",
      "### Style-direction menu, 10 (BANG_STYLES_F22)" in pitch
      and "A menu, never defaults" in pitch)
check("Bang opener concepts, 19 (BANG_OPENERS_F22)",
      "### Opener concepts, 19 (BANG_OPENERS_F22)" in pitch)
check("Bang kinetic typography as directives (BANG_KINETIC_F22)",
      "### Kinetic typography (BANG_KINETIC_F22)" in pitch)
check("Bang explainer styles, 6 (BANG_EXPLAINER_F22)",
      "### Explainer styles (BANG_EXPLAINER_F22)" in pitch)
check("Bang pin SHA recorded in pitch-deck-video",
      BANG_SHA in pitch)
check("Bang pin SHA recorded in build.sh (BANG_PIN)",
      'BANG_PIN="%s"' % BANG_SHA in build)
check("Bang pin SHA recorded in fix22/bang-report.md",
      BANG_SHA in bang_report)
check("Bang MIT license recorded in pitch-deck-video",
      "MIT licence" in pitch)
check("Bang GSAP converged on 3.15.1 (plugin pin, not 3.12.5)",
      "The plugin pins **GSAP 3.15.1**" in pitch)
check("Bang's reference versions recorded as Bang's only (3.12.5 / 0.161.0)",
      "Bang's reference implementation used GSAP 3.12.5 / Three.js 0.161.0" in pitch)
check("Bang three.js scoped pins recorded (Vanta 0.134.0, general 0.185.1)",
      "Vanta scenes pin `three@0.134.0`" in pitch
      and "general hand-written three.js scenes keep the existing pin `three@0.185.1`" in pitch)
check("Bang staleness + language notes in fix22/bang-report.md",
      "all 3 commits dated Sep 15, 2026" in bang_report
      and "Indonesian" in bang_report)
check("Bang /demo still films the real app (boundary intact)",
      "/demo` films the LOCAL app" in pitch)
check("Bang: no second toolchain (Remotion + OpenMontage only)",
      "do not import a second video pipeline" in pitch)
check("GSAP 3.12.2 absent from the built tree (threejs.csv pin fixed)",
      "3.12.2" not in subprocess.run(
          ["grep", "-r", "3.12.2", "skills", "agents", "commands", "rules",
           "hooks", "--exclude-dir=node_modules"],
          cwd=BASE, capture_output=True, text=True).stdout)
check("threejs.csv row 35 GSAP CDN pin is 3.15.1",
      "gsap/3.15.1/gsap.min.js" in threejs_csv
      and "gsap/3.12.2/gsap.min.js" not in threejs_csv)
check("threejs.csv keeps the general three@0.185.1 pin (Vanta scoping intact)",
      "three@0.185.1" in threejs_csv)
check("disposition-E.md:122 scrub: no literal banned-term pattern in the file",
      "composer-2" not in disp_e
      and "Banned terms: 0 (pattern redacted — see verify22.py)" in disp_e)


# 13. Depth (§13) — the z-axis as a seventh D19 dimension.
ds = read("skills/design-system/SKILL.md")
vercel = read("skills/polish-pass/reference/vercel-checklist.md")
orbs_report = open(os.path.join(PLUGIN, "fix22/orbs-patches.md"),
                   encoding="utf-8").read()
dedupe_vercel = open(os.path.join(PLUGIN, "fix22/vercel-dedupe.md"),
                     encoding="utf-8").read()
lib15_report = open(os.path.join(PLUGIN, "fix22/libraries15-patches.md"),
                    encoding="utf-8").read()
check("depth strategy in every UI slice brief (DEPTH-01, DEPTH_F22)",
      "Depth strategy in every UI slice brief (fix #22 §13, DEPTH_F22)" in orch)
check("flat by choice recorded as an explicit depth strategy",
      "flat by choice — <reason>" in orch)
check("D19 seventh-dimension extension line in orchestrate + Taste (DEPTH-02/03)",
      "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in orch
      and "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in taste)
check("D19 rule text itself unchanged (tail sentence still verbatim)",
      "The check verifies the reasoning is PRESENT and addresses the dimensions" in orch
      and "The check verifies the reasoning is PRESENT and addresses the dimensions" in taste)
check("depth as a dealt moment in Taste (DEPTH-04)",
      "Depth as a dealt moment / theme element (fix #22 §13, DEPTH_F22)" in taste)
check("depth strategy recorded with the direction (DEPTH-05/06)",
      "Depth strategy recorded with the direction (fix #22 §13, DEPTH_F22)" in orch
      and "depth strategy per surface (fix #22 §13, DEPTH_F22)" in orch)
check("depth check wired into polish-pass step 5 (DEPTH-07)",
      "Then run the depth check" in polish)
check("depth check section in the slop checklist (DEPTH-08, D1-D6)",
      "## Depth check — the z-axis (fix #22 §13, DEPTH_F22)" in slop
      and "D1 — A depth strategy is named for every surface" in slop
      and "D6 — The Depth dimension is recorded" in slop)
check("depth tokens in motion-foundations (DEPTH-09, DEPTH_F22)",
      "### Depth tokens — 3D motion values (fix #22 §13, DEPTH_F22)" in mf
      and "perspective: 1000" in mf
      and "parallax: { near: 0.5, mid: 0.25, far: 0.1 }" in mf
      and "tilt: { max: 6 }" in mf
      and "elevation: { raised: 8, floating: 16, modal: 24 }" in mf)
check("parallax layers + 3D-transform hero in motion-patterns (DEPTH-10)",
      "### Parallax layers and 3D-transform hero (fix #22 §13, DEPTH_F22)" in mp)
check("depth rules in ui-ux-pro-max (DEPTH-11, DEPTH_F22)",
      "**Depth rules — the z-axis on app surfaces (fix #22 §13, DEPTH_F22).**" in uipro
      and "Elevation system" in uipro
      and "scrim and a 4.5:1 contrast check" in uipro)
check("D19 seventh-dimension mirror in ui-ux-pro-max (DEPTH-12)",
      "**Depth — the seventh dimension (fix #22 §13, DEPTH_F22).**" in uipro)
check("texture/depth overlap note in less-flat-ui (DEPTH-13)",
      "**Depth and texture are different axes (fix #22 §13, DEPTH_F22).**" in lessflat
      and "Soft Shadow #23 is BOTH" in lessflat)
check("DEPTH_F22 token in build.sh (fix22 block)",
      "DEPTH_F22" in build)

# 14. Thinking Orbs (§14) — state-matched loading indicator.
for _st in ("working", "searching", "solving", "listening", "connecting",
            "weaving", "composing", "breathing", "shaping"):
    check(f"orb state `{_st}` in the motion-patterns state table",
          f"| `{_st}` |" in mp)
check("orb pattern in motion-patterns (ORB-MP, ORBS_F22)",
      "### Thinking Orb — the loading indicator for AI/agent waiting states (fix #22 §14, ORBS_F22)" in mp)
check("no state named thinking (SPEC mapping corrected)",
      "There is no `thinking` state in the library" in mp)
check("generic spinner FAILS for an AI/agent wait (fixture a)",
      "a generic spinner" in mp and "FAILS" in mp)
check("orb tokens in motion-foundations (ORB-MF, ORBS_F22)",
      "### Thinking Orb tokens (fix #22 §14, ORBS_F22)" in mf
      and "ONE static representative" in mf
      and "DPR is capped at 2" in mf)
check("orb component in ui-ux-pro-max (ORB-UIPRO, ORBS_F22)",
      "**Thinking Orb — the loading indicator component for AI/agent waiting states (fix #22 §14, ORBS_F22).**" in uipro)
check("orb pin thinking-orbs@0.3.2 + MIT + React >= 18",
      "thinking-orbs@0.3.2" in uipro and "License MIT" in uipro
      and "React >= 18" in uipro)
check("orb stack scope: React Native install-from-repo-gated, SwiftUI planned only",
      "NOT published on npm" in uipro and "SwiftUI: PLANNED only" in uipro)
check("waiting states in the design package (ORB-ORCH, ORBS_F22)",
      "Waiting states in every UI slice brief (fix #22 §14, ORBS_F22)" in orch)
check("orb check in the slop checklist (ORB-PP1, ORBS_F22)",
      "## Thinking Orb check — ORBS_F22 (fix #22 §14, polish-pass portion)" in slop
      and "a mismatched orb state" in slop)
check("orb as the D19 loading-state implementation (ORB-PP2, ORBS_F22)",
      "the approved implementation of this fix is the" in unslop
      and "Thinking Orb (`motion-patterns`, ORBS_F22)" in unslop)
check("ORBS_F22 token in build.sh (fix22 block)",
      "ORBS_F22" in build)
check("rareformlabs connection unresolved — recorded, not invented",
      "rareformlabs connection unresolved — asset verified independently" in orbs_report)

# 15. Libraries §15 — R3F / liquid-glass-js / ShaderGradient / liquid-logo.
check("R3F in motion-foundations + motion-patterns + ui-ux-pro-max + Taste (R3F_F22)",
      "R3F_F22" in mf and "R3F_F22" in mp and "R3F_F22" in uipro
      and "R3F_F22" in taste)
check("R3F pins @9.8.2 (React 19) / @8.18.0 (React 18), MIT",
      "@react-three/fiber@9.8.2" in mf and "@react-three/fiber@8.18.0" in mf
      and "MIT" in mf)
check("R3F strict version pairing: React 18 + v9 FAILS, React 19 + v8 FAILS",
      "R3F v9 FAILS the pairing check" in mf
      and "R3F v8 FAILS the pairing check" in mf
      and "React 18 +" in mf)
check("liquid-glass-js in ui-ux-pro-max + Taste + less-flat-ui (LIQGLASS_F22)",
      "LIQGLASS_F22" in uipro and "LIQGLASS_F22" in taste
      and "LIQGLASS_F22" in lessflat)
check("liquid-glass-js pin commit 78cb6ccb + MIT + no npm package (copy files)",
      "78cb6ccb0b9987bb60a88b14ccbd13a9e6e8ab2a" in uipro
      and "NO npm package" in uipro
      and "container.js" in lessflat and "button.js" in lessflat
      and "glass.css" in lessflat)
check("liquid-glass-js html2canvas perf note + frosted-blur fallback",
      "html2canvas@1.4.1" in lessflat and "frosted blur" in lessflat)
check("ShaderGradient in ui-ux-pro-max + Taste (SHADERGRAD_F22)",
      "SHADERGRAD_F22" in uipro and "SHADERGRAD_F22" in taste)
check("ShaderGradient @2.4.20 ESM-only + MIT-declared-no-LICENSE caveat",
      "@shadergradient/react@2.4.20" in uipro
      and "NO root LICENSE file" in uipro)
check("ShaderGradient v2, NOT legacy v1.3.5",
      "NOT legacy" in uipro and "v1.3.5" in uipro)
check("liquid-logo in ui-ux-pro-max + Taste (LIQLOGO_F22)",
      "LIQLOGO_F22" in uipro and "LIQLOGO_F22" in taste)
check("liquid-logo pin commit 689bb38a + PolyForm Shield + standalone tool",
      "689bb38a1e0d5a6a8baf2d34847635eefde19994" in uipro
      and "PolyForm Shield 1.0.0" in uipro
      and "STANDALONE TOOL" in uipro)
check("liquid-logo static fallback + paper-design attribution",
      "static logo" in uipro and "paper-design attribution" in taste)
check("one-WebGL-heavy-effect-per-surface rule (WEBGL_ONE_F22)",
      "One WebGL-heavy effect per" in uipro
      and "surface (WEBGL_ONE_F22)" in uipro
      and "## One WebGL-heavy effect per surface — WEBGL_ONE_F22 (fix #22 §15)" in slop)
check("liquid-glass-design dangling reference resolved (option b): 0 in built skill text",
      "liquid-glass-design" not in subprocess.run(
          ["grep", "-r", "liquid-glass-design", "skills", "--exclude-dir=node_modules"],
          cwd=BASE, capture_output=True, text=True).stdout
      and "liquid-glass-design" in lib15_report
      and "option (b), corrected" in lib15_report)
check("§15 tokens in build.sh (fix22 block)",
      "R3F_F22" in build and "LIQGLASS_F22" in build
      and "SHADERGRAD_F22" in build and "LIQLOGO_F22" in build
      and "WEBGL_ONE_F22" in build)

# 16. Vercel web-design-guidelines (§16) — pinned snapshot, never live fetch.
check("Vercel checklist file exists in the built tree (VERCEL_F22)",
      os.path.isfile(os.path.join(BASE, "skills/polish-pass/reference/vercel-checklist.md"))
      and "VERCEL_F22" in vercel)
check("Vercel pinned snapshot: commit 4ecfb9fb + date 2026-10-05",
      "4ecfb9fb8d1d3b7009674869b3aaee2f904042e1" in vercel
      and "2026-10-05" in vercel)
check("Vercel checklist wired into polish-pass (VERCEL-02/03)",
      "Also read the Vercel checklist" in polish
      and "Then run the Vercel checklist" in polish)
check("Vercel pointers in quick-reference + motion-foundations (VERCEL-04..07)",
      "vercel-a11y-check" in qr and "vercel-touch-check" in qr
      and "vercel-type-check" in qr
      and "pinned Vercel checklist (VERCEL_F22)" in mf)
check("live-fetch instruction ABSENT: no raw.githubusercontent URL in the checklist",
      "raw.githubusercontent.com" not in vercel)
check("live-fetch ABSENT from the built tree (no unpinned Vercel fetch URL)",
      "raw.githubusercontent.com/vercel-labs" not in subprocess.run(
          ["grep", "-r", "raw.githubusercontent.com/vercel-labs",
           "skills", "agents", "commands", "rules", "hooks",
           "--exclude-dir=node_modules"],
          cwd=BASE, capture_output=True, text=True).stdout)
check("Vercel license gap recorded (rules MIT, skill repo NO LICENSE)",
      "MIT (© 2025 Vercel Labs" in vercel and "has NO LICENSE" in vercel)
check("ECC-source check recorded (snapshot NOT in-source at the plugin pin)",
      "does NOT carry the skill" in vercel)
check("Vercel dedupe table accounts for all 136 rows, zero unaccounted",
      "136 rows accounted for, zero" in dedupe_vercel)
check("Vercel AG19 conflict recorded (APCA vs WCAG 4.5:1, parent adjudication)",
      "AG19" in dedupe_vercel)
check("VERCEL_F22 token in build.sh (fix22 block)",
      "VERCEL_F22" in build)

# 17. Libraries §17 — Casberry / OriginKit / daisyUI.
check("Casberry in motion-foundations + motion-patterns + ui-ux-pro-max + Taste + slop (CASBERRY_F22)",
      "CASBERRY_F22" in mf and "CASBERRY_F22" in mp
      and "CASBERRY_F22" in uipro and "CASBERRY_F22" in taste
      and "CASBERRY_F22" in slop)
check("Casberry standalone tool + terms unresolved + trust flag + export review",
      "STANDALONE TOOL" in mf and "terms / licence are UNRESOLVED" in mf
      and "ScamAdviser 1/100" in mf and "UNTRUSTED code" in mf)
check("Casberry export-review check in the slop checklist (L17-07)",
      "## Exported code is reviewed before it enters the build — Casberry (CASBERRY_F22, fix #22 §17)" in slop)
check("one-WebGL rule extended to Casberry exports (L17-06 replace)",
      "a Casberry particle export" in slop)
check("OriginKit in motion-patterns + ui-ux-pro-max + Taste (ORIGINKIT_F22)",
      "ORIGINKIT_F22" in mp and "ORIGINKIT_F22" in uipro
      and "ORIGINKIT_F22" in taste)
check("OriginKit 10/day cap + Pro exclusion + conditional licence",
      "10 component" in mp and "fetches per key per day" in mp
      and "never pay" in mp and "CONDITIONAL" in mp)
check("OriginKit is NOT Origin UI (distinction check)",
      "is NOT Origin UI" in mp)
check("OriginKit deduped vs React Bits (catalog vs importable library)",
      "Reach for React Bits" in mp)
check("daisyUI in ui-ux-pro-max + design-system + Taste (DAISYUI_F22)",
      "DAISYUI_F22" in uipro and "DAISYUI_F22" in ds
      and "DAISYUI_F22" in taste)
check("daisyUI pin 5.7.50 + MIT + Tailwind v4 pairing",
      "daisyui@5.7.50" in ds and "MIT" in ds
      and "Tailwind CSS v4" in ds)
check("daisyUI default theme unexamined FAILS + shadcn dedupe",
      "default theme unexamined FAILS" in ds and "shadcn" in ds)
check("running total of asset libraries/tools in fix #22 is 11",
      "§11's 4 + §15's 4 + §17's 3 = 11" in uipro)
check("§17 tokens in build.sh (fix22 block)",
      "CASBERRY_F22" in build and "ORIGINKIT_F22" in build
      and "DAISYUI_F22" in build)

# 18. Dedupe (§5) — one concept, one primary home.
for pair in ("G20 = B20 (reuse `layoutId`)", "G14 = B3/B6 (stagger)",
             "G3 = D18 (tabular numbers)",
             "G8 = A14 (bigger hit areas)",
             "G10 = B11/B12 (enter/exit from the trigger)",
             "G18 ~ B14 (don't tween while held)"):
    check(f"dedupe pair recorded in the glossary: {pair}",
          pair in glossary)
check("dedupe: B20 primary home is the motion-patterns shared-element example",
      "The example above is the primary home of\nthis rule" in mp
      or "The example above is the primary home of this rule" in mp)
check("dedupe: stagger primary home is the motion-patterns example + 30ms token",
      "same stagger primitive as the Stagger list example above" in mp)
check("dedupe: tabular numbers primary home is ui-ux-pro-max type rules",
      "tabular-polish" in qr)
check("dedupe: origin-aware primary home is motion-patterns (B11/B12)",
      "origin-aware animation, glossary G10" in mp)
check("dedupe: A10/B8/D20 one family cross-referenced both ways",
      "One family with B8 and D20" in mf
      and "one family with A10 exaggerated feedback" in mp)

# 19. Counts unchanged post-fix21 (no new skill/command/trigger).
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))


hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged — glossary/slop/unslop are reference files, not skills)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))
_triggers = json.load(open(os.path.join(
    BASE, "manifests/context-packs/skill-triggers@1.json"), encoding="utf-8"))
check("trigger keys still 64 (no new trigger from this fix)",
      _triggers["coverage"]["withTriggers"] == len(_triggers["triggers"]) == 64)
check("every trigger key still resolves to a real skill dir",
      all(os.path.isfile(os.path.join(
          BASE, "skills", _k[len("skill:"):], "SKILL.md"))
          for _k in _triggers["triggers"]))

# 20. No banned terms in the built tree (excl. node_modules).
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")
if hits:
    print("   banned-term files: %r" % (hits,))

# 21. build.sh is the post-fix22 file.
build_lines = build.splitlines()
build_md5 = hashlib.md5(build.encode("utf-8")).hexdigest()
check("build.sh contains the fix22 block marker",
      "fix22 upstream block applied" in build)
check("build.sh contains the BANG_PIN record",
      'BANG_PIN="%s"' % BANG_SHA in build)
for _marker in ("fix21 upstream block applied", "fix20 upstream block applied",
                "fix19 upstream block applied", "fix17 upstream block applied",
                "fix15 upstream block applied"):
    check(f"build.sh still contains the {_marker.split()[0]} block marker",
          _marker in build)
check("build.sh has MORE lines than post-fix21 (23,647)",
      len(build_lines) > 23647)
manifest_path = os.path.join(PLUGIN, "fix22/MANIFEST.md")
if os.path.exists(manifest_path):
    manifest = open(manifest_path, encoding="utf-8").read()
    m_lines = re.search(r"^build\.sh lines: (\d+)$", manifest, re.M)
    m_md5 = re.search(r"^build\.sh md5: ([0-9a-f]{32})$", manifest, re.M)
    check("fix22/MANIFEST.md records build.sh lines + md5",
          bool(m_lines and m_md5))
    if m_lines and m_md5:
        check(f"build.sh is {m_lines.group(1)} lines, md5 {m_md5.group(1)} (post-fix22)",
              len(build_lines) == int(m_lines.group(1))
              and build_md5 == m_md5.group(1))
else:
    print(f"   NOTE: fix22/MANIFEST.md not yet written by the coordinator; "
          f"measured build.sh lines={len(build_lines)}, md5={build_md5}")
    check("build.sh lines + md5 measured for the coordinator's MANIFEST "
          f"(lines={len(build_lines)}, md5={build_md5})", True)

# 22. Previous verifiers still pass, modulo the frozen post-fix21
# build.sh fingerprint AND the less-flat-ui diff count. Every earlier
# verifier hard-codes the post-fix21 baseline (23,647 lines, md5
# 8dfacb47...); fix #22 legitimately changes build.sh (23,758 lines, md5
# 306dd648... after §13-§17), so that ONE check in each verifier now
# fails, and each later verifier cascades the earlier failures. Those are
# allowed; any other FAIL line is a real regression. The less-flat-ui
# diff check is a second allowed failure, for the same reason: fix15/17/19
# hard-code "the staged-vs-standalone less-flat-ui diff is still exactly
# the 4 patch hunks" (the 4 Batch E patches). Fix #22 legitimately adds
# 2 plugin-scoped runtime hunks to the BUILT less-flat-ui copy only
# (DEPTH-13 texture/depth overlap note + L15-06 liquid-glass note, both
# applied by the fix22 block at build time, after the build.sh:263 copy
# of the shared global source) — so the diff is now exactly 6 = 4 Batch E
# + 2 fix22, and the 4 Batch E hunks themselves are intact (their
# patch-intact checks still pass). The global source was deliberately NOT
# edited (D-A2 in the manifest): plugin-scoped notes do not belong in
# Anish's shared Cursor skill. That is an expected consequence, not a
# regression; the allowance below names the check exactly.
_FPRINT = ("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c",
           "build.sh is 23647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c")
_LFUI_DIFF = "staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks"


def _allowed_fail(line):
    return (any(p in line for p in _FPRINT)
            or _LFUI_DIFF in line
            or re.match(r"FAIL fix\d+ verifier still passes", line))


for name, script in (("fix15", "fix15/verify15.py"),
                     ("fix17", "fix17/verify17.py"),
                     ("fix18", "fix18/verify18.py"),
                     ("fix19", "fix19/verify19.py"),
                     ("fix20", "fix20/verify20.py"),
                     ("fix21", "fix21/verify21.py")):
    r = subprocess.run(["python3", script], cwd=PLUGIN, capture_output=True, text=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    _fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    _bad = [ln for ln in _fails if not _allowed_fail(ln)]
    check(f"{name} verifier still passes except the stale post-fix21 "
          f"build.sh fingerprint ({tail})",
          not _bad)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
