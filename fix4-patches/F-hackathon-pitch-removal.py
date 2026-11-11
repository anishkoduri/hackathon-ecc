# --- Fix program #4, Batch F: pitch refresh on removal (skills/hackathon-pitch/SKILL.md) ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block to be placed LAST in build.sh, just before STEP 5, after the
# GATE / carve-out / Batch E / Batch F / fix-program-#3 patches, whose
# old-strings the substitution below is anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/skills/hackathon-pitch/SKILL.md —
# including the Batch F wave-2 canonical-lengths sentence on the storyboard
# item). Never edit hackathon-ecc/ directly. The substitution asserts
# exactly one match. Minor 28b (skill side): hackathon-pitch owns the pitch
# narrative, scripts, and demo storyboard (hackathon-mode §6), so its own
# text must say the pitch is refreshed when orch-change-feature step 5
# removes a feature — otherwise the pitch keeps promising a feature that
# no longer exists.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  ("skills/hackathon-pitch/SKILL.md",
   "3. **The demo storyboard.** Golden path only: one user, one task, under 90 seconds, narrated click by click, with the \"wow moment\" marked. This is the pitch storyboard (under 90s) — not the live demo storyboard (2–4 min) and not the demo video (1:30–1:50, pitch-deck-video / /demo). Demo lengths are canonical in hackathon-mode §6: the live demo storyboard is 2–4 min; the demo video is 1:30–1:50; the pitch storyboard is under 90s. Where another skill states a different length, the hackathon-mode statement governs.",
   "3. **The demo storyboard.** Golden path only: one user, one task, under 90 seconds, narrated click by click, with the \"wow moment\" marked. This is the pitch storyboard (under 90s) — not the live demo storyboard (2–4 min) and not the demo video (1:30–1:50, pitch-deck-video / /demo). Demo lengths are canonical in hackathon-mode §6: the live demo storyboard is 2–4 min; the demo video is 1:30–1:50; the pitch storyboard is under 90s. Where another skill states a different length, the hackathon-mode statement governs. After a feature removal (`orch-change-feature` step 5), refresh the pitch narrative, scripts, and this storyboard so nothing promises the removed feature: cut its beats, re-cut the scripts to their word targets, and re-mark the wow moment on what remains."),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("batch F fix4: hackathon-pitch refresh on removal applied")
PYEOF
