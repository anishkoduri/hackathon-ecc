#!/usr/bin/env python3
"""Fix program #13c — fix the 2 minors from dry-run #15 (Audit #43 was clean).

Staged-source edit (durable source of truth; build.sh copies it verbatim):
  M2  round2-skills/polish-pass/reference/impeccable-critique.md :222 —
      example critique question offers "warmer/bolder/more playful" as tonal
      options; "bolder" as a style direction contradicts the "more, not
      bolder" posture. Reword to "warmer / more playful / more distinctive".
      (Upstream template wording — reworded in the staged copy only.)

No-staged-source files (orch-build-mvp, gan-style-harness, gan-design are
upstream ECC patched at build time) are patched by the fix13c build.sh block
inserted by fix13c-assemble.py (M1a, M1b, M1c).

All substitutions assert count==1 before any write; on failure the script
exits non-zero having written nothing.
"""
import os
import sys

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sub(path, old, new, label):
    with open(path) as f:
        text = f.read()
    n = text.count(old)
    assert n == 1, f"{label}: anchor count={n} (expected 1) in {path}: {old[:80]!r}"
    text = text.replace(old, new)
    with open(path, "w") as f:
        f.write(text)
    print(f"applied {label}")


# ---------------------------------------------------------------- M2
crit = os.path.join(PLUGIN_ROOT, "round2-skills/polish-pass/reference/impeccable-critique.md")
sub(crit,
    "should it feel warmer/bolder/more playful?",
    "should it feel warmer / more playful / more distinctive?",
    "M2 critique tonal options")
