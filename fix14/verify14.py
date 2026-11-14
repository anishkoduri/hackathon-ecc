#!/usr/bin/env python3
"""verify14.py — checks fix #14 in the BUILT tree (read-only).

Run after a build: python3 fix14/verify14.py
Exits 0 only if every check passes.
"""
import os
import re
import sys

HOME = os.path.expanduser("~")
BASE = os.path.join(HOME, "workspace/hackathon-plugin/hackathon-ecc")
STAGED = os.path.join(BASE, "skills/less-flat-ui/SKILL.md")
SOURCE = os.path.join(HOME, "workspace/cursor-skills/less-flat-ui/SKILL.md")

checks = []


def check(name, ok):
    checks.append((name, ok))
    print(("PASS " if ok else "FAIL ") + name)


staged = open(STAGED, encoding="utf-8").read()
source = open(SOURCE, encoding="utf-8").read()

# 1. Counts: 23 everywhere in the staged copy.
check("staged frontmatter says 23 textured treatments",
      "23 textured treatments" in staged)
check("staged source line says Source of the 23 treatments",
      "Source of the 23 treatments" in staged)
check("staged heading is ## The 23 treatments",
      "## The 23 treatments" in staged)
check("no stale '22 treatments' text in staged copy (quoted reel title excepted)",
      staged.count("22 treatments") == 0)
check("quoted reel title '22 Backgrounds' preserved",
      '"22 Backgrounds to Make Designs Less Flat' in staged)
check("second source @lnunesdesigns named in staged copy",
      "@lnunesdesigns" in staged)
check("second source notes 9 of 10 already covered, Soft Shadow new",
      "9 of its 10 treatments were already covered" in staged
      and "Soft Shadow is the new one from it" in staged)

# 2. Treatment numbering 1..23, no gaps/duplicates, Soft Shadow is #23.
nums = [int(m) for m in re.findall(r"^### (\d+)\. ", staged, re.M)]
check("treatment headings number 1..23 exactly",
      nums == list(range(1, 24)))
check("### 23. Soft shadow present",
      "### 23. Soft shadow" in staged)
check("Soft Shadow CSS block present (.soft-shadow, .soft-shadow-sm, .soft-shadow-lg)",
      ".soft-shadow {" in staged and ".soft-shadow-sm {" in staged
      and ".soft-shadow-lg {" in staged)
check("Soft Shadow Best for line present (cards, buttons, modals, floating panels)",
      "Best for: cards, buttons, modals, floating panels" in staged)
check("Soft Shadow layering note present (layers with everything)",
      "Layers with everything: a shadow is a depth cue, not a pattern" in staged)
check("Soft Shadow in picker Premium row",
      "grainy gradients, soft shadow |" in staged)
check("Soft Shadow in surface table: cards",
      "speckled graphite, soft shadow |" in staged)
check("Soft Shadow in surface table: buttons",
      "iridescent shapes, grainy gradients, soft shadow |" in staged)
check("Soft Shadow in surface table: modals",
      "blurred photos, soft shadow |" in staged)
check("no duplicate treatments: each of the other 9 reel items appears once as a heading",
      all(len(re.findall(rf"^### \d+\. {n}", staged, re.M)) == 1 for n in [
          "Thermal gradients", "Blueprint grids", "Water ripples",
          "Speckled graphite", "Fluted glass", "Contour lines",
          "Grainy gradients", "Single-hue landscapes", "Grass texture"]))

# 3. The 3 runtime-patch additions survived the rebuild.
check("patch 1 intact: wow-moment rule",
      "Texture in service of the wow moment, not decoration" in staged)
check("patch 2 intact: design-tokens record line in Shared utilities",
      "Record every treatment applied, on which surface, in `docs/design-tokens.md`" in staged)
check("patch 3 intact: re-tint warning after the treatments heading",
      "Re-tint every example below to the project's dealt palette" in staged)

# 4. Staged == standalone except exactly the 3 known patch diffs.
# Patch 1 (wow-moment) and patch 3 (re-tint) are pure insertions; patch 2
# (design-tokens record line) is an inline APPEND to the Shared-utilities
# intro line, so difflib reports it as a replace, not an insert.
import difflib
s_lines = source.splitlines()
t_lines = staged.splitlines()
sm = difflib.SequenceMatcher(None, s_lines, t_lines)
nonequal = [(tag, s_lines[i1:i2], t_lines[j1:j2])
            for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
check("staged-vs-standalone diff is exactly the 3 patch hunks",
      len(nonequal) == 3)
patch_ok = False
if len(nonequal) == 3:
    (t1, s1, n1), (t2, s2, n2), (t3, s3, n3) = nonequal
    patch_ok = (
        t1 == "insert" and len(n1) == 1
        and "wow moment" in n1[0]
        and t2 == "replace" and len(s2) == 1 and len(n2) == 1
        and n2[0] == s2[0] + " Record every treatment applied, on which surface, in `docs/design-tokens.md` (or MASTER.md on a dashboard-only build) — later slices and polish-pass read the record from there, not from the CSS."
        and t3 == "insert" and len(n3) == 2
        and any("Re-tint every example below" in ln for ln in n3))
check("the 3 hunks are exactly the known patch additions (wow / record-append / re-tint)",
      patch_ok)

# 5. build.sh W2-C1 anchor reads 23 (both old and new).
build = open(os.path.join(HOME, "workspace/hackathon-plugin/build.sh"),
             encoding="utf-8").read()
check("build.sh W2-C1 anchor: '## The 22 treatments' gone",
      "## The 22 treatments" not in build)
check("build.sh W2-C1 anchor: '## The 23 treatments' present twice",
      build.count("## The 23 treatments") == 2)

failed = [n for n, ok in checks if not ok]
print(f"\n{len(checks) - len(failed)}/{len(checks)} checks pass")
sys.exit(1 if failed else 0)
