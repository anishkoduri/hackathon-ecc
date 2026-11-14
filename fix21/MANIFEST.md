# Fix #21 — MANIFEST: Long body and small text only; every text element gets an artistic font design decision

Coordinator-owned manifest for the whole of fix #21: the rule
implementation and fix-up #1 (fixup21). Engines: `fix21/fix21.py`,
`fix21/fixup21.py`. SPEC: `fix21/SPEC.md` (§§0–9). Verifier:
`fix21/verify21.py` (101 checks).

build.sh lines: 23647
build.sh md5: 8dfacb47a2a6698d47e4b4a5f8d9126c

## 0. Gate (verified before starting)

- `fix20/MANIFEST.md` existed.
- build.sh at the gate was 23,609 lines, md5
  `785fb40580a4d91f7a480e1cdbc21f24` (post-fix20).
- Anish's refinement (Nov 11 evening, his words): "the font usage of
  the one i said to use for plaintext is too much, every text should
  have an artistic font design decision behind it, not just default
  to this this is only for long length body text or small text here
  and there, not for main text we see visually."

## 1. Rule changes (built-tree file:line; staged sources edited, build.sh copies them verbatim unless noted)

All line numbers below are the BUILT tree
(`~/workspace/hackathon-plugin/hackathon-ecc/`). The canonical
constants live in `fix21/fix21.py` (F4_TIGHT/F7/STATIC21 +
F4_TIGHT_APP/F7_APP, POLISH_F21, TYPESET_F21,
TYPESET_CHECKBOX21). Banned tokens under the fix #16 scrub —
"Anthropic font" and "Claude's reading text" — are never used; rule
text says "Tiempos" / "Fraunces stand-in", as fix #19 and fix #20
did.

### 1.1 F4_TIGHT — the Tiempos rule tightened: long body and small text only

Old: fix #19 F4 said "Body and plain text use Tiempos" and fix #20
F4_SCOPE said the body face is "for BASIC text only ... NEVER used
for important text" — but neither said the body face is NOT a
default. A build could set every non-important text element
(labels, captions, buttons, prices, names, meta rows, table heads)
in Fraunces by default, with no artistic font decision behind any
of them, and be fully compliant. That is the leak Anish named.
New: F4_TIGHT (full rule) + F4_TIGHT_APP (app mirror) + STATIC21
(F4-tight item).

