# Fix #26 SPEC — Close up the small items left open after fix #25

## §0 Origin

Anish, Nov 13, 09:00 CST: "can you close up those small items" — the
small open items from the fix #25 close (pip pinning, the benchmark
alignment check, the stale README, and the other open parent
adjudications in `fix25/MANIFEST.md` §5/§6 that are closable without the
live smoke test).

Baseline: build.sh 24,079 lines, md5
`f19483f50e89998f8b9dc052ed5d5fae` (post-fix #25). Counts: 166 skills /
72 agents / 123 rules / 87 commands / 15 hooks; 64 trigger keys.

## §1 Pip pinning (Audit #37 scope)

- Pin the 17 unpinned install lines from the Audit #37 scope. Only
  `piper-tts` can fire in a first build (fallback documentation in
  pitch-deck-video); the rest are install lines elsewhere in the tree.
- Every pinned line gets a version pin a re-run can verify (grep for
  unpinned `pip install` lines = 0 in the built tree after the fix).
- Do not change what gets installed, only pin it. If a pin cannot be
  resolved to a real version, record that line as owed with the reason —
  do not invent a version.

## §2 F-14 — post-report /demo stale README

- A /demo run after the final report leaves the README stale (no video
  link). Fix #25 proposed no edit; this fix must propose and implement
  one: after a /demo run, the README gains the video link (or the
  first-build sequence re-runs the README step after /demo — pick the
  mechanism that fits the existing flow, do not invent a new gate).
- The /demo gates from fix #22 stand: /demo is never automatic, callable
  only on explicit invocation. The fix must not make /demo automatic and
  must not add a user-approval gate to the first build.

## §3 Stale build.sh fix25 comment (parent-authorized)

- `build.sh:24062–24067` describes fix25.py as "§4(a) S1" only; the
  script now also carries the §1 wires, the §2 inventory close, the
  §4(d) browser-qa line, and the loop-status references. Update the
  comment to describe what the script actually does.
- This was deliberately NOT edited in fix #25 because editing it breaks
  the additions-only diff invariant the verifiers assert. So this fix
  updates the verifier's diff invariant IN THE SAME CHANGE (the same
  pattern as the §4(a) S1 authorized verifier update in fix #25).
  Record the before/after in the manifest. No other verifier is edited.

## §4 Variable-font scoped exception — record it

- Parent decision at the fix #25 close: the pitch-deck-video template's
  Hanken Grotesk + JetBrains Mono variable woff2 are a SCOPED EXCEPTION
  to the static-only font rule — the video renders in a single
  controlled Chromium and the output is a fixed video file, so the
  cross-platform variance the rule guards against does not apply. App UI
  fonts stay static-only.
- The fix25 manifest states the variable-font fact but does not
  adjudicate it. Record the exception in the design inventory
  (`design-inventory.md`) and in this fix's manifest, with the scope
  (video template only) and the reason. No code change.

## §5 Trigger router B6 — decide it

- Verify the no-consumer claim by grep: all 64 keys resolve to real
  skill dirs, trigger-only count 0, but the consumer chain has no live
  Cursor entry point (neither `scripts/hooks` consumer is invoked from
  `hooks/*.js`; `context-prompt-suggestions.js` states it is
  upstream-only).
- Disposition: record `skill-triggers@1.json` as DOCUMENTATION-ONLY (a
  reference table, not a live routing table) — UNLESS the grep finds a
  live consumer, in which case say so, name it, and wire/verify it
  instead of recording documentation-only.
- The live smoke test cannot clear this (there is no Cursor event to
  fire it). Do not leave it open pending the smoke test.

## §6 Benchmark dimension 7 (alignment) — disposition, not a pass

- Dim 7 stays OWED: no live Campus Eats render exists in this workspace
  (only the v1-era tokens file), so browser-qa cannot run the ALIGN_F23
  matrix on it. The dry-run #40 re-trace passes 6/7 statically.
- Do NOT build a new Campus Eats render to verify it. Anish said Nov 11
  "It's ok render doesn't matter anymore" — the artifact needs no
  further work, and a fresh render just to check Dim 7 contradicts that
  call.
- Close the item as a RECORDED DECISION (owed, with the reason), not as
  a pass. The v5 figures stay render-history figures, not live-measured
  ones, and the manifest must say so.

## §7 Fix #17 R1/R4 — verify against the Home Run render

- R1 (iris-opens) + R4 (hero loop) are unverified against a live
  render. Check the Home Run render evidence: dry-run #40's re-trace
  records "hero loop + iris-opens applied" with 17/17 §6 assertions
  passing on the Home Run render.
- If the Home Run render record substantiates application of both
  moments, close R1/R4 as VERIFIED against the Home Run live render —
  and state the scope honestly (Home Run, not Campus Eats).
- If it does not substantiate them, record them as owed with the exact
  gap. Do not claim a verification the record does not support.

## §8 ck wire KEEP — record the decision, fix the stale cost lines

- Parent decision at the fix #25 close: KEEP the ck wire at its true
  cost (~1k tokens/session, not ~100). No code change to the wire.
- The fix25 manifest §5 still lists it open and notes two stale cost
  lines: the `.mjs`'s "~50 lines" comment and the skill's "~100 tokens
  per session" line. Correct both to the measured cost (live measurement
  7,382 chars / 890 words merged with an empty ck store; ~1k
  tokens/session). Record the KEEP decision in this fix's manifest.

## §9 Verification criteria

- Audit #73 (or next number): ZERO blocking, ZERO minor. Standalone
  report file in `fix26/` (per the AGENTS.md record-keeping rule — every
  fix's audit and sweep leaves a standalone report file).
- Sweep (next number): CLEAN, weaving-coherence CLEAN for the whole
  tree. Standalone report file in `fix26/`.
- Dry-run (next number): PASS — Leg 1 fixtures, Leg 2 render re-run
  (Home Run 17/17 §6 assertions; Campus Eats v5 benchmark re-trace 6/7
  with Dim 7 owed per §6), Leg 3 /demo, Leg 4 Cursor-readiness, Leg 5
  call-graph (re-run to confirm no regression from the §1–§8 edits).
- verify26.py: checks for every placement, exit 0. It also codifies the
  prior-verifier tails after §3: fix22 366/369 (unchanged), fix23
  194/211 excl. manifest, fix24 98/104 excl. manifest, verify13h 6/97
  fail — record any move with its cause traced to the files.
- Prior verifiers: re-run; fails must be only the codified tails. No
  regressions. The §3 verifier edit is the ONLY verifier edit
  authorized in this fix.
- Banned terms: 0 in the built tree. Counts and pins unchanged unless
  the manifest justifies a change.
- Manifest: fix26/MANIFEST.md, with the disposition table, the anchor
  tokens, the open parent adjudications, and the dry-run caveat if any
  check is environment-limited.

## §10 Non-goals

- Do not re-litigate fixes #14–#25 adjudications (C2/C3 scope splits,
  FILM_F1/F5/F6, /demo gates, Casberry bar, APCA informational, THE
  CORE, the inventory, the call map, epic-commands reachability).
- Do not rewrite frozen verifier-asserted texts — except the one
  authorized §3 update, and only that.
- Do not pre-decide the smoke test's live questions. Do not build a
  Campus Eats render. Do not add a live-render requirement anywhere.
- No bundle, no commit, no push. No Netlify touch-up (due after Dec 4,
  2026 — not yet due). No new skill, command, rule, agent, hook, or
  trigger unless the manifest justifies it.
