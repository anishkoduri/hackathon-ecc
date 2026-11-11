# --- Fix program #4, Batch A: orch-build-mvp — ONE ENGINE PER RUN + phase
# mapping (no step-1 redo) + record/scope-default input + 9-step rewrite ---
# Upstream ECC file, copied fresh on every build — this fix lives here as a
# patch block placed LAST in build.sh, just before STEP 5, after the GATE /
# carve-out / Batch E / Batch F / Fix-program-#3 Batch A patches, whose
# old-strings the substitutions below are anchored on (i.e. against the
# CURRENT built text in hackathon-ecc/skills/orch-build-mvp/SKILL.md).
# Never edit hackathon-ecc/ directly. Each substitution asserts exactly one
# match. The patch agent inserts this block last, just before STEP 5.
python3 - "$PLUGIN_DIR" <<'PYEOF'
import os, sys
base = sys.argv[1]
subs = [
  # DD1 — frontmatter: standalone only; orchestrate never invokes it.
  ("skills/orch-build-mvp/SKILL.md", r'''description: Orchestrate bootstrapping a working MVP from a design or spec document — ingest the SDD/PRD (or the grill-me decision record), plan thin vertical slices, scaffold the first end-to-end slice, then drive a generator-evaluator build loop with review and gated feat commits. Use when a design or spec document must become a running MVP through planned vertical slices. Use when the user explicitly invokes /orch-build-mvp or when orchestrate invokes it for the first build after grill-me — a prose request to build an MVP otherwise belongs to orchestrate, not this skill.''', r'''description: Orchestrate bootstrapping a working MVP from a design or spec document — ingest the grill-me decision record + scope (or a spec doc as standalone fallback), plan thin vertical slices, scaffold the first end-to-end slice, then drive a generator-evaluator build loop with review and gated feat commits. Use when a design or spec document must become a running MVP through planned vertical slices. Use ONLY when the user explicitly invokes /orch-build-mvp — standalone only; orchestrate never invokes it in the same run. A prose request to build an MVP otherwise belongs to orchestrate, not this skill.'''),
  # DD1 — one build engine per run (replaces the Fix-program-#3 wording that
  # said orchestrate "invokes this pipeline").
  ("skills/orch-build-mvp/SKILL.md", r'''**One build engine:** `orchestrate` drives the first build and invokes this pipeline — this skill is the pipeline orchestrate invokes, not a competing engine. The GAN harness (step 3 below) is the implementer loop WITHIN this pipeline (generator → evaluator per slice), not a separate build engine.''', r'''**One build engine per run:** this skill is the STANDALONE pipeline — it runs only when the user invokes `/orch-build-mvp` directly. Orchestrate IS the first-build engine; orchestrate never invokes this skill in the same run, and this skill never runs in a first build orchestrate is driving. One engine per run, never both. The GAN harness (orch-build-mvp step 4 below) is the implementer loop WITHIN this standalone pipeline (generator → evaluator per slice), not a separate build engine.'''),
  # Stale doc-path-first framing, "When to Use": record/scope is the
  # default; a doc path is only the standalone fallback.
  ("skills/orch-build-mvp/SKILL.md", r'''- The user has a **design / spec document** (SDD, PRD, system_design) and wants a
  working vertical slice bootstrapped from it.
- Takes a doc path as its argument, e.g. `civicpulse/docs/SDD-v0.6.md`.''', r'''- The user explicitly invoked `/orch-build-mvp` (standalone run) and wants a working vertical slice bootstrapped from the record/scope — `docs/decision-record.md` + `docs/scope.md` by default.
- A doc path in `$ARGUMENTS` (e.g. `civicpulse/docs/SDD-v0.6.md`) is only the standalone fallback when neither record file exists — the record/scope is the default, never the doc path.'''),
  # Stale doc-path-first framing, phase mask: "0 (read the spec)" + the
  # mask is whole-skill, NOT what step 1 runs (see step 1).
  ("skills/orch-build-mvp/SKILL.md", r'''- **Phase mask:** 0 (read the spec) → 1 → 2 (heavy) → 3 (scaffold) → 4 → 5 → 6.''', r'''- **Phase mask:** 0 (read the record/scope by default; the spec doc in `$ARGUMENTS` is only the standalone fallback) → 1 → 2 (heavy) → 3 (scaffold) → 4 → 5 → 6. The mask lists the phases that run across the whole skill — NOT the phases step 1 runs: orch-build-mvp step 1 runs orch-pipeline Phases 0–2 only (see the phase mapping in step 1).'''),
  # First move: qualify Phase 3 as orch-pipeline Phase 3 / step 3.
  ("skills/orch-build-mvp/SKILL.md", r'''**First move (phase 0 → 2):** read `docs/decision-record.md` + `docs/scope.md` by default — the grill-me decision record and the scope output — and extract scope, locked decisions,
  and the feature list; order it into **thin vertical slices** (one end-to-end
  path first, not all-models-then-all-views). Phase 3 stands up that first slice. If neither record file exists (standalone run, no grill-me), fall back to the doc path in `$ARGUMENTS` or the raw prompt with a stated assumption — never ask the user for a path during a first build.''', r'''**First move (phase 0 → 2):** read `docs/decision-record.md` + `docs/scope.md` by default — the grill-me decision record and the scope output — and extract scope, locked decisions,
  and the feature list; order it into **thin vertical slices** (one end-to-end
  path first, not all-models-then-all-views). Orch-pipeline Phase 3 (orch-build-mvp step 3) stands up that first slice. If neither record file exists (standalone run, no grill-me), fall back to the doc path in `$ARGUMENTS` or the raw prompt with a stated assumption — never ask the user for a path during a first build.'''),
  # Audit #31 blocking 3 — step 1 must NOT run the full orch-pipeline
  # engine (phase mask 0→6) and then have later steps redo Implement /
  # Review / Commit. Explicit phase mapping: the numbered steps ARE the
  # pipeline — step 1 is Phases 0–2 only; steps 3/4/6/7 are Phases 3–6,
  # each running once. Nothing is run twice and nothing is redone.
  ("skills/orch-build-mvp/SKILL.md", r'''1. Run the `orch-pipeline` engine with the settings above.''', r'''1. Run orch-pipeline Phases 0–2 ONLY (Intake/Research/Plan) with the settings above — read the record/scope, extract scope, locked decisions, and the feature list, order it into thin vertical slices, ending at Gate 1 (slice plan). This step does NOT run the full orch-pipeline engine (phase mask 0→6): the later numbered steps ARE orch-pipeline Phases 3–6, each running once — orch-build-mvp step 3 is Phase 3 (Scaffold), step 4 is Phase 4 (Implement, GAN loop), step 6 is Phase 5 (Review), step 7 is Phase 6 (Commit). Nothing is run twice and nothing is redone.'''),
  # Expansion wiring, standalone flow: Phases 0–3 run ONCE per run, here;
  # Phase 4 = step 4 GAN loop; Phase 5 = step 6; Phase 6 = step 9.
  # Numbering qualified throughout (expansion Phase N vs step N).
  ("skills/orch-build-mvp/SKILL.md", r'''2. **Expand automatically during the first build — split, not whole.** Right after scoping and before building the slices, run `feature-expansion` Phases 0–3 (ground, brainstorm, consolidate, planner pass): it brainstorms features and tools in line with the grill-me decision record, the planner approves, tweaks, or rejects each one, producing the approved list — with no user approval gate. Phases 4–6 run INSIDE this build, not here: Phase 4 implementers build the approved expansions alongside the MVP slices (the step 3 GAN loop drives each slice, expansions included), Phase 5 verification runs after the MVP is built, and Phase 6 feeds the final report (step 9). The skill is never invoked whole at this step. The user removes anything unwanted with one prompt afterward.''', r'''2. **Expand automatically — split, not whole (standalone run).** Right after scoping and before building the slices, run `feature-expansion` Phases 0–3 (ground, brainstorm, consolidate, planner pass): it brainstorms features and tools in line with the grill-me decision record, the planner approves, tweaks, or rejects each one, producing the approved list — with no user approval gate. **No double-run:** expansion Phases 0–3 run ONCE per run — here, in a standalone `orch-build-mvp` run; in an orchestrate-driven first build, orchestrate runs them instead. Expansion Phases 4–6 run INSIDE this build, not here: expansion Phase 4 implementers build the approved expansions alongside the MVP slices (the orch-build-mvp step 4 GAN loop drives each slice, expansions included), expansion Phase 5 verification runs in orch-build-mvp step 6 after the MVP is built, and expansion Phase 6 feeds the final report (orch-build-mvp step 9). The skill is never invoked whole at this step. The user removes anything unwanted with one prompt afterward.'''),
  # New step 3 (Scaffold = orch-pipeline Phase 3) + renumbered step 4
  # (GAN = orch-pipeline Phase 4, expansion Phase 4 inside it) + DD8
  # belief in the brief for the GAN implementers.
  ("skills/orch-build-mvp/SKILL.md", r'''3. **Reuse the existing GAN harness** instead of hand-rolling an iterate loop:
   - Translate the SDD into `gan-harness/spec.md` + `gan-harness/eval-rubric.md`
     (this stands in for what `gan-planner` would generate — you already have the spec).
   - Drive the build with `/gan-build "<one-line brief>" --skip-planner`
     (defaults: `--max-iterations 15`, `--pass-threshold 7.0`,
     `--eval-mode playwright`; use `--eval-mode code-only` for non-UI slices).
   - That command runs the `gan-generator` → `gan-evaluator` loop and writes
     `gan-harness/feedback/feedback-NNN.md` until the score passes or plateaus.''', r'''3. **Scaffold — orch-pipeline Phase 3.** Stand up the first end-to-end slice (the first thin vertical slice from orch-build-mvp step 1). The scaffold owns the final file layout: if a later implementer must move a file from the intended layout, the implementer records the move in its result and the orchestrator reconciles it in orch-build-mvp step 5 (Reconcile).
4. **Implement — orch-pipeline Phase 4: reuse the existing GAN harness** instead of hand-rolling an iterate loop (this step IS orch-pipeline Phase 4, not a rerun of it):
   - Translate the record/scope (or the fallback spec doc, if that was the input) into `gan-harness/spec.md` + `gan-harness/eval-rubric.md`
     (this stands in for what `gan-planner` would generate — you already have the spec).
   - Drive the build with `/gan-build "<one-line brief>" --skip-planner`
     (defaults: `--max-iterations 15`, `--pass-threshold 7.0`,
     `--eval-mode playwright`; use `--eval-mode code-only` for non-UI slices).
   - That command runs the `gan-generator` → `gan-evaluator` loop and writes
     `gan-harness/feedback/feedback-NNN.md` until the score passes or plateaus.
   - Expansion Phase 4 runs here: the GAN loop drives each slice, expansions included, per the feature-expansion Phase 4 brief format (Tool/API cell + UI rule + capped 2-round fix loop + per-feature `code-reviewer` pass). **Belief in the brief:** implementers trust the brief and build it — they do not second-guess the plan, hedge, or wait for reassurance; they commit to the approach and make it work; if a detail is ambiguous, they pick the reasonable option and note it, they don't stall.'''),
  # Old steps 4–6 (both gates + commit, reconcile, bare security-reviewer
  # line) become new steps 5–6–7 IN ORDER — a single substitution, so the
  # file reads 1..9 in order: 5 Reconcile, 6 Verify (orch-pipeline Phase 5
  # Review + expansion Phase 5), 7 Commit (orch-pipeline Phase 6, Gate 2
  # only — Gate 1 already passed in step 1).
  ("skills/orch-build-mvp/SKILL.md", r'''4. Stop at **Gate 1** (slice plan) and **Gate 2** (pre-commit) — except during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature, where both gates auto-approve and the run proceeds without waiting (see hackathon-mode §7). Commit the
   scaffold and each slice as separate `feat:` commits.
5. **Reconcile after each wave — this step owns collision reconciliation.** After each implementer wave, read every implementer's result (status, changed files, verification evidence, blockers); confirm the reported files exist, stayed in scope, and carry verification evidence. If two implementers in the same wave touched the same files, decide the merge order — the first-listed implementer's files win on conflict unless the planner marked a dependency (then the dependency's files win) — record the decision in `.hackathon/run-ledger.md`, and dependents proceed on the merged result. If the scaffold's first slice and an expansion feature touched the same files, the same rule applies (scaffold first unless the planner marked the expansion as the dependency). If an implementer moved a file from the planner's intended layout, record the actual layout in the ledger and use it in later briefs. When orchestrate runs the build, orchestrate owns reconciliation; this step owns it on a standalone run.
6. Add `security-reviewer` for any slice touching a security trigger.''', r'''5. **Reconcile after each wave — this step owns collision reconciliation.** After each implementer wave, read every implementer's result (status, changed files, verification evidence, blockers); confirm the reported files exist, stayed in scope, and carry verification evidence. If two implementers in the same wave touched the same files, decide the merge order — the first-listed implementer's files win on conflict unless the planner marked a dependency (then the dependency's files win) — record the decision in `.hackathon/run-ledger.md`, and dependents proceed on the merged result. If the scaffold's first slice and an expansion feature touched the same files, the same rule applies (scaffold first unless the planner marked the expansion as the dependency). If an implementer moved a file from the planner's intended layout, record the actual layout in the ledger and use it in later briefs. This step owns reconciliation — this skill runs standalone only, so there is no orchestrate-driven case in which orchestrate would own it instead.
6. **Verify — orch-pipeline Phase 5 (Review) + expansion Phase 5.** `code-reviewer` (+ `security-reviewer` on any security-trigger slice) reviews each slice; then run the whole-build verification: expansion Phase 5 checks BY NAME — `browser-qa` / `click-path-audit` / `verification-before-completion` per feature, after the MVP is built. Review findings are fixed inside the capped 2-round fix loop; past that, the item is recorded blocked with evidence and work moves on.
7. **Commit — orch-pipeline Phase 6.** Commit the scaffold and each slice as separate `feat:` commits → **Gate 2** (pre-commit; auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature — proceed without waiting; see hackathon-mode §7). Gate 1 (slice plan) was already passed in orch-build-mvp step 1 — it is not re-stopped here.'''),
  # Old steps 7+8 (deploy films deployed URL; film sets app.url) become
  # step 8 (deploy, then /demo films the LOCAL app only — video from code,
  # never a deployed URL).
  ("skills/orch-build-mvp/SKILL.md", r'''7. **Deploy via `deploy-fast`.** Deploy the working MVP so the demo films the real deployed app; if deploy is static-only or blocked, the demo films the local dev server instead and the final report notes that — never hard-abort the run for lack of a deployed URL.
8. **Film via `/demo` (`pitch-deck-video`).** The demo video is a required deliverable — film the real app by default (set `shots.json` `app.url` to the deployed URL, or `APP_DIR` to the app dir).''', r'''8. **Deploy via `deploy-fast`, then film via `/demo` (`pitch-deck-video`) — LOCAL only.** Deploy the working MVP; then film the LOCAL app from the project dir (`APP_DIR` to the app dir) — `/demo` never films the deployed URL, so do NOT set `shots.json` `app.url` to it. The demo video is a required deliverable. If deploy was static-only or blocked, the final report notes that — never hard-abort the run for lack of a deployed URL.'''),
  # Step 9 (final report): qualify "Phase 6 return text" as expansion
  # Phase 6; standalone only (no orchestrate-owned case).
  ("skills/orch-build-mvp/SKILL.md", r'''9. **Deliver the final report — this is the done signal.** Write it to `docs/final-report.md` in the project AND deliver it as the reply. State what was built, every assumption made, anything blocked or skipped, and anything the user may want to remove, with the files for each removable item (feature-to-files inventory — the inventory lives in that file). Take the expansion Phase 6 section from the stage ledger (`.hackathon/run-ledger.md`, expansion section) AND the Phase 6 return text (the landed / blocked / rejected lists) in a standalone run. When orchestrate runs the build, orchestrate owns the final report; this step covers standalone orch-build-mvp runs.''', r'''9. **Deliver the final report — this is the done signal.** Write it to `docs/final-report.md` in the project AND deliver it as the reply. State what was built, every assumption made, anything blocked or skipped, and anything the user may want to remove, with the files for each removable item (feature-to-files inventory — the inventory lives in that file). Take the expansion Phase 6 section from the stage ledger (`.hackathon/run-ledger.md`, expansion section) AND the expansion Phase 6 return text (the landed / blocked / rejected lists). This step covers standalone orch-build-mvp runs only — orchestrate never invokes this skill, so orchestrate never owns this report.'''),
  # Example: record/scope first (doc path is the standalone fallback) +
  # qualified step numbers (orch-build-mvp steps 3/6/7).
  ("skills/orch-build-mvp/SKILL.md", r'''orch-build-mvp: civicpulse/docs/SDD-v0.6.md
→ read SDD → slice list (vertical) → scaffold slice 1  [GATE 1: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature]
→ /gan-build --skip-planner (generator → evaluator loop) scores vs spec → review
→ commit feat:  [GATE 2: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature] → next slice''', r'''orch-build-mvp: (no argument — reads docs/decision-record.md + docs/scope.md; civicpulse/docs/SDD-v0.6.md is the standalone fallback)
→ read record/scope → slice list (vertical) → scaffold slice 1 (orch-build-mvp step 3)  [GATE 1: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature]
→ /gan-build --skip-planner (generator → evaluator loop) scores vs spec → review (orch-build-mvp step 6)
→ commit feat: (orch-build-mvp step 7)  [GATE 2: auto-approves during a hackathon first build after grill-me, or a one-prompt removal of a first-build feature] → next slice'''),
]
for rel, old, new in subs:
    p = os.path.join(base, rel)
    text = open(p, encoding="utf-8").read()
    assert text.count(old) == 1, f"{rel}: pattern not found exactly once: {old[:60]!r}"
    open(p, "w", encoding="utf-8").write(text.replace(old, new))
print("fix4 batch A: orch-build-mvp one-engine + phase mapping + 9-step rewrite applied")
PYEOF
