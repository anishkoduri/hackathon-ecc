#!/usr/bin/env python3
"""Fix program #13c — ASSEMBLER (coordinator).

Inserts the fix13c patch block into build.sh LAST, just before STEP 5
(after the fix13b block). The block patches the three files with no
staged sources (upstream ECC patched at build time):
  M1a orch-build-mvp/SKILL.md step 4 :40 — name browser-qa as the executor
      of the distinctiveness bar (in step 6's every-route visual loop);
      the GAN evaluator does NOT judge screen distinctiveness.
  M1b gan-style-harness/SKILL.md rubric — scoping note inside the rubric
      fence + deferral on the Design Quality 7-8 and Originality 7-8 rows:
      screen distinctiveness is judged ONLY by browser-qa, never here.
  M1c commands/gan-design.md — evaluator-prompt line gains the same
      deferral (its evaluator scores against eval-rubric.md, which now
      carries the deferral; no second screen judge in the design loop).

Preflight: every anchor is verified count==1 against the CURRENT built
tree (post-fix13b) before assembly — build.sh does `rm -rf $PLUGIN_DIR`
and regenerates the tree from scratch, so a stale or partial tree proves
nothing, but the anchors are the post-fix13b text and the current tree IS
post-fix13b. The block's own inner asserts re-verify each anchor count==1
at build time and fail the build loudly on any mismatch.
Idempotency guard: refuses to run if a fix13c block is already in build.sh.
Backup: run `cp build.sh build.sh.before-fix13c` before this script.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.dirname(HERE)          # ~/workspace/hackathon-plugin
BUILD_SH = os.path.join(PLUGIN_ROOT, "build.sh")
BUILT = os.path.join(PLUGIN_ROOT, "hackathon-ecc")
STEP5_ANCHOR = "\n# STEP 5 — Counts\n"

BLOCK = r"""# --- fix13c: dry-run #15 minors — M1a/M1b/M1c (single distinctiveness executor) ---
# (orch-build-mvp / gan-style-harness / gan-design have no staged sources;
#  they are upstream ECC patched here). Placement: LAST, just before STEP 5
#  (after the fix13b block).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # M1a orch-build-mvp step 4: browser-qa named as the bar's executor.
  ("skills/orch-build-mvp/SKILL.md",
   r'''Verify the built app's primary screens against the distinctiveness bar — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference) — within the existing fix caps.''',
   r'''The distinctiveness bar is executed by `browser-qa` ONLY, in step 6's every-route visual loop (browser-qa is the SOLE executor of the bar) — a named direction recorded AND visibly applied (tokens, type, colour, spacing trace to it); a finding, minor at least, when screens carry no named direction, no applied theme/tokens, read as a default template, or are derivative (the design is based on a searched external reference) — within the existing fix caps. The GAN evaluator does NOT judge screen distinctiveness: its Design Quality / Originality rows defer to browser-qa (see `gan-style-harness`).'''),
  # M1b gan-style-harness rubric: scoping note inside the rubric fence.
  ("skills/gan-style-harness/SKILL.md",
   r'''## Evaluation Rubric

### Design Quality (weight: 0.3)''',
   r'''## Evaluation Rubric

**Screen distinctiveness is NOT scored here.** Whether a named direction is recorded AND visibly applied on the rendered screens is judged ONLY by `browser-qa` in the visual loop (orch-build-mvp step 6) — never by this evaluator. The Design Quality and Originality rows below score the recorded direction and its code-level application only (direction recorded in `docs/design-tokens.md`; tokens, type, and spacing trace to it in the code). A screen that reads as a default template is a browser-qa finding, not a rubric deduction — do not raise or lower a score for screen distinctiveness.

### Design Quality (weight: 0.3)'''),
  # M1b gan-style-harness rubric: Design Quality 7-8 row defers.
  ("skills/gan-style-harness/SKILL.md",
   r'''- 7-8: Distinctive, cohesive visual identity''',
   r'''- 7-8: Distinctive, cohesive visual identity in the recorded direction and its code-level application — screen distinctiveness itself is judged ONLY by browser-qa, never here'''),
  # M1b gan-style-harness rubric: Originality 7-8 row defers.
  ("skills/gan-style-harness/SKILL.md",
   r'''- 7-8: Clear creative vision, unique approach''',
   r'''- 7-8: Clear creative vision, unique approach in the recorded direction — screen distinctiveness itself is judged ONLY by browser-qa, never here'''),
  # M1c gan-design: evaluator-prompt line gains the deferral.
  ("commands/gan-design.md",
   r'''- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?"''',
   r'''- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?" — but screen distinctiveness is NOT judged here: whether a named direction is recorded AND visibly applied is judged ONLY by `browser-qa` in the visual loop; the evaluator scores against `eval-rubric.md`, which carries that deferral.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    t = open(p).read()
    n = t.count(old)
    assert n == 1, f"fix13c anchor not found exactly once in {rel}: {old[:70]!r} (count={n})"
    open(p, "w").write(t.replace(old, new))
print("fix13c single-executor block applied")
PYEOF

"""

# Preflight anchors: (rel path in built tree, old text, label)
PREFLIGHT = [
    ("skills/orch-build-mvp/SKILL.md",
     "Verify the built app's primary screens against the distinctiveness bar",
     "M1a step-4 bar statement"),
    ("skills/gan-style-harness/SKILL.md",
     "## Evaluation Rubric\n\n### Design Quality (weight: 0.3)",
     "M1b rubric header"),
    ("skills/gan-style-harness/SKILL.md",
     "- 7-8: Distinctive, cohesive visual identity",
     "M1b Design Quality 7-8"),
    ("skills/gan-style-harness/SKILL.md",
     "- 7-8: Clear creative vision, unique approach",
     "M1b Originality 7-8"),
    ("commands/gan-design.md",
     '- Evaluator prompt emphasizes "would this win a design award?" over "do all features work?"',
     "M1c evaluator-prompt line"),
]


def main():
    with open(BUILD_SH) as f:
        sh = f.read()
    assert "fix13c: dry-run #15 minors" not in sh, "fix13c block already in build.sh — refusing (idempotency guard)"
    assert STEP5_ANCHOR in sh, "STEP 5 anchor not found in build.sh"
    for rel, old, label in PREFLIGHT:
        p = os.path.join(BUILT, rel)
        t = open(p).read()
        n = t.count(old)
        assert n == 1, f"preflight {label}: anchor count={n} (expected 1) in {rel}"
        print(f"preflight OK: {label}")
    sh = sh.replace(STEP5_ANCHOR, "\n" + BLOCK + STEP5_ANCHOR, 1)
    with open(BUILD_SH, "w") as f:
        f.write(sh)
    print("fix13c block inserted into build.sh (LAST, just before STEP 5)")


if __name__ == "__main__":
    main()