- `skills/design-taste-frontend/SKILL.md:277` F4_TIGHT — Tiempos /
  Fraunces stand-in are for LONG-LENGTH body text and SMALL
  incidental text only; NOT a default for text generally; NEVER for
  main text we see visually. "'Body and plain text use Tiempos'
  (fix #19 F4) reads, after this fix, as long-length body text and
  small incidental text only." Role-scoping from fix #20 stands (a
  pairing dealing Fraunces as the DISPLAY face is governed by fix
  #19 F3 / fix #20 F5, not by this scope rule). After X1 (`:275`),
  before F7 (`:279`).
- `skills/orchestrate/SKILL.md:122` F4_TIGHT (same text, in the
  design-package rule area). After X1 (`:120`), before F7 (`:124`).
- `skills/ui-ux-pro-max/SKILL.md:114` F4_TIGHT_APP — app-surface
  mirror; after X1_APP (`:112`), before F7_APP (`:116`).
- `skills/orch-build-mvp/SKILL.md:57` F4_TIGHT_APP (step 4); after
  X1_APP (`:55`), before F7_APP (`:59`).

### 1.2 F7 — every text element gets an artistic font design decision

Old: no rule required a deliberate, recorded font decision per text
element — a text element could default to the body face with nothing
recorded, and a main visible element in the body face was only
caught if it counted as "important" under fix #20 F5.
New: F7 (full rule) + F7_APP (app mirror) + STATIC21 (F7 items).

- `skills/design-taste-frontend/SKILL.md:279` F7 — every text
  element (heading, label, caption, button, price, name, body, meta
  row, table head, chip, nav link, call to action) has a deliberate,
  recorded artistic font decision: which face, why, what job it
  serves, how it matches the theme and the brand. Recorded in the
  decision record's Type list, per text element — or per text class
  where the class is genuinely uniform (one decision line per class,
  naming the class and the face and the reason; a blanket 'all text'
  line is not a class decision). Main visible text uses the unique
  important font (fix #20 F5) or another artistic face chosen
  through the skills, never the body face as a default. The decision
  is covered by its fix #19 D19 reason; the font decision is the
  D19 reason for that text element's font choice. After F4_TIGHT
  (`:277`).
- `skills/orchestrate/SKILL.md:124` F7 (same text). After F4_TIGHT
  (`:122`).
- `skills/ui-ux-pro-max/SKILL.md:116` F7_APP — app-surface mirror,
  decisions recorded in MASTER.md's Type list. After F4_TIGHT_APP
  (`:114`).
- `skills/orch-build-mvp/SKILL.md:59` F7_APP (step 4). After
  F4_TIGHT_APP (`:57`).

### 1.3 STATIC21 — the static checks (mirrors STATIC19 / STATIC20)

- `skills/design-taste-frontend/SKILL.md:333` STATIC21 (step 6) —
  after STATIC20 (`:331`). (F4 tight) Type list marks the body face
  long-body-and-small-text-only; no token for main visible text
  points at the body face. (F7) Every text element in the Type list
  — or every genuinely uniform text class — carries its recorded
  artistic font decision; no recorded decision is an incomplete
  build; a main visible text element set in the body face is an
  incomplete build; a blanket 'all text' class line is not a class
  decision. (F7 record) The decision record lists the font decision
  per element or per uniform class; the D19 reason covers the font
  choice.
- `skills/orchestrate/SKILL.md:69` STATIC21 (Verify 5a paragraph) —
  after STATIC20, before the `5b. Final polish` bullet (`:70`).
- `skills/orch-build-mvp/SKILL.md:76` STATIC21 (step 6) — after
  STATIC20 (`:74`).

### 1.4 POLISH_F21 — polish-pass harmony

- `skills/polish-pass/SKILL.md:22` POLISH_F21 — appended after
  POLISH_F20 (same line, char offset after it): verifies the
  tightened font scope — each Type-list body-face row marked
  long-body-and-small-text-only, no main visible text token points
  at the body face, every text element carries its recorded artistic
  font decision; a token or element that does not is a harmony
  divergence, recorded as candidate evidence, never a verdict.

### 1.5 TYPESET_F21 + TYPESET_CHECKBOX21 — the typeset lens

- `skills/polish-pass/reference/lenses/typeset.md:59` TYPESET_F21 —
  appended after TYPESET_F20 (`:57`): body face for long-length
  body text and small incidental text only; a heading, hero line,
  call to action, key label, price, name, or prominent label set in
  the body face is a finding; every text element needs a recorded
  artistic font decision; a blanket 'all text' class line is not a
  decision; the squint test is the visual proof.
- `skills/polish-pass/reference/lenses/typeset.md:78`
  TYPESET_CHECKBOX21 — REPLACES the fix #20 checkbox
  (fix20's TYPESET_CHECKBOX_NEW, "the body face is used for basic
  text only"). New text: "the body face is used for long-length
  body text and small incidental text only ... every text element
  has a recorded artistic font decision (fix #21 F7)." The fix #20
  checkbox is GONE from every live surface (staged, built,
  build.sh) — verified by sweep #29 §2.

### 1.6 Placement summary (SPEC §3)

- Staged sources edited directly (build.sh copies them verbatim):
  `new-skills/design-taste-frontend/SKILL.md` (step 4a + step 6),
  `new-skills/orchestrate/SKILL.md` (design-package rule + Verify
  5a), `round2-skills/polish-pass/SKILL.md` (harmony),
  `round2-skills/polish-pass/reference/lenses/typeset.md` (lens +
  checkbox swap).
- build.sh patch block (upstream, no staged source): the fix21
  block, lines 23600–23637 (38 lines, before STEP 5 at 23638, after
  the fix20 blocks), patches `skills/ui-ux-pro-max/SKILL.md`
  (F4_TIGHT_APP + F7_APP) and `skills/orch-build-mvp/SKILL.md`
  (F4_TIGHT_APP + F7_APP + STATIC21). Per-entry anchoring (SPEC
  §3 rows 7–8): X1_APP occurs twice in build.sh, so the anchor is
  within each file's fix20 patch-block entry, never a bare
  build.sh-wide count.
- The canonical variety + theme-match block is NOT modified
  (verbatim ×1 in all 11 files, verify15 44/44). No new weave
  pointers: the §10 weave carries pointers to the design-package
  rule, and the new rules live IN the design-package rule (Taste
  step 4a / orchestrate) — the chain pointer → design-package rule
  → F4_TIGHT/F7 is connected, no dead end (verify21 check 12;
  dry-run #35 §9: 32 pointer lines, 0 off-target, no duplicates
  added).

## 2. Scope-tightening evidence (SPEC §1 + dry-run #35)

- The gap: fix #19 F4 ("Body and plain text use Tiempos") and fix
  #20 F4_SCOPE ("for BASIC text only ... NEVER used for important
  text") never said the body face is NOT a default. F4_TIGHT closes
  that leak by interpretation — it re-reads F4 without editing its
  text (F4_RULE is a verify19 anchor, full-text `in` check; SPEC §3
  forbids editing any fix19/fix20 rule text in place). The tightened
  rule sits immediately after the anchor in every file (Taste
  `:277` after F4_RULE `:263`; orchestrate `:122` after `:108`;
  ui-ux-pro-max `:114` after F4_APP `:100`).
- Fix #20 F5's small-labels permission (ordinary small labels —
  nav links, table heads, captions, chips, form labels, meta rows —
  in the body face, a step smaller) is the permitted set's second
  half: those small labels ARE the "small text here and there" —
  but only WITH a recorded F7 decision per element or per genuinely
  uniform class (SPEC §5, resolved tension, not a contradiction).
- Campus Eats repair evidence (recorded fix #20 findings, dry-run
  #31/#32 — the artifact is read-only, the workspace tokens file is
  v1-era/stale and is NOT evidence): the repair set plain text in
  Fraunces broadly, and its CTA buttons `.btn` (`index.html:193`)
  and `.roll-btn` (`:679`) are set in Fraunces, the body face — a
  genuine F5 leak in a pre-fix-#20 artifact. `.step-btn` is NOT a
  leak (display face primary, Fraunces only as fallback, `:485`).
  Under fix #21 the two CTAs also fail F7 (no recorded artistic
  font decision). The package rule correctly catches exactly this
  leak; no repair was made to the artifact in this program.
- Dry-run #35 fixtures (13/13) prove the checks fire: price in
  Fraunces with no decision FAILS F7; button without a decision
  FAILS / with a decision PASSES; heading in Fraunces FAILS
  F4_TIGHT / in the display face PASSES; long body in Fraunces
  PASSES; caption/meta row in Fraunces with a uniform-class
  decision PASSES; blanket "all text: Fraunces" FAILS F7.

## 3. Fix-up rounds

### Fix-up #1 — fix21/fixup21.py (verifier pin bumps; NOT a new fix)

Three root causes, all verified by the coordinator (SPEC §7 check 11
+ §8): running verify21.py after the implementation gave 96/101,
all 5 failures the check-11 subprocesses.

1. build.sh pin (5 direct + cascades). All five earlier verifiers
   pin build.sh to the post-fix20 values (23,609 lines / md5
   785fb40580a4d91f7a480e1cdbc21f24). Post-fix21 it is legitimately
   23,647 lines / md5 8dfacb47a2a6698d47e4b4a5f8d9126c (the fix21
   block is exactly 38 lines, verified by diff against
   build.sh.before-fix21). Bump the pin in verify15/17/18/19/20:
   check lines + docstring sentences + the fix19 section-11 label
   (same scope as fixup20d's pin bump).
2. Typeset checkbox supersession (verify19 + verify20). Both
   assert the fix20 checkbox is present. SPEC §3 row 6 and §7
   check 4 REQUIRE replacing it with fix21's TYPESET_CHECKBOX21 —
   so both checks now assert the fix21 checkbox is present and the
   fix20 checkbox is GONE (the "old checkbox is gone" half is kept,
   with fix20 now the old one).
3. verify19 system-ui subtraction. The check-7
   RULE_TEXTS_WITH_SYSTEM_UI list subtracts the fix20 checkbox
   (comment: "the CURRENT typeset checkbox (fix #20's...)"). The
   fix21 checkbox also names `system-ui` once, so the subtraction
   list swaps in the fix21 checkbox. The *.md mention total stays
   14 and the total stays 161 — no count check changes.

verify20's pin is MANIFEST-driven (check 10 reads fix20/MANIFEST.md,
the CLOSED post-fix20 record): since the MANIFEST is a closed
historical record and is NOT edited here, check 10's value
comparison is replaced by the literal post-fix21 pin — same pattern
as verify15/17/18/19. The "MANIFEST records lines + md5" presence
check is kept.

Scope: verifier .py files ONLY (fix15/verify15.py,
fix17/verify17.py, fix18/verify18.py, fix19/verify19.py,
fix20/verify20.py). fix21.py, fix21/verify21.py, build.sh, staged
sources, and the built tree are NOT touched. No commit, no bundle,
no GitHub touch. No build is run — the fix-up edits no build input,
so no rebuild is needed. One-shot applicator with preflight
assertions, amendments in place, self-checks, and a preflight that
refuses re-run (fix20/fixup20.py pattern). The NEW checkbox is
imported live from fix21.py and the OLD fix20 checkbox live from
fix20.py. Every substitution asserts count==1.

## 4. Builds + verifiers (final state)

- build.sh: 23,647 lines, md5
  `8dfacb47a2a6698d47e4b4a5f8d9126c`. Two final builds exit 0, diff 0
  (build logs `fix21/build1.log`, `fix21/build2.log`, both ending
  "build complete"). Diff against `build.sh.before-fix21` is exactly
  +38 lines / −0 lines — the fix21 block only.
- Backup: `build.sh.before-fix21` (23,609 lines, md5
  `785fb40580a4d91f7a480e1cdbc21f24`, matching the fix #20 gate).
- Counts: 166 skills / 72 agents / 123 rules / 87 commands / 15
  hooks — unchanged post-fix20. Banned terms 0 in the built tree
  (verify21 check 9; re-verified by the coordinator with an
  independent grep). Grok pins only: `grok-4.7-high` 54,
  `cursor-grok-4.6-high-fast` 102, zero bare `grok-4.6-high-fast`
  (coordinator's own counts).
- verify21.py: 102/102 checks pass (exit 0). verify15.py: 44/44.
  verify17.py: 60/60. verify18.py: 72/72. verify19.py: 76/76.
  verify20.py: 169/169. All six re-run by the coordinator after
  this MANIFEST was written. The 101 → 102 step is check 10: before
  this MANIFEST existed, check 10 passed on a NOTE + measured
  lines/md5; now that the MANIFEST exists, check 10 validates the
  recorded lines + md5 at the top of this file as a real check
  ("fix21/MANIFEST.md records build.sh lines + md5" — PASS).
  Audit #66, dry-run #35, and sweep #29 all ran pre-MANIFEST and
  correctly recorded 101/101 at that time.
- Earlier verifiers' pins were bumped by fixup21 (check lines only;
  docstring history sentences kept as history, with a new sentence
  appended per fix-up).

## 5. Checkers (all verified by the coordinator against the files, not trusted from reports)

| Round | Audit | Dry-run | Sweep |
|---|---|---|---|
| Rule implementation + fix-up #1 | #66 ZERO (0 blocking, 0 minor) | #35 9/9 PASS (fixtures 13/13) | #29 CLEAN (0 blocking, 0 minor) |

- Audit #66 spot-checks by the coordinator: all 14 fix21
  placements present ×1 at the file:lines in §1 (audit §1);
  prior-fix anchors intact (canonical block ×1 in all 11 files,
  fix17 E1, fix18 FEATURES_CUTS_SECTION, fix19 F4_RULE/D19_RULE/
  STATIC19/F4_APP/D19_APP, fix20 F4_SCOPE/F5/F6/B1/X1 + app
  mirrors + STATIC20, fixup #3 H1/BIND/INNOV/OVERDRIVE); counts
  166/72/123/87/15; banned terms 0; Grok pins 54/102.
  Note recorded by the audit (not a finding): F4_APP counts 0 in
  orch-build-mvp — pre-existing fix #19 state (F4_APP was only
  ever placed in ui-ux-pro-max); orch-build-mvp carries
  F4_SCOPE_APP instead, as recorded in fix20/MANIFEST.md §1.1.
- Dry-run #35 re-run by the coordinator: verify21.py 101/101
  (exit 0); fixtures `fix21/dryrun35-fixtures.py` 13/13. All nine
  SPEC §6 items PASS — rule presence, criteria coverage (3/3 scope
  tokens named as check triggers in STATIC21), repair compliance
  (repair-reported), the four negative demonstrations, the positive
  demonstrations, and interconnection (32 pointer lines, 0
  off-target).
- Sweep #29 spot-checks by the coordinator: all 8 fix21 constants
  count exactly 1 in every SPEC-required placement (14 built, 9
  staged) with matching md5s and correct ordering; old fix20
  checkbox 0 in staged, built, and build.sh; fix21 block exactly
  38 lines (23600–23637) before STEP 5, no LAST claim; banned
  terms 0 in built tree, staged sources, fix21 block, and all 8
  constants; TODO/FIXME/XXX 0 in all 10 fix21 files and the fix21
  block; staged-vs-built diffs only the 4 pre-existing build.sh
  patch hunks (sweep23 §11); counts unchanged; verify21 re-run
  101/101.

## 6. Deviations, known items, open items

Recorded deviations (all in SPEC §5/§8):
- F4_RULE / F4_SCOPE / F4_SCOPE_APP / TYPESET_F20 are verify19 /
  verify20 anchors (full-text `in` checks) and are NOT edited —
  F4_TIGHT scopes them by interpretation, with the tightened rule
  placed immediately after in every file. Sweep #29 §4b records
  TYPESET_F20 and F4_SCOPE_APP explicitly as checked-and-cleared
  (they are verify20 anchors; flagging them would demand edits
  that break verify20) — a SPEC decision, not a sweep miss.
- verify21 check 10 passes on block-marker + measured line-count /
  md5 evidence until this MANIFEST exists; now that it exists,
  check 10 validates against the lines + md5 recorded at the top
  of this file.
- Dry-run #35 §2 note (not a finding): STATIC21's trigger for the
  main-visible-text token is phrased as the prohibition (a main
  visible token in the body face is an incomplete build); the
  positive prescription (use the display/artistic face) lives in
  the F7 rule text in the same skill file, one step up (step 4a).
  The check fires on the bug either way; if the parent wants the
  positive wording literal inside STATIC21, that is a one-line
  wording addition, not a rule gap.
- Dry-run #35 §3 repair compliance is REPAIR-REPORTED, not
  re-verified from this VM — the live repaired artifact source
  does not exist in this workspace, and the workspace tokens file
  is v1-era/stale and was not used as evidence. The `.btn` /
  `.roll-btn` Fraunces CTAs remain recorded F5 leaks, now also F7
  failures. F7 recording for the repair's small-text elements is a
  build-record matter for a future build (F7 did not exist when
  the repair was made), not a defect in the repair.
- No dry-run #31 / #32 report files exist in the workspace — the
  `.btn` / `.roll-btn` / `.step-btn` findings are cited from
  `fix20/SPEC.md` §11 and `fix21/SPEC.md` §1.
- Staged-vs-built diffs in Taste (1 frontmatter hunk) and
  polish-pass (4 hunks) are the pre-existing build.sh patch blocks
  documented in sweep23 §11, not fix21 edits.
- Standing rules kept throughout: staged sources only, never the
  built tree; no fix11/fix11-stage.py re-run; fix #16 Grok pins
  and the Claude/Codex scrub untouched (banned terms 0); fix
  #15/17/18/19/20 anchors intact (their verifiers all pass); no
  commit, no bundle, no GitHub touch; Campus Eats artifact not
  touched.

## 7. Open items (not fix #21's to close)

- The b2444de bundle predates fixes #14–#21 — a fresh bundle is
  needed before any push. Do NOT push b2444de as the current state.
- The live smoke test in Anish's Cursor
  (`~/workspace/hackathon-plugin/LIVE_SMOKE_TEST.md`) is still the
  gate before GitHub publish (it decides the agent-resolution
  question, frontmatter name vs filename, and the model-bracket,
  hooks, and ccg runtime items).
- Fix #17's R1/R4 rule-effectiveness finding is unverified against
  the live render.
- Pip pinning pass still pending (Audit #37 scope: 17 unpinned
  install lines; only `piper-tts` can fire in a first build).
- Campus Eats final desktop/phone visual verification still pending
  (Anish was asked to confirm the type on his phone and on Windows).
- Fix #21's F7 recording for the repair's small-text elements is a
  build-record matter for a future build (see §6).
