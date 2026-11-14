# Fix #25 — Parent guidance for the coordinator

## Your job

Implement fix #25 per `fix25/SPEC.md` (§1–§4), then run the loops until
clean and write `fix25/MANIFEST.md`. Report back to the parent with the
final numbers. The parent spot-checks before anything is reported to Anish.

## Standing rules (do not re-litigate)

- Edit STAGED sources only, never the built tree. build.sh is the source of
  truth. Never re-run `fix11/fix11-stage.py`.
- Verify your own claims: every audit round's first-pass claims have
  contained at least one error. Re-read the files; do not trust a summary.
- Sweeps run on SOURCE skills.
- The loops: audit (ZERO blocking, ZERO minor) → sweep (CLEAN, weaving
  CLEAN) → dry-run (PASS, incl. the new Leg 5 call-graph leg) →
  verify25.py (exit 0) → manifest. Loop until fully clear; Anish's
  standing instruction is "continue the audit loop until fully clear and
  you're 100% confident."
- Prior verifiers: re-run, do not edit — EXCEPT the two authorized §4(a)
  updates (S1: the verify23 styles-count assertion; verify13h M3
  expectations at :57,63). Those two edits are parent-authorized; record
  them in the manifest with before/after tails. No other verifier is
  edited.
- Banned terms: 0 in the built tree (claude/codex/anthropic/opus/sonnet/
  haiku/composer-2.5, case-insensitive, excl. node_modules). Grok pins
  only: `grok-4.7-high` / `cursor-grok-4.6-high-fast`. Never the bare
  `grok-4.6-high-fast`.
- The /demo gates from fix #22 stand: /demo is never automatic, callable
  only on explicit invocation, contract intact. Do not reintroduce any
  auto-invocation. The narration-key prompt fires ONLY when the user asked
  for a demo video.
- "More, not bolder" stands. THE CORE (memorable above all) stands.
  Anti-derivative stands. D19 (all seven dimensions incl. Depth) stands.
  browser-qa is the sole verdict executor. The C2/C3 scope splits stand.

## Notes on this fix

- The call map (§1) is the new durable artifact. It must be generated or
  verified from the tree, not hand-asserted — a hand-written map that
  drifts is worse than none. Its counts must agree with the tree, and
  verify25 must check that agreement.
- §4(b) template-fonts self-host is the one change in this fix that can
  clear a real, long-standing caveat (the Leg 3 environmental FAIL).
  Prove it with a dry-run Leg 3 result, not an assertion. If the sandbox
  still cannot reach what it needs, record exactly what remains owed and
  do not claim the clear.
- §4(a) is small but load-bearing for trust: the S1 header fix and the
  verify13h M3 updates must each land with their verifier assertion in
  the SAME change, and the manifest must show the before/after tails
  (fix23's tail may move back toward 212 — record the new codified tail
  in verify25).
- §4(c) is deliberately bounded: improvements the call/weave audit
  exposes, not a feature grab-bag. If an improvement needs a new skill,
  the manifest must justify it; the default is to wire, tighten, or
  record — not to add.
- /tmp is a 512 MB tmpfs: keep test copies out of it or clean them
  promptly (fix #24 filled it to 97% and crashed Chrome). `/tmp/skill-add`
  holds pinned upstream clones — never delete it.
- The smoke test file (`LIVE_SMOKE_TEST.md`) may gain steps for any new
  live-only item this fix exposes (it is a checklist, not plugin code —
  editing it is in scope). The §15 from fix #24 stays.
- Keep the disposition table honest: every SPEC item accounted for, with
  anchor tokens as the stable locators (line numbers drift).
- No bundle, no commit, no push. The parent handles the report to Anish.
