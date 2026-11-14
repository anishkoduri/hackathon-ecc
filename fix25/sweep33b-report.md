# Sweep #33b — Fix #25, re-sweep (Sweep #33 minors + Audit #72 M2) — CHECK-ONLY report

**SWEEP #33b: CLEAN — 0 blocking, 0 minor, weaving-coherence CLEAN**

Scope: staged sources (`new-skills/`, `round2-skills/`, `rewritten-skills/`,
`new-rules/`), the built tree `~/workspace/hackathon-plugin/hackathon-ecc/`
(node_modules excluded everywhere), `build.sh`, and the fix #25 working
files. Check-only: no plugin file edited, no `build.sh` run, no fix/apply/
verify script edited or run. No bundle, commit, push, or message sent.

Read first, in full: `fix25/SPEC.md` (§0–§6),
`fix25/PARENT-GUIDANCE.md`, `fix25/sweep33-report.md`,
`fix25/sweep33-fixes.md`, `fix25/audit72-report.md`,
`fix25/audit72-m2-fix.md`. Every number below was re-derived by this
sweeper's own greps/commands listed in §8; nothing was copied from the
fix notes without re-running.

Scope note on the re-run: the three fixes touch exactly three files
(orchestrate SKILL.md :266, hackathon-scope SKILL.md :90, mobile-ship
launch-marketing.md :15) and introduce no new element, pointer target,
call-map entry, or fix25.py anchor. This re-sweep therefore re-ran the
full anchor census, the frozen-text checks, the staged-vs-built diffs
for the three edited files, and regression spot-checks (banned terms,
Grok pins, counts, DEMOGATE, deferred six, six/seven convention,
verify19) rather than re-deriving the entire Sweep #33 (call-map
regeneration, all 14 fix25.py anchors, the full pointer table) — those
numbers are untouched by the fixes and Sweep #33's derivations of them
stand. This scoping is stated explicitly per the task.

## 1. Build fingerprint + diff (re-derived)

| Item | Re-derived value | Expected | Result |
|---|---|---|---|
| `build.sh` lines | 24,079 (`wc -l`) | 24,079 | PASS |
| `build.sh` md5 | `f19483f50e89998f8b9dc052ed5d5fae` | same | PASS |
| `build.sh.before-fix23` lines / md5 | 23,774 / `4799a819791b9c3ec4c19136ad698397` | same | PASS |
| `diff build.sh.before-fix23 build.sh` | **+305 / −0** | +305/−0 | PASS |

## 2. Finding 1 (Sweep #33 MINOR 1) — VERIFIED FIXED

**The step-2 reviewer backing check for REASON_F25 is present.**

- Staged `new-skills/orchestrate/SKILL.md:266` (Verify step 2,
  Design-direction record check paragraph) now reads, immediately after
  the frozen D19_REVIEWER sentence: "The reviewer also checks the
  three-part reasoning block — INFERRED / CHOSEN / REJECTED (REASON_F25)
  — on the decision-record entries presented in the diff; an entry
  missing any of the three lines is a finding, minor at least." The
  built copy `hackathon-ecc/skills/orchestrate/SKILL.md:266` carries the
  identical sentence. Both lines re-read in full, not asserted from the
  fix note.
- **:149 claim agrees:** staged and built orchestrate:149 still read
  "The three lines are checked by the step-2 reviewer and the step-5a
  static check (REASON_F25)" — the reviewer check now exists (:266)
  and the 5a check still exists (:96, REASON_F25 static check, re-read).
  Both named checkers are real.
