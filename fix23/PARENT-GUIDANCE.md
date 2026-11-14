# Fix #23 — Parent guidance for the coordinator

## Your job

Implement fix #23 per `fix23/SPEC.md` (§1–§6), then run the loops until
clean and write `fix23/MANIFEST.md`. Report back to the parent with the
final numbers. The parent spot-checks before anything is reported to Anish.

## Standing rules (do not re-litigate)

- Edit STAGED sources only, never the built tree. build.sh is the source of
  truth. Never re-run `fix11/fix11-stage.py`.
- Verify your own claims: every audit round's first-pass claims have
  contained at least one error. Re-read the files; do not trust a summary.
- Sweeps run on SOURCE skills.
- The loops: audit (ZERO blocking, ZERO minor) → sweep (CLEAN, weaving
  CLEAN) → dry-run (PASS) → verify23.py (exit 0) → manifest. Loop until
  fully clear; Anish's standing instruction is "continue the audit loop
  until fully clear and you're 100% confident."
- Prior verifiers: re-run, do not edit. Fails must be only the frozen
  post-fix21 fingerprint + the less-flat-ui diff-hunk pattern + cascades.
- Banned terms: 0 in the built tree (claude/codex/anthropic/opus/sonnet/
  haiku/composer-2.5, case-insensitive, excl. node_modules). Grok pins only:
  `grok-4.7-high` / `cursor-grok-4.6-high-fast`. Never the bare
  `grok-4.6-high-fast`.
- The /demo gates from fix #22 stand: /demo is never automatic, callable
  only on explicit invocation, contract intact. Do not reintroduce any
  auto-invocation. The narration-key prompt fires ONLY when the user asked
  for a demo video.
- "More, not bolder" stands. Anti-derivative stands. D19 (all seven
  dimensions incl. Depth) stands. browser-qa is the sole verdict executor.

## Notes on this fix

- §3 (fonts) is the subtlest section: the mechanism matters more than the
  wording. A type-audit step that only records faces is not enough — it
  must be able to FAIL a build whose typography reads as defaulted. Define
  the fail condition concretely (faces used, share of visible text by face,
  trio-vs-previous-build) and make the check real in polish-pass with
  browser-qa as the verdict executor.
- §6 (alignment) is the most concrete section: the Home Run render
  alignment audit is running in parallel (separate agent, same evening).
  Its findings are input to your assertion list, not a substitute for it:
  define the assertions from the SPEC, then check them against what the
  render audit found. If the render audit is still running when you reach
  §6, proceed from the SPEC and note the render audit as a cross-check to
  confirm before the manifest is final.
- §1 (ambition) needs a real bar, not a slogan. "Uses all elements" must
  be checkable: the design record lists used vs considered-and-rejected
  per build, and the audit can verify the record exists and is specific.
  A vague "we considered everything" line fails.
- §5 (functionality) must not become a generic "add a diagram" rule: the
  mechanism shown must be THIS build's mechanism (its pipeline, its data,
  its stack), theme-matched, visible early.
- Keep the disposition table honest: every SPEC item accounted for, with
  anchor tokens as the stable locators (line numbers drift).
- No bundle, no commit, no push. The parent handles the report to Anish.
