#!/usr/bin/env python3
"""Fix #23 §6 applier (worker W4) — alignment + centering.

Inserts ONE runtime-patch block into build.sh immediately BEFORE the line
`# STEP 5 — Counts`. The block patches skills/browser-qa/SKILL.md (upstream;
browser-qa remains the SOLE executor of pass/fail verdicts on rendered
screens — everything else is candidate evidence) with the §6 alignment
assertions (ALIGN_F23), the coverage matrix (COVER_F23), and the
blocking-gap rule (BLOCK_F23).

Do NOT run build.sh from here — integration runs it later. Do NOT touch the
built tree (hackathon-ecc/) directly. Do NOT re-run fix11/fix11-stage.py.
Do NOT touch /demo wiring or DEMOGATE tokens. Grok pins only
(grok-4.7-high / cursor-grok-4.6-high-fast); no banned terms in new text.

Idempotency guard: refuses if the block marker comment is already present
in build.sh. Preflight: every anchor is verified count==1 against the
CURRENT built tree before build.sh is touched; fails loudly on mismatch.
Anchor counts were also verified by grep before this script was written
(all 5 anchors count==1 in hackathon-ecc/skills/browser-qa/SKILL.md).

Usage: python3 apply-w4.py
"""

import os
import sys

PLUGIN = os.path.expanduser("~/workspace/hackathon-plugin")
BUILT = os.path.join(PLUGIN, "hackathon-ecc")
BUILD_SH = os.path.join(PLUGIN, "build.sh")

MARKER = "# --- fix23 §6: alignment + centering (ALIGN_F23) ---"
STEP5 = "# STEP 5 — Counts"

# (id, rel-path, old-anchor, add-text, mode) — mode in {after, before, replace}.
# Follows the fix22 block pattern: the block below re-verifies count==1 at
# build time and fails the build loudly on mismatch.
SUBS = [
    ("ALIGN_F23-A", "skills/browser-qa/SKILL.md",
     "### Phase 3: Visual Regression",
     "\n\n**Alignment assertions (fix #23 §6, ALIGN_F23).** Eyeballing screenshots is not a check: run these programmatic assertions wherever the harness allows, on the live rendered page via `getBoundingClientRect()`. Tolerances: 0px for overflow; ≤ 2px for centering / grid / spacing equality. (a) No horizontal overflow at any tested width (`scrollWidth - innerWidth == 0`); no leaf text element with `scrollWidth > clientWidth + 1`. (b) Hero / phone frame centered in the viewport (offset ≤ 2px); at the mid band, if side panels share the row, the hero GROUP is centered with equal outer margins ≤ 2px. (c) Nav items evenly spaced (adjacent gaps equal ± 2px) and the nav group centered; each label center == its item center ± 2px. (d) Card edges aligned to a common left/right grid: full-width children share one left and one right edge (± 2px); a narrower child is left-aligned or centered; feed cards share one left and one right edge. (e) No text clipped or overflowing its container; no element beyond its frame unless a declared intentional bleed recorded in the decision record (page overflow still 0). (f) No label collisions: diagram / SVG text boxes pairwise non-overlapping and inside the viewport; stamps centered on their parent ± 2px; status pairs judged by vertical CENTERS, not tops. (g) Primary actions centered on their axis: grouped inputs centered on their panel ± 2px; full-width actions share the grid edges, narrower ones centered. (h) Desktop side panels: gutters symmetric ± 2px, tops aligned ± 2px unless a stagger is recorded in the decision record; stacked mid-band blocks centered as a group. Full checklist (candidate evidence): `polish-pass` reference/alignment.md (`ALIGN_F23`).",
     "after"),
    ("ALIGN_F23-B", "skills/browser-qa/SKILL.md",
     "1. Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)",
     "\n\nWidths (fix #23 §6, COVER_F23): 1440 desktop, 900 mid-band default probe (band 768–1100), 390 mobile — these three widths supersede the 375 / 768 / 1440 breakpoints in step 1 above for alignment coverage. If a layout breakpoint falls inside 768–1100, probe at the breakpoint ± 1 as well and take a mid full-page composition shot.",
     "after"),
    ("ALIGN_F23-C", "skills/browser-qa/SKILL.md",
     "3. Flag layout shifts > 5px, missing elements, overflow",
     "\n\nCoverage is MANDATORY for EVERY flow state, not just the happy path (COVER_F23): enumerate all screens × all reachable states — error / wrong-code, empty, success / delivered, accepted, scrolled positions — and measure + screenshot each at all three widths. A build with an unverified width or an unverified flow state is NOT shippable (BLOCK_F23, see the verdict rule below).",
     "after"),
    ("ALIGN_F23-D", "skills/browser-qa/SKILL.md",
     "# verdict ∈ SHIP / SHIP WITH FIXES / DO NOT SHIP; use INCONCLUSIVE if no visual baseline",
     "\n\n**Blocking-gap rule (fix #23 §6, BLOCK_F23).** A build with an unverified width or an unverified flow state is NOT shippable — the gap is a blocking finding, not a note. Missing coverage → blocking finding → verdict DO NOT SHIP. A coverage matrix with an empty cell is never reported as SHIP, SHIP WITH FIXES, or INCONCLUSIVE-as-pass; the matrix is complete or the build does not ship.",
     "after"),
    ("ALIGN_F23-E", "skills/browser-qa/SKILL.md",
     "### Visual\n- [✗] Hero section overflows on 375px viewport",
     "\n\n### Alignment (fix #23 §6, ALIGN_F23)\n- [✓/✗] Overflow: 0px at 1440 / 900 / 390; text overflow: 0 elements\n- [✓/✗] Centering: frame / hero-group offset ≤ 2px at every width\n- [✓/✗] Nav: gaps equal ± 2px, group centered, labels centered on items\n- [✓/✗] Grid: card edges share one left / one right per width\n- [✓/✗] Clipping / collisions: 0 clipped, 0 label collisions, 0 undeclared beyond-frame\n- [✓/✗] Actions: primary actions centered on their axis ± 2px\n- [✓/✗] Coverage: every width × every flow state measured + screenshotted (BLOCK_F23: any gap → DO NOT SHIP)",
     "after"),
]

