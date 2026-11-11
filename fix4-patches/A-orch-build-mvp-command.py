# --- Fix program #4, Batch A: commands/orch-build-mvp.md — rewrite to match
# the skill's 9 steps + record/scope-default input ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block placed LAST in build.sh, just before STEP 5, after the GATE /
# carve-out / Batch E / Batch F / Fix-program-#3 Batch A patches, whose
# old-strings the substitutions below are anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/commands/orch-build-mvp.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. The patch agent inserts this block last, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # Intro: standalone only; record/scope first, spec doc is the fallback.
  ("commands/orch-build-mvp.md", r'''Manually launch the **orch-build-mvp** orchestrator: turn an SDD/PRD/system-design
document into a running vertical slice.''', r'''Manually launch the **orch-build-mvp** orchestrator (standalone only — user-invoked): turn the record/scope (or an SDD/PRD/system-design document as the standalone fallback) into a running vertical slice.'''),
  # Usage: the doc path is optional — the standalone fallback, not the input.
  ("commands/orch-build-mvp.md", r'''```
/orch-build-mvp <path to design/spec doc>
```

Examples:

```
/orch-build-mvp civicpulse/docs/SDD-v0.6.md
```''', r'''```
/orch-build-mvp [path to design/spec doc — optional, standalone fallback only]
```

Examples:

```
/orch-build-mvp
/orch-build-mvp civicpulse/docs/SDD-v0.6.md
```'''),
  # Invoke line: record/scope default; $ARGUMENTS only the fallback; the
  # numbered steps ARE orch-pipeline Phases 0–6, each once.
  ("commands/orch-build-mvp.md", r'''Invoke the `orch-build-mvp` skill with `$ARGUMENTS` as the doc path. The skill
(via the shared `orch-pipeline` engine, full pipeline incl. Scaffold) will:''', r'''Invoke the `orch-build-mvp` skill — standalone only; orchestrate never invokes it in the same run. Input is the record/scope by default (`docs/decision-record.md` + `docs/scope.md`); a doc path in `$ARGUMENTS` is only the standalone fallback when neither record file exists. The skill (via the shared `orch-pipeline` engine — its numbered steps ARE orch-pipeline Phases 0–6, each once; orch-build-mvp step 1 runs Phases 0–2 only, never the full engine) will:'''),
  # Rewrite the 6-item list as the skill's 9 steps (expansion Phases 0–3,
  # Reconcile step 5, Phase 5 verification in step 6, Phase 6 intake in
  # step 9, final report step 9) — the command must not describe a
  # different pipeline from the skill. Step 8 films the LOCAL app only.
  ("commands/orch-build-mvp.md", r'''1. Read `docs/decision-record.md` + `docs/scope.md` by default (or the spec doc in `$ARGUMENTS` if one was given); extract scope, locked decisions, and a feature list ordered as
**thin vertical slices** (one end-to-end path first). → **GATE 1** (approve slice plan; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).
2. Scaffold the first end-to-end slice.
3. Reuse the GAN harness: translate the SDD into `gan-harness/spec.md` +
   `eval-rubric.md`, then drive `/gan-build "<brief>" --skip-planner`
   (generator → evaluator loop) until the score passes or plateaus.
4. `code-reviewer` (+ `security-reviewer` on any security-trigger slice), then
   commit the scaffold and each slice as separate `feat:` commits. → **GATE 2** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).
5. Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — the demo video is a required deliverable; film the deployed app (or the local dev server if deploy was static-only or blocked, noted in the final report).
6. Deliver the final report — the done signal: write it to `docs/final-report.md` in the project AND deliver it as the reply — what was built, every assumption, anything blocked or skipped, and anything the user may want to remove, with the files for each removable item.''', r'''1. Read `docs/decision-record.md` + `docs/scope.md` by default (the spec doc in `$ARGUMENTS` only as the standalone fallback when neither record file exists); extract scope, locked decisions, and a feature list ordered as
**thin vertical slices** (one end-to-end path first). This is orch-build-mvp step 1 = orch-pipeline Phases 0–2 only — it never runs the full engine. → **GATE 1** (approve slice plan; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).
2. Expansion Phases 0–3 (ground, brainstorm, consolidate, planner pass) produce the planner-approved list — no user approval gate. Expansion Phases 0–3 run ONCE per run, here in a standalone run; expansion Phases 4–6 run inside the build below, never whole here.
3. Scaffold the first end-to-end slice (orch-pipeline Phase 3).
4. Reuse the GAN harness (orch-pipeline Phase 4): translate the record/scope (or the fallback spec doc) into `gan-harness/spec.md` +
   `eval-rubric.md`, then drive `/gan-build "<brief>" --skip-planner`
   (generator → evaluator loop) until the score passes or plateaus. Expansion Phase 4 implementers build alongside the MVP slices here.
5. Reconcile after each wave (orch-build-mvp step 5 owns collision reconciliation).
6. Verify (orch-pipeline Phase 5 Review + expansion Phase 5): `code-reviewer` (+ `security-reviewer` on any security-trigger slice), then the whole-build checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature.
7. Commit the scaffold and each slice as separate `feat:` commits (orch-pipeline Phase 6). → **GATE 2** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).
8. Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — the demo video is a required deliverable; film the LOCAL app from the project dir only, never a deployed URL (if deploy was static-only or blocked, noted in the final report).
9. Deliver the final report — the done signal (expansion Phase 6 feeds it): write it to `docs/final-report.md` in the project AND deliver it as the reply — what was built, every assumption, anything blocked or skipped, and anything the user may want to remove, with the files for each removable item.'''),
  # $ARGUMENTS is only the standalone fallback, never the default.
  ("commands/orch-build-mvp.md", r'''If `$ARGUMENTS` is empty, do NOT ask the user for a path — never ask during a hackathon first build: default to `docs/decision-record.md` + `docs/scope.md` (or the raw prompt with a stated assumption if neither exists).''', r'''If `$ARGUMENTS` is empty, do NOT ask the user for a path — never ask during a hackathon first build: default to `docs/decision-record.md` + `docs/scope.md` (or the raw prompt with a stated assumption if neither exists). A doc path in `$ARGUMENTS` is only the standalone fallback, never the default.'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix4 batch A: orch-build-mvp command rewritten to the skill's 9 steps")
PYEOF
