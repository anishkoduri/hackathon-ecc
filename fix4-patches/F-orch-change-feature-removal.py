# --- Fix program #4, Batch F: removal delivery + failure branches (orch-change-feature) ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block to be placed LAST in build.sh, just before STEP 5, after the
# GATE / carve-out / Batch E / Batch F / fix-program-#3 patches, whose
# old-strings the substitutions below are anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/skills/orch-change-feature/SKILL.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. Covers dry-run #3 gaps 10-13 and minors 26-28 (removal side).
# Redirect note: the demo video is made from the CODE (local app), never a
# deployed URL — every re-film line below films local (APP_DIR/project dir).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Minor 26: step 4 failure branch + fix-loop cap. A failing TEST suite
  # follows a DIFFERENT rule from the orch-pipeline review-findings rule
  # (unresolvable CRITICAL finding -> recorded as blocked, commit proceeds
  # under auto-approval): a review finding is about the diff's quality,
  # but a failing test suite means the app itself is broken, so the commit
  # does NOT proceed — the removal is blocked instead.
  ("skills/orch-change-feature/SKILL.md",
   "4. Run the tests and the app to confirm the removal did not break anything else, then commit under the usual gates (auto-approved during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature).",
   "4. Run the tests and the app to confirm the removal did not break anything else, then commit under the usual gates (auto-approved during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature). If the tests fail or the app breaks after the deletion, fix with a CAP of 2 fix rounds: after 2 rounds, if it is still broken, do NOT commit it broken and do NOT loop unboundedly — mark the removal blocked in the final report (with the failing test or the broken behaviour as evidence), stop, and leave the deletion uncommitted. A failing TEST suite follows a DIFFERENT rule from the orch-pipeline review-findings rule (an unresolvable CRITICAL review finding is recorded as blocked and the commit proceeds under auto-approval): a review finding is about the diff's quality, but a failing test suite means the app itself is broken, so the commit does NOT proceed — the removal is blocked instead."),
  # Gap 12: split backends — the push to main redeploys ONLY the Vercel
  # frontend; the Railway API/backend needs its own redeploy (`railway up`)
  # and migrations need `supabase db push` (both per deploy-fast).
  ("skills/orch-change-feature/SKILL.md",
   "5. After the commit, re-deploy by pushing the removal commit to `main` — the git-linked deploy fires from that push (`deploy-fast`).",
   "5. After the commit, re-deploy by pushing the removal commit to `main` — the git-linked deploy fires from that push (`deploy-fast`). That push redeploys ONLY the Vercel frontend: a split backend does NOT redeploy from it — redeploy the Railway API/backend separately with `railway up` from the backend directory, and apply any migration with `supabase db push` (both per `deploy-fast`, split-backend redeploy)."),
  # Minor 27 (Supabase CLI auth named explicitly in blocked-deploy
  # handling) + Gap 11 (bounded deploy-ready wait/poll before re-filming,
  # local-film fallback, never film a stale deployed URL) + Minor 28a
  # ("shots.json FIRST" = first relative to the re-film, not first in
  # step 5) + Gap 13 (re-upload the re-filmed video + update the video LINK).
  ("skills/orch-change-feature/SKILL.md",
   "Do not run an interactive deploy CLI for this step: if the deploy CLI is unauthenticated (or the project has no git-linked deploy), do not wait for a login — the removal still counts as done-with-blocked-deploy; note the blocked deploy in the final report and move on, update `shots.json` FIRST — remove the feature's shots, selectors, and narration lines — then re-film via `/demo --rebuild`,",
   "Do not run an interactive deploy CLI for this step: if a deploy CLI is unauthenticated (or the project has no git-linked deploy), do not wait for a login — the removal still counts as done-with-blocked-deploy; note the blocked deploy in the final report and move on. That covers the Vercel/Railway deploy CLIs AND `supabase db push`: an unauthenticated Supabase CLI is blocked-deploy handling too — record it as blocked in the final report with the exact command and error, never stall on an interactive `supabase login`. After the push, wait for the deploy to be ready before re-filming: poll the deployed app until it serves the new version (no removed feature, no dangling references), with a BOUNDED wait — check every ~30s, stop after ~5 minutes. If it never becomes ready in that bound, film local and note it in the final report — never film a stale deployed URL, and never wait unboundedly. Then, before re-filming, update `shots.json` FIRST relative to the re-film — remove the feature's shots, selectors, and narration lines (FIRST means first before the re-film, not first in this step overall: the push/re-deploy above precedes it) — then re-film via `/demo --rebuild`, which films the LOCAL app from the project dir (`APP_DIR`/project root), never a deployed URL; if the deploy was blocked, film local anyway and note in the final report that the video shows the local app, not the deployed one. After re-filming, re-upload the new video to the same YouTube/Vimeo host (upload HOURS before the deadline — processing can take several hours, per `devpost-autofiller`) and update the video LINK wherever it appears (the Devpost submission and the README if it embeds it) — text updates alone leave the judge-visible artefact stale, so the link must point at the re-uploaded video, not the pre-removal one,"),
  # Minor 28b: hackathon-pitch joins the step-5 update list — the pitch
  # narrative, scripts, and demo storyboard must stop promising the
  # removed feature.
  ("skills/orch-change-feature/SKILL.md",
   "the README (`readme-writer`), and the Devpost submission (`devpost-autofiller`) if one exists",
   "the README (`readme-writer`), the pitch narrative, scripts, and demo storyboard (`hackathon-pitch` — refresh them so the pitch no longer promises the removed feature), and the Devpost submission (`devpost-autofiller`) if one exists"),
  # Gap 10: the updated final report IS DELIVERED as the reply after a
  # removal — a new step 6. The first-build-only delivery rule in
  # hackathon-mode §7 / orchestrate does NOT cover removals; this step
  # is what covers them.
  ("skills/orch-change-feature/SKILL.md",
   "a removal is not done until the deployed app, the demo video, the ledger, and the inventory all reflect it; none of them may go stale.",
   "a removal is not done until the deployed app, the demo video, the ledger, and the inventory all reflect it; none of them may go stale.\n6. Deliver the updated final report as the reply — this is the done signal for the removal. Update `docs/final-report.md` first (feature-to-files inventory plus what was removed, anything blocked, and the re-uploaded video link), then deliver the updated report as the reply. The first-build-only delivery rule in hackathon-mode §7 / orchestrate covers the first build's final report, NOT removals — this step is what covers removals, so a removal is not done until this delivery has happened.\n\n"),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("batch F fix4: orch-change-feature removal delivery + failure branches applied")
PYEOF
