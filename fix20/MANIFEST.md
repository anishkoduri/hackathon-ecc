# Fix #20 — MANIFEST: Tiempos is body-only, important text gets a unique important font, impressive is the bar

Coordinator-owned manifest for the whole of fix #20: the rule
implementation, the §10 weaving pass, and fix-ups #1–#4 (fixup20,
fixup20b, fixup20c, fixup20d). Engines: `fix20/fix20.py`,
`fix20/weave20.py`, `fix20/fixup20.py`, `fix20/fixup20b.py`,
`fix20/fixup20c.py`, `fix20/fixup20d.py`. SPEC: `fix20/SPEC.md`
(§§0–12). Verifier: `fix20/verify20.py` (168 checks).

build.sh lines: 23609
build.sh md5: 785fb40580a4d91f7a480e1cdbc21f24

## 0. Gate (verified before starting)

- `fix19/MANIFEST.md` existed.
- build.sh at the gate was 23,314 lines, md5
  `a8d3d3c6f6d32344d0168c5323d9364b` (post-fix19).
- Anish's refinement (Nov 11 evening, his words): "The rule of that
  font is just for basic text, anything that's supposed to be
  important should be a unique important font, and most of all the
  design just has to be impressive."

## 1. Rule changes (built-tree file:line; staged sources edited, build.sh copies them verbatim unless noted)

All line numbers below are the BUILT tree
(`~/workspace/hackathon-plugin/hackathon-ecc/`). The canonical
constants live in `fix20/fix20.py` (F4_SCOPE/F5/F6/B1/X1/STATIC20 +
_APP mirrors, POLISH_F20, TYPESET_F20) and `fix20/fixup20c.py`
(H1/BIND/INNOV/OVERDRIVE). Banned tokens under the fix #16 scrub —
"Anthropic font" and "Claude's reading text" — are never used; rule
text says "Tiempos" / "Fraunces stand-in".

### 1.1 F4_SCOPE — F4 (Tiempos / Fraunces stand-in) is BODY-ONLY

Old: fix #19 F4 said body/plain text is Tiempos (Fraunces stand-in)
but did not scope it — nothing said the body face must never serve
important text, and nothing closed a leak where the body face reached
a heading or display token.
New: F4_SCOPE (full rule) + F4_SCOPE_APP (app mirror) + TYPESET_F20
(typeset-lens check) + STATIC20 (F4-scope item).

