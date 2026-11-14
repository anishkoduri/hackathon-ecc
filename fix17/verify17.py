#!/usr/bin/env python3
"""verify17.py -- checks fix #17 in the BUILT tree (read-only).

Run after a build: python3 fix17/verify17.py
Exits 0 only if every check passes.

Checks, against ~/workspace/hackathon-plugin/hackathon-ecc:
  1. U1/T1/F1/E1 anchors present in the files SPEC assigns them to.
  2. M1-M6 anchors present (motion-* skills, make-interfaces-feel-better,
     step-6 static checks).
  3. Sticker exceptions A + B present, with the Motion pointer.
  4. R3 widening present in less-flat-ui.
  5. Canonical block (fix #15) still verbatim x1 in all 11 files; D1 rule
     still present in Taste/orchestrate/polish-pass/orch-build-mvp.
  6. Treatments still number 1..23; staged-vs-standalone less-flat-ui diff
     still exactly the 4 patch hunks (patch 4 is the weave20 pointer —
     baseline update by fix #20's weaving pass).
  7. Counts unchanged post-fix16: 166/72/123/87/15.
  8. No banned terms (fix #16 scrub) in the built skill tree (excl.
     node_modules).
  9. build.sh is the post-fix17 file (23,276 lines, recorded md5) and still
     contains the fix15 + fix17 blocks intact. Updated by fix #19 to the
     post-fix19 values (23,314 lines, a8d3d3c6...) and by fix #20 to the
     post-fix20 values (23,349 lines, e5ff7d6c...) and by fix #20's
     weaving pass to the post-weave20 values (23,582 lines, 766a35e4...) —
     baseline updates, same precedent as fix #19, not anchor changes.
     Updated by fix #20's fix-up pass (audit #62 + sweep #25) to the
     post-fixup20 values (23,582 lines, 766a35e4...) — same precedent.
     Updated by fix #20's second fix-up pass (sweep #26) to the
     post-fixup20b values (23,582 lines, 766a35e4...) — same precedent.
     Updated by fix #20's third fix-up pass (sweep #27 + steers #3/#4/#5/#6)
     to the post-fixup20c values (23,609 lines, 3c7b45bb...) — same precedent.
     Updated by fix #20's fourth fix-up pass (sweep #28 MINOR-1) to the
     post-fixup20d values (23,609 lines, 785fb405...) — same precedent.
     Updated by fix #21 to the
     post-fix21 values (23,647 lines, 8dfacb47...) — same precedent.
"""
import difflib
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix15"))
sys.path.insert(0, os.path.join(os.path.expanduser("~"),
                                "workspace/hackathon-plugin/fix17"))
from fix15 import CANONICAL, D1_RULE  # noqa: E402
from fix17 import (U1_RULE, T1_RULE, F1_RULE, E1_RULE, M1_RULE, M2_RULE,  # noqa: E402
                   M3_RULE, M4_RULE, M5_RULE, STATIC_CHECKS,
                   STICKER_EXCEPTIONS)

HOME = os.path.expanduser("~")
PLUGIN = os.path.join(HOME, "workspace/hackathon-plugin")
BASE = os.path.join(PLUGIN, "hackathon-ecc")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()


taste = read("skills/design-taste-frontend/SKILL.md")
uipro = read("skills/ui-ux-pro-max/SKILL.md")
lessflat = read("skills/less-flat-ui/SKILL.md")
polish = read("skills/polish-pass/SKILL.md")
typeset = read("skills/polish-pass/reference/lenses/typeset.md")
orch = read("skills/orchestrate/SKILL.md")
mvp = read("skills/orch-build-mvp/SKILL.md")
mfound = read("skills/motion-foundations/SKILL.md")
mpatt = read("skills/motion-patterns/SKILL.md")
madv = read("skills/motion-advanced/SKILL.md")
mife = read("skills/make-interfaces-feel-better/SKILL.md")
sticker = read("skills/design-taste-frontend/references/hallmark/references/themes/sticker.md")

# 1. U1.
check("U1 Taste step 4a: unique page-only elements, at least three",
      U1_RULE in taste)
check("U1 ui-ux-pro-max anti-generic bar (app surfaces)",
      "Unique page-only elements (fix #17 U1, app surfaces)" in uipro)
check("U1 less-flat-ui record section (app/dashboard count)",
      "record the page-only elements alongside the treatments" in lessflat)
check("U1 static check in Taste step 6",
      "The 'Unique elements' list in `docs/design-tokens.md` has at least three complete entries" in taste)
