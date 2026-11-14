# Fix #26 — Parent guidance for the coordinator

## Your job

Implement fix #26 per `fix26/SPEC.md` (§1–§8), then run the loops until
clean and write `fix26/MANIFEST.md`. Report back to the parent with the
final numbers. The parent spot-checks before anything is reported to
Anish.

## Standing rules (do not re-litigate)

- Edit STAGED sources only, never the built tree. build.sh is the source
  of truth. Never re-run `fix11/fix11-stage.py`.
- Verify your own claims: every audit round's first-pass claims have
  contained at least one error. Re-read the files; do not trust a summary.
- Sweeps run on SOURCE skills.
- The loops: audit (ZERO blocking, ZERO minor) → sweep (CLEAN, weaving
  CLEAN) → dry-run (PASS) → verify26.py (exit 0) → manifest. Loop until
  fully clear; Anish's standing instruction is "continue the audit loop
  until fully clear and you're 100% confident."
- Prior verifiers: re-run, do not edit — EXCEPT the one authorized §3
  update (the build.sh fix25 comment + the verifier's additions-only
  diff invariant, in the same change). That edit is parent-authorized;
  record it in the manifest with before/after tails. No other verifier
  is edited.
- Banned terms: 0 in the built tree (claude/codex/anthropic/opus/sonnet/
  haiku/composer-2.5, case-insensitive, excl. node_modules). Grok pins
  only: `grok-4.7-high` / `cursor-grok-4.6-high-fast`. Never the bare
  `grok-4.6-high-fast`.
- The /demo gates from fix #22 stand: /demo is never automatic, callable
  only on explicit invocation, contract intact. Do not reintroduce any
  auto-invocation. The narration-key prompt fires ONLY when the user
  asked for a demo video.
- "More, not bolder" stands. THE CORE (memorable above all) stands.
  Anti-derivative stands. D19 (all seven dimensions incl. Depth) stands.
  browser-qa is the sole verdict executor. The C2/C3 scope splits stand.
- Every fix's audit and sweep leaves a STANDALONE report file in the fix
  dir (AGENTS.md rule — fix #24's Audit #71 and Sweep #32 have no report
  files, only the manifest's record; do not repeat that gap).

## Notes on this fix

- §1 pip pinning: the Audit #37 scope is 17 unpinned install lines.
  Find them by grep, do not trust the count from memory. Only
  `piper-tts` can fire in a first build; the rest are install lines
  elsewhere — pinning must not change what gets installed.
- §2 F-14: no edit was proposed in fix #25, so the coordinator must
  propose one. The mechanism has to fit the existing flow (final report
  → README, /demo explicit-only). If the cleanest mechanism is "the
  README step re-runs after /demo", say so and implement it; if it is
  "the /demo run appends the video link to the README", say so instead.
  Do not add a user-approval gate.
- §3 is small but load-bearing for trust, same class as fix #25 §4(a):
  the comment fix and the verifier invariant update land in the SAME
  change, and the manifest shows the before/after tails. If the comment
  turns out to live in a staged source rather than in build.sh itself,
  trace it to the source and fix it there.
- §5 B6: the parent leans documentation-only, but the grep decides. If
  a live consumer exists, the disposition flips to wire/verify — do not
  force the parent's lean against the evidence.
- §6 Dim 7: the disposition is a recorded decision, not a pass. The
  manifest must state plainly that Dim 7 is owed and why, and that no
  Campus Eats render will be built to verify it (Anish's Nov 11 call).
  Do not soften this into a pass.
- §7 R1/R4: the Home Run render is the evidence, if it substantiates
  application. Check the actual render record (dry-run #40's re-trace +
  the render's own docs), not the benchmark file's summary line alone.
  If the evidence is thin, record owed — do not stretch it.
- §8: the ck KEEP decision is already made; the work is recording it
  and fixing the two stale cost lines to the measured cost. Do not
  re-open the keep/trim/dormant question.
- /tmp is a 512 MB tmpfs: keep test copies out of it or clean them
  promptly (fix #24 filled it to 97% and crashed Chrome). `/tmp/skill-add`
  holds pinned upstream clones — never delete it. `/tmp/ecc-repo-clean`
  is build-referenced — never delete it.
- Keep the disposition table honest: every SPEC item accounted for, with
  anchor tokens as the stable locators (line numbers drift).
- No bundle, no commit, no push. The parent handles the report to Anish.
