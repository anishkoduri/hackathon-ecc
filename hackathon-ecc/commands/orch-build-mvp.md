---
description: Orchestrate bootstrapping a working MVP from a design/spec doc — ingest, slice, scaffold, TDD, review, gated commit (reuses the GAN harness). Wrapper for the orch-build-mvp skill.
---

# /orch-build-mvp

**MODEL check (fix #33, MODELSEL_F33):** before anything else — the `orch-pipeline` engine runs its MODEL check first (Step 0, before classifying): if the selected model is Auto, or the model cannot be determined to be a specific model, tell the user to pick a specific model before proceeding; do not silently orchestrate on an unknown fallback.

Manually launch the **orch-build-mvp** orchestrator (standalone only — user-invoked): turn the record/scope (or an SDD/PRD/system-design document as the standalone fallback) into a running vertical slice.

## Usage

```
/orch-build-mvp [path to design/spec doc — optional, standalone fallback only]
```

Examples:

```
/orch-build-mvp
/orch-build-mvp civicpulse/docs/SDD-v0.6.md
```

## What It Does

Invoke the `orch-build-mvp` skill — standalone only; orchestrate never invokes it in the same run. Input is the record/scope by default (`docs/decision-record.md` + `docs/scope.md`); a doc path in `$ARGUMENTS` is only the standalone fallback when neither record file exists. The skill (via the shared `orch-pipeline` engine — its numbered steps ARE orch-pipeline Phases 0–6, each once; orch-build-mvp step 1 runs Phases 0–2 only, never the full engine) will:

1. Read `docs/decision-record.md` + `docs/scope.md` by default (the spec doc in `$ARGUMENTS` only as the standalone fallback when neither record file exists); extract scope, locked decisions, and a feature list ordered as
**thin vertical slices** (one end-to-end path first). This is orch-build-mvp step 1 = orch-pipeline Step 0 (MODEL check + Classify) first, then Phases 0–2 only — it never runs the full engine. → **GATE 1** (approve slice plan; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).
2. Expansion Phases 0–3 (ground, brainstorm, consolidate, planner pass) produce the planner-approved list — no user approval gate. Expansion Phases 0–3 run ONCE per run, here in a standalone run; expansion Phases 4–6 run inside the build below, never whole here.
3. Scaffold the first end-to-end slice (orch-pipeline Phase 3).
4. Reuse the GAN harness (orch-pipeline Phase 4): translate the record/scope (or the fallback spec doc) into `gan-harness/spec.md` +
   `eval-rubric.md`, then drive `/gan-build "<brief>" --skip-planner`
   (generator → evaluator loop) until the score passes or plateaus. Expansion Phase 4 implementers build alongside the MVP slices here.
5. Reconcile after each wave (orch-build-mvp step 5 owns collision reconciliation).
6. Verify (orch-pipeline Phase 5 Review + expansion Phase 5): `code-reviewer` (+ `security-reviewer` on any security-trigger slice), then the whole-build checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature.
7. Commit the scaffold and each slice as separate `feat:` commits (orch-pipeline Phase 6). → **GATE 2** (auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting).
8. Deploy via `deploy-fast`. Do NOT film via `/demo` here — `/demo` runs ONLY when the user invokes it explicitly (or the user's request explicitly asks for a demo video); if the user asked for one, film the LOCAL app from the project dir only, never a deployed URL (if deploy was static-only or blocked, noted in the final report). (fix #22 /demo gate, DEMOGATE_B2C1_F22)
9. Deliver the final report — the done signal (expansion Phase 6 feeds it): write it to `docs/final-report.md` in the project AND deliver it as the reply — what was built, every assumption, anything blocked or skipped, and anything the user may want to remove, with the files for each removable item.

Honor both gates — do not write implementation before Gate 1, do not commit before Gate 2 — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting.

If `$ARGUMENTS` is empty, do NOT ask the user for a path — never ask during a hackathon first build: default to `docs/decision-record.md` + `docs/scope.md` (or the raw prompt with a stated assumption if neither exists). A doc path in `$ARGUMENTS` is only the standalone fallback, never the default.