check("U1 static check in orchestrate Verify 5a",
      "The 'Unique elements' list in `docs/design-tokens.md` has at least three complete entries" in orch)
check("U1 static check in orch-build-mvp step 6",
      "The 'Unique elements' list in `docs/design-tokens.md` has at least three complete entries" in mvp)

# 2. T1.
check("T1 Taste step 4a: type fills its bubble",
      T1_RULE in taste)
check("T1 ui-ux-pro-max type-scale step",
      T1_RULE in uipro)
check("T1 typeset lens Rules checkbox",
      "Display, figure and label type fills its bubble (glyph box ≥ 60% of the container's inner size); no dead space, no overflow, no crowding (fix #17 T1)." in typeset)
check("T1 typeset lens Verify bullet",
      "Fill (fix #17 T1): display, figure and label type inside a bounded container fills it" in typeset)
check("T1 polish-pass harmony verifies fill ratios",
      "T1 fill ratios recorded per Type-list row (glyph box ≥ 60% of the container's inner size)" in polish)
check("T1 static check: fill ratio minimum 0.60 + dead-space item",
      "fill ratio (glyph box / container box, minimum 0.60)" in taste
      and "largest empty band exceeds 25% of its minor dimension" in taste)

# 3. F1.
check("F1 Taste step 4a: every font decision cites the type system",
      F1_RULE in taste)
check("F1 ui-ux-pro-max type-scale step",
      F1_RULE in uipro)
check("F1 static check: weight/tracking columns + Source cell",
      "The Type list gains weight and tracking columns and a Source cell per row naming the exact skill text" in taste
      and "a row with an empty or 'default' Source is an incomplete build" in taste)
check("F1 polish-pass harmony verifies Source cells",
      "weight and tracking columns and Source cells (fix #17 F1)" in polish)

# 4. E1 (active push, not permission).
check("E1 Taste step 4a: push boundaries, trailblazing, not dumb",
      E1_RULE in taste)
check("E1 orchestrate design-package rule (after canonical block)",
      E1_RULE in orch)
check("E1 orch-build-mvp step 4",
      E1_RULE in mvp)
check("E1 ui-ux-pro-max anti-generic bar",
      E1_RULE in uipro)
check("E1 wording is a push, not a permission",
      "MUST push boundaries and aim to be trailblazing" in taste
      and "MAY invent page-specific elements" not in taste)

# 5. M1-M6.
check("M1 motion-patterns rule 9: scroll entrances, motion-governed surfaces",
      M1_RULE in mpatt)
check("M1 motion-foundations rule 9",
      M1_RULE in mfound)
check("M2 motion-patterns rule 10: 1500ms fail-safe",
      M2_RULE in mpatt)
check("M2 motion-foundations rule 10",
      M2_RULE in mfound)
check("M2 motion-patterns scroll-reveal example note",
      "1500ms fail-safe (fix #17 M2)" in mpatt)
check("M2 motion-advanced useScrollRevealSafe hook",
      "useScrollRevealSafe" in madv and "setTimeout(() => setRevealed(true), 1500)" in madv)
check("M3-M5 make-interfaces-feel-better Motion section (default set)",
      "Default motion set (fix #17, v4-level)" in mife
      and M3_RULE in mife and M4_RULE in mife and M5_RULE in mife)
check("M3-M5 make-interfaces-feel-better Checklist items",
      "fix #17 M3" in mife and "fix #17 M4" in mife and "fix #17 M5" in mife)
check("M6 motion-foundations Accessibility note (reduced-motion gating)",
      "Under reduced motion the fail-safe still reveals" in mfound
      and "fix #17 M6" in mfound)
check("M1-M6 static checks: Motion list record (entrances/fail-safe/hovered/bit/reduced-motion)",
      "each scroll entrance with its tokens and fail-safe mechanism (M1/M2" in taste
      and "hovered shots per interactive surface" in taste
      and "one working interactive bit per page with an interactive surface" in taste
      and "the reduced-motion render noted, or recorded as not run (M6)" in taste)

# 6. Sticker exceptions.
check("Sticker exception A: hand-drawn ink marks, scoped, named",
      "Hand-drawn ink marks (fix #17, exception A)" in sticker
      and "Added at Anish's direction in the Campus Eats cold-start render, Nov 11, 2026" in sticker)
check("Sticker exception B: scroll rise-and-settle entrances, scoped, named",
      "Scroll rise-and-settle entrances (fix #17, exception B)" in sticker)
check("Sticker Motion line points at the exception (do-not intact)",
      "nothing on scroll, except the scoped exception in 'Scoped exceptions' below" in sticker
      and "Never a drawn sticker, mascot or doodle" in sticker)
