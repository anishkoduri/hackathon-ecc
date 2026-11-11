# Master prompt (fix program #4): orch-build-mvp — adversarial audit as a
# distinct named step inside step 6, + final-report format additions in
# step 9 (design/engineering decisions, tests and visual checks actually
# performed, highest-value next improvements).
# orch-build-mvp has NO staged source: its content is created and patched
# inside build.sh only — this fix lives here as a patch block placed LAST —
# just before STEP 5 — after the GATE / carve-out / Batch E / Batch F /
# fix-program-#3 patches and the fix4 Batch A block, whose old-strings the
# substitution below is anchored on (i.e. against the CURRENT built text).
# Never edit hackathon-ecc/ directly. The substitution asserts exactly one
# match. The coordinator inserts this block last, just before STEP 5.
#
# What it adds, and what it deliberately does NOT duplicate:
# - Step 6 already has `code-reviewer` (+ `security-reviewer` on any
#   security-trigger slice) reviewing each slice, and the capped 2-round
#   fix loop. What was missing was the adversarial step itself: the
#   skeptical staff-engineer stance, severity (blocker/major/minor), and
#   the confirmed-vs-suspected distinction. The code-reviewer STANCE lives
#   in agents/ecc-code-reviewer.md (MP-code-reviewer.py patch); this step
#   only NAMES the audit as a distinct step inside step 6.
# - Step 9 already lists what was built, assumptions, blocked/skipped, and
#   removals. Added: design + engineering decisions, tests and visual
#   checks actually performed, highest-value next improvements — mirroring
#   the orchestrate final-report format.
# - No approval gate, no wait point, no new agent/skill/file. The
#   one-engine rule is untouched: this step covers standalone
#   orch-build-mvp runs only.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Master prompt — adversarial audit as a distinct named step, inside
  # orch-build-mvp step 6 (after the code-reviewer pass).
  ("skills/orch-build-mvp/SKILL.md",
   r'''Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on.''',
   r'''Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on.

**Adversarial audit (a distinct named step, inside step 6, after the `code-reviewer` pass):** `code-reviewer` (+ `security-reviewer` on any security-trigger slice) audits the built code as a skeptical staff engineer — try to break it, falsify the claimed behaviour. Every finding carries a severity (blocker / major / minor) and is marked **confirmed** (reproduced against the running code) or **suspected** (reasoned but not reproduced) — a suspected finding is never presented as a confirmed defect. Fix blockers and majors inside the capped 2-round fix loop; minors go in the final report.'''),
  # Master prompt — final-report format additions in step 9.
  ("skills/orch-build-mvp/SKILL.md",
   r'''This step covers standalone orch-build-mvp runs only — orchestrate never invokes this skill, so orchestrate never owns this report.''',
   r'''The report also includes: important design + engineering decisions (what was chosen, what was rejected, and why); the tests and visual checks actually performed (only checks that really ran, with their outcome — never a confident description in place of a check that did not happen); and the highest-value next improvements (prioritized by impact/effort/risk).

This step covers standalone orch-build-mvp runs only — orchestrate never invokes this skill, so orchestrate never owns this report.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("master-prompt orch-build-mvp adversarial audit + final-report format applied")
PYEOF