- `skills/design-taste-frontend/SKILL.md:267` F4_SCOPE — "for BASIC
  text only — body copy and plain reading text. They are NEVER used
  for important text." Binds the face IN ITS ROLE as the body/reading
  face (fix-up #1): a pairing dealing Fraunces as the DISPLAY face
  with a different body face is governed by F3/F5, not this scope
  rule. Boundary: F3 governs display/important, F4 governs basic text
  only. A face is either display or body, never both on one build,
  except a scoped, recorded exception (D19 reason + F6 justification;
  the exception is about the FACE, never the delivery format — F2
  still binds).
- `skills/orchestrate/SKILL.md:112` F4_SCOPE (same text, in the
  design-package rule area).
- `skills/ui-ux-pro-max/SKILL.md:104` F4_SCOPE_APP; `skills/orch-build-mvp/SKILL.md:47`
  F4_SCOPE_APP. Role-scoped wording included (fix-up #1).
- `skills/polish-pass/reference/lenses/typeset.md:57` TYPESET_F20
  (typeset-lens check: body face for basic text only; a heading/hero/
  CTA/key-label token in the body face is a finding; display face needs
  its D19 reason + F6 justification; the squint test is the visual
  proof).

### 1.2 F5 — important text uses a UNIQUE, IMPORTANT font

Old: fix #19 F3 forced a unique/interesting pairing but did not say
important text must use a distinctive display face chosen through the
design skills and recorded with its D19 reason — nor what counts as
"important".
New: F5 (full rule) + F5_APP (app mirror) + STATIC20 (F5 item).

- `skills/design-taste-frontend/SKILL.md:269` F5 — headings, display
  type, hero text, emphasis, key labels, calls to action, anything
  meant to stand out use the display face, never the body face, never
  a generic/system font; recorded with its D19 reason + F6
  justification. "Key label" DEFINED (fix-up #1): a label meant to
  stand out; ordinary small labels follow the Hallmark gates in the
  body face. Examples (fix-up #2): featured section label, emphasis
  badge, price label — "hero eyebrow or kicker" was DROPPED (Hallmark
  gate 54 bans eyebrows).
- `skills/orchestrate/SKILL.md:114` F5 (same text).
- `skills/ui-ux-pro-max/SKILL.md:106` F5_APP;
  `skills/orch-build-mvp/SKILL.md:49` F5_APP.

### 1.3 F6 — the design just has to be IMPRESSIVE (governing bar)

Old: no governing bar — a rule-correct but unimpressive design could
pass.
New: F6 (full rule) + F6_APP (app mirror) + STATIC20 (F6-record and
F6-verdict items).

- `skills/design-taste-frontend/SKILL.md:271` F6 — a font choice
  correct per the rules but leaving the design unimpressive still
  fails. The finish review / browser-qa visual verdict judges
  impressiveness; the decision record must state why the important
  font is the impressive choice for that surface. Connects to
  more-not-bolder, the E1 creativity push, and D19 — not a parallel
  bar.
- `skills/orchestrate/SKILL.md:116` F6 (same text).
- `skills/ui-ux-pro-max/SKILL.md:108` F6_APP;
  `skills/orch-build-mvp/SKILL.md:51` F6_APP.

### 1.4 B1 — branding

Old: no brand requirement — a build could look like a generic
template.
New: B1 (full rule) + B1_APP (app mirror) + STATIC20 (B1 item).

- `skills/design-taste-frontend/SKILL.md:273` B1 — every build
  carries a distinct brand identity (wordmark, identity tokens,
  voice), recorded in the decision record. The brand is the
  through-line: every surface, component, and decision expresses it.
  A build with no recorded brand identity fails the check.
- `skills/orchestrate/SKILL.md:118` B1 (same text).
- `skills/ui-ux-pro-max/SKILL.md:110` B1_APP;
  `skills/orch-build-mvp/SKILL.md:53` B1_APP.

### 1.5 X1 — every component is an experience

Old: components could be recorded as plain functional blocks.
New: X1 (full rule) + X1_APP (app mirror) + STATIC20 (X1 item).

- `skills/design-taste-frontend/SKILL.md:275` X1 — each component is
  designed as a moment/interaction, not a static functional block.
  Each component's recorded reasoning states what experience it
  creates (what it feels like, what moment it is), alongside the six
  D19 dimensions. A plain functional block fails the check.
- `skills/orchestrate/SKILL.md:120` X1 (same text).
- `skills/ui-ux-pro-max/SKILL.md:112` X1_APP;
  `skills/orch-build-mvp/SKILL.md:55` X1_APP.

### 1.6 STATIC20 — the fix #20 static checks (never screen verdicts)

- `skills/design-taste-frontend/SKILL.md:327` STATIC20 (step 6, after
  STATIC19).
- `skills/orchestrate/SKILL.md:69` STATIC20 (Verify 5a, after
  STATIC19, before the 5b bullet).
- `skills/orch-build-mvp/SKILL.md:70` STATIC20 (step 6, after
  STATIC19).
- Items: (F4 scope) Type list marks the body face body-only; (F5)
  every important-text token points at the display face; (F6 record)
  the record states why the important font is the impressive choice;
  (F6 verdict) impressiveness is browser-qa's at the finish review,
  never a static check; (B1) brand identity named on the record; (X1)
  every component entry states the experience it creates.

### 1.7 POLISH_F20 (polish-pass harmony check)

- `skills/polish-pass/SKILL.md:22` POLISH_F20 (harmony rule line) —
  harmony also verifies the font scope (body-face rows marked
  body-only; a heading/display/hero/CTA/key-label token in the body
  face is a harmony divergence, candidate evidence, never a verdict)
  and the important font's record (D19 reason + F6 justification),
  including the B1/X1 sentence (SPEC §2 printed it without the
  sentence; §3/§7 require it — the worker used §2 text PLUS the
  sentence).

### 1.8 H1 — model hierarchy (fix-up #3, steer #3.2)

Old: the fix #16 pins existed (orchestrator/design-lead/deep-reasoner
on `grok-4.7-high`; scout/fast-worker/composer-tier on
`cursor-grok-4.6-high-fast`) but the hierarchy was not stated as a
rule at the decision points.
New: H1_RULE (`fix20/fixup20c.py`).

- `skills/orchestrate/SKILL.md:30` H1 — "Grok 4.7 High decides, Grok
  4.6 High executes": 4.7 is the ORCHESTRATOR and the main mind behind
  big decisions; 4.6 are underlings (fast execution workers). A 4.6
  worker facing a decision routes it up to the 4.7 mind; it never
  decides on its own. A dispatch putting a big decision on 4.6, or
  execution a 4.6 worker could do on 4.7, is a routing error — a
  static check item, never a screen verdict.
- `rules/hackathon-mode.mdc:42` H1 (§6 bullet, same text).
- `skills/orchestrate/SKILL.md:98` design-package rule paragraph
  carries the one-line H1 pointer ("Model hierarchy (fix #20 H1):
  the design-lead decides on Grok 4.7 High; executors implement on
  Grok 4.6 High …").

### 1.9 BIND + INNOV — binding weave + creativity through the skills (fix-up #3, steers #4/#5/#6)

Old: the fix #13 standing rule ("every design decision is made BY a
named package skill; Grok executes THROUGH the package, never
replaces it") applied to design decisions only; nothing forced every
decision through a named skill, and nothing said what happens when no
skill covers a needed step.
New: BIND_RULE + INNOV_RULE (`fix20/fixup20c.py`).

- `skills/orchestrate/SKILL.md:32` BIND — "the skills are the only
  path": the operating skill is named in the brief before the work
  starts; a decision with no named operating skill is refused and
  routed to the skill that owns it; work without a named skill in its
  brief is an incomplete build (static check). The audit/dry-run FAIL
  off-skill work WHERE a skill exists and was bypassed.
- `skills/orchestrate/SKILL.md:32` (same paragraph) recorded-gap
  fallback (steer #6): binding never blocks needed work — when a
  needed step has no skill covering it, the agent does NOT stop: it
  records the gap in the decision record (what was needed, why no
  skill covers it), does the work by the closest skill's principles,
  and flags it so the gap can become a skill later. A needed step done
  through the fallback PASSES. Priority: (1) everything needed gets
  done, (2) on the skills wherever a skill exists, (3) through the
  recorded-gap fallback where none does.
- `skills/orchestrate/SKILL.md:34` INNOV — "innovation builds on the
  skills": an original element/approach extending, combining, or
  pushing a skill's principles is on-skill innovation: it PASSES,
  recorded with its D19 reason. Channels the fix #17 E1 creativity
  push (trailblazing, not dumb) through the skills. The audit/dry-run
  FAIL off-skill improvisation but do NOT fail on-skill innovation.
- `rules/hackathon-mode.mdc:43` BIND (§6 bullet); `:44` INNOV (§6
  bullet) — same texts.
- `skills/orchestrate/SKILL.md:98` design-package rule paragraph
  carries the BIND/INNOV pointer sentence.
- `skills/orch-build-mvp/SKILL.md:41` BIND pointer (design-package
  bullet tail, via the fixup20c build.sh block).
- `skills/orch-pipeline/SKILL.md:60` BIND pointer ("Each phase
  delegates" tail, via the fixup20c build.sh block).

### 1.10 OVERDRIVE expansion (fix-up #3, steer #3.3)

Old: `feature-expansion` Phase 1 = 4 lenses × 3–5 candidates each
(12–20 raw); Phase 2 = "Keep it to 4–7 features."
New: OVERDRIVE_RULE (`fix20/fixup20c.py`) — about 75% more (~1.75x).

- `skills/feature-expansion/SKILL.md:40` OVERDRIVE rule (before
  Phase 0): 5–9 candidates per lens, 7–12 shortlisted. Anti-drift
  bound explicit: expansion PROPOSES, the planner APPROVES / TWEAKS /
  REJECTS (Phase 3); a feature contradicting a recorded decision is
  rejected, never tweaked around; nothing drifting from the OG idea
  gets built. 7–12 is a CAP, not a quota — never pad to reach it.
  The proposal table usually exceeds the 20-line ledger — expected;
  the full table goes in `docs/expansion.md`, the ledger carries a
  one-line pointer (existing overflow rule); never cut features to fit
  the ledger.
- `skills/feature-expansion/SKILL.md:54` Phase 1: "Each returns 5–9
  candidates, no more" + OVERDRIVE pointer.
- `skills/feature-expansion/SKILL.md:106` Phase 2: "Keep it to 7–12
  features (fix #20 OVERDRIVE …)" + cap-not-quota + overflow
  sentences.
- `skills/orchestrate/SKILL.md:61` OVERDRIVE pointer (step 2).
- `rules/hackathon-mode.mdc:12` OVERDRIVE pointer (§1, next to the
  expansion sentence). The §1 "fewer exceptional features beat many
  mediocre ones" guard (line 14) is untouched — it IS the anti-padding
  guard.

## 2. Scope-clarification evidence (SPEC §1 + fix-ups)

- SPEC §1's claim ("No staged source explicitly tells a build to use
  the body face for headings") was WRONG as applied to the type
  catalogue: Taste's catalogue pairing `fraunces`
  (`library/type.json:1233`, display Fraunces / Figtree body) deals
  Fraunces as the DISPLAY face — literally contradicting F4_SCOPE's
  "NEVER used for important text". RULING (fix-up #1): the scope rule
  binds the face IN ITS ROLE as the body/reading face; a pairing
  dealing Fraunces as display with a different body face is governed
  by F3/F5, not F4. The pairing stays; F4_SCOPE/F4_SCOPE_APP/STATIC20
  gained role-scoping sentences. SPEC §1 corrected.
- Hallmark gates 64/67 + hallmark-floor rule 9 prescribe the body
  face for labels/captions/table heads/nav links/tags/chips; F5 said
  "key labels" use the display face with "key label" undefined.
  RULING (fix-up #1): F5 defines "key label" (a label meant to stand
  out; ordinary small labels follow the Hallmark gates in the body
  face). Fix-up #2 dropped "hero eyebrow or kicker" from the examples
  (Hallmark gate 54 bans eyebrows; floor rule 9 opens "Never an
  eyebrow"). Definition unchanged.
- Campus Eats artifact (read-only reference, pre-fix-#20): dry-run
  #31 found `.btn` (`index.html:193`) and `.roll-btn` (`:679`) set in
  Fraunces (body face) — a genuine F5 leak the package rule now
  catches. `.step-btn` (`:485`) is NOT a leak (Bowlby One SC first).
  `.total small` (`:492`) in Fraunces is an ordinary small label per
  the Hallmark gates, not a leak (dry-run #33).
- vantage.md UNCHANGED: display and body still Geologica — the fix
  governs the deal, it does not rewrite theme data; the scope rule
  text names the collision handling (re-deal a distinct display face,
  or a scoped, recorded exception with D19 + F6).

## 3. Weaving — the rules at every decision point (SPEC §10)

- Census: 27 in-scope skills + 139 out-of-scope = 166. 32 one-line
  "Design-decision pointer:" lines in 27 in-scope skills (5 skills
  ×2, 22 ×1). Pointer form: "F2/F3/F4/F5/F6/D19/B1/X1 as relevant —
  design-package rule — Taste step 4a / orchestrate."
- Trigger keys 58 → 64 (6 new: skill:accessibility,
  skill:ai-feature-spec, skill:gan-style-harness, skill:motion-advanced,
  skill:motion-foundations, skill:motion-patterns);
  `coverage.withTriggers` = 64, all resolve; orch-pipeline
  deliberately triggerless (internal engine, weave1 precedent).
- Borderline calls (documented in the engine): motion-* IN (SPEC §4
  excluded them from rule-text edits only; their decisions are
  governed by record-level D19/F6); gan-style-harness IN (its rubric
  scores direction/tokens/type); feature-expansion/grill-me/
  hackathon-scope IN (they set/derive the design direction);
  frontend-design-direction OUT per hackathon-mode §5 (production UI
  outside hackathons).
- Interconnection (fix-up #3): every rule token (F2/F3/F4/F5/F6/D19/
  B1/X1/H1/BIND/INNOV) resolves to a defining phrase in the built
  tree (verify20 check 14); every pointer targets the design-package
  rule in orchestrate, which carries the H1 + BIND/INNOV pointers —
  no orphan rule, no dead-end reference. The 32 pointers were NOT
  re-edited for fix-up #3: they invoke the design-package rule, which
  now carries the new pointers (SPEC §12.4 reasoning).

## 4. Fix-up rounds

### 4.1 Fix-up #1 (`fix20/fixup20.py`) — audit #62 / dry-run #31 / sweep #25

- `manifests/context-packs/skill-triggers@1.json` `coverage.skills`
  169 → 166 (stale upstream metadata, generated Oct 30, 2026;
  metadata-only; verify20 gained check 13 asserting it).
- F4_SCOPE role-scoping sentences (see §2, fraunces pairing).
- F5 "key label" definition (see §2).
- Dry-run #31 item 3 (Campus Eats CTA leak) recorded as a known
  pre-fix-#20 artifact deviation (see §2).
- Two self-caught engine errors, fixed and recorded: (1) first build
  failed with a SyntaxError — over-escaped quotes in the generated
  fixup20 block (`\\\"` in the engine source); fixed by rewriting
  `build_sh_block()` with triple-quoted strings and compile-checking
  generated Python before rebuilding. (2) Re-running the append
  snippet failed importing fixup20 — it imports the OLD constants
  from fix20.py, which it had already amended; fixed by importing
  the amended constants as NEW and deriving OLD by reversing each
  insertion. Lesson: never assume escape levels — verify generated
  code compiles before building; an engine that amends its own import
  source is not re-runnable without reversal logic.
- Result: build.sh 23,553 lines, md5
  `2abc40ed5a55943905d622c37ff49e02` (3 builds exit 0, manifest diff
  0). Audit #63 ZERO ERRORS, dry-run #32 13/13 PASS, sweep #25
  (1 finding + 1 minor — the two rulings above).

### 4.2 Fix-up #2 (`fix20/fixup20b.py`) — sweep #26 (0 blocking, 3 minor)

- MINOR-1: "hero eyebrow or kicker" dropped from the F5/F5_APP
  key-label examples (see §2).
- MINOR-2: "hackathon-mode §37" → §5 (5 occurrences: verify20.py:84,
  :168; weave20.py:167, :205, :478). weave1/MANIFEST.md:127 hedges the
  same cite — closed historical manifest, left as-is by design.
- MINOR-3: Batch E comment in build.sh corrected (it falsely claimed
  last placement before STEP 5 and that no build.sh patch touches
  less-flat-ui; W2-G9/W2-C1/weave20-A10 + the block itself patch it).
  Comment-only.
- Result: build.sh 23,582 lines, md5
  `766a35e47e83f921b4e30e8b4da36efd` (2 builds exit 0, manifest diff
  0). Audit #64 ZERO ERRORS, dry-run #33 13/13 PASS, sweep #27
  (1 finding + observations — see §4.3).

### 4.3 Fix-up #3 (`fix20/fixup20c.py`) — steers #3/#4/#5/#6 + sweep #27

- H1 (§1.8), OVERDRIVE (§1.10), BIND + INNOV (§1.9) — including the
  recorded-gap fallback amendment (steer #6, applied by direct edit
  after the engine ran, to the engine constant + staged orchestrate +
  staged hackathon-mode + SPEC §12.4 + verify20 check 17; verify20
  imports the amended constant).
- Sweep #27 FINDING 1: build.sh:23475 still cited "hackathon-mode
  section 37" in the embedded weave20 block — fixed to §5 (comment).
- MINOR-3 re-opened: all placement-"LAST" phrases in build.sh
  normalized (64 replacements, probed on a /tmp copy first; line
  count unchanged). Only the two TRUE "This patch runs LAST (after
  every audit_patch …" lines remain (build.sh:19846, :19880).
  Generator header strings in weave20.py / fix20.py / fixup20.py /
  fixup20b.py updated to match the normalized embedded copies;
  docstrings describing the historical action left as-is. fix15/17/
  18/19 generators left historical (one-shot, not regenerated).
- fixup20b.py re-import fix (same reversal pattern as fixup20.py):
  imports the amended F5/F5_APP as NEW, derives OLD by reversing;
  import succeeds; re-run still refused by preflight (one-shot).
  Two self-caught engine errors, fixed and recorded: (1) the
  self-check marker for the orchestrate step-2 OVERDRIVE pointer
  missed the `**` bold markers ("OVERDRIVE (fix #20): 7–12" vs the
  actual "**OVERDRIVE (fix #20):** 7–12") — marker corrected, all
  edits had already applied, self-checks re-run and passed. (2) The
  reversed asserts in the fixup20b import fix were wrong twice over
  (`_F5_EX_NEW not in F5` fails because the NEW example string is a
  substring of the OLD one; `_F5A_EX_NEW not in F5_APP_NEW2` checked
  the wrong variable) — corrected to assert the OLD text is present
  in the derived value, in both the engine and the applied file.
- verify20 gained checks 14–18 (52 sub-checks): interconnection,
  H1, OVERDRIVE, BIND/INNOV (+ fallback), build.sh hygiene.
- One real bug caught by verify20 (not by the engine): the verify20
  check string for the orchestrate step-2 OVERDRIVE pointer missed
  the same `**` bold markers — fixed in the check string; the rule
  text itself was present all along.
- Result: build.sh 23,609 lines, md5
  `3c7b45bbfca8dbe10d10b9eb4b445160` (2 builds exit 0, manifest diff
  0, logs identical; built tree 3,284 files). Audit #65 ZERO ERRORS,
  dry-run #34 15/15 PASS, sweep #28 (0 blocking, 1 minor — see §4.4).

### 4.4 Fix-up #4 (`fix20/fixup20d.py`) — sweep #28 MINOR-1, comment-only

- Sweep #28 found the fixup20c probe only counted uppercase `LAST`:
  20 build.sh block headers still said "The coordinator inserts this
  block last, just before STEP 5." (or "The patch agent inserts …").
  Fixed: 20 replacements (13 single-line + 7 split-line, probed on a
  /tmp copy first; line count unchanged; built tree byte-identical to
  the fixup20c build — manifest diff 0, proving comment-only).
- The lowercase "Runs last so it sees …" (build.sh:15853) is TRUE
  intra-block patch order and is left alone.
- verify20 check 18 gained a lowercase assertion ("inserts this block
  last" == 0; "last, just before STEP 5" == 0) — verify20 is now 168
  checks. The fix19:330 section label ("post-fixup20b") was corrected
  to post-fixup20d with the pin bump.
- Result: build.sh 23,609 lines (unchanged), md5
  `785fb40580a4d91f7a480e1cdbc21f24` (2 builds exit 0, manifest diff
  0, logs identical). Audit #65 and dry-run #34 ran against the
  fixup20c-built tree; fixup20d is comment-only and the built-tree
  diff 0 proves the tree they verified is the tree being delivered,
  so neither needed re-running for this fix-up.

## 5. Builds + verifiers (final state)

- build.sh: 23,609 lines, md5
  `785fb40580a4d91f7a480e1cdbc21f24`. Two final builds (fixup20d)
  exit 0, manifest diff 0 over 3,284 files, build logs identical.
  Built tree byte-identical to the fixup20c builds (comment-only
  fixup20d).
- Counts: 166 skills / 72 agents / 123 rules / 87 commands / 15
  hooks. Banned terms 0 in the built tree (verify20 check 9).
  `coverage.skills` = 166, `coverage.withTriggers` = 64, keys = 64.
- verify20.py: 168/168 checks pass (exit 0). verify15.py: 44/44.
  verify17.py: 60/60. verify18.py: 72/72. verify19.py: 76/76.
  (Totals moved during the program: verify15 43→44, verify17 59→60,
  verify19 75→76 — each gained a named patch-4 check for the weave20
  less-flat-ui pointer; verify18 stayed 72/72; verify20 grew
  80→114→115→167→168 across weaving, fix-up #1, fix-up #3, fix-up #4.)
- Earlier verifiers' pins were bumped at each fix-up (check lines
  only; docstring history sentences kept as history, with a new
  sentence appended per fix-up).

## 6. Checkers (all verified by the coordinator against the files, not trusted from reports)

| Round | Audit | Dry-run | Sweep |
|---|---|---|---|
| Rule implementation + weave | #51–#61 range (fix #19 base) | #30 PASS (fix #19) | #24 CLEAN (fix #19) |
| Fix-up #1 | #63 ZERO ERRORS | #32 13/13 PASS | #26 (3 minors → fix-up #2) |
| Fix-up #2 | #64 ZERO ERRORS | #33 13/13 PASS | #27 (1 finding + observations → fix-up #3) |
| Fix-up #3 | #65 ZERO ERRORS | #34 15/15 PASS | #28 (0 blocking, 1 minor → fix-up #4) |
| Fix-up #4 | — (comment-only; tree identical, see §4.4) | — (same) | — (same) |

- Audit #65 spot-checks by the coordinator: H1/BIND/fallback each
  1× in built orchestrate + built hackathon-mode; OVERDRIVE rule/5–9/
  7–12 each 1×; "section 37" 0; "LAST" only the 2 true lines; models
  only `grok-4.7-high` (54) and `cursor-grok-4.6-high-fast` (102),
  zero bare `grok-4.6-high-fast`; no stale `a8d3d3c6` / "169 skills".
- Dry-run #34 fixture (`/tmp/dryrun34/dryrun34.py`) re-run by the
  coordinator: exit 0, 15/15 PASS — including all three BIND branches
  (off-skill FAILS, on-skill innovation PASSES, recorded-gap fallback
  PASSES), OVERDRIVE volume + cap-not-quota + anti-drift reject +
  ledger overflow, H1 positive + wrong-tier dispatches, and the
  pointer → design-package-rule → H1/BIND/INNOV chain with no dead
  end.
- Sweep #28 spot-checks by the coordinator: fixup20c block
  regenerates byte-identical; weave20 BLOCK byte-identical; fixup20b
  imports and its reversal recovers the old eyebrow texts; all 64
  comment replacements verified against `build.sh.before-fixup20c`;
  pins correct in the check lines; Minor 1 (20 lowercase "inserts
  this block last" headers) confirmed real — 13 single-line + 7
  split-line, all 20 in the backup too.

## 7. Deviations, known items, open items

Recorded deviations (all in SPEC §11/§12):
- POLISH_F20 in SPEC §2 printed without the B1/X1 sentence while
  §3/§7 require it — the worker used §2 text PLUS the sentence.
- SPEC §3 row 5 anchor wrong (POLISH_F19 count 2, not 1 — anchored on
  the full constant); row 6 anchor mid-sentence — anchored on the full
  TYPESET_F19 constant.
- verify20 check 10 passes on block-marker + line-count evidence
  until this MANIFEST exists; now that it exists, check 10 validates
  against the lines + md5 recorded at the top of this file.
- fix19/manifest1.txt + manifest2.txt pre-date the fix19 fix-up (raw
  diff also shows the fix-up's 25 files + node_modules churn — not
  fix20's).
- Weave: `fix20/manifest2.txt` cannot serve as a built-tree diff
  baseline (matches 0/3,284 current files — predates an upstream input
  refresh); the changed-files list was derived from the weave's own
  footprint + grep, not that manifest.
- fixup20/fixup20b generator body literals diverge from their embedded
  copies (the generators now emit the fixup-amended rule texts while
  the embedded blocks carry the pre-fixup texts, incl. the old "hero
  eyebrow/kicker" examples in fixup20's block) — documented generator
  history, intentional; the fixup20b block runs after fixup20 and swaps
  the built text. Headers match ("before STEP 5" both sides).
- Sweep #27 observation (not a finding): Taste's component library
  still ships eyebrow elements (`.cx-eyebrow`) while Hallmark gate 54
  + floor rule 9 ban eyebrows — pre-existing library/lint tension; the
  ban is enforced by lint, not a fix #20 regression. Left as-is.
- Sweep #28 observations (not findings): staged `claude` hits are
  pre-existing fix #16 staged/built drift (built tree is scrubbed);
  build.sh contains banned-list terms by design (upstream ECC content
  the fix16 scrub removes at build time + the scrub code itself) — a
  literal 0-in-build.sh is unsatisfiable; the operative check (built
  tree) is 0. "LAST" strings remaining in generator files are
  non-emitted (docstrings / old-text literals / search patterns).
- The Campus Eats artifact's `.btn`/`.roll-btn` F5 leak (see §2) is
  recorded, read-only, pre-fix-#20 — the package rule now catches
  exactly this leak; no repair was made to the artifact in this
  program.
- Standing rules kept throughout: staged sources only, never the
  built tree; no fix11/fix11-stage.py re-run; fix #16 Grok pins and
  the Claude/Codex scrub untouched (banned terms 0); fix #15/17/18/19
  anchors intact (their verifiers all pass); no commit, no bundle, no
  GitHub touch.

## 8. Open items (not fix #20's to close)

- The b2444de bundle predates fixes #14–#20 — a fresh bundle is
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
