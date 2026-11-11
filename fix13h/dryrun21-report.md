# Dry-run #21 — hackathon-ecc first build (Campus Eats) — report

- Build: `~/workspace/hackathon-plugin/build.sh`, 23,058 lines, md5 `d2b1b856d7b5bef96da11d3bb1f36144` (verified)
- Built tree: `~/workspace/hackathon-plugin/hackathon-ecc/`
- Fix round under test: #13h (`~/workspace/hackathon-plugin/fix13h/MANIFEST.md` read first)
- Method: read-only simulation of the Campus Eats first build end-to-end (grill-me → scope → expansion Phases 0–3 → slices → Verification stage Verify steps 1–6 → 5b polish + polish-routed redesign → 5c deploy → 5d demo → step 6 commit/README/final report), plus the standalone `orch-build-mvp` branch (steps 6 + 6b) and the cold-start `/gan-build` / `/gan-design` path. Every finding verified by reading the built file.
- Verdict: **NOT CLEAN — 1 BLOCKING, 7 MINOR**

## Verdict

**NOT CLEAN.** One blocking defect in the #13h snapshot/revert mechanism itself (B1): the whole-tree snapshot has no exclusion for `.hackathon/`, so a revert restores a stale run ledger and corrupts the shared fresh-verdict budget — the exact accounting #13h was built to protect. Everything else in the #13h scope verified as implemented; the remaining items are minor.

## BLOCKING (1)

### B1 — Whole-tree snapshot has no `.hackathon/` exclusion: revert restores a stale ledger and corrupts the fresh-verdict budget
- `skills/orchestrate/SKILL.md:60` (5b snapshot rule + revert steps) and `skills/orch-build-mvp/SKILL.md:53` (6b, same text).
- Simulated step: 5b / 6b polish-routed redesign that FAILS re-verification → revert → 5c deploy / step-7 commit.
- What the text says: "copy the WHOLE tree into `.hackathon/redesign-snapshot/<redesign-id>/` ... The snapshot covers every file in the tree, not just the files the redesign brief enumerates". No exclusion anywhere in either file: 0 hits for `excluding` in either file, and no `except`/`other than` in any snapshot-matching line (the two `EXCEPT` hits in orchestrate are in Verify step 6, about Specificity).
- Two breaks follow:
  1. **Self-referential copy.** The snapshot directory lives inside the tree being copied (`.hackathon/redesign-snapshot/<id>/` under project root). A literal whole-tree copy into a subdirectory of itself is not executable as written (a copy tool either refuses the self-subtree or recurses); the instruction names no tool and no exclusion.
  2. **Revert restores stale run state.** The snapshot contains `.hackathon/run-ledger.md` as it stood at snapshot time — including its `fresh-verdict rounds used: N/2` line and any `re-verification <id>:` entries. Revert step (1) ("copy every file in the snapshot back over the tree at its recorded relative path (the snapshot is the whole tree, so this restores the verified state exactly)") therefore overwrites the live ledger with the pre-redesign copy. The round consumed by the failed re-verification run is forgotten: revert step (3) re-records the `re-verification <id>: BLOCKED` entry, but nothing re-records the rounds-used count. The shared 2-round budget silently regains a spent round, so a later redesign can spend a round that was already consumed — the budget invariant (one shared `fresh-verdict rounds used: N/2` line, "never spend from working-context memory") is broken by the revert itself. Secondary effect: `.hallmark/candidate-evidence.md` is likewise restored to its pre-redesign state, un-marking the `Superseded by redesign <id> — do not re-judge` entries, so a later fresh-verdict run can re-judge superseded evidence.
- Fix direction: exclude `.hackathon/` (at minimum the snapshot directory itself and `run-ledger.md`) from the snapshot copy, and state that revert never restores run-state files under `.hackathon/` (or, equivalently, snapshot only the app/source tree). A whole-tree snapshot that includes its own destination and the live budget ledger cannot be "exact" and cannot be reverted safely.

## MINOR (7)

### M1 — "5c/Verify-step-6 checks below" points at a check that does not exist after 5b
- `skills/orchestrate/SKILL.md:60` (5b): "the 5c/Verify-step-6 checks below consult the entry for that redesign-id".
- Verify step 6 runs inside 5a (the Verification stage), *before* 5b polish; no Verify-step-6 check exists below 5b. The checks below 5b that consult the entry are 5c (deploy, `:61`) and orchestrate step 6 (commit, `:64`), and both do carry their own correctly worded re-verification checks — so the flow still works, but the sentence misdirects the orchestrator (looks like an M3 over-rename of "step 6" into "Verify step 6"). Standalone 6b gets this right ("the step-7/step-8 checks below", `skills/orch-build-mvp/SKILL.md:53`).

### M2 — Verification stage has TWO items numbered "Verify step 4"
- `skills/orchestrate/SKILL.md:187` (blind UI reviewer) and `:191` (adversarial audit).
- Known held-back item from the #13h manifest (M3 numbering: "Renumbering was out of scope"). No other text currently dereferences "Verify step 4", so nothing breaks today, but the stage numbering is self-contradictory (two 4s, then 5, then 6) and any future reference to "Verify step 4" is ambiguous.