- **Frozen texts byte-identical (verified from the files, not the fix
  note):** D19_REVIEWER, D19_RULE, D19_ROUTING were extracted from
  `fix19/fix19.py:110,122,124` by script and substring-checked against
  staged and built orchestrate — each present **×1** in each copy.
  The new sentence sits immediately after the frozen D19_REVIEWER
  sentence and immediately before "The reviewer does NOT judge the
  built screens" in both copies (adjacency checked by script, staged
  and built). The D19 lead sentence ("Every UI decision carries a
  thought-out reason across the FULL experience") still appears exactly
  **1×** in staged orchestrate.
- **verify19 re-run by this sweeper: 71/76** — exactly its codified
  tail per Audit #72 §2; the frozen-text assertions pass.
- **Anchor census holds, REASON_F25 now 5 occurrences in orchestrate
  (was 4):** `grep -o` count on orchestrate = 5 in staged and 5 in
  built (lines :87, :96, :149 ×2, :266). Full-census REASON_F25: staged
  5 lines / 6 occ, built 5 lines / 6 occ (orchestrate 5 + grill-me 1).
- **Staged-vs-built orchestrate diff:** exactly 3 lines (:96, :261,
  :268) — the pre-existing build-time agent-link expansion (bare
  `` `code-reviewer` `` → `` `code-reviewer` agent
  (`agents/ecc-code-reviewer.md`) ``), present in the run-2 tree as
  well; not caused by this fix. The two edited lines (:149, :266) are
  identical staged vs built.

## 3. Finding 2 (Sweep #33 MINOR 2) — VERIFIED FIXED

**The hackathon-scope trap row "Edge case obsession" now defers to
TECHDEPTH_F25 by name.**

- Staged `rewritten-skills/hackathon-scope/SKILL.md:90` and built
  `hackathon-ecc/skills/hackathon-scope/SKILL.md:90` both read:
  "| **Edge case obsession** | "What if the user enters X" | Demo
  doesn't enter X — that is a cut, not a handling: record what was cut
  and why in the cut list (TECHDEPTH_F25) |". `diff` staged vs built
  for the whole file: clean. The full file was re-read.
- **TECHDEPTH_F25 now 3 occurrences in hackathon-scope (was 2):**
  `grep -o` count = 3 in staged and 3 in built (:57 Technical-substance
  section, :90 trap row, :96 Quiet re-scope row).
- **"Demo doesn't enter X" now occurs exactly 2× in the file**
  (staged and built): :65 (TECHDEPTH section — "is not a handling; it
  is a cut") and :90 (trap row, qualified identically). Both consistent.
- **No other trap row contradicts a TECHDEPTH_F25 statement:** all
  nine remaining trap rows re-read ("Real" auth, Real database, Real
  deploy, Generality, Architecture astronautism, Real ML training, Real
  scale, Generic UI, Quiet re-scope). None touches edge cases, cut
  recording, or the no-silent-re-scope rule; the "Quiet re-scope" row
  itself defers to TECHDEPTH_F25 by name. The table's preamble
  (traps apply only to unrequested infra; user-required infra is built
  properly, off-the-shelf) is the same carve-out the TECHDEPTH section
  relies on ("the substance is the architecture, algorithms, and system
  design around the chosen tools, never a from-scratch rewrite") — no
  contradiction. The "Real database" antidote ("In-memory dict, JSON
  file") vs the TECHDEPTH example of a silent re-scope ("a real system
  replaced by a single in-memory dict where the demo needs more") is
  reconciled by that same preamble: where the demo needs more, the
  infra is required, not a trap.

## 4. Audit #72 M2 — VERIFIED FIXED

**The mobile-ship launch-marketing.md:15 reword landed in staged and
built copies, prescribing the self-hosted template fonts.**

- Staged `round2-skills/mobile-ship/references/launch-marketing.md:15`
  and built `hackathon-ecc/skills/mobile-ship/references/
  launch-marketing.md:15` both read: "Fonts: Google Fonts under the
  OFL, self-hosted as vendored woff2 via `@remotion/fonts` +
  `staticFile` (the pitch-deck-video template pattern)." `diff` staged
  vs built for the file: clean. The mechanism named matches the
  template as built: `template/src/fonts.ts` imports `loadFont` from
  `@remotion/fonts` and `staticFile` from `remotion` (re-read :22–:23),
  loading vendored woff2 from `public/fonts/`.
- **"@remotion/google-fonts" in the built tree (excluding
  node_modules) is now exactly the fonts.ts:2 provenance comment and
  nothing else:** `grep -rn "@remotion/google-fonts" hackathon-ecc/
  --exclude-dir=node_modules` returns exactly 1 hit —
  `hackathon-ecc/skills/pitch-deck-video/template/src/fonts.ts:2`
  ("// families live from Google Fonts via `@remotion/google-fonts`,
  which fetched…"), the intentional provenance comment, which loads
  nothing. The same grep over staged sources returns exactly the same
  single hit (staged `new-skills/pitch-deck-video/template/src/
  fonts.ts:2`). Zero imports, zero dependencies, zero prose
  prescriptions remain. Audit #72's M2 decision (prose mentions do not
  count against the §4(b) self-host requirement) now holds with only
  the intentional comment left.

## 5. Dispatch-prompt.md decision — DECIDED: NO, the template does NOT need the matching line

**Question (from fix25/sweep33-fixes.md):** `new-skills/orchestrate/
references/dispatch-prompt.md`'s `[UI diff:]` reviewer block mirrors
the design-direction check but does not name the three-part
INFERRED/CHOSEN/REJECTED block. Does the template need the matching
line?

**Decision: No. Not a finding. Reasons, from the files:**

1. **The template already omits the other sub-check too.** SKILL.md
   :266's "Design-direction record check (UI diffs)" paragraph contains
   three sub-checks: (a) direction RECORDED (named direction, tokens
   tracing); (b) D19-dimensions coverage (the frozen D19_REVIEWER
   sentence); (c) the three-part reasoning block (new REASON_F25
   sentence). The template's `[UI diff:]` block names only (a) plus the
   do-NOT-judge-screens guard. It never carried (b) either — the frozen
   D19 check has always lived in SKILL.md alone. The template is a
   summary of the check, not an enumeration of its sub-checks; adding
   only (c) would make it name 2 of 3 sub-checks and create a new
   inconsistency rather than fix one.
2. **SKILL.md is the authority; the template invokes the check by
   name.** The template says "ALSO check the design-direction record"
   — the same named check :266 defines. The reviewer is dispatched by
   orchestrate under :266 ("Every reviewer dispatch (template in
   dispatch-prompt.md) scopes the review…"), so the dispatched reviewer
   is bound by the SKILL.md definition of that check, which now
   includes the three-part block. The template is the dispatched
   prompt's shape, not the check's definition.
3. **The mechanism is already in the template.** The new :266 sentence
   scopes the three-part check to "the decision-record entries
   presented in the diff"; the template already instructs the reviewer
   to check the design-direction record "present in the diff". Only
   the enumeration lives in SKILL.md, which is where it belongs.
4. **No SPEC clause requires template/SKILL.md parity.** SPEC §2
   requires every decision routes through a named skill and named
   enforcement points resolve to real checks — satisfied: the
   enforcement point is orchestrate :266, a named skill, and the check
   is real. This matches Sweep #33 §8.4's own treatment of the
   benchmark in the same template (dispatch-prompt.md §5a names the
   inventory but not the benchmark — "not a bypass", because the read
   is instructed at the design-lead's own steps).
5. **If parity is ever wanted, it is a two-line addition, not one:**
   the D19-dimensions line and the three-part line together. That is a
   future-fix choice, not this round's scope — and a one-line addition
   of the three-part line alone would be the wrong change.

## 6. Regression spot-checks (coherence areas the new edits could affect)

- **Anchor census (full, re-derived):** staged vs built, lines /
  occurrences — RECIPES_F25 1/1 vs 1/1; TESTCOV_F25 1/1 vs 1/1;
  PLATFORM_F25 2/2 vs 2/2; BENCHMARK_V5_F25 8/8 vs 10/10 (the +2 are
  the fix25.py browser-qa patch, explained in Sweep #33 §2, unchanged);
  TECHDEPTH_F25 8/8 vs 8/8 (was 7/7 — +1 is the :90 trap-row
  qualification, staged + built); ADAPT_F25 2/2 vs 2/2; REASON_F25 5/6
  vs 5/6 (was 4/5 — +1 line/+1 occ is the :266 sentence, staged +
  built); CREATIVE_F25 3/3 vs 3/3. Unique-token census over staged +
  built reconciles exactly: RECIPES 2, TESTCOV 2, PLATFORM 4,
  BENCHMARK 18, TECHDEPTH 16, ADAPT 4, REASON 12, CREATIVE 6. No new
  `_F25` token exists; no orphan anchor.
- **Pointer resolution for new references:** the three fixes introduce
  no new file pointers. The :266 sentence references only REASON_F25
  and the decision record (both in-file); the :90 row references
  TECHDEPTH_F25 (same file, :57); the :15 reword references
  `@remotion/fonts` + `staticFile` (the template pattern — verified
  against `template/src/fonts.ts`, which imports exactly those two).
  Nothing new to resolve; nothing dangling.
- **Six/seven count-convention:** unchanged. Count-convention line
  present at orchestrate:66 ("wherever a frozen rule text says 'six
  dimensions', read seven"); the Depth extension at :147 extends the
  frozen text without editing it; the new :266 sentence carries no
  count. The frozen texts say "six" (byte-identical, §2) and the
  editable sites say seven — exactly the fix #24 adjudication.
- **No new contradictions with THE CORE / "more, not bolder" / C2/C3:**
  the :266 sentence is a presence check ("an entry missing any of the
  three lines is a finding"), explicitly "never a verdict on the
  reasoning's quality" per :149 — it judges nothing about design
  quality, loudness, or memorability, so it cannot restate THE CORE or
  "more, not bolder". The :90 qualifier records a cut; it does not
  restate a stagger, exit factor, or any fix #14–#24 adjudication.
  C2/C3 split texts (built motion-foundations:409/:435) untouched by
  the fixes; no fix text mentions them.
- **Banned terms:** 0 in the built tree (`grep -rliE
  "claude|codex|anthropic|opus|sonnet|haiku|composer-2.5"` over
  `hackathon-ecc/skills|agents|commands|rules|hooks|scripts`, excl.
  node_modules). **Grok pins only, whole built tree excl.
  node_modules:** `grok-4.7-high` ×54, `cursor-grok-4.6-high-fast`
  ×103, bare `grok-4.6-high-fast` ×0 — exactly Audit #72's numbers.
- **Counts:** skills 166, agents 72, rules 123, commands 87 (directory
  counts); hooks.json `hooks` dict 15; skill-triggers coverage
  skills 166 / withTriggers 64; call-map header 166/72/123/87/15/64.
  All agree with the tree and with Sweep #33 / Audit #72.
- **/demo gates + deferred six:** DEMOGATE tokens present (B2S1–S7,
  B3S1–S7 ×1 each; H1/H2/O4/O9 ×2 each — staged + built). The deferred
  six are still named only at end-of-project in orchestrate (:8, :103,
  :370, re-read). No fix #25 text in this round touches /demo or the
  deferred set.
- **No verifier asserts the new sentence yet:** `fix25/verify25.py`
  does not exist (confirmed) — the fix note's statement stands; the
  verify25 worker owns asserting :266 (and the :90 / :15 lines).

## 7. Findings

None. 0 blocking, 0 minor.

## 8. Open items (carried, explicitly — not findings this round)

1. **verify25 codification** (Audit #72 M1 tails + the new :266 / :90 /
   :15 assertions): owned by the verify25 worker; no verify25.py
   exists yet.
2. **Dispatch-prompt.md parity** (decided in §5, not a finding): if a
   future fix wants the template to enumerate the reviewer sub-checks,
   add the D19-dimensions line and the three-part line together.
3. **Sweep #33 §8 open items carried forward unchanged:** no Sweep #32
   report file exists; benchmark file not cited from the call map
   (generator change, not a skill edit); skip-grilling stub record vs
   the REASON_F25 5a check (stub format unspecified — the 5a check
   catches it rather than silently passing); no 5a-style whole-build
   static check in orch-build-mvp (belt-and-braces, not a gap); Netlify
   row touch-up due after Dec 4, 2026; pip pinning pass; fix #17 R1/R4
   unverified; fresh bundle needed before any push (do NOT push
   b2444de).
4. **Dry-run #40 owns** the Leg 2 beat-v5 re-trace and Leg 3 /demo
   59/59 verdict; the live smoke test owns the ck wire's live Cursor
   behavior.

## 9. Commands run (method)

All run read-only from `~/workspace/hackathon-plugin` (built-tree
greps from `hackathon-ecc/`; upstream greps from `/tmp/ecc-dev-install`
and `/tmp/uipro` not needed this round — no fix25.py anchor was
re-touched; no test copies made):

- `wc -l build.sh build.sh.before-fix23 && md5sum …` + `diff … |
  grep -c '^>'` / `'^<'`
- `grep -n REASON_F25` staged + built orchestrate (full-line read);
  `grep -o REASON_F25 | wc -l` per file; same for TECHDEPTH_F25 in
  hackathon-scope
- Per-token census loop for all 8 `_F25` tokens (staged and built,
  lines + occurrences); unique-token census via `grep -rho
  "[A-Z][A-Z0-9_]*_F25" | sort | uniq -c`
- Python substring check: D19_REVIEWER / D19_RULE / D19_ROUTING
  extracted from `fix19/fix19.py:110,122,124`, presence ×1 in staged
  and built orchestrate; adjacency of the new sentence after the
  frozen sentence and before the NOT-judge sentence, staged and built
- `diff` staged vs built for orchestrate SKILL.md, hackathon-scope
  SKILL.md, dispatch-prompt.md, launch-marketing.md
- `grep -rn "Demo doesn't enter X"` over staged + built; full read of
  staged hackathon-scope (155 lines) incl. all trap rows
- `grep -rn "@remotion/google-fonts"` over the built tree and over
  staged sources (excl. node_modules); direct read of staged + built
  launch-marketing.md:15 and `template/src/fonts.ts:1–30`
- Full read of staged dispatch-prompt.md (all templates + [UI diff:]
  block) for the §5 decision
- Banned-term grep (built tree, 0); Grok-pin counts (whole built tree
  excl. node_modules: 54 / 103 / 0, bare via `grep -rPo
  '(?<!cursor-)grok-4.6-high-fast'`)
- Counts: `ls | wc -l` per built directory; `hooks.json` hooks dict
  (15); skill-triggers coverage (166 / 64); call-map header re-read
- DEMOGATE token census; deferred-six grep in built orchestrate
- `python3 fix19/verify19.py` (71/76, codified tail); `ls
  fix25/verify25.py` (absent)
- `grep -n "six dimensions|seven dimensions"` in staged orchestrate

## Verdict

**SWEEP #33b: CLEAN — 0 BLOCKING, 0 MINOR, weaving-coherence CLEAN.**

Sweep #33 MINOR 1 is fixed (the step-2 reviewer check for REASON_F25
exists at orchestrate:266 in staged and built, immediately after the
byte-identical frozen D19_REVIEWER sentence; :149 agrees; REASON_F25
is 5 occurrences in orchestrate). Sweep #33 MINOR 2 is fixed (the
"Edge case obsession" trap row defers to TECHDEPTH_F25 by name at
hackathon-scope:90 in staged and built; TECHDEPTH_F25 is 3 occurrences
in the file; no other trap row contradicts a TECHDEPTH_F25 statement).
Audit #72 M2 is fixed (launch-marketing.md:15 prescribes the self-
hosted template fonts in staged and built; "@remotion/google-fonts" in
the built tree is exactly the fonts.ts:2 provenance comment, nothing
else). The dispatch-prompt.md open observation is decided: the template
does NOT need the matching line (§5 — SKILL.md :266 is the authority,
the template already omits the frozen D19 check too, and adding only
the three-part line would create a 2-of-3 inconsistency). The anchor
census, pointer resolution, six/seven convention, banned terms, Grok
pins, counts, /demo gates, and deferred-six standing all hold with no
regression. No blocking finding: no orphan anchor, no dangling
reference, no bypassed step, no contradiction with THE CORE, "more,
not bolder", the frozen D19 texts, or the C2/C3 scope splits.
