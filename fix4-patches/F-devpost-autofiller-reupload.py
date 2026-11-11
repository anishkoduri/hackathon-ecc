# --- Fix program #4, Batch F: re-uploaded video link (skills/devpost-autofiller/SKILL.md) ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block to be placed LAST in build.sh, just before STEP 5, after the
# GATE / carve-out / Batch E / Batch F / fix-program-#3 patches, whose
# old-strings the substitutions below are anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/skills/devpost-autofiller/SKILL.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. Gap 13 (removal side): the demo video is a LINK (:10), so after a
# removal the re-filmed video must be re-uploaded AND the link on the
# submission updated — a text-only update leaves judges watching the stale
# pre-removal video. The hours-early processing note (:89-93) applies to
# the re-upload exactly as it does to the first upload.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  ("skills/devpost-autofiller/SKILL.md",
   "the demo video is a **link** to a publicly-hosted YouTube/Vimeo video, not an upload.",
   "the demo video is a **link** to a publicly-hosted YouTube/Vimeo video, not an upload. If a feature is removed (or anything else changes) after the video was uploaded, re-upload the re-filmed video and update the link on the submission — a text-only update leaves judges watching the stale pre-removal video. Re-upload HOURS before the deadline: processing can take several hours, so a last-minute re-upload may still be processing when judging starts."),
  ("skills/devpost-autofiller/SKILL.md",
   r'''[ ] Video uploaded HOURS early — YouTube processing can take "a few minutes to
    several hours" (Devpost's words), and the deadline doesn't care''',
   r'''[ ] Video uploaded HOURS early — YouTube processing can take "a few minutes to
    several hours" (Devpost's words), and the deadline doesn't care
[ ] After any removal or re-film, the video LINK on the submission points at the re-uploaded video (not the pre-removal one) — re-upload hours early, the same processing delay applies'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("batch F fix4: devpost-autofiller re-uploaded video link applied")
PYEOF