### M3 — No uniqueness rule for `<redesign-id>`
- `skills/orchestrate/SKILL.md:60`, `skills/orch-build-mvp/SKILL.md:53`: "`<redesign-id>` is the polish finding's short id, e.g. `landing-template`" and "one directory per redesign".
- Two distinct polish findings with the same short id (two `landing-template` findings, or a second redesign attempt on the same screen) would share one snapshot directory (second overwrites the first) and one `re-verification <id>:` ledger entry, making the two redesigns indistinguishable. Trace (e) distinguishability holds only when the ids happen to differ; nothing guarantees it. Needs a uniqueness rule (e.g. suffix with a counter).

### M4 — Revert verification's unconditional `git status` vs "no repo at all"
- `skills/orchestrate/SKILL.md:60`, `skills/orch-build-mvp/SKILL.md:53`, revert step (2): "verify with `git status` plus a diff restricted to snapshot-listed paths".
- The same paragraph says "File-copy, not git: the tree may be uncommitted or have no repo at all". The *identification* half has a no-repo fallback ("or by comparing the post-redesign tree against the snapshot manifest"), but the *verification* half does not — `git status` errors in a repo-less tree. Normally masked in practice because `create-next-app` inits git (`skills/app-scaffold/SKILL.md:81`), but the explicitly contemplated no-repo case breaks the verification step as written. (Standalone flow is unaffected: `commands/gan-build.md:19` initializes git in Phase 0.)

### M5 — `fresh-verdict rounds used: N/2` is never initialized to `0/2`
- No `fresh-verdict rounds used: 0/2` (or any initialization) exists anywhere in `skills/` or `commands/` (grep: 0 hits); the line is only ever "updated" / "consulted" (`skills/orchestrate/SKILL.md:60`, `:195`; `skills/orch-build-mvp/SKILL.md:49`, `:53`).
- The no-candidate-evidence guard's "record that in the ledger (rounds used unchanged)" (`skills/orchestrate/SKILL.md:195`, `skills/orch-build-mvp/SKILL.md:49`) is unexecutable verbatim on a first run with no prior spend — there is no line to leave unchanged, so the orchestrator must invent the `0/2` line. The first spend creates the line implicitly via the update rule, so the flow continues; the guard just has no defined initial state.

