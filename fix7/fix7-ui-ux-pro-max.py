# Fix program #7: ui-ux-pro-max — M1 no-landing fallback for the
# design-token handoff.
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block placed LAST, just before STEP 5, after the GATE / carve-out /
# Batch E / Batch F / fix-program-#4 / master-prompt / fix5 / fix6 patches,
# whose old-strings the substitutions below are anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/skills/ui-ux-pro-max/SKILL.md, as
# written by fix6 batch 4).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. The coordinator inserts this block last, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # M1 — no-landing fallback: the tokens file has exactly one writer (the
  # landing slice) and ui-ux-pro-max said only "wait for it" when the file
  # does not exist yet. In a dashboard-only app there is no landing slice,
  # so the gate is never satisfied. The fallback: if there is no landing
  # slice in this build (or it is blocked), the first UI slice defines the
  # system itself in MASTER.md and writes docs/design-tokens.md from it.
  ("skills/ui-ux-pro-max/SKILL.md",
   r'''(The landing slice writes `docs/design-tokens.md` at the end of `design-taste-frontend` step 4a; if the file does not exist yet, the landing slice has not run — wait for it, do not guess the tokens.)''',
   r'''(The landing slice writes `docs/design-tokens.md` at the end of `design-taste-frontend` step 4a; if the file does not exist yet, the landing slice has not run — wait for it, unless there is no landing slice in this build (dashboard-only app, or the landing slice is blocked): then define the system yourself in MASTER.md and write `docs/design-tokens.md` from it — you are the tokens file's writer then, and that file is the single source of truth. Never guess the tokens.)'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix7: ui-ux-pro-max M1 no-landing fallback applied")
PYEOF
