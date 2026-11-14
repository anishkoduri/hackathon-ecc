# Fix #25, Phase 2 — §2 weave re-verification + wiring + §4(c) (worker B)

Status: DONE. No rebuild, no loop run (per task — a later worker builds and
runs the loops). No `verify*.py` touched. No pitch-deck-video template file
touched. `design-inventory.md` NOT touched (worker C's line-29 edit intact).
Worker E's staged edits NOT clobbered (built on them; see §6). `build.sh`
NOT touched (see §7 for why its fix25 comment is now stale).

Anchor tokens: `RECIPES_F25`, `TESTCOV_F25`, `PLATFORM_F25`,
`BENCHMARK_V5_F25` (new, staged), `INVENTORY_F23` (existing, reused in the
fix25.py orch patches), `BENCHMARK_V5_F25` (reused in the browser-qa patch).

## §0 What was read first (per task)

SPEC §2 + §4(c), PARENT-GUIDANCE.md, and all Phase 1 notes:
`callmap/wiring-list.md` + `callmap/call-map-data.json` (A),
`design-tech-depth.md` (E), `verifier-updates.md` (C), `template-fonts.md`
(D), `fix25-run-log.md` (coordinator).

## §1 §2 weave re-verification — fix #24 coherence as the baseline

Re-verified from the files (not from summaries):

- **Every decision routes through a named skill.** Holds, with ONE hole
  found and closed — see §3 (orch-* family inventory bypass).
- **Design package runs on every UI surface.** Holds in orchestrate row 10
  (relevance by surface type, never by size), dispatch-prompt 5a,
  feature-expansion Phase 4 UI rule, orch-build-mvp design-package section,
  and the four orch-* UI rules. No "may skip the design package" language
  found in any of those files (grep for `may skip|can skip|skip the design|
  without the design`: 0 hits in orchestrate / Taste).
- **Inventory read BEFORE deciding.** Holds in orchestrate (dispatch-prompt
  5a: "READ it at the design-package step BEFORE deciding") and
  feature-expansion Phase 4 — but NOT in the orch-* family. Closed — §3.
- **No off-skill improvisation path.** The only `improvis*` hits in the
  checked files (orchestrate, Taste, polish-pass) are the recorded-gap rule
  itself ("surfaced as a recorded gap instead of improvised around;
  improvising around a directive is off-skill improvisation and fails").
  No `best judgment / use your judgment / decide for yourself / whatever
  you think / your own discretion` path exists in the checked files.
  The Binding rule (fix #20 BIND/INNOV) is present in orchestrate row 10
  and orch-build-mvp ("a decision with no named skill is refused and
  routed; on-skill innovation passes, off-skill improvisation fails").
- **Fix #24 adjudications intact (spot-checked in the built tree):** C2 —
  B3 30ms per-row stagger vs Rule 5 container floor
  (`motion-foundations/SKILL.md:409`, "Adjudicated fix #24: Rule 5's 0.05s
  floor governs container-le…"); C3 — B15 `exitFactor: 0.8`
  (`motion-foundations/SKILL.md:435`) as the single source of truth;
  FILM_F1/F5/F6 naming untouched (no edit touches pitch-deck-video);
  Grok pins only (`grok-4.7-high` / `cursor-grok-4.6-high-fast`, 0 bare
  `grok-4.6-high-fast` in every touched file); THE CORE + "more, not
  bolder" present in orchestrate; /demo gates present
  (`DEMOGATE_O4_F23`/`O9` tokens in orchestrate); the fix #19 D19 frozen
  sentence appears exactly 1× in orchestrate (byte-identical, not edited);
  the deferred six still run only at end-of-project (orchestrate
  "End-of-project checks" names all six by name); banned terms 0 in all
  touched files (grep `claude|codex|anthropic|opus|sonnet|haiku|
  composer-2.5`, excluding the pre-existing non-term `composer-tier`: 0).

## §2 The four wires (+1 linked) — all implemented

### W1. `ck` — WIRED (build-time patch, fix25.py)

**The gap (verified, not assumed).** `skills/ck/hooks/session-start.mjs`
had zero callers: nothing references `skills/ck/` outside its own SKILL.md,
and `hooks/session-start.js` never runs it. `runExistingHook` cannot run it
(it only resolves `scripts/hooks/*`, and the ck hook is an ESM `.mjs` under
`skills/ck/hooks/`).

**The wire (real dispatch path).** `fix25/fix25.py` patches built
`hooks/session-start.js` (2 anchors, both count==1):
- requires: `} = require('./adapter');` →
  same + `const { spawnSync } = require('child_process');` +
  `const fs = require('fs');` + `const path = require('path');`
- before the final `process.stdout.write(...)`: a fail-soft block that
  spawns `node skills/ck/hooks/session-start.mjs` with
  `JSON.stringify(hookInput)` on stdin (hookInput carries `session_id`
  via the adapter's `transformToHookPayload`), parses its stdout JSON,
  converts `additionalContext` (camelCase) → `additional_context`
  (snake_case) and merges it into the same `outputs` array.
  **The conversion is load-bearing:** `normalizeSessionStartOutput` only
  reads `additional_context` (snake_case) or
  `hookSpecificOutput.additionalContext` (shared) — a naive
  runExistingHook-style merge would silently drop the brief. Fail-soft
  throughout (missing hook / non-zero exit / unparsable output = stderr
  note, never a broken session start); inherits the `session:start` gate
  (disabling `session:start` disables ck too); 15s timeout, matching
  `runExistingHook`'s default.
- `skills/ck/SKILL.md` note (same patch): after the `$HOME` paragraph,
  "In this plugin the hook is already wired — no manual registration
  needed: `hooks/session-start.js` runs `skills/ck/hooks/session-start.mjs`
  on every session start (fix #25 §1)…" — the skill's own SessionStart
  Hook section previously said the hook "must be registered in the
  plugin's settings", which is now true via the chain, not via a manual
  settings block.

**What it lights up:** `ck` (skill) — and only `ck`. The `.mjs` also
reads/writes `~/.cursor/ecc/ck` (projects store), unchanged.

**Proof (scratch tree, not asserted).** `fix25.py` on a hardlinked scratch
copy of the plugin: 14 changes, exit 0 (see §5). Live run of the patched
scratch `hooks/session-start.js` with fake stdin `{}` and a fake `$HOME`:
exit 0, output JSON carries `additional_context` containing the full ck
skill text merged with the session-env output — the conversion works; a
naive merge would have produced no ck text. Real built tree verified
untouched (0 hits for all three patch markers).

**True cost — the wiring list understated it (PARENT DECISION, §7).**
The list said "~100-token project-brief injection". Measured: the `.mjs`
ALWAYS injects the full ck SKILL.md — 167 lines / 785 words / 6,100 chars
(its "only ~50 lines" comment is stale) — plus the ~100-token project
summary, even with zero registered projects (`entries.length === 0`
returns `parts` = [skill]). Live measurement: merged `additional_context`
was 7,382 chars / 890 words with an empty ck store. So the wire costs
~1k tokens on EVERY session start, not ~100. The wire is implemented as
specified; whether to keep it at that cost is a parent call.

### W2. `conventional-commit-review` — WIRED (build-time patch + staged dispatch)

**The wire (two real dispatch paths, both named).**
- `fix25/fix25.py` patches built `commands/prp-commit.md` Phase 3
  (message drafting), anchor
  `Craft a single-line commit message in imperative mood:` (count==1):
  "Draft the message with the `conventional-commit-review` skill
  (`skills/conventional-commit-review/SKILL.md`, fix #25 §1) — it reads
  the repo's own history norms (`git log --no-merges --format=%s -30`)
  for type, scope, and length instead of the generic table below; the
  table is the fallback when the skill cannot run. Then have the
  `ecc-commit-reviewer` agent (`agents/ecc-commit-reviewer.md`) check
  the drafted message against those norms before committing; it presents
  the message, it never runs `git commit` itself."
- Staged second path in `new-skills/orchestrate/SKILL.md` step 6
  (first-build commits go through orch-pipeline Phase 6, NOT /prp-commit
  — the /prp-commit wire alone would never fire on a first build):
  "…before writing the final report — draft each commit message with the
  `conventional-commit-review` skill (`skills/conventional-commit-review/
  SKILL.md`), which reads the repo's own history norms for type, scope,
  and length, and have the `ecc-commit-reviewer` agent
  (`agents/ecc-commit-reviewer.md`) check the drafted message against
  those norms before the commit lands (it presents the message; it never
  runs `git commit` itself);"

**What it lights up:** `conventional-commit-review` (skill),
`ecc-commit-reviewer` (agent — A's linked "wire in WITH it": the skill
drafts, the agent checks; distinct roles, no duplicated draft), and
`git-workflow` (the +1 linked second-order orphan: its only live invoker
is this skill — backticked `git-workflow` at
`conventional-commit-review/SKILL.md:104`).

### W3. `ecc-recipes` — WIRED (staged, orchestrate)

**The wire.** `new-skills/orchestrate/SKILL.md`, new paragraph before the
Design-package rule (anchor `**Design-package rule (row 10 — relevance
by surface type, never by size).**`, count==1), token `RECIPES_F25`:
"**Multi-command pipeline lookup — `ecc-recipes` (fix #25 §1,
RECIPES_F25).** When a run needs a multi-command pipeline and the
orchestrator does not already know which command group runs it, consult
the `ecc-recipes` skill: it maps a described workflow to the right ECC
command group with run-order and stop condition, read live from the
`commands/` directory each run — never from memory. It is advisory only
and never executes: route to the matched command itself to run the work.
Its epic-* and continuous-learning families are multi-week / maintenance
pipelines: the lookup may NAME them, but dispatching an epic command
(`/epic-decompose`, `/epic-claim`, `/epic-validate`, `/epic-review`,
`/epic-unblock`, `/epic-sync`, `/epic-publish`) or `/prune` needs a run
that genuinely needs that machinery — a hackathon build does not — so
those commands stay dormant in use even though the lookup reaches them;
see the call map's wiring list."

**What it lights up:** `ecc-recipes` + 8 second-order commands, exactly
as A predicted: `/epic-claim`, `/epic-decompose`, `/epic-publish`,
`/epic-review`, `/epic-sync`, `/epic-unblock`, `/epic-validate`,
`/prune`. `/learn-eval` is NOT lit (ecc-recipes never references it —
verified: it stays uncalled, intentionally dormant).

**Nuance recorded (not decided silently).** Those 8 commands now read as
"called" in the map (textual dispatch exists through the recipes lookup),
but their dormant-group reason still governs USE: dispatching one needs a
genuine multi-week epic / maintenance need, which a hackathon build does
not have. The map measures reachability, not runtime use. The wiring
list's epic-pipeline group decision is updated to say so (appended §8
below, in `fix25/callmap/wiring-list.md` — A's original text untouched).

### W4. `/test-coverage` — WIRED (staged, orchestrate Verify step 1)

**The gap (verified).** No Verify step checked test coverage:
`tdd-workflow` owns 80%+ at implement time (`SKILL.md:47`, `:228-234`),
`verification-before-completion` never mentions coverage (grep: 0), and
orchestrate's "coverage" is `browser-qa`'s screen matrix (COVER_F23).

**The wire.** `new-skills/orchestrate/SKILL.md` Verify step 1, appended
to the step-1 sentence (count==1), token `TESTCOV_F25`: "**Coverage check
(fix #25 §1, TESTCOV_F25).** When the wave adds or changes code, run the
`/test-coverage` command's measurement (its Steps 1–2: detect the test
framework, run coverage, list files below 80%) — `tdd-workflow` owns 80%+
at implement time, but until now no Verify step checked it; orchestrate's
other 'coverage' is `browser-qa`'s screen matrix (COVER_F23), not test
coverage. Files below 80% are a finding routed to the fix loop (the
implementer adds tests under `tdd-workflow`); the command's Step 3 test
generation runs only when the fix loop routes it there, never as part of
the check itself." Scoping the invocation to Steps 1–2 is deliberate:
Verify is a CHECK, not a generation run — generation inside Verify would
expand scope per wave.

**What it lights up:** `/test-coverage` (command). Side effect, recorded:
`tdd-workflow` gains orchestrate as an additional strong invoker (the
paragraph names it as the fix-loop owner — a genuine reference; it was
already called).

### Wires NOT done (intentionally dormant — unchanged from A)

All other 75 uncalled/second-order elements stay dormant with A's reasons
as recorded. No dormant element was wired, and no new element was added.

## §3 §2 bypass closed: the orch-* family never read the inventory

**Finding.** The inventory-read-BEFORE-deciding step existed only in
orchestrate's dispatch-prompt 5a (orchestrate's own subagent dispatches)
and feature-expansion's Phase 4 UI rule — but NOT in the orch-* family,
where orchestrate row 3 routes ALL single-feature work
(`/orch-add-feature`, `/orch-change-feature`, `/orch-fix-defect`,
`/orch-refine-code`) and standalone MVP builds (`/orch-build-mvp`).
Verified by grep: 0 `design-inventory` mentions in
`skills/orch-{add-feature,change-feature,fix-defect,refine-code,
build-mvp,pipeline}/SKILL.md`. Their UI rules name the design components
and the direction record, but never point the design-lead at the
inventory — so a UI change built through the /orch-* pipelines could be
decided without the inventory read. That is the bypass the call map
exposes: the design package ran, but the inventory step was skippable on
the family's path.

**The close (fix25.py build-time patches — all five files are upstream,
already patched at build time by build.sh, so the close lives here).**
- 4 UI rules, one shared sentence (1× per file, verified):
  old: `run the applicable package components before the change lands.`
  new: same + ` Read the design inventory
  (`skills/orchestrate/references/design-inventory.md`, INVENTORY_F23)
  BEFORE deciding — the design-lead records used vs
  considered-and-rejected inventory entries with D19 reasons in the
  decision record; a UI change whose design-lead never read the inventory
  is incomplete.`
- `orch-build-mvp` design-package paragraph, anchor
  `Every slice that touches a UI surface names its design components in
  its brief and records its direction in `docs/design-tokens.md` before
  building UI` (1×): appended ` — and the design-lead reads the design
  inventory (…, INVENTORY_F23) BEFORE deciding, recording used vs
  considered-and-rejected entries with D19 reasons in the decision
  record`.
- `orch-pipeline` Verification bullet (the family's enforcement point),
  anchor `- UI work (if any): the design package was named in the brief,
  the direction is recorded, and the distinctiveness bar passed or its
  findings were fixed within the caps` (1×): inserted `, the design
  inventory was read before deciding (used vs considered-and-rejected
  recorded, INVENTORY_F23),` after "the direction is recorded,".

**Reason-recorded instead of closed: none.** No bypass was found that
needed a reason instead of a close.

## §4 §4(c) improvements (bounded — no new skill)

### C1. Inventory bypass closure (§3 above)
The highest-leverage §4(c) item: the weakest surface the Home Run lessons
exposed was "the design could have been made without the package" — the
inventory is the package's catalog, and the family's path skipped it.

### C2. Platform rule — never silently convert (Home Run lesson, missing from every skill)
**Finding.** The Home Run lesson — "when a request names a platform the
plugin does not build, state the constraint, name the options, and ask
before building" — existed only in fix notes/memory. Verified: 0 matches
for `does not build|not build native|Swift|native iOS|platform the plugin`
in orchestrate / grill-me / hackathon-scope. A native-iOS prompt could
still be silently converted to web.
**The fix (two staged homes — the question point AND the scope record,
so the "skip the grilling" shortcut cannot bypass it).**
- `new-skills/grill-me/SKILL.md` step 4, appended to the
  `Stack and platform` branch bullet (count==1), token `PLATFORM_F25`:
  "**Platform constraint — never silently convert (fix #25 §4(c),
  PLATFORM_F25).** This plugin builds responsive web apps; it does not
  build native iOS (Swift/SwiftUI), native Android, or desktop apps. If
  the user names a platform the plugin does not build, do NOT convert it
  silently to web: state the constraint, name the options (a web build
  now, or a native build outside this plugin), and ask the user to choose
  BEFORE scoping — record the choice in the decision record. A build that
  started as a native-app request and proceeded as web with no recorded
  choice is an incomplete build."
- `rewritten-skills/hackathon-scope/SKILL.md`, new bullet after the
  design-direction bullet (anchor `orchestrate's slice briefs and
  `docs/design-tokens.md` build on this line`, count==1): "- The platform,
  copied from the decision record — web (what this plugin builds), or the
  platform the record names if it names another (grill-me's platform
  rule, PLATFORM_F25): a scope that names a non-web platform does NOT
  convert it to web — the conversion needs the user's recorded choice
  (state the constraint, name the options, ask before scoping); a scope
  written as web from a native-app record with no recorded choice is an
  incomplete scope."

### C3. Benchmark pointer at the Taste deal point (E's §8.8 flag)
**Finding.** E wired the beat-v5 bar through orchestrate + polish-pass
only, and flagged Taste step 4a / step 6 as weave scope. Verified:
`BENCHMARK_V5_F25` / `design-benchmark` appeared 0× in Taste (staged or
built). The deal point — where themes and moments are dealt — had no
pointer to the bar the deal must beat. (Taste IS staged:
`new-skills/design-taste-frontend/` flows through the STEP 2 copy; the
built file differs from staged by one line from a STEP 3 patch, which my
edit does not touch.)
**The fix.** `new-skills/design-taste-frontend/SKILL.md`, appended after
the dealt-moments line (anchor `**Every dealt moment is applied or
re-dealt (fix #15 R1 — baseline: iris-opens was dealt and never applied).**
…`, count==1), token `BENCHMARK_V5_F25`: "**Design bar — beat Campus
Eats v5 (fix #25 §4(d), BENCHMARK_V5_F25).** The design-lead reads
`skills/orchestrate/references/design-benchmark-v5.md` alongside the
inventory BEFORE dealing/deciding: the re-traced design must beat v5 on
all seven dimensions (count ≥ 62 literal / ≥ 61 stricter; variety ≥ 7
kinds with ≥ 2 kinds above v5; hero inventory + loop or second moment;
Motion ≥ 18 / ≥ 17 stricter; ≥ 9 interactive items with ≥ 2 cross-surface
drives; ≥ 3 live-data surfaces; 0 alignment problems) — a tie on any
dimension is below the bar on that dimension. The static table is checked
at orchestrate step 5a; the live dimensions (hero strength, live dynamic
behaviour, live functionality, alignment) are `browser-qa`'s verdict
alone."
**Not done, with reason:** no matching pointer was added to `ui-ux-pro-max`
(upstream, would need a fix25.py patch). The bar is enforced at
orchestrate step 5a + polish-pass + browser-qa regardless of which skill
leads, so a ui-ux-pro-max pointer would duplicate the enforcement point,
not add a new one. The Taste pointer is different: the deal itself happens
there. If the coordinator wants symmetry, it is a one-line follow-up.

### Not a §4(c) item (recorded to avoid re-litigation)
No new skill was created (default per task). No fix #14–#24 adjudication
was re-litigated. THE CORE, "more, not bolder", anti-derivative, D19 (all
seven dimensions incl. Depth), browser-qa sole verdict, /demo gates, and
the deferred six stand.

## §5 Regenerated call map — counts + assertion result

Generator: `fix25/callmap/generate_call_map.py` (unchanged — no edits).

**Real tree (staged wires visible; build-time patches land at rebuild):**
exit 0. Counts assert: skills 166 / agents 72 / rules 123 / commands 87 /
hooks 15 / triggers 64. Corpus 1,709 files.
- Uncalled: 53 elements (was 57) — skills 25 (was 27), agents 21 (was 22),
  commands 7 (was 8), rules 0, hooks 0, triggers 0.
- Second-order orphans: 13 (was 22) — skills 8, agents 4, commands 1
  (`/python-review` only).
- Newly called: skills `conventional-commit-review`, `ecc-recipes`;
  agent `ecc-commit-reviewer`; command `/test-coverage`. Newly uncalled:
  none. `git-workflow` left the second-order list (its invoker is now
  called). The 8 epic/`/prune` commands left the second-order list.
- The map diff vs A's map is ONLY the wired entries (42 changed lines):
  the four newly-called rows, the 8 epic/`/prune` rows (now also naming
  orchestrate as an invoker — the RECIPES_F25 paragraph names them as the
  gated set), the `tdd-workflow` row (one extra invoker, orchestrate —
  the TESTCOV_F25 paragraph names it as the fix-loop owner), and the
  summary counts. Byte-identical elsewhere.

**Scratch proof tree (hardlinked copy + fix25.py applied — the
post-rebuild state):** exit 0, counts assert identically. Uncalled 52
(was 53 on the real tree): `ck` now called, invoker
`hackathon-ecc/hooks/session-start.js [strong]`, flow "always-on (Cursor
event)". `conventional-commit-review` + `ecc-commit-reviewer` gain
`commands/prp-commit.md [strong]` as a second invoker. `orchestrate`
gains `browser-qa/SKILL.md [strong]` (the benchmark paragraph names the
orchestrate reference path — already called, no status change). The
scratch-vs-real map diff is ONLY those rows. This is the proof the
build-time wires light up as specified; the real build worker's
post-rebuild regeneration must show the same 52.

**Scratch method (so the build worker can repeat it).**
`fix25/scratch/map-prove/` held a `cp -rl` hardlinked copy of the plugin
(`cp -al` fails here: `--archive` tries to preserve ownership and exits
1, breaking `&&` chains — use `cp -rl`). The 11 files fix25.py patches
were de-linked first (`rm` + plain `cp`, never `cp` over a hardlink —
that truncates the real file in place), as were the two generator
outputs. fix25.py ran against the scratch built tree (14 changes, exit 0,
log at scratch `fix25/fix25-patch-log.md`); the generator ran from the
scratch path. Real built tree verified untouched throughout (0 hits for
all three patch markers in `hackathon-ecc/`). Scratch tree DELETED after
verification (results recorded here); `/tmp` was not used.

## §6 Browser-qa benchmark decision — ADD the explicit line (decided)

E left this open ("if the coordinator wants an explicit browser-qa
benchmark line, that's weave-worker follow-up"). **Decided: ADD it.**
Reason: browser-qa's existing remit covers the four live dimensions
generically (HERO-BQA_F23 hero verdict, DYNAMIC_F23 dynamic row,
FUNC-BQA_F23 mechanism-on-hero, ALIGN_F23 + BLOCK_F23 alignment/coverage)
— but nothing told it to score them AGAINST the v5 figures. A generic
"dynamic ✓" does not establish "dynamic beats v5's 8 items / 1 drive",
so without the line the benchmark would live only as a static table
(orchestrate step 5a + polish-pass candidate evidence), not as a live
verdict — and the Leg 2 dry-run could not score the live dimensions
against v5. The line is now in browser-qa (upstream, so a fix25.py
patch, 2 anchors, both count==1):
- after `This verdict is `browser-qa`'s alone: no other step judges
  memorability.` — "**Beat-v5 benchmark verdict (fix #25 §4(d),
  BENCHMARK_V5_F25).** At the finish review, score the four live
  benchmark dimensions from
  `skills/orchestrate/references/design-benchmark-v5.md` §2 against the
  v5 figures — hero strength (full v5 hero inventory AND the R4 hero loop
  applied OR a second dealt moment applied in/near the hero), dynamic
  interface (≥ 9 interactive items with ≥ 2 cross-surface state drives),
  functionality (≥ 3 live-data surfaces with real state; the mechanism on
  the hero/first screen), alignment (0 problems across the full coverage
  matrix) — and render each as beat-v5 PASS / FAIL in the report. The
  static dimensions (element count, variety) are scored from the decision
  record's beat-v5 table (orchestrate step 5a static check), never
  re-judged here; the four live dimensions are this skill's verdict alone
  — a dimension that cannot be scored live is recorded as owed, never as
  passed. A tie on any dimension is below the bar on that dimension."
- output-format line after the Memorability row: "- [✓/✗] Beat-v5
  benchmark (BENCHMARK_V5_F25): hero / dynamic / functionality /
  alignment vs the v5 figures — PASS / FAIL per dimension (a tie is below
  the bar; an unscored dimension is owed, never passed)".
This does NOT move any verdict away from browser-qa (it is still the sole
executor); it gives the sole executor the benchmark to execute. No
polish-pass static check was changed; the static/live split is preserved
(5a table = static; browser-qa = live).

## §7 Parent-decision items (NOT decided here — for the manifest)

1. **Trigger router: maintain or record as documentation-only?**
   (A's B6, carried forward unchanged.) All 64 keys resolve to real skill
   dirs, trigger-only count 0, but the consumer chain has no live Cursor
   entry point (neither `scripts/hooks` consumer is invoked from
   `hooks/*.js`; `context-prompt-suggestions.js` states it is
   upstream-only). The live smoke test cannot clear this — there is no
   Cursor event to fire it. PARENT CALL: keep maintaining
   `skill-triggers@1.json`, or record it as documentation-only.
2. **ck wire cost: keep at ~1k tokens/session, or record dormant?**
   The wire is implemented and proven (live run, §2 W1), but its true cost
   is ~1k tokens on every session start (full 167-line SKILL.md injected
   even with no registered projects), not the ~100 tokens the wiring list
   assumed. The `.mjs`'s "~50 lines" comment and the skill's "~100 tokens
   per session" line are both stale. PARENT CALL: accept the cost, trim
   the injection (a fix25.py patch to the .mjs — upstream behaviour
   change, not done here), or record `ck` dormant after all.
3. **Epic commands: reachable but dormant-in-use.** The `ecc-recipes`
   wire makes the 8 epic/`/prune` commands textually reachable; their
   dormant-group reason now governs USE, not reachability (§2 W3). If the
   parent prefers the map to show them dormant, the alternative is to
   un-wire `ecc-recipes` (revert RECIPES_F25) — PARENT CALL only if the
   reachability reading is rejected.
4. **`build.sh` fix25 comment is now stale (not a decision, a note).**
   `build.sh:24062-24067` describes fix25.py as "§4(a) S1" only; the
   script now also carries the §1 wires, the §2 inventory close, and the
   §4(d) browser-qa line. `build.sh` was NOT edited (editing its comment
   would break the additions-only diff invariant the verifiers assert —
   same reason worker C did not edit `build.sh:586`). The manifest /
   verify25 worker may note the stale comment; do not "fix" it by editing
   build.sh without a parent-authorized verifier update.

## §8 Files touched (complete list)

Staged (flow through the STEP 2 copy; built tree picks them up on rebuild):
- `new-skills/orchestrate/SKILL.md` — 387 → 389 lines. RECIPES_F25
  paragraph (before the Design-package rule); TESTCOV_F25 in Verify step 1;
  conventional-commit-review + ecc-commit-reviewer in step 6.
- `new-skills/orchestrate/references/call-map.md` — REGENERATED by the
  generator (53 uncalled, 13 second-order). `fix25/callmap/
  call-map-data.json` — regenerated alongside.
- `new-skills/grill-me/SKILL.md` — 51 → 52 lines. PLATFORM_F25 in the
  step-4 Stack-and-platform branch.
- `rewritten-skills/hackathon-scope/SKILL.md` — 154 → 155 lines. Platform
  bullet in "Write docs/scope.md".
- `new-skills/design-taste-frontend/SKILL.md` — 635 → 637 lines.
  BENCHMARK_V5_F25 pointer after the dealt-moments line.
- `fix25/fix25.py` — 150 → 298 lines. Merged patches: ck (3 subs),
  prp-commit (1), orch family inventory close (6), browser-qa benchmark
  (2), plus the S1 block (unchanged, worker C's). Docstring extended.
  Invocation unchanged (`build.sh` already calls it after fix24, before
  STEP 5); `build.sh` itself NOT edited.
- `fix25/callmap/wiring-list.md` — appended Phase 2 outcomes section
  (below in this note's §9; A's text untouched).
- `fix25/weave-wiring.md` — this note.

NOT touched: `design-inventory.md`, any `verify*.py`, any pitch-deck-video
template file, the built tree (`hackathon-ecc/`), `fix11/fix11-stage.py`
(never run), `build.sh`, worker E's files (orchestrate E-paragraphs,
hackathon-scope TECHDEPTH section, feature-expansion, grill-me ADAPT /
REASON paragraphs, polish-pass benchmark check, design-benchmark-v5.md —
all re-read, none edited).

## §9 Wiring-list update (appended to fix25/callmap/wiring-list.md)

Phase 2 (worker B) wired all four WIRE IN items. `ck` is called via the
SessionStart chain (fix25.py patch; live-tested on a scratch copy — the
real-tree map shows it as called only after rebuild). `conventional-
commit-review` is called via /prp-commit Phase 3 (fix25.py) AND
orchestrate step 6 (staged); `ecc-commit-reviewer` is called with it, and
`git-workflow` left the second-order list. `ecc-recipes` is called via
orchestrate (RECIPES_F25); the 8 epic/`/prune` commands left the
second-order list — they are reachable through the lookup, but dispatching
one still needs a genuine multi-week epic / maintenance need, so they stay
dormant IN USE. `/test-coverage` is called via orchestrate Verify step 1
(TESTCOV_F25, measurement only — Steps 1–2). Post-wire map (real tree,
pre-rebuild): 53 uncalled, 13 second-order; post-rebuild expectation: 52
uncalled (ck joins), 13 second-order. All other dormant reasons stand.

## §10 What I could not verify / what remains owed

1. **Post-rebuild map (52 uncalled) is proven on a scratch tree, not the
   real build.** The build worker must re-run the generator after
   `build.sh` and confirm 52 uncalled / 13 second-order with `ck` called
   via `hooks/session-start.js`. The scratch proof (same fix25.py, same
   generator) is the evidence it will match.
2. **Live Cursor behaviour of the ck wire is owed to the smoke test.**
   The scratch run proves the Node mechanics (spawn, stdin, conversion,
   merge, exit 0) — it does not prove Cursor fires `hooks/session-start.js`
   on session start in Anish's Cursor, or that the merged
   `additional_context` surfaces in the model context. The smoke test
   owns that.
3. **The ck cost question (§7.2) is a parent call, not a verification
   gap.** The numbers are measured; the decision is open.
4. **No full loop was run** (per task). Audit / sweep / dry-run (incl. Leg
   5 call-graph + Leg 2 beat-v5 with the new browser-qa line) / verify25
   belong to later workers. The dry-run worker should note: the browser-qa
   benchmark line is new in this fix — the Leg 2 re-trace is the first
   exercise of it.
