# --- Batch B (fix program #4): inline first-build carve-out on the empty-$ARGUMENTS ask in the four orch-* commands ---
# Dry-run minor 30: commands/orch-add-feature.md, orch-change-feature.md,
# orch-fix-defect.md and orch-refine-code.md all say "If `$ARGUMENTS` is empty,
# ask the user ..." with no inline carve-out (commands/orch-build-mvp.md has
# one — "do NOT ask ... default to docs/decision-record.md + docs/scope.md").
# This block adds the same one-line carve-out to each of the four, in the
# orch-build-mvp wording: during a hackathon first build after grill-me, or a
# one-prompt removal of a first-build feature, do NOT ask — proceed on the
# decision record + scope (or the raw prompt with a stated assumption if
# neither exists). Same placement rule as the GATE / Batch F blocks: this block
# runs LAST, just before STEP 5, after all earlier patches. Each substitution
# asserts exactly one match against the CURRENT built text.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
CARVE = " — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where you do NOT ask: proceed on `docs/decision-record.md` + `docs/scope.md` (or the raw prompt with a stated assumption if neither exists)."
subs = [
  ("commands/orch-add-feature.md",
   "If `$ARGUMENTS` is empty, ask the user what capability to add.",
   "If `$ARGUMENTS` is empty, ask the user what capability to add." + CARVE),
  ("commands/orch-change-feature.md",
   "If `$ARGUMENTS` is empty, ask the user what behavior should change.",
   "If `$ARGUMENTS` is empty, ask the user what behavior should change." + CARVE),
  ("commands/orch-fix-defect.md",
   "If `$ARGUMENTS` is empty, ask the user to describe the defect.",
   "If `$ARGUMENTS` is empty, ask the user to describe the defect." + CARVE),
  ("commands/orch-refine-code.md",
   "If `$ARGUMENTS` is empty, ask the user what to refine.",
   "If `$ARGUMENTS` is empty, ask the user what to refine." + CARVE),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("orch-* commands patched with first-build carve-out on empty $ARGUMENTS")
PYEOF