BLOCK = r'''# --- fix23 §6: alignment + centering (ALIGN_F23) ---
# (browser-qa is upstream; it has no staged source and is patched here.
#  browser-qa remains the SOLE executor of pass/fail verdicts on rendered
#  screens; polish-pass reference/alignment.md (ALIGN_F23) is candidate
#  evidence only. All anchors were verified count==1 against the post-fix22
#  built tree by fix23/apply-w4.py's preflight; the asserts below
#  re-verify at build time and fail the build loudly on mismatch.
#  Measurement model: the Home Run render alignment audit harness
#  (cold-start-render/home-run/qa/align-audit.mjs) — getBoundingClientRect()
#  geometry at 1440 / 900 / 390 across every flow state, never eyeballing.
# Placement: before STEP 5 (after the fix22 block).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]

subs = [
  ('ALIGN_F23-A', 'skills/browser-qa/SKILL.md', '### Phase 3: Visual Regression', "\n\n**Alignment assertions (fix #23 §6, ALIGN_F23).** Eyeballing screenshots is not a check: run these programmatic assertions wherever the harness allows, on the live rendered page via `getBoundingClientRect()`. Tolerances: 0px for overflow; ≤ 2px for centering / grid / spacing equality. (a) No horizontal overflow at any tested width (`scrollWidth - innerWidth == 0`); no leaf text element with `scrollWidth > clientWidth + 1`. (b) Hero / phone frame centered in the viewport (offset ≤ 2px); at the mid band, if side panels share the row, the hero GROUP is centered with equal outer margins ≤ 2px. (c) Nav items evenly spaced (adjacent gaps equal ± 2px) and the nav group centered; each label center == its item center ± 2px. (d) Card edges aligned to a common left/right grid: full-width children share one left and one right edge (± 2px); a narrower child is left-aligned or centered; feed cards share one left and one right edge. (e) No text clipped or overflowing its container; no element beyond its frame unless a declared intentional bleed recorded in the decision record (page overflow still 0). (f) No label collisions: diagram / SVG text boxes pairwise non-overlapping and inside the viewport; stamps centered on their parent ± 2px; status pairs judged by vertical CENTERS, not tops. (g) Primary actions centered on their axis: grouped inputs centered on their panel ± 2px; full-width actions share the grid edges, narrower ones centered. (h) Desktop side panels: gutters symmetric ± 2px, tops aligned ± 2px unless a stagger is recorded in the decision record; stacked mid-band blocks centered as a group. Full checklist (candidate evidence): `polish-pass` reference/alignment.md (`ALIGN_F23`).", 'after'),
  ('ALIGN_F23-B', 'skills/browser-qa/SKILL.md', '1. Screenshot key pages at 3 breakpoints (375px, 768px, 1440px)', "\n\nWidths (fix #23 §6, COVER_F23): 1440 desktop, 900 mid-band default probe (band 768–1100), 390 mobile — these three widths supersede the 375 / 768 / 1440 breakpoints in step 1 above for alignment coverage. If a layout breakpoint falls inside 768–1100, probe at the breakpoint ± 1 as well and take a mid full-page composition shot.", 'after'),
  ('ALIGN_F23-C', 'skills/browser-qa/SKILL.md', '3. Flag layout shifts > 5px, missing elements, overflow', "\n\nCoverage is MANDATORY for EVERY flow state, not just the happy path (COVER_F23): enumerate all screens × all reachable states — error / wrong-code, empty, success / delivered, accepted, scrolled positions — and measure + screenshot each at all three widths. A build with an unverified width or an unverified flow state is NOT shippable (BLOCK_F23, see the verdict rule below).", 'after'),
  ('ALIGN_F23-D', 'skills/browser-qa/SKILL.md', '# verdict ∈ SHIP / SHIP WITH FIXES / DO NOT SHIP; use INCONCLUSIVE if no visual baseline', "\n\n**Blocking-gap rule (fix #23 §6, BLOCK_F23).** A build with an unverified width or an unverified flow state is NOT shippable — the gap is a blocking finding, not a note. Missing coverage → blocking finding → verdict DO NOT SHIP. A coverage matrix with an empty cell is never reported as SHIP, SHIP WITH FIXES, or INCONCLUSIVE-as-pass; the matrix is complete or the build does not ship.", 'after'),
  ('ALIGN_F23-E', 'skills/browser-qa/SKILL.md', '### Visual\n- [✗] Hero section overflows on 375px viewport', "\n\n### Alignment (fix #23 §6, ALIGN_F23)\n- [✓/✗] Overflow: 0px at 1440 / 900 / 390; text overflow: 0 elements\n- [✓/✗] Centering: frame / hero-group offset ≤ 2px at every width\n- [✓/✗] Nav: gaps equal ± 2px, group centered, labels centered on items\n- [✓/✗] Grid: card edges share one left / one right per width\n- [✓/✗] Clipping / collisions: 0 clipped, 0 label collisions, 0 undeclared beyond-frame\n- [✓/✗] Actions: primary actions centered on their axis ± 2px\n- [✓/✗] Coverage: every width × every flow state measured + screenshotted (BLOCK_F23: any gap → DO NOT SHIP)", 'after'),
]
for pid, rel, old, add, mode in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    n = t.count(old)
    assert n == 1, f"fix23 §6 anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    if mode == 'after':
        new = old + add
    elif mode == 'before':
        new = add.rstrip('\n') + '\n\n' + old
    else:  # replace
        new = add
    open(p, "w").write(t.replace(old, new))
print("fix23 §6 alignment block applied")
PYEOF
'''


def main():
    with open(BUILD_SH, encoding="utf-8") as f:
        text = f.read()
    if MARKER in text:
        print(f"REFUSE: marker already present in build.sh: {MARKER!r}")
        sys.exit(1)
    n_step5 = text.count(STEP5)
    assert n_step5 == 1, f"{STEP5!r} count={n_step5}, expected 1"
    # Preflight: every anchor count==1 in the CURRENT built tree.
    for pid, rel, old, _add, _mode in SUBS:
        p = os.path.join(BUILT, rel)
        t = open(p, encoding="utf-8").read()
        n = t.count(old)
        assert n == 1, f"preflight {pid}: anchor count={n} in {rel}: {old[:70]!r}"
    idx = text.index(STEP5)
    new_text = text[:idx] + BLOCK + "\n" + text[idx:]
    with open(BUILD_SH, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"inserted fix23 §6 block ({len(SUBS)} subs) before {STEP5!r}")


if __name__ == "__main__":
    main()
