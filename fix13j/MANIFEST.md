# Fix round #13j — manifest

## Build
- `build.sh` **23,160 lines** (was 23,117), md5 `b7432cc6ff576dbdf620b8d26bd87984`
- Two clean builds, exit 0, manifest diff = 0 (`a188d10d2900e5b022d5ca173627fa07`)
- Counts **169 skills / 72 agents / 123 rules / 96 commands / 15 hooks, 57 MB** (unchanged)
- Method: `fix13j/fix13j.py` (5 staged subs + preflight of 5 build-patch anchors,
  all count==1 before any write) + `fix13j/build-patch-j.txt` (inserted LAST,
  just before STEP 5, after fix13i). `fix13j/verify13j.py`: **23 present/gone
  checks against the BUILT tree — all pass.** Staged orchestrate == built by diff.

## Item re-traced (parent-verified, confirmed by the coordinator in the built tree)
Dry-run M1 — snapshot manifest location contradicts the 20-line ledger cap:
- Orchestrate `:8`: "The **stage ledger** stays a short run-state file (20 lines
  max), not a PRD. Bulky loads overflow to `docs/run-ledger-appendix.md` (one
  line per item) with a one-line pointer in the ledger."
- Orchestrate `:60` and standalone `:53` snapshot rules: "record the snapshot
  path + the full file list (excluding those two paths) + per-file hashes in
  `.hackathon/run-ledger.md`" — a whole-tree list is dozens to hundreds of
  lines, so the two rules cannot both be followed literally.
- Revert step (2) in both engines: "verify against the snapshot manifest alone"
  — names no file if the orchestrator overflows it to the appendix.
- Standalone had 0 mentions of `run-ledger-appendix` and no ledger cap.

## Fix (both engines, identical wording)
1. Snapshot intro: the manifest (file list + per-file hashes) is recorded in
   `docs/run-ledger-appendix.md` (one line per file: relative path + hash),
   with a one-line pointer in `.hackathon/run-ledger.md` (snapshot path +
   appendix file + line count).
2. Snapshot rule: the manifest — snapshot path + full file list (excluding
   `.hackathon/` and `.hallmark/candidate-evidence.md`) + per-file hashes,
   one line per file — lives in `docs/run-ledger-appendix.md` under a
   `<redesign-id>` heading, with a one-line pointer in the ledger. "The
   manifest lives in the appendix, never in the ledger itself: a whole-tree
   file list is a bulky load, and the ledger stays a short run-state file —
   bulky records go to the appendix (one line per item) with a one-line
   pointer in the ledger." The appendix is defined inline in the rule, so the
   wording is self-contained in standalone (no standalone-wide cap rule
   invented).
3. Coverage check and both revert-step-(2) manifest references NAME the
   manifest's file: `docs/run-ledger-appendix.md` (the `<redesign-id>` section).
4. Unchanged: the 20-line ledger cap (orchestrate :8); per-redesign-id
   `re-verification` entries and the `fresh-verdict rounds used: N/2` line
   stay in the ledger itself (single lines, not bulky loads).

## Files
- Staged: `new-skills/orchestrate/SKILL.md` (5 subs) — staged == built by diff.
- Build patch: `fix13j/build-patch-j.txt` → `skills/orch-build-mvp/SKILL.md`
  (5 subs, build-time asserts).
- Logs: `fix13j/build1.log`, `fix13j/build2.log`;
  manifests `fix13j/manifest1.txt`, `fix13j/manifest2.txt`;
  verifier `fix13j/verify13j.py`.

## Checkers (on this build) — LOOP CLOSED
- Audit #51: **ZERO ERRORS** (0 blocking / 0 minor). Report: `fix13j/audit51-report.md`.
  Fix13j routing verified end to end in both engines; verify13j.py re-run 23/23;
  staged orchestrate == built; counts/pins/SSML/Grok/single-executor all clean.
- Dry-run #23: **CLEAN** (0 blocking / 0 minor). Report: `fix13j/dryrun23-report.md`.
  Campus Eats polish-routed redesign traced end to end in both engines
  (snapshot → appendix manifest + ledger pointer → budget check → coverage
  check → fresh verdict → revert incl. no-repo fallback → hold → deploy of
  the reverted verified tree); all #13 invariants re-verified with file:line.
- Single-executor sweep: **CLEAN** (0 blocking / 0 minor). Report:
  `fix13j/sweep13j-report.md`. Zero surviving ship/fix/rebuild first-word
  values tree-wide; the only SHIP / DO NOT SHIP language is browser-qa's own
  (`browser-qa/SKILL.md:105–106`); all named areas clean.

## Remainder
- **None. The #13 audit loop is CLOSED**: audit ZERO ERRORS + dry-run CLEAN +
  sweep CLEAN on the same build (build.sh 23,160 lines, md5
  `b7432cc6ff576dbdf620b8d26bd87984`). Next step (parent's): fresh git bundle,
  upload, hand to Anish to push from his Windows Git Bash.

## Held back
- None.
