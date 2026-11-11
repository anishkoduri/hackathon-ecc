# Batch E (fix program #4): less-flat-ui — texture in service of the wow moment.
# Source is NOT staged in hackathon-plugin: build.sh line 223 copies it fresh
# from ~/workspace/cursor-skills/less-flat-ui/ (the global Cursor skill) on
# every build, so this fix lives here as a patch block placed LAST — just
# before STEP 5 — after the GATE / carve-out / Batch E / Batch F /
# fix-program-#3 patches. The substitution below is anchored on the CURRENT
# built text (identical to ~/workspace/cursor-skills/less-flat-ui/SKILL.md;
# no build.sh patch touches skills/less-flat-ui/SKILL.md).
# Never edit hackathon-ecc/ directly, and do not edit the global
# ~/workspace/cursor-skills/less-flat-ui/ copy (it is shared outside this
# plugin). The substitution asserts exactly one match. The coordinator
# inserts this block last, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Design Decision 7 (design part) — texture in service of the wow moment,
  # not decoration: apply treatments where they amplify the captivating
  # moment; never texture for its own sake. Placed in the Rules list, next
  # to "Apply all that fit, then edit down."
  ("skills/less-flat-ui/SKILL.md",
   r'''- **Apply all that fit, then edit down.** Layer every fitting treatment, then look at the result: if it reads busy or muddy, remove the weakest treatment and check again. Stop as soon as it reads clean. Restraint is applied at the end, not the start.''',
   r'''- **Apply all that fit, then edit down.** Layer every fitting treatment, then look at the result: if it reads busy or muddy, remove the weakest treatment and check again. Stop as soon as it reads clean. Restraint is applied at the end, not the start.
- **Texture in service of the wow moment, not decoration:** apply treatments where they amplify the page's captivating moment; never texture for its own sake — if a treatment does not make the memorable moment stronger, leave that surface flat.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("batch E less-flat-ui captivating bar applied")
PYEOF
