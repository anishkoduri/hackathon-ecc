# --- Fix program #5, Batch 2: orch-build-mvp — standalone alignment:
# narration-key prompt early (B1-standalone), readme-writer invocation
# (M11-standalone), final-report video handoff (B2a-standalone) ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block to be placed LAST in build.sh, just before STEP 5, after all
# prior patches, whose old-strings the substitutions below are anchored on
# (i.e. against the CURRENT built text in
# hackathon-ecc/skills/orch-build-mvp/SKILL.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. Covers Fix-5 Batch 2 items B1-standalone, M11-standalone,
# B2a-standalone (standalone flow only — the orchestrate-driven flow's
# equivalents are handled elsewhere).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # B1-standalone — CHECK FOUND IT BROKEN: the standalone flow had no
  # early narration-key prompt. The only prompt trigger was step 8's
  # `/demo` (commands/demo.md + pitch-deck-video's narration-key prompt),
  # which fires at the END of the run — after scaffold, implement,
  # reconcile, verify, commit, and deploy — with no build left as the
  # "meanwhile" work the B1 principle requires (prompt once, early, right
  # after grill-me; build continues regardless). The /demo prompt itself
  # is non-blocking and the video never aborts (music-only/silent
  # fallback), so nothing stalls — but the prompt was late, not early.
  # Align: prompt once at the START of the standalone run (step 1),
  # non-blocking, env var only, never written to disk; if the key never
  # arrives, music-only/silent with a note. This is the ONE sanctioned
  # user prompt during the standalone run besides grill-me (hackathon-mode
  # §7 carve-out) — never a wait point, never an approval gate. And do
  # NOT re-prompt at step 8 `/demo` time: the single early prompt covers
  # the run; `/demo` uses the key if present, else falls back.
  ("skills/orch-build-mvp/SKILL.md",
   "If neither holds, do not auto-approve with zero recorded decisions and no check: proceed on the raw prompt with a stated assumption — do NOT re-run `grill-me` (see hackathon-mode §7).",
   "If neither holds, do not auto-approve with zero recorded decisions and no check: proceed on the raw prompt with a stated assumption — do NOT re-run `grill-me` (see hackathon-mode §7).\n\n**Narration-key prompt — once, at the start of the standalone run, never blocking.** At the start of the run (step 1), if narration will need a key and none is set (no `ELEVENLABS_API_KEY` in the environment, no MiniMax credentials), issue the single `pitch-deck-video` narration-key prompt once (ElevenLabs free tier — 10,000 characters a month, no credit card — with the free-tier facts), then continue the build immediately without waiting: the prompt never blocks, the key is an env var only and is never written to any file, and if it never arrives the video renders music-only/silent with a note in the final report. This is the ONE sanctioned user prompt during the standalone run besides grill-me itself (hackathon-mode §7 carve-out) — never a wait point, never an approval gate. Do NOT re-prompt at step 8 `/demo` time: the single early prompt covers the run, and `/demo` uses the key if present, else falls back to music-only/silent."),
  # M11-standalone — CHECK FOUND IT MISSING: no step in orch-build-mvp
  # invoked readme-writer (verified: zero "readme" in the built skill).
  # Add the named invocation after the build (deploy + film, step 8) and
  # before the final report (step 9) — same placement logic as the
  # orchestrate flow — so the README exists for devpost-autofiller to
  # draft the Devpost submission from. Step numbering unchanged.
  ("skills/orch-build-mvp/SKILL.md",
   "If deploy was static-only or blocked, the final report notes that — never hard-abort the run for lack of a deployed URL.",
   "If deploy was static-only or blocked, the final report notes that — never hard-abort the run for lack of a deployed URL. After filming, invoke `readme-writer` to write/update the README from the built app, before the final report in step 9 (the README is what `devpost-autofiller` later drafts the Devpost submission from)."),
  # B2a-standalone — CHECK FOUND IT MISSING: step 9 (final report) did
  # not state the video file path or any upload instruction (verified:
  # zero "video" / "YouTube" / "Vimeo" / "Devpost" / "upload" in the
  # built skill outside step 8's filming line). Add the handoff to step
  # 9: the video file path AND the instruction to upload the file to
  # YouTube/Vimeo and paste the link into Devpost — the first build never
  # uploads the video anywhere (it has no YouTube/Devpost account
  # access), so the path + upload instruction is how the video reaches
  # the submission.
  ("skills/orch-build-mvp/SKILL.md",
   "The report also includes: important design + engineering decisions (what was chosen, what was rejected, and why); the tests and visual checks actually performed (only checks that really ran, with their outcome — never a confident description in place of a check that did not happen); and the highest-value next improvements (prioritized by impact/effort/risk).",
   "The report also includes: important design + engineering decisions (what was chosen, what was rejected, and why); the tests and visual checks actually performed (only checks that really ran, with their outcome — never a confident description in place of a check that did not happen); and the highest-value next improvements (prioritized by impact/effort/risk). The report also states the demo video handoff: the video file path (the local filmed video file) AND the instruction \"upload this file to YouTube/Vimeo and paste the link into Devpost\" — the first build never uploads the video anywhere (it has no YouTube/Devpost account access), so the file path + upload instruction is how the video reaches the submission."),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix5 batch 2: orch-build-mvp B1-standalone + M11-standalone + B2a-standalone applied")
PYEOF
