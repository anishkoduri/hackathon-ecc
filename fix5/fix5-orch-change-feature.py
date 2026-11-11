# --- Fix program #5, Batch 2: orch-change-feature — removal re-upload /
# redeploy conditionality, blocked-branch routing, step-3 cap ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block to be placed LAST in build.sh, just before STEP 5, after all
# prior patches, whose old-strings the substitutions below are anchored on
# (i.e. against the CURRENT built text in
# hackathon-ecc/skills/orch-change-feature/SKILL.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. Covers Fix-5 Batch 2 items B2, M2, M4, Audit M1 (+ step-6
# coherence for B2).
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Audit M1: step 3 dangling-reference fix had no cap (step 4 has the
  # 2-round cap). Cap: one fix per found reference, then re-grep once; if
  # new references keep appearing after 2 passes, mark blocked and skip
  # to step 6 (the report delivery) instead of looping unboundedly.
  ("skills/orch-change-feature/SKILL.md",
   "3. Verify nothing still references the removed code, routes, UI, or database objects — grep the repo for the feature's identifiers (component, function, route, and table/column names) and check every file in the final-report inventory's entry for the feature — and fix or remove any dangling references.",
   "3. Verify nothing still references the removed code, routes, UI, or database objects — grep the repo for the feature's identifiers (component, function, route, and table/column names) and check every file in the final-report inventory's entry for the feature — and fix or remove any dangling references, with a CAP of 2 passes: one fix per found reference, then re-grep once; if new references keep appearing after 2 passes, mark the removal blocked in the final report (with the still-dangling references as evidence) and skip to step 6 and deliver the updated final report — never loop unboundedly on dangling references."),
  # M4: step 4's blocked branch said "stop" without routing to step 6,
  # which delivers the updated final report as the reply (the done
  # signal). Add the explicit skip-to-step-6 routing.
  ("skills/orch-change-feature/SKILL.md",
   "mark the removal blocked in the final report (with the failing test or the broken behaviour as evidence), stop, and leave the deletion uncommitted.",
   "mark the removal blocked in the final report (with the failing test or the broken behaviour as evidence), stop, and leave the deletion uncommitted — then skip to step 6 and deliver the updated final report."),
  # M2: step 5 assumed a git-linked deploy ("re-deploy by pushing the
  # removal commit to `main`"), but no first-build step creates a GitHub
  # repo, sets a git remote, or links Vercel to git (deploy-fast's Vercel
  # CLI deploy links the local folder, not git). Conditional: push only
  # if a git remote is linked to the deploy; otherwise redeploy via the
  # path deploy-fast established in the first build. If neither exists,
  # the existing blocked-deploy handling applies.
  ("skills/orch-change-feature/SKILL.md",
   "5. After the commit, re-deploy by pushing the removal commit to `main` — the git-linked deploy fires from that push (`deploy-fast`). That push redeploys ONLY the Vercel frontend: a split backend does NOT redeploy from it — redeploy the Railway API/backend separately with `railway up` from the backend directory, and apply any migration with `supabase db push` (both per `deploy-fast`, split-backend redeploy).",
   "5. After the commit, re-deploy: if the project has a git remote linked to the deploy, push the removal commit to `main` — the git-linked deploy fires from that push (`deploy-fast`); otherwise redeploy via the path `deploy-fast` established in the first build (Vercel CLI link / `railway up` / `supabase db push`). Do not assume a git remote exists — no first-build step creates a GitHub repo, sets a git remote, or links Vercel to git (deploy-fast's Vercel CLI deploy links the local folder, not git). If neither a git-linked deploy nor a deploy-fast path exists, the blocked-deploy handling below applies. A push redeploys ONLY the Vercel frontend: a split backend does NOT redeploy from it — redeploy the Railway API/backend separately with `railway up` from the backend directory, and apply any migration with `supabase db push` (both per `deploy-fast`, split-backend redeploy)."),
  # M2 follow-through: the downstream "After the push, wait for the
  # deploy to be ready" assumed a push happened; reword to the redeploy
  # so the no-git-remote branch reads coherently.
  ("skills/orch-change-feature/SKILL.md",
   "After the push, wait for the deploy to be ready before re-filming: poll the deployed app until it serves the new version (no removed feature, no dangling references), with a BOUNDED wait — check every ~30s, stop after ~5 minutes.",
   "After the redeploy, wait for the deploy to be ready before re-filming: poll the deployed app until it serves the new version (no removed feature, no dangling references), with a BOUNDED wait — check every ~30s, stop after ~5 minutes."),
  # B2 (BLOCKING): step 5 said "re-upload the new video to the same
  # YouTube/Vimeo host" — but nothing in the first build ever uploads the
  # video anywhere (no YouTube/Vimeo upload skill, command, CLI, or step
  # exists, and the first build never runs devpost-autofiller), so there
  # is no submission and no hosted video to re-upload to. The first
  # build CANNOT upload (it needs the user's YouTube/Devpost account —
  # no credentials, no tool), so no upload mechanism is invented here.
  # Conditional instead: re-upload ONLY if a hosted video link exists
  # (Devpost submission, README, or final report); ELSE record the honest
  # hosting note in the final report and deliver it. Never claim a
  # re-upload happened when it did not. The done-condition ("the demo
  # video reflects the removal") is satisfied by the re-filmed LOCAL
  # video + the honest hosting note, not by a phantom upload.
  ("skills/orch-change-feature/SKILL.md",
   "After re-filming, re-upload the new video to the same YouTube/Vimeo host (upload HOURS before the deadline — processing can take several hours, per `devpost-autofiller`) and update the video LINK wherever it appears (the Devpost submission and the README if it embeds it) — text updates alone leave the judge-visible artefact stale, so the link must point at the re-uploaded video, not the pre-removal one, and update the stage ledger (`.hackathon/run-ledger.md`),",
   "After re-filming, IF a hosted video link exists (in the Devpost submission, the README, or the final report), re-upload the new video to the same YouTube/Vimeo host (upload HOURS before the deadline — processing can take several hours, per `devpost-autofiller`) and update the video LINK wherever it appears (the Devpost submission and the README if it embeds it) — text updates alone leave the judge-visible artefact stale, so the link must point at the re-uploaded video, not the pre-removal one; ELSE (no hosted video link exists — the first build never uploads the video anywhere, so there is nothing to re-upload to) record in the final report \"video re-filmed locally at <path>, not yet hosted — upload it and update the link at <location>\" and deliver that report. Never claim a re-upload happened when it did not. The removal's done-condition (\"the demo video reflects the removal\") is satisfied by the re-filmed LOCAL video + the honest hosting note, not by a phantom upload. Then update the stage ledger (`.hackathon/run-ledger.md`),"),
  # B2 coherence in step 6: the final report lists the re-uploaded video
  # link only when one exists; otherwise it carries the honest hosting
  # note from step 5.
  ("skills/orch-change-feature/SKILL.md",
   "Update `docs/final-report.md` first (feature-to-files inventory plus what was removed, anything blocked, and the re-uploaded video link), then deliver the updated report as the reply.",
   "Update `docs/final-report.md` first (feature-to-files inventory plus what was removed, anything blocked, and the re-uploaded video link if a hosted video existed, else the honest hosting note from step 5 — \"video re-filmed locally at <path>, not yet hosted\"), then deliver the updated report as the reply."),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix5 batch 2: orch-change-feature B2 + M2 + M4 + Audit M1 applied")
PYEOF