### M6 — Detector path lets polish rewrite a template pattern without `browser-qa`'s verdict
- `skills/polish-pass/reference/polish.md:49` (Step 5.2): "Re-run the Impeccable detector too (`npx impeccable@4.8.0 detect <paths>`), and fix real findings the same way."
- The Impeccable detector's 62 rules include `icon-tile-stack` (`skills/polish-pass/reference/impeccable-detector-rules.json:182`: "A small rounded-square icon container above a heading is the universal AI feature-card template") — the same substance as the craft-floor same-size-cards template pattern (gates.md gate 3). Step 5.2 has no template-pattern carve-out and no routing to `.hallmark/candidate-evidence.md` for detector findings.
- The only defense is the generic gloss at `polish.md:39` ("where the two floors disagree, the stricter ban wins"), which never names detector findings, and `craft-floor.md`'s template-pattern routing ("do NOT fix on this check alone") is written for the craft-floor check, not the detector. Contrast with the correctly gated paths: `impeccable-critique.md:142` (Priority fixes carry a generic-template item only when `browser-qa`'s verdict has established it) and `scoring.md:55-56` (Persona-fit cap applies only on `browser-qa`'s verdict). This is a rewrite-on-static-evidence path, not a pass/fail verdict on a rendered screen — hence minor, not blocking — but it is a real hole in trace (d).

### M7 — Duplicated ledger-update sentence still in the step-6 fresh-run paragraphs (held back)
- `skills/orchestrate/SKILL.md:195` ("after the run, the orchestrator records `fresh-verdict rounds used: N/2` in `.hackathon/run-ledger.md` (see the round definition in 5b)") and `skills/orch-build-mvp/SKILL.md:49` ("— see the round definition in 6b —").
- Known held-back item from the #13h manifest (M2 scope: the duplication was removed only in 5b/6b). Duplication, not contradiction; the round definition in 5b/6b remains the single source.

## Fix-#13h areas verified clean

- **(a) No-candidate-evidence guard.** Present in both engines with identical wording: orchestrate `:195` and standalone `:49` — "If the Hallmark audit produces no candidate evidence (no Specificity under 3, no template observations), no fresh round is spent — record that in the ledger (rounds used unchanged)." Trace: Hallmark audit with Specificity ≥ 3 and no finish-review template observations → no fresh-verdict run, no round consumed. (Caveats: M5 initial-state gap; B1 ledger-restore interaction.)
- **(b) Failing polish-routed redesign → revert → deploy verified tree.** Snapshot-before-redesign, budget check before building, re-verification on the shared budget, hold + revert on failure, and deploy/commit of the reverted tree are all specified in both engines (orchestrate `:60`, `:61`, `:64`; standalone `:53`, `:55`, `:56`). The revert steps correctly delete redesign-created files and restore from the snapshot copy, never from version control alone (`git checkout -- <file>`: 0 hits in both files). The one break is B1 (stale ledger restore) plus M4 (`git status` in a no-repo tree).
- **(c) Cold start.** `commands/gan-build.md:23-24` step 0 reads `docs/decision-record.md` FIRST, adopts its direction (writing it into `docs/design-tokens.md` if the tokens file lacks it or differs), invokes the design-lead (grok-4.7-high) only when neither the record nor the tokens file carries a direction, and states record-over-spec.md precedence; `:37` Phase 2 generator reads "spec.md and `docs/design-tokens.md`" with the same precedence. `commands/gan-design.md:17` Setup step 0 and `:12` intro carry the identical chain. Both readers agree: record wins over spec.md. Step 0 runs ALWAYS, including under `--skip-planner` (`gan-build.md:23`), as `orch-build-mvp` step 4 relies on. Taste and ui-ux-pro-max carry no direction-adoption lines reading the record (0 hits), as the manifest states.
- **(d) Impeccable Refuse template patterns.** `impeccable-craft-floor.md:30` exception clause, `:34` same-size-cards and `:35` hero-metric template each append to `.hallmark/candidate-evidence.md` and are "not rewritten on this check alone"; glosses corrected in `polish.md:39`, `polish-pass/SKILL.md:92`, `design-taste-frontend/SKILL.md:242` (step 4a); `craft-floor.md:111` routes template-pattern bans to candidate evidence; `ui-ux-pro-max/SKILL.md:87` carve-out intact. Critique bands reworded to candidate evidence (`impeccable-critique.md:595`, `:598`, `:599`, `:601`; "ship it" / "Redesign needed" / "Major UX overhaul required": 0 hits). Gap: M6 detector path only.
- **(e) Per-redesign-id re-verification entries.** All entries keyed (`re-verification <redesign-id>: PASSED/BLOCKED`); plain `re-verification: PASSED/BLOCKED` entries: 0 hits in both engines. Orchestrate `:60`/`:61`/`:64` and standalone `:53`/`:55`/`:56` all consult the entry for that redesign-id. Two redesigns are distinguishable given distinct ids (caveat: M3 uniqueness).
- **(f) Harmony.** Records consistency only, never verdicts: `polish-pass/SKILL.md:22` ("consistent / diverges, with the tokens cited") and `polish.md:24` (Step 7) and `:79` (table column "<consistent / diverges (tokens cited)>"). Distinctiveness-bar sentences untouched.

## Rest of the flow (spot-verified, no findings)

- All referenced skills/commands exist and are wired: grill-me (writes `docs/decision-record.md` incrementally), hackathon-scope, feature-expansion (Phases 0–3 auto, no gate; table to ledger/`docs/expansion.md`), browser-qa (sole distinctiveness executor, `SKILL.md:68`, verdict `SHIP / DO-NOT-SHIP` at `:106`), click-path-audit, verification-before-completion, deploy-fast (Timing rule at `:32`, security-review pre-deployment checklist), pitch-deck-video + `commands/demo.md` (local-only filming, Environment-field key handoff at `demo.md:13`), readme-writer, orch-pipeline (Phases 0–6, Gates 1/2), app-scaffold, gan-style-harness, gan-planner/generator/evaluator agents, design-taste-frontend, ui-ux-pro-max, polish-pass, design-system (slop findings → candidate evidence, `:56`), less-flat-ui.
- Single-executor sweep: Taste captivating-hero bar reworded to candidate evidence (`design-taste-frontend/SKILL.md:53`); gates.md §5 judged clauses reworded to candidate evidence (6b, 8/32, 9, 23, 80–82, 83); sloplint-render.mjs carries the scope guard (header `:2`, `observeSpace` `:740-747`: template gates 80/81/82/83/85 emit NOTE candidate evidence on landing, skipped on app scope mirroring `APP_SKIP` in `sloplint.mjs:798-799`); hero review (`review-hero.md:5,11,16`) and finish review (`review-finish.md:5,9,13,15`) both route template observations to candidate evidence and never drive their first word; gates.md §3 Specificity is candidate evidence only.
- Verification stage numbering: "Verify step 1" … "Verify step 6" at orchestrate `:183`, `:184`, `:185`, `:187`, `:191`, `:193`, `:195` (except the M2 duplicate 4); orchestrate's own steps untouched (`:64` step 6, `:61` 5c, `:279` "per orchestrate step 5 above").
- `memory.;`: 0 hits in both engines. "copy every file the redesign will touch": 0 hits. "diff the tree against the snapshot directory": gone (replaced by diff restricted to snapshot-listed paths).
- Fresh-verdict budget accounting is consistent across engines: one shared budget of 2 rounds across 5b/Verify step 6 (orchestrate) and 6b/step 6 (standalone), round defined identically as one `browser-qa` verdict run, separate from the Verify-step-5 visual loop caps (max 3 rounds, ≤2 fix rounds per problem list).

## Counts

- BLOCKING: 1 (B1)
- MINOR: 7 (M1–M7)
- Verdict: **NOT CLEAN**