check("Sticker exceptions section present verbatim",
      STICKER_EXCEPTIONS in sticker)

# 7. R3 widening.
check("R3 widening: handmade surface treatment counts as a treatment kind",
      "A theme-matched handmade surface treatment — tape, perforation, washi, a hand-drawn ink mark — counts as a treatment kind (fix #17)" in lessflat)
check("R3 widening: record section, handmade treatments record the same way",
      "Handmade surface treatments (tape, perforation, washi, hand-drawn ink marks) record the same way" in lessflat)

# 8. Fix #15 anchors intact (canonical block + D1).
CANON_TARGETS = [
    "skills/design-taste-frontend/SKILL.md",
    "skills/ui-ux-pro-max/SKILL.md",
    "skills/less-flat-ui/SKILL.md",
    "skills/polish-pass/SKILL.md",
    "skills/design-taste-frontend/references/hallmark/references/hallmark-floor.md",
    "skills/make-interfaces-feel-better/SKILL.md",
    "skills/motion-foundations/SKILL.md",
    "skills/motion-patterns/SKILL.md",
    "skills/motion-advanced/SKILL.md",
    "skills/orchestrate/SKILL.md",
    "skills/orch-build-mvp/SKILL.md",
]
for rel in CANON_TARGETS:
    text = read(rel)
    check(f"canonical block verbatim x1 in {rel}", text.count(CANONICAL) == 1)
check("D1 rule still in Taste step 6", D1_RULE in taste)
check("D1 rule still in orchestrate step 5", D1_RULE in orch)
check("D1 rule still in polish-pass Capture", D1_RULE in polish)
check("D1 rule still in orch-build-mvp step 6", D1_RULE in mvp)

# 9. Treatments still 23; staged-vs-standalone diff still the 4 patch hunks
# (patch 4 is the weave20 design-decision pointer — baseline update by fix
# #20's weaving pass, same precedent as the build.sh pin bump).
nums = [int(m) for m in re.findall(r"^### (\d+)\. ", lessflat, re.M)]
check("less-flat-ui treatments still number 1..23 exactly", nums == list(range(1, 24)))
check("patch 4 intact: weave20 design-decision pointer at check-every-surface",
      "**Design-decision pointer:** F2/F3/F4/F5/F6/D19/B1/X1 as relevant — design-package rule — Taste step 4a / orchestrate." in lessflat)
source_lf = open(os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md"),
                 encoding="utf-8").read()
sm = difflib.SequenceMatcher(None, source_lf.splitlines(), lessflat.splitlines())
nonequal = [op for op in sm.get_opcodes() if op[0] != "equal"]
check("staged-vs-standalone less-flat-ui diff is still exactly the 4 patch hunks",
      len(nonequal) == 4)

# 10. Counts unchanged post-fix16.
def count_dir(d):
    return len(os.listdir(os.path.join(BASE, d)))
hooks_n = len(json.load(open(os.path.join(BASE, "hooks/hooks.json"),
                             encoding="utf-8"))["hooks"])
check("counts 166/72/123/87/15 (unchanged)",
      (count_dir("skills"), count_dir("agents"), count_dir("rules"),
       count_dir("commands"), hooks_n) == (166, 72, 123, 87, 15))

# 11. No banned terms in the built skill tree (excl. node_modules).
import subprocess
banned = ["claude", "codex", "anthropic", "opus", "sonnet", "haiku", "composer-2.5"]
hits = subprocess.run(
    ["grep", "-riE", "|".join(banned), "skills", "agents", "commands", "rules",
     "hooks", "README.md", "--exclude-dir=node_modules", "-l"],
    cwd=BASE, capture_output=True, text=True).stdout.strip()
check("banned terms 0 in built tree (skills/agents/commands/rules/hooks/README)",
      hits == "")

# 12. build.sh post-fix17 + fix15 block intact.
import hashlib
build = open(os.path.join(PLUGIN, "build.sh"), encoding="utf-8").read()
build_lines = build.splitlines()
check("build.sh is 23,647 lines, md5 8dfacb47a2a6698d47e4b4a5f8d9126c (post-fix21)",
      len(build_lines) == 23647
      and hashlib.md5(build.encode("utf-8")).hexdigest() == "8dfacb47a2a6698d47e4b4a5f8d9126c")
check("build.sh contains the fix17 block marker",
      "fix17 upstream block applied" in build)
check("build.sh still contains the fix15 block marker",
      "fix15 upstream block applied" in build)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
