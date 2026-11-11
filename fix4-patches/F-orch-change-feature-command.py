# --- Fix program #4, Batch F: removal procedure pointer (commands/orch-change-feature.md) ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block to be placed LAST in build.sh, just before STEP 5, after the
# GATE / carve-out / Batch E / Batch F / fix-program-#3 patches, whose
# old-strings the substitution below is anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/commands/orch-change-feature.md).
# Never edit hackathon-ecc/ directly. The substitution asserts exactly one
# match. Mirrors the skill-side removal steps (F-orch-change-feature-removal.py)
# so the command's one-line summary no longer omits the failure branch,
# the split-backend redeploy, the bounded deploy-ready wait, the local
# re-film, the video re-upload + link update, or the final-report delivery.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  ("commands/orch-change-feature.md",
   "follow the skill's `Removing a feature` section instead of the change steps below: delete, verify no references remain, commit, then re-deploy, re-film, and update the docs and inventory.",
   "follow the skill's `Removing a feature` section instead of the change steps below: delete, verify no references remain, commit (or mark blocked and stop if the tests fail after deletion — never commit broken, see the skill), then re-deploy (push to `main` for the Vercel frontend + `railway up` for a split Railway backend), wait for the deploy to be ready (bounded wait, local-film fallback — never film a stale deployed URL), update `shots.json` before re-filming, re-film locally via `/demo --rebuild`, re-upload the video and update its link, update the docs, inventory, and pitch, and deliver the updated final report as the reply (the done signal for the removal)."),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("batch F fix4: orch-change-feature command removal pointer applied")
PYEOF
