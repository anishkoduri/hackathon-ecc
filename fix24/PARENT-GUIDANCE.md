# Fix #24 — Parent guidance for the coordinator

## Your job

Implement fix #24 per `fix24/SPEC.md` (§1–§2), then run the loops until
clean and write `fix24/MANIFEST.md`. Report back to the parent with the
final numbers. The parent spot-checks before anything is reported to Anish.

## Standing rules (do not re-litigate)

- Edit STAGED sources only, never the built tree. build.sh is the source of
  truth. Never re-run `fix11/fix11-stage.py`.
- Verify your own claims: every audit round's first-pass claims have
  contained at least one error. Re-read the files; do not trust a summary.
- Sweeps run on SOURCE skills.
- The loops: audit (ZERO blocking, ZERO minor) → sweep (CLEAN, weaving
  CLEAN) → dry-run (PASS) → verify24.py (exit 0) → manifest. Loop until
  fully clear; Anish's standing instruction is "continue the audit loop
  until fully clear and you're 100% confident."
- Prior verifiers: re-run, do not edit. Fails must be only the frozen
  post-fix21 fingerprint + the less-flat-ui diff-hunk pattern + cascades.
  If §1(d) forces a verifier change, do NOT make it — record it as owed
  for a parent decision in the manifest.
- Banned terms: 0 in the built tree (claude/codex/anthropic/opus/sonnet/
  haiku/composer-2.5, case-insensitive, excl. node_modules). Grok pins only:
  `grok-4.7-high` / `cursor-grok-4.6-high-fast`. Never the bare
  `grok-4.6-high-fast`.
- The /demo gates from fix #22 stand: /demo is never automatic, callable
  only on explicit invocation, contract intact. Do not reintroduce any
  auto-invocation. The narration-key prompt fires ONLY when the user asked
  for a demo video.
- "More, not bolder" stands. THE CORE (memorable above all) stands.
  Anti-derivative stands. D19 (all seven dimensions incl. Depth) stands.
  browser-qa is the sole verdict executor.

## Notes on this fix

- This is a COHERENCE fix, not a feature fix. The value is in what it
  removes and aligns, not what it adds. A re-weave that only adds text has
  failed. The audit should be able to point at specific duplications
  removed, contradictions adjudicated, and pointers fixed.
- §1(d) staleness: the styles.csv 89-rows vs "80 searchable styles"
  header is the known case — reconcile it with the csv as source. Hunt for
  more of the same class (counts, version numbers, cross-references that
  drifted across fixes #14–#23). Do not "fix" staleness by rewriting a
  frozen verifier-asserted text.
- §2 is about the plugin READING as Cursor-native. Where Cursor behavior
  cannot be verified statically (agent resolution, pin fallback, hooks
  firing, /demo film), write the plugin to be robust to either outcome,
  state the prerequisite once, and put the item in the dry-run's
  Cursor-readiness leg as OWED to the live smoke test — never claim it as
  verified.
- The smoke test file (`LIVE_SMOKE_TEST.md`) is the consumer of the
  Cursor-readiness leg: if a §2 item needs a smoke-test step that does not
  exist yet, add the step to the file (it is a checklist, not plugin
  code — editing it is in scope for this fix).
- Keep the disposition table honest: every SPEC item accounted for, with
  anchor tokens as the stable locators (line numbers drift).
- No bundle, no commit, no push. The parent handles the report to Anish.
